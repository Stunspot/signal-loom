"""Synthetic archive contracts; no real candidate release is built here."""
import io,json,tempfile,unittest,zipfile
from pathlib import Path
from scripts.archive_paths import check_members
from scripts.build_release import ROOT_FILES,DIRECTORIES,REQUIRED,build
from scripts.verify_release import verify
from scripts.init_loomfile import initialize
from scripts.package_loomfile import package

class ReleaseContractTests(unittest.TestCase):
 def test_complete_synthetic_release_preserves_empty_directories_and_detects_tamper(self):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);source=base/'synthetic';source.mkdir()
   for name in DIRECTORIES:(source/name).mkdir()
   for name in {*ROOT_FILES,*REQUIRED}:
    p=source/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('synthetic fixture\n',encoding='utf-8')
   (source/'manifest.json').write_text(json.dumps({'name':'signal-loom','version':'0.2.0'}),encoding='utf-8')
   (source/'examples/empty-return').mkdir()
   (source/'verification').mkdir();(source/'verification/private.txt').write_text('must stay outside cargo',encoding='utf-8')
   (source/'delivery-sidecars/old v0.1.1.md').write_text('superseded',encoding='utf-8')
   (source/'delivery-sidecars/current v0.2.0.md').write_text('current',encoding='utf-8')
   before={p.relative_to(source).as_posix():p.read_bytes() for p in source.rglob('*') if p.is_file()}
   target=base/'synthetic.zip';build(source,target);archive_before=target.read_bytes()
   with zipfile.ZipFile(target) as archive:archive.extractall(base/'extracted')
   extracted=base/'extracted/signal-loom-v0.2.0';self.assertGreater(verify(extracted),10)
   self.assertTrue((extracted/'examples/empty-return').is_dir());self.assertFalse((extracted/'verification').exists());self.assertFalse((extracted/'delivery-sidecars/old v0.1.1.md').exists());self.assertTrue((extracted/'delivery-sidecars/current v0.2.0.md').is_file())
   self.assertEqual(before,{p.relative_to(source).as_posix():p.read_bytes() for p in source.rglob('*') if p.is_file()})
   with self.assertRaisesRegex(ValueError,'existing archive'):build(source,target)
   self.assertEqual(archive_before,target.read_bytes())
   (extracted/'README.md').write_text('changed',encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'payload differs'):verify(extracted)

 def test_portable_namespace_controls_and_customer_sources_remain_opaque(self):
  controls=[('root/normal.txt',b'ok'),('root/sub/',b''),('root/sub/data.csv',b'a,b\n')];check_members(controls)
  contrasts=[[('../escape.txt',b'x')],[('root/NUL.txt',b'x')],[('root/trailing./x',b'x')],[('root/A',b'x'),('root/a',b'y')],[('root/file',b'x'),('root/file/nested',b'y')],[('root/\u00e9',b'x'),('root/e\u0301',b'y')],[('root/'+('x'*200),b'x')]]
  for case in contrasts:
   with self.subTest(case=case):
    with self.assertRaises(ValueError):check_members(case)
  nested=io.BytesIO()
  with zipfile.ZipFile(nested,'w') as archive:archive.writestr('../escape.txt','x')
  with self.assertRaises(ValueError):check_members([('root/runtime.zip',nested.getvalue())])
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);work=initialize(base/'story','Draft backup')
   source=work/'sources/originals/supplied.zip';source.write_bytes(nested.getvalue())
   package(work,base/'draft.zip')
   with zipfile.ZipFile(base/'draft.zip') as archive:
    self.assertEqual(nested.getvalue(),archive.read('story/sources/originals/supplied.zip'))
    project=json.loads(archive.read('story/project.yaml'));self.assertEqual('draft',project['authority_status']);self.assertEqual('intake',project['stage'])
   self.assertFalse((base/'escape.txt').exists())

if __name__=='__main__':unittest.main()