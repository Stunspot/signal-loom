#!/usr/bin/env python3
"""Build the complete Signal Loom product ZIP after release acceptance.

One intentional installable root serves both declared hosts. Excludes Git data,
private review evidence, caches, prior releases and shelf-only sidecars.
"""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
try:
 from .archive_paths import assert_chain,assert_unlinked,check_tree,atomic_zip
except ImportError:
 from archive_paths import assert_chain,assert_unlinked,check_tree,atomic_zip

ROOT_FILES=('SKILL.md','README.md','manifest.json','CHANGELOG.md','LICENSE.md','SECURITY.md','SUPPORT.md','CONTRIBUTING.md','VALIDATION.md','documentation-manifest.json')
DIRECTORIES=('agents','assets','docs','examples','fallbacks','knowledge','schemas','scripts','tests','delivery-sidecars')
SKIP_PARTS={'__pycache__','.pytest_cache','.git'}
REQUIRED=('scripts/init_loomfile.py','scripts/validate_loomfile.py','scripts/migrate_loomfile.py','scripts/capture_review_basis.py','scripts/package_loomfile.py','scripts/verify_release.py','knowledge/infographic-toolkit-v2-canonical.md','examples/counts-and-rates/README.md','agents/openai.yaml')

def selected(source):
 source=assert_unlinked(source)
 paths=[]
 for name in ROOT_FILES:
  path=source/name
  if not path.is_file():raise ValueError('missing release source: '+name)
  paths.append(path)
 for name in DIRECTORIES:
  folder=source/name
  if not folder.is_dir():raise ValueError('missing release directory: '+name)
  paths.extend(p for p in sorted(folder.rglob('*')) if p.is_file() and not SKIP_PARTS.intersection(p.relative_to(source).parts) and p.suffix not in {'.pyc','.pyo'} and not (name=='delivery-sidecars' and 'v0.1.1' in p.name))
 names={p.relative_to(source).as_posix() for p in paths}
 for name in REQUIRED:
  if name not in names:raise ValueError('missing required release member: '+name)
 return paths

def entries(source):
 source=assert_unlinked(source)
 info=json.loads((source/'manifest.json').read_text(encoding='utf-8'))
 if info.get('name')!='signal-loom' or info.get('version')!='0.2.0':raise ValueError('unsupported product identity/version')
 prefix='signal-loom-v'+info['version']
 payload=check_tree(source,selected(source),prefix)
 directories=[]
 for name in DIRECTORIES:
  directories.append(name)
  directories.extend(p.relative_to(source).as_posix() for p in (source/name).rglob("*") if p.is_dir() and not SKIP_PARTS.intersection(p.relative_to(source).parts))
 directories=sorted(set(directories))
 manifest={'format':'signal-loom-product-release/v1','product':'signal-loom','version':info['version'],'root':prefix,'hosts':['codex','claude'],'boundary':'Package consistency, not discovery, invocation, model behavior or human approval.','directories':directories,'files':[{'path':name[len(prefix)+1:],'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()} for name,data in payload]}
 payload.extend((prefix+'/'+name+'/',b'') for name in directories)
 payload.append((prefix+'/product-release.json',(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n').encode('utf-8')))
 return payload

def build(source,output):
 source=assert_unlinked(source);output=assert_chain(output.expanduser(),allow_missing=True)
 if output.is_relative_to(source):raise ValueError('release output must be outside source')
 payload=entries(source);atomic_zip(payload,output)
 return {'output':str(output),'file_count':sum(not name.endswith('/') for name,_ in payload),'product':'signal-loom','version':'0.2.0'}

def main(argv=None):
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args(argv)
 try:print(json.dumps(build(args.source,args.output),indent=2));return 0
 except (OSError,ValueError) as exc:print('Release not built: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())