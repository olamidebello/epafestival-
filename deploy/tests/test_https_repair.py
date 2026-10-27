import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('https_repair',Path(__file__).parents[1]/'olamidepanel/https.py')
h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)

class DNSChecks(unittest.TestCase):
    def lookup(self,addresses):
        return lambda *args,**kwargs:[(2,1,6,'',(address,0)) for address in addresses]
    def test_correct_public_address(self):
        self.assertEqual(h.dns_check(self.lookup(['154.16.170.86']),{'154.16.170.86'}),['154.16.170.86'])
    def test_wrong_aaaa_is_not_ignored(self):
        with self.assertRaises(ValueError):h.dns_check(self.lookup(['154.16.170.86','2001:db8::1']),{'154.16.170.86'})
    def test_empty_dns_refused(self):
        with self.assertRaises(ValueError):h.dns_check(self.lookup([]),{'154.16.170.86'})

class ACMEPaths(unittest.TestCase):
    def test_http_and_https_modes_keep_dedicated_challenge_path(self):
        spec=importlib.util.spec_from_file_location('activation',Path(__file__).parents[1]/'olamidepanel/activate.py')
        a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
        for cert in [None,('/cert.pem','/key.pem')]:
            text=a.render('/opt/epa-festival/current','a'*40,cert)
            self.assertIn('location ^~ /.well-known/acme-challenge/ { root /var/www/epa-festival-acme; }',text)

if __name__=='__main__':unittest.main()
