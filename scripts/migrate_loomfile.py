#!/usr/bin/env python3
"""Copy old/current Loomfiles into a new review cycle without changing originals."""
from __future__ import annotations
import argparse,json,os,shutil,uuid
from datetime import datetime,timezone
from pathlib import Path
try:
    from .archive_paths import assert_chain,assert_unlinked
    from .loomfile_state import FORMAT,read_json,file_digest
    from .validate_loomfile import validate
except ImportError:
    from archive_paths import assert_chain,assert_unlinked
    from loomfile_state import FORMAT,read_json,file_digest
    from validate_loomfile import validate

def snapshot(root):
    root=assert_unlinked(root)
    return {p.relative_to(root).as_posix():file_digest(p) for p in sorted(root.rglob('*')) if p.is_file()}

def migrate(source,destination):
    source=assert_unlinked(source);destination=assert_chain(destination.expanduser(),allow_missing=True)
    if os.path.lexists(destination):raise ValueError('destination already exists; preserve it and choose a new copy')
    if destination.is_relative_to(source):raise ValueError('destination must be outside the original Loomfile')
    if (source/'.migration-incomplete.json').exists():raise ValueError('original has incomplete-copy marker; inspect it first')
    project=read_json(source,'project.yaml');version=project.get('loomfile_version')
    if not isinstance(version,str) or version not in {'0.1.0',FORMAT}:raise ValueError('unsupported original Loomfile version')
    original=snapshot(source)
    destination.parent.mkdir(parents=True,exist_ok=True);assert_chain(destination.parent);destination.mkdir()
    marker=destination/'.migration-incomplete.json';marker.write_text(json.dumps({'source':str(source),'state':'incomplete_copy_preserve_for_inspection'})+'\n',encoding='utf-8',newline='\n')
    for directory in sorted((p for p in source.rglob('*') if p.is_dir())):
        (destination/directory.relative_to(source)).mkdir(parents=True,exist_ok=True)
    for relative in original:
        src=assert_chain(source/relative);dst=destination/relative;dst.parent.mkdir(parents=True,exist_ok=True)
        with src.open('rb') as incoming,dst.open('xb') as outgoing:shutil.copyfileobj(incoming,outgoing)
    copied=snapshot(destination);copied.pop('.migration-incomplete.json')
    if original!=copied or original!=snapshot(source):raise ValueError('copy/source changed; incomplete marker and both trees retained for inspection')
    history=destination/'checkpoints/snapshots'/('prior-review-'+uuid.uuid4().hex[:8]);history.mkdir(parents=True)
    shutil.copy2(destination/'project.yaml',history/'project.yaml')
    current_review=destination/'review';old_review=history/'review'
    assert current_review.resolve().is_relative_to(destination.resolve()) and old_review.resolve().is_relative_to(destination.resolve())
    assert_chain(current_review);assert_chain(old_review.parent)
    current_review.rename(old_review);current_review.mkdir()
    prior_stage=project.get('stage');prior_authority=project.get('authority_status')
    project.update(loomfile_version=FORMAT,stage='intake',authority_status='draft',approval={},updated_at=datetime.now(timezone.utc).isoformat())
    project['previous_review']={'path':history.relative_to(destination).as_posix(),'prior_format':version,'prior_stage':prior_stage,'prior_authority':prior_authority,'status':'historical_only'}
    (destination/'project.yaml').write_text(json.dumps(project,indent=2)+'\n',encoding='utf-8',newline='\n')
    diagnostic={'artifact':'output/web/index.html','status':'not_run','reviewer':'','intended_use':'','reviewed_at':None,'basis':None,'evidence':[],'conditions':[],'top_three':[],'secondary':[],'unproved_layers':['current material and output review','current approval']}
    (current_review/'diagnostics.json').write_text(json.dumps(diagnostic,indent=2)+'\n',encoding='utf-8',newline='\n')
    if snapshot(source)!=original:raise ValueError('original changed during migration; incomplete marker retained')
    marker.unlink()
    errors,warnings=validate(destination)
    return {'destination':str(destination),'source_unchanged':True,'original_files_preserved':len(original),'historical_review':str(history),'stage':'intake','authority_status':'draft','validation_errors':errors,'validation_warnings':warnings,'boundary':'New copy; existing content preserved, old review/approval historical. Reconcile reported state gaps before advancing.'}

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('source',type=Path);parser.add_argument('destination',type=Path);args=parser.parse_args(argv)
    try:print(json.dumps(migrate(args.source,args.destination),indent=2));return 0
    except (OSError,ValueError) as exc:print('Copy not completed: '+str(exc));return 2
if __name__=='__main__':raise SystemExit(main())