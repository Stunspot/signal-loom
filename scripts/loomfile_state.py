"""Loomfile record parsing and current material/output review bindings.

A binding proves declared byte/state consistency, never truth, reviewer identity
or permission. It excludes workflow labels, timestamps, review and history so
recording an assessment does not change the thing assessed.
"""
from __future__ import annotations
import hashlib,json,os
from pathlib import Path,PurePosixPath
try:
    from .archive_paths import assert_chain,assert_unlinked
except ImportError:
    from archive_paths import assert_chain,assert_unlinked

FORMAT='0.2.0'
MATERIAL_JSON=('state/brief.json','state/spine.json','state/visual-plan.json','state/theme.tokens.json','state/interactions.json','state/distribution.json','sources/manifest.json')
WORKFLOW_FIELDS={'stage','authority_status','publication_status','created_at','updated_at','approval'}
VERDICTS={'not_run','PASS','PASS_WITH_CONDITIONS','REVISE','BLOCKED'}

def text(value):return isinstance(value,str) and bool(value.strip())
def oneof(value,options):return isinstance(value,str) and value in options
def strings(value):return isinstance(value,list) and all(text(v) for v in value)
def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=value
    return result

def parse(raw):
    def invalid(value):raise ValueError('non-finite JSON value: '+value)
    return json.loads(raw,object_pairs_hook=unique_object,parse_constant=invalid)

def member(root,relative):
    if not text(relative) or '\\' in relative:raise ValueError('member must be a relative forward-slash path')
    parts=relative.split('/')
    if any(not p or p in {'.','..'} or ':' in p or '\x00' in p for p in parts):raise ValueError('unsafe member path: '+relative)
    path=assert_chain(root.joinpath(*parts))
    if not path.is_relative_to(root) or not path.is_file():raise ValueError('missing regular member: '+relative)
    return path

def read_json(root,relative):
    try:value=parse(member(root,relative).read_text(encoding='utf-8-sig'))
    except (OSError,UnicodeError,ValueError) as exc:raise ValueError(relative+': '+str(exc)) from exc
    if not isinstance(value,dict):raise ValueError(relative+': expected JSON object')
    return value

def read_lines(root,relative):
    try:lines=member(root,relative).read_text(encoding='utf-8-sig').splitlines()
    except (OSError,UnicodeError,ValueError) as exc:raise ValueError(relative+': '+str(exc)) from exc
    result=[]
    for number,raw in enumerate(lines,1):
        if not raw.strip():continue
        try:value=parse(raw)
        except ValueError as exc:raise ValueError(f'{relative}:{number}: {exc}') from exc
        if not isinstance(value,dict):raise ValueError(f'{relative}:{number}: expected JSON object')
        result.append(value)
    return result

def digest(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')
def file_digest(path):
    value=hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b''):value.update(chunk)
    return value.hexdigest()

def review_basis(root):
    """Capture the whole Loomfile's material basis; never create an assessment."""
    root=assert_unlinked(root)
    project=read_json(root,'project.yaml')
    material={'project':{k:v for k,v in project.items() if k not in WORKFLOW_FIELDS},'claims':read_lines(root,'state/claims.jsonl')}
    for relative in MATERIAL_JSON:material[relative]=read_json(root,relative)
    sources=material['sources/manifest.json'].get('sources')
    if not isinstance(sources,list):raise ValueError('source manifest: sources must be a list')
    source_bytes={}
    for source in sources:
        if not isinstance(source,dict) or not text(source.get('id')):raise ValueError('source record needs an id')
        if source['id'] in source_bytes:raise ValueError('duplicate source id: '+source['id'])
        source_bytes[source['id']]={'path':source.get('path'),'sha256':file_digest(member(root,source.get('path')))}
    outputs={}
    output_root=assert_chain(root/'output')
    if not output_root.is_dir():raise ValueError('output directory missing')
    for path in sorted(output_root.rglob('*')):
        if path.is_file():outputs[path.relative_to(root).as_posix()]=file_digest(path)
    value={'format':'signal-loom-review-basis/v1','material_sha256':digest(canonical(material)),'source_files':source_bytes,'output_files':outputs}
    value['sha256']=digest(canonical(value))
    return value

def review_errors(root,project,diagnostic):
    errors=[]
    verdict=diagnostic.get('status')
    if not oneof(verdict,VERDICTS-{'not_run'}):errors.append('review/diagnostics.json: current assessment verdict required')
    for key in ('reviewer','intended_use'):
        if not text(diagnostic.get(key)):errors.append('review/diagnostics.json: '+key+' required')
    if not strings(diagnostic.get('evidence')) or not diagnostic.get('evidence'):errors.append('review/diagnostics.json: actual assessment evidence references required')
    if not isinstance(diagnostic.get('top_three'),list) or not isinstance(diagnostic.get('secondary'),list):errors.append('review/diagnostics.json: top_three and secondary must be lists')
    conditions=diagnostic.get('conditions')
    if not isinstance(conditions,list):errors.append('review/diagnostics.json: conditions must be a list');conditions=[]
    conditions=list(conditions)
    for condition in conditions:
        if isinstance(condition,dict) and not isinstance(condition.get('blocking'),bool):errors.append('review/diagnostics.json: each condition needs an explicit blocking boolean')
    for group in ('top_three','secondary'):
        findings=diagnostic.get(group,[])
        if not isinstance(findings,list):continue
        for finding in findings:
            if not isinstance(finding,dict) or not isinstance(finding.get('blocking'),bool):
                errors.append('review/diagnostics.json: each finding needs an explicit blocking boolean');continue
            issue=dict(finding)
            if issue.get('status')=='resolved':issue['status']='met'
            conditions.append(issue)
    condition_ids=set()
    for condition in conditions:
        if not isinstance(condition,dict) or not text(condition.get('id')) or not oneof(condition.get('status'),{'open','met','accepted_residual'}):
            errors.append('review/diagnostics.json: condition needs unique id and open/met/accepted_residual status');continue
        if condition['id'] in condition_ids:errors.append('review/diagnostics.json: duplicate condition id')
        condition_ids.add(condition['id'])
        if not text(condition.get('statement')):errors.append('review/diagnostics.json: condition statement required')
        if condition['status']=='met' and not text(condition.get('resolution_evidence')):errors.append('review/diagnostics.json: met condition needs resolution evidence')
        if condition['status']=='accepted_residual':
            acceptance=condition.get('acceptance',{})
            if not isinstance(acceptance,dict) or not all(text(acceptance.get(k)) for k in ['owner','intended_use','evidence']):errors.append('review/diagnostics.json: accepted residual needs owner, intended use and evidence')
    if isinstance(diagnostic.get('top_three'),list) and len(diagnostic['top_three'])>3:errors.append('review/diagnostics.json: top_three has more than three findings; move additional findings to secondary')
    if verdict=='PASS_WITH_CONDITIONS' and not conditions:errors.append('review/diagnostics.json: conditional verdict needs its conditions')
    try:current=review_basis(root)
    except (OSError,ValueError) as exc:errors.append('review basis: '+str(exc));return errors
    if diagnostic.get('basis')!=current:errors.append('review/diagnostics.json: material inputs or outputs differ from the reviewed basis; preserve old review and assess current work')
    if project.get('authority_status')=='approved' or project.get('stage')=='approved_for_export':
        approval=project.get('approval',{})
        if not oneof(verdict,{'PASS','PASS_WITH_CONDITIONS'}):errors.append('approval requires a passing current review; REVISE/BLOCKED cannot support it')
        if not isinstance(approval,dict):errors.append('project.yaml: approval must be an object');approval={}
        if not all(text(approval.get(k)) for k in ['owner','intended_use','evidence']):errors.append('project.yaml: explicit approval owner, intended use and evidence required')
        if approval.get('basis_sha256')!=current['sha256']:errors.append('project.yaml: approval is not bound to the current material/output basis')
        if approval.get('intended_use')!=diagnostic.get('intended_use'):errors.append('project.yaml: approval intended use differs from the review')
        for condition in conditions:
            if not isinstance(condition,dict):continue
            if condition.get('status')=='open' and (condition.get('blocking',True) or oneof(condition.get('severity'),{'high','critical'})):errors.append('approval blocked by open condition: '+str(condition.get('id')))
            if condition.get('status')=='accepted_residual':
                acceptance=condition.get('acceptance',{})
                if not isinstance(acceptance,dict) or acceptance.get('owner')!=approval.get('owner') or acceptance.get('intended_use')!=approval.get('intended_use'):errors.append('approval residual acceptance must name the same accountable owner and use')
    return errors