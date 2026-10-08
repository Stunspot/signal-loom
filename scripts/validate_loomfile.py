#!/usr/bin/env python3
"""Validate declared Loomfile state, relationships and current review consistency."""
from __future__ import annotations
import argparse
from pathlib import Path
try:
    from .archive_paths import assert_unlinked
    from .loomfile_state import FORMAT,MATERIAL_JSON,read_json,read_lines,member,text,strings,oneof,file_digest,review_errors
except ImportError:
    from archive_paths import assert_unlinked
    from loomfile_state import FORMAT,MATERIAL_JSON,read_json,read_lines,member,text,strings,oneof,file_digest,review_errors

STAGES=('intake','spined','planned','built','reviewed','approved_for_export')
AUTHORITIES={'draft','reviewed','approved'}
CLAIM_STATUSES={'sourced','inferred','illustrative','missing','stale','disputed'}
CURRENTNESS={'timeless','dated','current-sensitive'}
REQUIRED_DIRS=('sources/originals','state','output/web','output/carousel','output/platforms','review','checkpoints/snapshots')
REQUIRED_FILES=('project.yaml',*MATERIAL_JSON,'state/claims.jsonl','state/decisions.jsonl')

def validate(root:Path,verify_hashes:bool=True):
    errors=[];warnings=[]
    try:root=assert_unlinked(root.expanduser())
    except (OSError,ValueError) as exc:return [str(exc)],warnings
    if (root/'.migration-incomplete.json').exists():errors.append('incomplete copy marker present; inspect preserved copy before proceeding')
    for relative in REQUIRED_DIRS:
        if not (root/relative).is_dir():errors.append('missing required directory: '+relative)
    records={}
    for relative in ('project.yaml',*MATERIAL_JSON):
        try:records[relative]=read_json(root,relative)
        except ValueError as exc:errors.append(str(exc))
    try:claims=read_lines(root,'state/claims.jsonl');read_lines(root,'state/decisions.jsonl')
    except ValueError as exc:errors.append(str(exc));claims=[]
    if errors:return errors,warnings
    project=records['project.yaml'];stage=project.get('stage');authority=project.get('authority_status')
    if project.get('loomfile_version')!=FORMAT:
        return ['project.yaml: supported loomfile_version is '+FORMAT+'; preserve older work and use migrate_loomfile.py to create a separate current-format copy'],warnings
    if stage not in STAGES:errors.append('project.yaml: unsupported stage')
    if not oneof(authority,AUTHORITIES):errors.append('project.yaml: unsupported authority_status')
    if project.get('publication_status')!='manual_only':errors.append('project.yaml: publication_status must remain manual_only')
    for key in ('project_id','title'):
        if not text(project.get(key)):errors.append('project.yaml: '+key+' required')
    requested=project.get('requested_outputs')
    if not strings(requested) or not requested or len(set(requested))!=len(requested) or not set(requested)<={'web','carousel','platform'}:
        errors.append('project.yaml: requested_outputs needs unique web/carousel/platform values');requested=[]
    if stage=='approved_for_export' and authority!='approved':errors.append('approved_for_export requires explicit current approved authority')
    index=STAGES.index(stage) if stage in STAGES else 0
    if oneof(authority,{'reviewed','approved'}) and index<3:errors.append('reviewed/approved authority requires a built artifact')
    if not verify_hashes:
        warnings.append('source hash comparison explicitly skipped; this is diagnostic evidence only')
        if index>=4 or oneof(authority,{'reviewed','approved'}):errors.append('current review/approval validation requires source hash checks')
    brief_outputs=records['state/brief.json'].get('outputs')
    if not strings(brief_outputs) or set(brief_outputs)!=set(requested):errors.append('state/brief.json: outputs differ from project requested_outputs')
    manifest=records['sources/manifest.json'];sources=manifest.get('sources');source_ids=set()
    if manifest.get('manifest_version')!='0.1.0':errors.append('sources/manifest.json: unsupported manifest_version')
    if not isinstance(sources,list):errors.append('sources/manifest.json: sources must be a list');sources=[]
    for number,source in enumerate(sources,1):
        label=f'sources/manifest.json:{number}'
        if not isinstance(source,dict):errors.append(label+': expected source object');continue
        source_id=source.get('id')
        if not text(source_id):errors.append(label+': source id required')
        elif source_id in source_ids:errors.append(label+': duplicate source id '+source_id)
        else:source_ids.add(source_id)
        if not oneof(source.get('kind'),{'original','notes','dataset','existing_artifact','user_assertion'}):errors.append(label+': supported source kind required')
        if not oneof(source.get('authority'),{'supplied','user_asserted','derived','illustrative'}):errors.append(label+': supported source authority required')
        try:path=member(root,source.get('path'))
        except (OSError,ValueError) as exc:errors.append(label+': '+str(exc));continue
        expected=source.get('sha256')
        if expected is None:warnings.append(label+': no manifest hash; current review basis still records actual source bytes')
        elif not isinstance(expected,str) or len(expected)!=64 or any(c not in '0123456789abcdefABCDEF' for c in expected):errors.append(label+': invalid SHA-256')
        elif verify_hashes and file_digest(path)!=expected.lower():errors.append(label+': source hash mismatch')
    claim_ids=set();by_claim={}
    for number,claim in enumerate(claims,1):
        label=f'state/claims.jsonl:{number}';cid=claim.get('id')
        if not text(cid):errors.append(label+': claim id required')
        elif cid in claim_ids:errors.append(label+': duplicate claim id '+cid)
        else:claim_ids.add(cid);by_claim[cid]=claim
        for key in ('text','type'):
            if not text(claim.get(key)):errors.append(label+': '+key+' required')
        status=claim.get('status');currentness=claim.get('currentness')
        if not oneof(status,CLAIM_STATUSES):errors.append(label+': unsupported claim status')
        if not oneof(currentness,CURRENTNESS):errors.append(label+': unsupported currentness')
        sid=claim.get('source_id')
        if sid is not None and (not isinstance(sid,str) or sid not in source_ids):errors.append(label+': source_id is not declared')
        if status=='sourced' and (sid not in source_ids if isinstance(sid,str) else True):errors.append(label+': sourced claim needs a declared source_id')
        if status=='sourced' and not text(claim.get('locator')):errors.append(label+': sourced claim needs a locator')
        if status=='sourced' and oneof(currentness,{'dated','current-sensitive'}) and not text(claim.get('as_of')):errors.append(label+': dated/current-sensitive sourced claim needs as_of')
    spine=records['state/spine.json'];visual=records['state/visual-plan.json']
    for label,record in [('state/spine.json',spine),('state/visual-plan.json',visual)]:
        if not oneof(record.get('status'),{'not_started','draft','reviewed'}):errors.append(label+': unsupported status')
    beats=spine.get('beats');reps=visual.get('representations');beat_ids=set();used_claims=set()
    if not isinstance(beats,list):errors.append('state/spine.json: beats must be a list');beats=[]
    if not isinstance(reps,list):errors.append('state/visual-plan.json: representations must be a list');reps=[]
    def links(value,label):
        if not strings(value):errors.append(label+': claim_ids must be a list of nonempty ids');return
        if len(set(value))!=len(value):errors.append(label+': duplicate claim reference')
        for cid in value:
            if cid not in claim_ids:errors.append(label+': unknown claim '+cid)
            else:used_claims.add(cid)
    for number,beat in enumerate(beats,1):
        label=f'state/spine.json:beat{number}'
        if not isinstance(beat,dict):errors.append(label+': expected object');continue
        bid=beat.get('id')
        if not text(bid):errors.append(label+': beat id required')
        elif bid in beat_ids:errors.append(label+': duplicate beat id '+bid)
        else:beat_ids.add(bid)
        if not text(beat.get('role')):errors.append(label+': role required')
        links(beat.get('claim_ids'),label)
    represented=set()
    for number,rep in enumerate(reps,1):
        label=f'state/visual-plan.json:representation{number}'
        if not isinstance(rep,dict):errors.append(label+': expected object');continue
        bid=rep.get('beat_id')
        if not isinstance(bid,str) or bid not in beat_ids:errors.append(label+': unknown beat_id')
        else:represented.add(bid)
        form=rep.get('form')
        if not oneof(form,{'prose','diagram','chart','interaction','omit'}):errors.append(label+': unsupported form')
        if not text(rep.get('rationale')):errors.append(label+': rationale required')
        links(rep.get('claim_ids'),label)
        if form=='chart' and not rep.get('claim_ids'):errors.append(label+': chart needs declared supporting claims; numerical fitness still requires actual review')
    if index>=1 and (not beats or spine.get('status')=='not_started'):errors.append('spined or later requires an actual linked story')
    if index>=2:
        if not reps or visual.get('status')=='not_started':errors.append('planned or later requires actual representations')
        if beat_ids-represented:errors.append('visual plan must represent or expressly omit every beat: '+', '.join(sorted(beat_ids-represented)))
    if visual.get('mobile_first') is not True:errors.append('state/visual-plan.json: mobile_first must be true')
    if not strings(visual.get('semantic_outline')):errors.append('state/visual-plan.json: semantic_outline must be a string list')
    if index>=3:
        try:
            if member(root,'output/web/index.html').stat().st_size==0:errors.append('built or later requires nonempty output/web/index.html')
        except (OSError,ValueError) as exc:errors.append(str(exc))
        for output in requested:
            folder=root/'output'/('platforms' if output=='platform' else output)
            if not any(p.is_file() and p.stat().st_size for p in folder.rglob('*')):errors.append('requested output has no produced file: '+output)
    if authority=='approved' or stage=='approved_for_export':
        for cid in sorted(used_claims):
            if oneof(by_claim[cid].get('status'),{'missing','stale','disputed'}):errors.append('approved output uses unresolved claim: '+cid)
    if index>=4 or oneof(authority,{'reviewed','approved'}):
        try:diagnostic=read_json(root,'review/diagnostics.json')
        except ValueError as exc:errors.append(str(exc))
        else:
            if not errors:errors.extend(review_errors(root,project,diagnostic))
    return errors,warnings

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('loomfile',type=Path);parser.add_argument('--skip-hashes',action='store_true');args=parser.parse_args(argv)
    errors,warnings=validate(args.loomfile,verify_hashes=not args.skip_hashes)
    for warning in warnings:print('WARN: '+warning)
    for error in errors:print('ERROR: '+error)
    if errors:print(f'FAIL: {len(errors)} error(s), {len(warnings)} warning(s)');return 1
    print(f'PASS: Loomfile declared-state checks ({len(warnings)} warning(s)); not truth, rendering or authenticated authority');return 0
if __name__=='__main__':raise SystemExit(main())