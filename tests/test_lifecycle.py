"""Consequential Loomfile state, return and review controls; fictional data only."""
import copy,hashlib,json,shutil,tempfile,unittest,zipfile
from pathlib import Path
from unittest import mock
from scripts.init_loomfile import initialize
from scripts.validate_loomfile import validate
from scripts.loomfile_state import review_basis
from scripts.capture_review_basis import capture
from scripts.migrate_loomfile import migrate,snapshot
from scripts.package_loomfile import package


def read(p):return json.loads(p.read_text(encoding='utf-8'))
def put(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8',newline='\n')
def update(p,**changes):x=read(p);x.update(changes);put(p,x)

def built(root):
    initialize(root,'Fictional count comparison')
    data=b'region,count\nNorth,60\nSouth,40\n';(root/'sources/originals/counts.csv').write_bytes(data)
    update(root/'sources/manifest.json',sources=[{'id':'S-001','kind':'dataset','path':'sources/originals/counts.csv','authority':'illustrative','sha256':hashlib.sha256(data).hexdigest()}])
    claims=[{'id':'C-001','text':'North60;South40 fictional responses.','type':'count','source_id':'S-001','locator':'North and South rows','currentness':'dated','as_of':'2026-10-01','status':'sourced'}]
    (root/'state/claims.jsonl').write_text(''.join(json.dumps(c)+'\n' for c in claims),encoding='utf-8',newline='\n')
    update(root/'state/spine.json',status='draft',beats=[{'id':'B-001','role':'comparison','claim_ids':['C-001'],'text':'Compare counts without inventing rates.'}])
    update(root/'state/visual-plan.json',status='draft',representations=[{'beat_id':'B-001','form':'chart','rationale':'Comparable counts; no population denominators.','claim_ids':['C-001']}],semantic_outline=['h1 question','h2 counts','h2 limits'])
    (root/'output/web/index.html').write_text('<!doctype html><html lang="en"><head><title>Fictional counts</title><link rel="stylesheet" href="style.css"></head><body><main><h1>Counts, not rates</h1><p>Fictional data. North60;South40. Denominators not supplied.</p></main></body></html>',encoding='utf-8')
    (root/'output/web/style.css').write_text('body { color:#111; background:#fff }',encoding='utf-8')
    update(root/'project.yaml',stage='built');return root

def reviewed(root):
    built(root);update(root/'project.yaml',stage='reviewed',authority_status='reviewed')
    (root/'review/synthetic-observation.md').write_text('Synthetic native consistency fixture, not actual human review.',encoding='utf-8')
    update(root/'review/diagnostics.json',status='PASS',reviewer='fictional test reviewer',intended_use='internal discussion export',basis=review_basis(root),evidence=['review/synthetic-observation.md']);return root

def approve(root):
    basis=review_basis(root);update(root/'project.yaml',stage='approved_for_export',authority_status='approved',approval={'owner':'fixture-owner','intended_use':'internal discussion export','evidence':'Fictional test consent, not actual permission.','basis_sha256':basis['sha256']})

class LifecycleTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def assertValid(self,p):errors,_=validate(p);self.assertEqual(errors,[])
    def assertInvalid(self,p,fragment):errors,_=validate(p);self.assertTrue(any(fragment in e for e in errors),errors)
    def clone(self,p,name):q=self.root/name;shutil.copytree(p,q);return q

    def test_useful_intake_and_built_control_with_unearned_stage_contrasts(self):
        intake=initialize(self.root/'intake','New question');self.assertValid(intake)
        update(intake/'project.yaml',stage='spined');self.assertInvalid(intake,'actual linked story')
        update(intake/'project.yaml',stage='approved_for_export',authority_status='approved');(intake/'output/web/index.html').write_text('');self.assertInvalid(intake,'nonempty')
        self.assertValid(built(self.root/'built'))

    def test_known_identity_graph_and_record_contrasts(self):
        base=built(self.root/'base');self.assertValid(base)
        duplicate=self.clone(base,'duplicate');q=duplicate/'state/claims.jsonl';q.write_text(q.read_text(encoding='utf-8')*2,encoding='utf-8');self.assertInvalid(duplicate,'duplicate claim id')
        dangling=self.clone(base,'dangling');x=read(dangling/'state/spine.json');x['beats'][0]['claim_ids']=['C-999'];put(dangling/'state/spine.json',x);self.assertInvalid(dangling,'unknown claim')
        dangling=self.clone(base,'beat');x=read(dangling/'state/visual-plan.json');x['representations'][0]['beat_id']='B-999';put(dangling/'state/visual-plan.json',x);self.assertInvalid(dangling,'unknown beat_id')
        broken=self.clone(base,'broken');(broken/'state/spine.json').write_text('{bad');self.assertInvalid(broken,'state/spine.json')
        future=self.clone(base,'future');update(future/'project.yaml',loomfile_version='999.0.0');self.assertInvalid(future,'supported loomfile_version')

    def test_review_tracks_material_and_output_resources_not_history_or_journal(self):
        base=reviewed(self.root/'base');self.assertValid(base)
        (base/'state/decisions.jsonl').write_text('{"decision":"preserve historical note"}\n',encoding='utf-8');(base/'checkpoints/snapshots/note.txt').write_text('Historical note.');self.assertValid(base)
        for name,relative in [('number','output/web/index.html'),('style','output/web/style.css'),('brief','state/brief.json'),('source','sources/originals/counts.csv')]:
            p=self.clone(base,name);q=p/relative
            if name=='brief':update(q,intended_change='A different audience decision.')
            else:q.write_bytes(q.read_bytes()+b'\nchanged')
            if name=='source':x=read(p/'sources/manifest.json');x['sources'][0]['sha256']=hashlib.sha256(q.read_bytes()).hexdigest();put(p/'sources/manifest.json',x)
            self.assertInvalid(p,'reviewed basis')

    def test_approval_preserves_conditions_and_current_findings(self):
        base=reviewed(self.root/'base');approve(base);self.assertValid(base)
        rows=[('open',{'id':'Q1','statement':'Obtain missing denominator.','status':'open'},False),('met',{'id':'Q1','statement':'Obtain missing denominator.','status':'met','resolution_evidence':'Recorded actual resolution fixture.'},True),('accepted',{'id':'Q1','statement':'Omit rates.','status':'accepted_residual','acceptance':{'owner':'fixture-owner','intended_use':'internal discussion export','evidence':'Explicit fixture acceptance.'}},True),('wrong_owner',{'id':'Q1','statement':'Omit rates.','status':'accepted_residual','acceptance':{'owner':'another-person','intended_use':'internal discussion export','evidence':'Different owner.'}},False)]
        for name,condition,valid in rows:
            condition['blocking']=True
            p=self.clone(base,name);update(p/'review/diagnostics.json',status='PASS_WITH_CONDITIONS',conditions=[condition]);errors,_=validate(p);self.assertEqual(not errors,valid,(name,errors))
        for status in ['REVISE','BLOCKED']:
            p=self.clone(base,status);update(p/'review/diagnostics.json',status=status);self.assertInvalid(p,'passing current review')
        p=self.clone(base,'high');update(p/'review/diagnostics.json',top_three=[{'id':'F1','statement':'Incorrect visible count.','status':'open','blocking':True,'severity':'high'}]);self.assertInvalid(p,'open condition')
        p=self.clone(base,'note');update(p/'review/diagnostics.json',secondary=[{'id':'N1','statement':'Optional typography refinement.','status':'open','blocking':False,'severity':'low'}]);self.assertValid(p)

    def test_current_review_cannot_use_skipped_hash_validation(self):
        p=reviewed(self.root/'reviewed');self.assertValid(p);errors,warnings=validate(p,verify_hashes=False);self.assertTrue(any('requires source hash' in e for e in errors));self.assertTrue(warnings)

    def test_basis_capture_is_exclusive_and_does_not_promote_state(self):
        p=built(self.root/'built');before=(p/'project.yaml').read_bytes();target=p/'review/basis.json';capture(p,target);self.assertEqual(read(target),review_basis(p));self.assertEqual(before,(p/'project.yaml').read_bytes());saved=target.read_bytes()
        with self.assertRaisesRegex(ValueError,'already exists'):capture(p,target)
        self.assertEqual(saved,target.read_bytes())
        with self.assertRaisesRegex(ValueError,'material inputs'):capture(p,p/'output/web/basis.json')

    def test_separate_current_and_legacy_copies_preserve_all_originals_and_old_review(self):
        for version in ['0.1.0','0.2.0']:
            source=reviewed(self.root/('source-'+version));update(source/'project.yaml',loomfile_version=version);(source/'user-note.txt').write_text('Keep my preferred wording.');before=snapshot(source);dest=self.root/('copy-'+version);result=migrate(source,dest)
            self.assertEqual(snapshot(source),before);self.assertEqual(result['validation_errors'],[]);self.assertEqual(read(dest/'project.yaml')['authority_status'],'draft');self.assertEqual(read(dest/'review/diagnostics.json')['status'],'not_run');history=Path(result['historical_review'])
            self.assertEqual((history/'project.yaml').read_bytes(),(source/'project.yaml').read_bytes());self.assertEqual((history/'review/diagnostics.json').read_bytes(),(source/'review/diagnostics.json').read_bytes())
            for n in before:
                if n!='project.yaml' and not n.startswith('review/'):self.assertEqual((source/n).read_bytes(),(dest/n).read_bytes(),n)

    def test_copy_interruption_and_existing_destination_preserve_work(self):
        source=reviewed(self.root/'source');before=snapshot(source);dest=self.root/'partial'
        with mock.patch('scripts.migrate_loomfile.shutil.copyfileobj',side_effect=OSError('injected copy failure')):
            with self.assertRaisesRegex(OSError,'injected'):migrate(source,dest)
        self.assertTrue((dest/'.migration-incomplete.json').is_file());self.assertEqual(snapshot(source),before);partial=snapshot(dest)
        with self.assertRaisesRegex(ValueError,'already exists'):migrate(source,dest)
        self.assertEqual(partial,snapshot(dest));self.assertInvalid(dest,'incomplete copy')

    def test_reviewed_archive_roundtrip_keeps_review_basis_and_source(self):
        source=reviewed(self.root/'source');before=snapshot(source);out=self.root/'project.zip';package(source,out);extracted=self.root/'unpacked'
        with zipfile.ZipFile(out) as archive:archive.extractall(extracted)
        self.assertValid(extracted/source.name);self.assertEqual(snapshot(source),before)

    def test_wrong_json_types_return_diagnostics(self):
        base=reviewed(self.root/'base')
        cases=[('project.yaml','authority_status',[]),('state/spine.json','status',{}),('review/diagnostics.json','status',[])]
        for i,(relative,key,value) in enumerate(cases):
            p=self.clone(base,'shape'+str(i));update(p/relative,**{key:value});errors,_=validate(p);self.assertTrue(errors)
        p=self.clone(base,'claimshape');claim=json.loads((p/'state/claims.jsonl').read_text());claim['status']=[];(p/'state/claims.jsonl').write_text(json.dumps(claim)+'\n');self.assertTrue(validate(p)[0])

if __name__=='__main__':unittest.main()