import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('activate',Path(__file__).parents[1]/'olamidepanel/activate.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

class DomainRoutingTests(unittest.TestCase):
    def test_preserve_neighbor_and_ignore_comments_and_quoted_braces(self):
        neighbor='server { listen 80; server_name other.example; location / { return 200 "a { b }"; } }'
        target='server { listen 80; server_name '+a.DOMAIN+'; root /wrong/path; }'
        text='# server { server_name '+a.DOMAIN+'; }\n'+neighbor+'\n'+target
        new,certs,roots,count=a.plan_file(text)
        self.assertIn(neighbor,new)
        self.assertNotIn('root /wrong/path;',new)
        self.assertEqual(roots,['/wrong/path'])
        self.assertEqual(count,1)
    def test_both_http_and_https_and_certificate_paths(self):
        text='server {listen 80;server_name '+a.DOMAIN+';} server {listen 443 ssl;server_name '+a.DOMAIN+';ssl_certificate /cert.pem;ssl_certificate_key /key.pem;}'
        new,certs,roots,count=a.plan_file(text)
        self.assertEqual(count,2)
        self.assertEqual(certs,[('/cert.pem','/key.pem')])
        self.assertNotIn('server_name',new)
    def test_shared_domain_block_rejected(self):
        with self.assertRaises(ValueError):a.plan_file('server {server_name '+a.DOMAIN+' other.example;}')
    def test_custom_backend_listener_rejected(self):
        with self.assertRaises(ValueError):a.plan_file('server {listen 8080;server_name '+a.DOMAIN+';}')
    def test_wildcard_fallback_is_preserved(self):
        text='server {listen 80;server_name *.africandroid.world;root /fallback;}'
        self.assertEqual(a.plan_file(text)[0],text)
    def test_certificate_render_keeps_port80_redirect_and_asset_root(self):
        text=a.render('/opt/epa-festival/current','a'*40,('/cert.pem','/key.pem'))
        self.assertIn('listen 80;',text);self.assertIn('listen 443 ssl;',text)
        self.assertIn('return 301 https://'+a.DOMAIN+'$request_uri',text)
        self.assertIn('root /opt/epa-festival/current;',text)
        self.assertEqual(len(a.server_blocks(text)),2)
    def test_nginx_variables_with_braces(self):
        text='server {server_name '+a.DOMAIN+'; location / { proxy_set_header X ${variable}; }}'
        self.assertEqual(a.plan_file(text)[3],1)


class ReloadReadinessTests(unittest.TestCase):
    def setUp(self):
        import tempfile
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        for name in a.ASSETS:
            p=self.root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(('fixture:'+name).encode())
        self.revision='a'*40
    def tearDown(self):self.tmp.cleanup()
    def test_stale_worker_response_then_ready(self):
        calls=[]
        def fetch(name,tls):
            calls.append(name)
            if len(calls)==1:return 404,{},b'old worker'
            return 200,{'x-epa-release':self.revision},(self.root/name).read_bytes()
        diag={}
        a.verify_assets(self.root,self.revision,False,diag,attempts=3,delay=0,fetch=fetch)
        self.assertEqual(diag['attempt'],2)
        self.assertEqual(diag['verified_assets'],len(a.ASSETS))
    def test_wrong_release_is_rejected_with_diagnostics(self):
        diag={}
        def fetch(name,tls):return 200,{'x-epa-release':'old'},(self.root/name).read_bytes()
        with self.assertRaisesRegex(RuntimeError,'release_header'):
            a.verify_assets(self.root,self.revision,False,diag,attempts=2,delay=0,fetch=fetch)
        self.assertEqual(diag['attempt'],2)
        self.assertEqual(diag['last_failure']['release_header'],'old')
    def test_correct_header_cannot_mask_wrong_content(self):
        diag={}
        def fetch(name,tls):return 200,{'x-epa-release':self.revision},b'wrong game'
        with self.assertRaisesRegex(RuntimeError,'received_sha256'):
            a.verify_assets(self.root,self.revision,False,diag,attempts=1,delay=0,fetch=fetch)



class ExplicitListenerTests(unittest.TestCase):
    def test_join_public_loopback_and_ipv6_groups_without_default_flags(self):
        text="""server {
          listen 80 default_server;
          listen 127.0.0.1:80;
          listen 154.16.170.86:80 bind;
          listen [::]:80 default_server;
          listen [::1]:80;
          server_name sprintforge.netwizzard.tech;
        } server {listen 127.0.0.1:443 ssl;server_name other.example;}
          server {listen 8090;server_name panel.example;}"""
        groups=a.listener_groups(text)
        self.assertEqual(groups[80],['80','127.0.0.1:80','154.16.170.86:80','[::]:80','[::1]:80'])
        out=a.render('/opt/epa-festival/current','a'*40,('/cert.pem','/key.pem'),groups)
        self.assertIn('listen 154.16.170.86:80;',out)
        self.assertIn('listen 127.0.0.1:443 ssl;',out)
        self.assertNotIn('default_server',out)
        self.assertNotIn('bind;',out)
        self.assertNotIn('8090',out)
    def test_literal_addresses_only_and_deduplicated(self):
        text='server {listen 127.0.0.1:80;listen 127.0.0.1:80;listen hostname:80;listen unix:/tmp/sock;server_name example.org;}'
        self.assertEqual(a.listener_groups(text)[80],['80','127.0.0.1:80'])

if __name__=='__main__':unittest.main()
