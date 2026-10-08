#!/usr/bin/env python3
"""Write current material/output basis to a new file; does not review or approve."""
from __future__ import annotations
import argparse,json,os
from pathlib import Path
try:
    from .archive_paths import assert_chain,assert_unlinked
    from .loomfile_state import FORMAT,read_json,review_basis
except ImportError:
    from archive_paths import assert_chain,assert_unlinked
    from loomfile_state import FORMAT,read_json,review_basis

def capture(root,output):
    root=assert_unlinked(root);output=assert_chain(output.expanduser(),allow_missing=True)
    if os.path.lexists(output):raise ValueError('output already exists; choose a new basis file')
    if any(output.is_relative_to(root/folder) for folder in ['sources','state','output']):raise ValueError('basis output must not change material inputs or artifacts; use review/ or an external path')
    if read_json(root,'project.yaml').get('loomfile_version')!=FORMAT:raise ValueError('migrate the legacy Loomfile into a separate current-format copy first')
    basis=review_basis(root)
    output.parent.mkdir(parents=True,exist_ok=True);assert_chain(output.parent)
    with output.open('x',encoding='utf-8',newline='\n') as handle:handle.write(json.dumps(basis,indent=2)+'\n')
    return {'output':str(output),'basis_sha256':basis['sha256'],'boundary':'Basis capture only; no assessment, condition resolution, approval or status change.'}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('loomfile',type=Path);parser.add_argument('output',type=Path);args=parser.parse_args(argv)
    try:print(json.dumps(capture(args.loomfile,args.output),indent=2));return 0
    except (OSError,ValueError) as exc:print('Basis not captured: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())