import re,unittest
from pathlib import Path
EXPECTED=['valkey/valkey:8.1.5@sha256:7d94253109069f6cb2c9ac7b89d6fdee41b272ca82d525944f54f3c98ef285af']
PINS=[['valkey/valkey:8.1.5', '7d94253109069f6cb2c9ac7b89d6fdee41b272ca82d525944f54f3c98ef285af']]
def accept(ref,base,digest):
 if not re.fullmatch('[0-9a-f]{64}',digest) or ref!=base+'@sha256:'+digest:raise ValueError('mutable or unreviewed source reference')
class ImmutableRuntimeSource(unittest.TestCase):
 def test_actual_source_image_list(self):
  refs=re.findall(r'(?m)^\s*image:\s*["\']?([^"\'\s#]+)',(Path(__file__).parents[1]/'stack.runtime.yaml').read_text())
  self.assertEqual(EXPECTED,refs)
  for base,digest in PINS:accept(base+'@sha256:'+digest,base,digest)
 def test_floating_rejected(self):
  for base,digest in PINS:
   with self.subTest(base=base),self.assertRaises(ValueError):accept(base.rsplit(':',1)[0]+':latest',base,digest)
 def test_version_only_rejected(self):
  for base,digest in PINS:
   with self.subTest(base=base),self.assertRaises(ValueError):accept(base,base,digest)
 def test_malformed_digest_rejected(self):
  for base,digest in PINS:
   for bad in ['a'*63,'g'*64,'A'*64,'a'*65,'']:
    with self.subTest(base=base,bad=bad),self.assertRaises(ValueError):accept(base+'@sha256:'+bad,base,digest)
 def test_wrong_digest_rejected(self):
  for base,digest in PINS:
   with self.subTest(base=base),self.assertRaises(ValueError):accept(base+'@sha256:'+'0'*64,base,digest)
if __name__=='__main__':unittest.main()
