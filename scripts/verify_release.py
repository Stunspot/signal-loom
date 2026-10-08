#!/usr/bin/env python3
"""Verify the exact extracted product payload against its embedded file manifest."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
try:
 from .archive_paths import assert_unlinked,check_members
except ImportError:
 from archive_paths import assert_unlinked,check_members

def verify(root):
 root=assert_unlinked(root)
 manifest=json.loads((root/'product-release.json').read_text(encoding='utf-8'))
 if manifest.get('format')!='signal-loom-product-release/v1' or manifest.get('product')!='signal-loom' or manifest.get('version')!='0.2.0':raise ValueError('unsupported release manifest')
 files=manifest.get('files')
 if not isinstance(files,list):raise ValueError('release manifest needs file list')
 if not all(isinstance(item,dict) and isinstance(item.get('path'),str) for item in files):raise ValueError('invalid release file record')
 check_members([(item['path'],b'') for item in files],inspect_payload=False)
 directories=manifest.get('directories')
 if not isinstance(directories,list) or not all(isinstance(name,str) for name in directories):raise ValueError('release manifest needs directory list')
 check_members([(name+'/',b'') for name in directories]+[(item['path'],b'') for item in files],inspect_payload=False)
 actual_dirs={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
 if set(directories)!=actual_dirs:raise ValueError('release directory inventory differs')
 expected={item['path']:item for item in files}
 actual={p.relative_to(root).as_posix():p for p in root.rglob('*') if p.is_file() and p!=root/'product-release.json'}
 if set(expected)!=set(actual):raise ValueError('release file inventory differs: '+str(sorted(set(expected)^set(actual))))
 for name,item in expected.items():
  data=actual[name].read_bytes()
  if len(data)!=item.get('bytes') or hashlib.sha256(data).hexdigest()!=item.get('sha256'):raise ValueError('release payload differs: '+name)
 info=json.loads((root/'manifest.json').read_text(encoding='utf-8'))
 if info.get('version')!=manifest['version'] or info.get('name')!=manifest['product']:raise ValueError('product identity differs')
 return len(files)

def main(argv=None):
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('root',type=Path);args=parser.parse_args(argv)
 try:print(f'PASS: {verify(args.root)} exact extracted product files; manifest is consistency evidence, not an authenticated signature');return 0
 except (OSError,ValueError) as exc:print('FAIL: '+str(exc));return 1
if __name__=='__main__':raise SystemExit(main())