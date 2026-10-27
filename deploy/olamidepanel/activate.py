#!/usr/bin/env python3
"""Transactional, domain-scoped Epa deployment on an existing Olamidepanel host."""
import contextlib
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import socket
import ssl
import subprocess
import sys
import time
import urllib.request

DOMAIN = 'epafestival.africandroid.world'
TOKEN = re.compile(r'''\#[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|\$\{[^}]*\}|[{};]|[^\s{};#]+''')
ASSETS = ['index.html','game.js','advanced.js','style.css','sw.js','manifest.json','assets/epa-logo.png','assets/festival-welcome.webp','assets/festival-evening.webp']


def run(args, check=True):
    p = subprocess.run(args, capture_output=True, text=True, timeout=45)
    if check and p.returncode:
        raise RuntimeError('Command failed: '+args[0]+'; '+p.stderr[-2000:])
    return p


def server_blocks(text):
    """Return server spans and direct child directives; ignore comments/quoted braces."""
    tokens = [m for m in TOKEN.finditer(text) if not m.group().startswith('#')]
    stack, directive, found = [], [], []
    for t in tokens:
        v = t.group()
        if v == '{':
            name = directive[0].group() if directive else ''
            frame = {'name': name, 'start': directive[0].start() if directive else t.start(), 'directives': []}
            stack.append(frame)
            directive = []
        elif v == '}':
            if not stack:
                raise ValueError('Unbalanced Nginx block')
            frame = stack.pop()
            if frame['name'] == 'server':
                frame['end'] = t.end()
                found.append(frame)
            directive = []
        elif v == ';':
            if stack and stack[-1]['name'] == 'server' and directive:
                stack[-1]['directives'].append([x.group().strip('"\'') for x in directive])
            directive = []
        else:
            directive.append(t)
    if stack:
        raise ValueError('Unbalanced Nginx block')
    return found


def plan_file(text, domain=DOMAIN):
    changes, certs, roots = [], [], []
    for b in server_blocks(text):
        ds = b['directives']
        names = [name for d in ds if d[0]=='server_name' for name in d[1:]]
        if domain not in names:
            continue
        if set(names) - {domain, 'www.'+domain}:
            raise ValueError('A target vhost also serves other domains; split it in Olamidepanel before deploying.')
        for d in ds:
            if d[0]=='listen':
                address=d[1]
                port=address.rsplit(':',1)[-1] if ':' in address else address
                if not port.isdigit() or int(port) not in (80,443):
                    raise ValueError('Target domain uses a custom listen address/port; configure its edge route explicitly.')
            if d[0]=='root' and len(d)==2: roots.append(d[1])
        cert=next((d[1] for d in ds if d[0]=='ssl_certificate' and len(d)==2),None)
        key=next((d[1] for d in ds if d[0]=='ssl_certificate_key' and len(d)==2),None)
        if cert and key: certs.append((cert,key))
        changes.append((b['start'],b['end']))
    for a,b in sorted(changes,reverse=True):
        text=text[:a]+'# Epa route migrated to /etc/nginx/conf.d/epa-festival.conf\n'+text[b:]
    return text,certs,roots,len(changes)


def render(root, revision, cert=None):
    shared=f'''    root {root};
    index index.html;
    add_header X-Epa-Release "{revision}" always;
    add_header X-Content-Type-Options nosniff always;
    add_header Referrer-Policy strict-origin-when-cross-origin always;
    location ~ /\\. {{ deny all; }}
    location / {{ try_files $uri $uri/ =404; }}
    location ~* \\.(html|js|css|json)$ {{
        add_header Cache-Control "no-cache" always;
        add_header X-Epa-Release "{revision}" always;
        add_header X-Content-Type-Options nosniff always;
        try_files $uri =404;
    }}
'''
    # Loopback health checks use the same named vhost; browsers redirect to TLS when available.
    http=f'''# Managed by Epa Festival Ansible — Olamidepanel
server {{
    listen 80;
    server_name {DOMAIN};
'''
    if cert:
        http+=f'''    location = /_epa_health {{ add_header X-Epa-Release "{revision}" always; return 200 "{revision}"; }}
    location ^~ /.well-known/acme-challenge/ {{ root {root}; }}
    location / {{ return 301 https://{DOMAIN}$request_uri; }}
}}
server {{
    listen 443 ssl;
    server_name {DOMAIN};
    ssl_certificate "{cert[0]}";
    ssl_certificate_key "{cert[1]}";
    ssl_protocols TLSv1.2 TLSv1.3;
'''+shared+'}\n'
    else:
        http+=shared+'}\n'
    return http


def atomic(path, content, mode=0o644):
    path=Path(path);temp=path.with_name(path.name+'.epa-tmp')
    if temp.is_symlink():raise ValueError('Unsafe temporary file')
    fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_TRUNC|os.O_NOFOLLOW,mode)
    with os.fdopen(fd,'w') as f:
        f.write(content);f.flush();os.fsync(f.fileno())
    os.chmod(temp,mode);os.replace(temp,path)


def switch(target, link):
    temporary=link.with_name(link.name+'.epa-next')
    if temporary.exists() and not temporary.is_symlink():raise ValueError('Unsafe release switch path')
    temporary.unlink(missing_ok=True);temporary.symlink_to(target);os.replace(temporary,link)


def fetch_local(path, tls=False):
    # HTTPS connects to localhost with domain SNI and full certificate verification.
    import http.client
    class LocalTLS(http.client.HTTPSConnection):
        def connect(self):
            sock=socket.create_connection(('127.0.0.1',443),timeout=10)
            self.sock=ssl.create_default_context().wrap_socket(sock,server_hostname=DOMAIN)
    con=LocalTLS(DOMAIN,timeout=10) if tls else http.client.HTTPConnection('127.0.0.1',80,timeout=10)
    try:
        con.request('GET','/'+path,headers={'Host':DOMAIN})
        r=con.getresponse();return r.status,dict((k.lower(),v) for k,v in r.getheaders()),r.read()
    finally:con.close()


def panel_connection(root):
    for p in [root,root/'panel',root/'panel/database.py']:
        info=p.stat()
        if info.st_uid or info.st_mode & 0o022:
            raise ValueError('Panel code must be root-owned and not group/world-writable')
    sys.path.insert(0,str(root/'panel'))
    from database import connect
    return connect()


def main(config):
    if os.geteuid():raise ValueError('Run on the Olamidepanel server as root')
    root=Path(config.get('panel_root','/opt/olamidepanel')).resolve()
    base=Path('/opt/epa-festival');release=Path(config['release']).resolve()
    revision=config['revision']
    if not re.fullmatch('[a-f0-9]{40}',revision) or release!=base/'releases'/revision:
        raise ValueError('Unexpected release path or revision')
    for name in ASSETS:
        p=release/name
        if not p.is_file() or p.is_symlink() or p.stat().st_size==0:
            raise ValueError('Missing/unsafe release asset: '+name)
    worker=Path('/var/lib/olamidepanel-provisioner');worker.mkdir(mode=0o700,exist_ok=True)
    if worker.is_symlink() or worker.stat().st_uid or worker.stat().st_mode & 0o022:
        raise ValueError('Unsafe publisher state directory')
    lockpath=worker/'worker.lock'
    if lockpath.is_symlink():raise ValueError('Unsafe publisher lock')
    lock=open(lockpath,'a');deadline=time.monotonic()+60
    while True:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);break
        except BlockingIOError:
            if time.monotonic()>deadline:raise ValueError('Panel publisher is busy; retry when its current job completes')
            time.sleep(.25)
    backup=Path('/var/backups/epa-festival')/str(time.time_ns());backup.mkdir(mode=0o700,parents=True)
    report={'domain':DOMAIN,'revision':revision,'document_root':str(base/'current'),'release_root':str(release),'backup':str(backup),'ports':{'http':80,'https':443,'application':None},'status':'preflight','old_document_roots':[]}
    originals={};modes={};aliases={};link=base/'current';previous=os.readlink(link) if link.is_symlink() else None
    if link.exists() and not link.is_symlink():raise ValueError('Active document root must be a managed symlink')
    managed=Path('/etc/nginx/conf.d/epa-festival.conf')
    metadata=Path('/etc/olamidepanel/apps/epa-festival.json')
    metadata_before=metadata.read_bytes() if metadata.exists() else None
    activated=False
    def report_save():
        payload=json.dumps(report,indent=2)
        atomic(backup/'report.json',payload,0o600)
        status_dir=Path('/var/lib/epa-festival');status_dir.mkdir(mode=0o700,exist_ok=True)
        atomic(status_dir/'report.json',payload,0o600)
    try:
        with panel_connection(root) as db:
            existing=db.execute('SELECT d.id,d.owner,u.username,u.active FROM domains d JOIN users u ON u.id=d.owner WHERE d.name=? FOR UPDATE',(DOMAIN,)).fetchone()
            owner=config.get('panel_owner') or ''
            if existing:
                if not existing['active'] or (owner and existing['username']!=owner):raise ValueError('Existing panel domain owner is suspended or does not match the requested owner')
                owner=existing['username'];domain_id=existing['id']
            else:
                users=db.execute("SELECT id,username FROM users WHERE active=1 AND role='root' ORDER BY id FOR UPDATE").fetchall() if not owner else db.execute('SELECT id,username FROM users WHERE active=1 AND username=? FOR UPDATE',(owner,)).fetchall()
                if len(users)!=1:raise ValueError('Specify epa_panel_owner for a unique active panel account')
                owner=users[0]['username'];domain_id=None
            job=db.execute('SELECT * FROM website_requests WHERE domain_id=(SELECT id FROM domains WHERE name=?) FOR UPDATE',(DOMAIN,)).fetchone()
            atomic(backup/'panel-before.json',json.dumps({'domain':dict(existing) if existing else None,'website_request':dict(job) if job else None},default=str,indent=2),0o600)
            report['listeners']=run(['ss','-ltnp'],check=False).stdout
            dump=run(['nginx','-T']);combined=dump.stdout+'\n'+dump.stderr
            files=[]
            for name in re.findall(r'^# configuration file (.+):$',combined,re.M):
                raw=Path(name);p=raw.resolve()
                if p==managed and raw!=managed and raw.is_symlink():aliases[str(raw)]=os.readlink(raw)
                if p.is_file() and str(p).startswith('/etc/nginx/') and p not in files:files.append(p)
            if not files:raise ValueError('Nginx active include inventory unavailable')
            changes={};certs=[];count=0
            for p in files:
                old=p.read_text();new,pairs,roots,n=plan_file(old)
                if n:
                    info=p.stat()
                    if info.st_uid or info.st_mode & 0o022:raise ValueError('Target Nginx configuration must be root-owned and not group/world-writable')
                    modes[str(p)]=info.st_mode & 0o777
                    count+=n;certs+=pairs;report['old_document_roots']+=roots
                    originals[str(p)]=old;changes[p]=new
            defaults=(f'/etc/letsencrypt/live/{DOMAIN}/fullchain.pem',f'/etc/letsencrypt/live/{DOMAIN}/privkey.pem')
            valid=[pair for pair in certs+[defaults] if all('$' not in s and '\n' not in s and '"' not in s and Path(s).is_file() for s in pair)]
            if certs and not valid:raise ValueError('Existing TLS certificate could not be preserved; repair its certificate paths first')
            cert=valid[0] if valid else None
            if config.get('require_tls') and not cert:raise ValueError('No certificate found. Provision domain TLS through Olamidepanel, then rerun.')
            if managed.is_symlink():raise ValueError('Managed vhost path is a symlink; resolve it before deployment')
            if managed.exists() and str(managed) not in originals:
                if 'Managed by Epa Festival Ansible' not in managed.read_text():raise ValueError('Dedicated Epa vhost path belongs to another application')
                originals[str(managed)]=managed.read_text();modes[str(managed)]=managed.stat().st_mode & 0o777
            report.update({'tls':bool(cert),'replaced_server_blocks':count,'owner':owner,'changed_config_files':list(originals)})
            for i,(name,content) in enumerate(originals.items()):atomic(backup/(str(i)+'.conf'),content)
            atomic(backup/'restore-map.json',json.dumps({'files':originals,'current_target':previous,'managed_preexisting':managed.exists(),'alias_links':aliases,'modes':modes},indent=2),0o600)
            if str(managed) not in originals:originals[str(managed)]=None
            for name in aliases:Path(name).unlink()
            for p,text in changes.items():atomic(p,text,modes.get(str(p),0o644))
            atomic(managed,render(link,revision,cert))
            run(['nginx','-t'])
            switch(release,link);activated=True
            run(['systemctl','start','nginx']);run(['systemctl','reload','nginx'])
            for name in ASSETS:
                status,headers,body=fetch_local(name,bool(cert))
                expected=(release/name).read_bytes()
                if status!=200 or headers.get('x-epa-release')!=revision or hashlib.sha256(body).digest()!=hashlib.sha256(expected).digest():
                    raise RuntimeError('Routing/content verification failed for /'+name)
            if cert:
                status,headers,_=fetch_local('index.html')
                if status!=301 or headers.get('location')!='https://'+DOMAIN+'/index.html':raise RuntimeError('HTTP to HTTPS redirect verification failed')
            if domain_id is None:
                cursor=db.execute('INSERT INTO domains(owner,name,created) VALUES(?,?,?)',(users[0]['id'],DOMAIN,int(time.time())))
                domain_id=cursor.lastrowid
            if job:
                db.execute("UPDATE website_requests SET state='external_backend',message=?,updated=? WHERE domain_id=?",('Epa game deployed externally; use Epa Ansible for releases',int(time.time()),domain_id))
            db.execute('INSERT INTO audit(actor,action,created) VALUES(?,?,?)',(owner,'Epa game release '+revision+' deployed to '+DOMAIN,int(time.time())))
            metadata.parent.mkdir(parents=True,exist_ok=True,mode=0o750)
            atomic(metadata,json.dumps({'name':'Epa: Spirit of Oro-Ago','domain':DOMAIN,'owner':owner,'document_root':str(link),'release_root':str(release),'revision':revision,'repository':'https://github.com/olamidebello/epafestival-.git','http_port':80,'https_port':443 if cert else None,'backend_port':None,'hosting':'external static game','verified_assets':ASSETS,'backup':str(backup)},indent=2),0o640)
            report['status']='succeeded';report['url']=('https' if cert else 'http')+'://'+DOMAIN
            try:report['dns_addresses']=sorted({a[4][0] for a in socket.getaddrinfo(DOMAIN,None)})
            except OSError:report['dns_addresses']=[]
            report['listeners']=run(['ss','-ltn'],check=False).stdout
            report['note']='Local named-vhost and exact asset checks passed. External DNS/firewall reachability must be checked from outside this host.'
            report_save()
        # Keep the worker lock through the transaction commit.
        print(json.dumps(report))
    except Exception as exc:
        errors=[]
        try:
            if activated:
                if previous:switch(previous,link)
                else:link.unlink(missing_ok=True)
            for name,content in originals.items():
                if content is None:Path(name).unlink(missing_ok=True)
                else:atomic(Path(name),content,modes.get(name,0o644))
            for name,target in aliases.items():
                if not Path(name).is_symlink():Path(name).symlink_to(target)
            if metadata_before is None:metadata.unlink(missing_ok=True)
            else:atomic(metadata,metadata_before.decode(),0o640)
            run(['nginx','-t']);run(['systemctl','reload','nginx'])
        except Exception as rollback:errors.append(str(rollback))
        report.update({'status':'failed','reason':str(exc),'rolled_back':not errors,'rollback_errors':errors});report_save()
        print(json.dumps(report));raise
    finally:lock.close()


if __name__=='__main__':
    try:main(json.load(sys.stdin))
    except Exception as exc:
        print('Epa deployment failed: '+(str(exc) if isinstance(exc,(ValueError,RuntimeError)) else type(exc).__name__),file=sys.stderr)
        sys.exit(1)
