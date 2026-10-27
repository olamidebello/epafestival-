#!/usr/bin/env python3
"""Obtain/renew only the Epa certificate, then verify its public named route."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import secrets
import socket
import subprocess
import sys
import urllib.request
import urllib.parse

DOMAIN='epafestival.africandroid.world'
WEBROOT=Path('/var/www/epa-festival-acme')
REPORT=Path('/var/lib/epa-festival/https-report.json')


def run(argv, required=True):
    p=subprocess.run(argv,text=True,capture_output=True,timeout=240)
    if required and p.returncode:raise RuntimeError('Command failed: '+argv[0]+'; '+p.stderr[-1500:])
    return p


def local_addresses():
    addresses=set()
    for interface in json.loads(run(['ip','-j','address','show']).stdout):
        for a in interface.get('addr_info',[]):addresses.add(a['local'])
    p=Path('/etc/olamidepanel/provisioning.json')
    if p.is_file():
        public=json.loads(p.read_text()).get('public_ipv4')
        if public:addresses.add(public)
    return addresses


def dns_check(lookup=socket.getaddrinfo, local=None):
    actual={r[4][0] for r in lookup(DOMAIN,None,type=socket.SOCK_STREAM)}
    known=local_addresses() if local is None else local
    if not actual or actual-known:
        raise ValueError('Domain DNS must resolve only to this server before certificate issuance; unexpected addresses: '+', '.join(sorted(actual-known)))
    return sorted(actual)


def request(url):
    # Direct connection: local proxy environment cannot mask routing errors.
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(url,timeout=20) as response:
        if urllib.parse.urlparse(response.url).hostname!=DOMAIN:
            raise ValueError('Public URL redirected to another website')
        return response.status,dict((k.lower(),v) for k,v in response.headers.items()),response.read()


def issue(email=''):
    dns=dns_check()
    challenge=WEBROOT/'.well-known/acme-challenge'
    challenge.mkdir(mode=0o755,parents=True,exist_ok=True)
    if any(p.is_symlink() for p in [WEBROOT,WEBROOT/'.well-known',challenge]):raise ValueError('Unsafe ACME document path')
    for p in [WEBROOT,WEBROOT/'.well-known',challenge]:os.chmod(p,0o755)
    token='epa-preflight-'+secrets.token_hex(12);path=challenge/token
    proof=secrets.token_hex(32).encode()
    try:
        with path.open('xb') as f:f.write(proof)
        path.chmod(0o644)
        status,_,body=request('http://'+DOMAIN+'/.well-known/acme-challenge/'+token)
        if status!=200 or body!=proof:raise ValueError('The public ACME challenge path does not serve this server’s proof. Check port 80, DNS and routing.')
    finally:path.unlink(missing_ok=True)
    if not email:
        p=Path('/etc/olamidepanel/provisioning.json')
        if p.is_file():email=str(json.loads(p.read_text()).get('acme_email') or '')
    if email and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+',email):raise ValueError('Invalid ACME contact email')
    argv=['certbot','certonly','--webroot','--webroot-path',str(WEBROOT),'--cert-name',DOMAIN,'-d',DOMAIN,'--non-interactive','--agree-tos','--keep-until-expiring']
    argv+=['--email',email] if email else ['--register-unsafely-without-email']
    run(argv)
    cert=Path('/etc/letsencrypt/live')/DOMAIN/'fullchain.pem'
    run(['openssl','x509','-in',str(cert),'-noout','-checkhost',DOMAIN])
    run(['openssl','x509','-in',str(cert),'-noout','-checkend','0'])
    return {'status':'certificate_ready','dns_addresses':dns,'certificate':str(cert),'webroot':str(WEBROOT)}


def verify():
    report=json.loads(Path('/var/lib/epa-festival/report.json').read_text())
    if report.get('status')!='succeeded' or not report.get('tls'):raise ValueError('The Epa TLS deployment did not succeed')
    spec=importlib.util.spec_from_file_location('epa',Path(__file__).with_name('activate.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    revision=report['revision'];root=Path(report['release_root'])
    for name in module.ASSETS:
        status,headers,body=request('https://'+DOMAIN+'/'+name)
        if status!=200 or headers.get('x-epa-release')!=revision or hashlib.sha256(body).digest()!=hashlib.sha256((root/name).read_bytes()).digest():raise ValueError('Public HTTPS asset verification failed: '+name)
    return {'status':'succeeded','url':'https://'+DOMAIN,'verified_assets':len(module.ASSETS),'revision':revision,'tls':True}


if __name__=='__main__':
    result={}
    try:
        if os.geteuid():raise ValueError('Run as root on the panel server')
        config=json.load(sys.stdin)
        result=verify() if config.get('mode')=='verify' else issue(config.get('email',''))
        REPORT.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(result,indent=2));REPORT.chmod(0o600)
        print(json.dumps(result))
    except Exception as error:
        result={'status':'failed','error':str(error),'stage':'https-repair'}
        REPORT.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        REPORT.write_text(json.dumps(result,indent=2));REPORT.chmod(0o600)
        print(json.dumps(result));sys.exit(1)
