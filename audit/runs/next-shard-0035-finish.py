"""Classify retained changes and record specific final finding decisions."""
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf8'))
def save(p,v):(ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def command(*args):
    for attempt in range(10):
        p=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True)
        if not p.returncode:return
        if not any(code in p.stdout+p.stderr for code in ('WinError 5','WinError 32')):break
        time.sleep(1)
    raise RuntimeError(p.stdout+p.stderr)
ref='audit/runs/next-shard-0035-reviews.json'
changes=read('audit/runs/next-shard-0035-changes.json')
bank={q['id']:q for p in (ROOT/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf8'))}
for i,c in ([] if '--skip-classify' in sys.argv else changes.items()):
    assert c['after']==bank[int(i)] and c['before']!=c['after']
    command('classify',i,*[x for t in c['types'] for x in ('--type',t)],'--reviewer','Codex','--reason',c['reason'],'--reference',ref)
reasons={
'duplicate-5404a6922e9ad79c3e98':'The 2021 Philharmagic addition is a theme-park programming fact; identifying the song performed by Miguel and Hector at the film contest is a distinct scene fact. One location relationship does not establish the other.',
'duplicate-a0b286420002ecf4ed54':'Mademoiselle Minnie in the atrium and Aladdin in the theatre are separate entertainment/design facts. The statue identification does not establish the current production assignment.',
'duplicate-a87da87094d9912c3ab0':'The 2011 maiden voyage and the 2017 Beauty and the Beast debut are separate historical events. Identifying the ship in one event does not establish that it hosted the later production.',
'duplicate-af16e889b82c231aba0a':'Toy Story in 2008 and Frozen in 2016 are different productions and debut events. Knowing either was on Wonder does not locate the other without another fact.',
'duplicate-b8b1e6ecfc83b585ea02':'Eric dog name Max does not establish Grimsby household role. The common film and Prince Eric wording describe different relationships and answers.',
'duplicate-c4872626fbb94a8ae483':'Scoring Hunchback does not establish completion of a competitive EGOT in July 2020; an artistic credit and later award milestone are distinct.',
'duplicate-ccc358ec1ff1f43aba0b':'The Duke sending bodyguards is a plot action. Alan Tudyk voicing him is an English cast credit. Neither fact establishes the other merely because the character identity is shared.',
'duplicate-d255c327723d9d4e4a76':'The Admiral Donald atrium statue and 2017 Beauty and the Beast debut are independent ship details. Identifying the statue ship does not locate the later production.',
'duplicate-deeb33c484ddad9b6b48':'Writing Little Mermaid/Beauty/Aladdin music does not establish completion of a competitive EGOT in 2020. The award milestone is not another restatement of those credits.',
'duplicate-e929757d4cf14cef014c':'Kerchak identity as Kala mate and original leader differs from his choice of Tarzan as successor at death. Knowing the original leader does not identify the chosen successor; knowing Tarzan is the successor does not supply Kala mate without the separate earlier relationship.',
'leak-bd67b43ed9b4ebd4c999':'Princess is part of the required film title, not a statement of Charlotte ambition. Tiana restaurant and Louis musical ambition in the same film show that the title does not make every character seek a royal marriage.'}
report=read('artifacts/question-audit.json'); planned=set(read('audit/runs/next-shard-0035-plan.json')['questionIds'])
findings=[f for f in report['openFindings'] if planned.intersection(f['questionIds'])]
pending={f['id'] for f in findings}
assert pending <= set(reasons)|{'manual-6c24a178d2e1e3483a94'}
cref='audit/runs/next-shard-0035-comparisons.json'
if not (ROOT/cref).exists():
    save(cref,dict(reviewer='Codex',at='2026-11-09',scope=sorted(planned),topicContext='Read the complete combined catalog of 1080 unique questions from all 22 applicable topic digests; followed final wording changes with affected film/ship comparisons and cross-shard name searches.',findings=[dict(f,questions=[bank[i] for i in f['questionIds']],rationale=reasons.get(f['id'],'Replaced unsupported full film-name assertion with the screenplay-backed Kenneth exchange; see final schema-2 review.')) for f in findings],limitations='No current local player-report export was available and no live Firestore connector was connected. Player reports were not checked or resolved. Pre-existing manual concern on #2324 is outside this batch.'))
for fid,why in reasons.items():
    if fid in pending:command('decide',fid,'accepted','--reviewer','Codex','--reason',why,'--reference',cref)
if 'manual-6c24a178d2e1e3483a94' in pending:
    command('decide','manual-6c24a178d2e1e3483a94','fixed','--reviewer','Codex','--reason','Final question asks only the longer first name Kenneth explicitly used by Lotso. The unsupported middle name and surname were removed, and all four final options were verified after the issue was opened.','--reference',ref)
print('Classified',len(changes),'retained edits; resolved',len(findings),'applicable final findings.')
