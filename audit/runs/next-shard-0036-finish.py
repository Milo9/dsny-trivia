"""Classify final edits and decide individually reviewed batch comparisons."""
import contextlib,io,json,sys,time
from pathlib import Path
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'scripts'))
from question_audit import main
def read(p):return json.loads((R/p).read_text(encoding='utf8'))
def cmd(*args):
 for attempt in range(8):
  out=io.StringIO()
  with contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):code=main(list(map(str,args)))
  if not code:return
  if 'WinError 5' not in out.getvalue():break
  time.sleep(0.25)
 print(out.getvalue());raise SystemExit(code)
changes=read('audit/runs/next-shard-0036-changes.json')
ledger=read('audit/ledger.json')
for i,c in changes.items():
 if ledger.get('changeClassifications',{}).get(i,{}).get('hash')==ledger['questions'][i]['hash']:continue
 args=['classify',i]
 for t in c['types']:args+=['--type',t]
 cmd(*args,'--reviewer','Codex','--reason',c['reason'],'--reference','audit/runs/next-shard-0036-reviews.json')
reasons={
 frozenset([1223,2352]):'Different facts: Cinderella statue ship versus joint Wish/Treasure technical dimensions. The statue does not identify a technical-plan pairing.',
 frozenset([729,2352]):'Different facts: a July 2022 maiden voyage versus dimensions in the joint Treasure/Wish deck plan. A shared ship answer is not shared knowledge.',
 frozenset([2274,2346]):'Different productions and premiere years: Toy Story musical in 2008 versus Frozen in 2016. Knowing either show\'s ship does not establish the other.',
 frozenset([2329,2461]):'Different short/feature pairings and years: Piper with Finding Dory in 2016 versus Bao with Incredibles 2 in 2018. Similar question form does not duplicate the fact.',
 frozenset([218,2322]):'Bambi\'s skunk name Flower versus a physical flower given by the baker in Cinderella II. A common word does not connect these facts.',
 frozenset([961,2346]):'Wonder\'s 1999 service introduction differs from hosting the Frozen stage-show debut in November 2016. Ship entry date does not disclose the later show.',
 frozenset([57,2364]):'Seven dwarfs in Snow White versus seven billed recording acts on a 2022 chart credit. These count unrelated sets.',
 frozenset([258,2338]):'Wendy offers Peter a kiss in the nursery; Quasimodo and Madellaine share a kiss in a sequel finale. Separate characters, films and events.'}
qs={q['id']:q for n in range(1,10) for q in read(f'questions/q-{n:03}.json')}
report=read('artifacts/question-audit.json');ids=set(read('audit/runs/next-shard-0036-plan.json')['questionIds']);comparisons=[]
for f in report['findings']:
 if f['kind']=='duplicate' and ids.intersection(f['questionIds']):
  reason=reasons[frozenset(f['questionIds'])]
  comparisons.append(dict(findingId=f['id'],questions=[qs[i] for i in f['questionIds']],reason=reason,challenge='Codex compared both final stems and all four options; neither answer supplies the other fact.'))
ref='audit/runs/next-shard-0036-comparisons.json'
(R/ref).write_text(json.dumps(dict(reviewer='Codex',at='2026-11-09',comparisons=comparisons,additionalChecks=[dict(questions=[qs[2337],qs[2437]],reason='The old common six-year answer concerned unrelated story chronology and production duration. Disney establishes seven story years for Hunchback II; no duplicate remains.'),dict(questions=[qs[2353],qs[2354]],reason='Artist attribution and presentation city are separate facts about the same map. Retain both.')]),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
for f in comparisons:cmd('decide',f['findingId'],'accepted','--reviewer','Codex','--reason',f['reason'],'--reference',ref)
cmd('decide','manual-3b00745a4acea7907790','fixed','--reviewer','Codex','--reason','Corrected the glasses-wearing White Geri as the actor of the heart-attack ruse. The renewed schema-2 review checks the final distraction question against plot and director interview; Black Geri is no longer claimed to win.','--reference','audit/runs/next-shard-0036-reviews.json')
print(f'Classified {len(changes)} retained edits and decided {len(comparisons)} distinct-fact comparisons plus the Geri concern.')
