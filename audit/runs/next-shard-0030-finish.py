"""Record batch-30 editorial classifications and final comparison decisions."""
import json
import subprocess
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/question_audit.py'
def run(*args):
    command=[sys.executable,str(SCRIPT),*map(str,args)]
    for attempt in range(3):
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
        if result.returncode and 'WinError 5' in result.stdout+result.stderr and attempt<2:
            time.sleep(0.5)
            continue
        print(result.stdout,end='')
        print(result.stderr,end='',file=sys.stderr)
        result.check_returncode()
        return

classes = {
2019: ('clarification','Removed an unnecessary sibling age qualifier.'),
2020: ('factual','Corrected Morgana’s henchman from an electric eel to a shark.'),
2021: ('clarification distractors','Shortened the assigned marriage mission and made the purpose options parallel.'),
2023: ('clarification distractors','Asked the count directly; removed the three-token echo and overlapping count formulations.'),
2025: ('clarification distractors','Replaced an unsupported primary-weapon ranking with the studio-described telescoping arm fact and distinct mechanisms.'),
2026: ('clarification distractors','Asked the full surname and gave all options the same title and initial.'),
2030: ('clarification','Specified initial disbelief without asserting an earlier change of belief.'),
2031: ('clarification distractors','Used the film’s concise title and parallel war options.'),
2033: ('factual clarification distractors','Corrected who performs the shrinking; identified the entered Brasil pop-up book.'),
2034: ('clarification','Removed unsupported age specificity and shortened the relationship question.'),
2035: ('clarification','Focused the occupation and removed incidental act detail.'),
2039: ('factual clarification distractors','Corrected loss of talent to Forte’s desire to retain musical influence and appreciation.'),
2041: ('factual clarification','Removed an in-film marriage claim and asked the final choice of romantic partner.'),
2043: ('clarification','Used presumed dead instead of asserting deliberate death-faking.'),
2044: ('factual clarification','Removed the erroneous ward relationship and retained the supported parents/son relationship.'),
2047: ('clarification distractors','Distinguished first pickup from later possession; made all options individual people.'),
2048: ('clarification distractors','Focused the reversal’s destination, distinct from the changed slipper recipient.'),
2049: ('factual','Corrected the baker romance’s film from Cinderella III to Cinderella II.'),
2050: ('clarification distractors','Removed carved necklace as an overlapping description of an amulet.'),
2051: ('clarification distractors','Removed the answer from the stem and made relationship answers parallel.'),
2053: ('factual clarification','Separated captive Frank’s role from local guide Jake’s role; removed kangaroo-mouse wording.'),
2054: ('clarification distractors','Asked the specific folk-art creature name; removed generic spirits/guardians descriptions.'),
2060: ('factual clarification distractors','Corrected the scene to an assumption people make rather than a true shared rescue history; parallel assumptions.'),
2061: ('clarification','Removed the venue giveaway for the separate meeting-location question.'),
2062: ('clarification','Asked directly which listed character attends the specified meeting.'),
2063: ('clarification distractors','Shortened parallel venue options and distinguished the station concourse.'),
2064: ('clarification','Specified the 2017 live-action version.'),
2065: ('clarification distractors','Specified the 2017 version and supplied only keyboard-instrument options.'),
2066: ('clarification','Used stool, supported by both screenplay and final-film account; shortened wording.'),
}
ledger=json.loads((ROOT/'audit/ledger.json').read_text(encoding='utf-8'))
review_hashes={r['questionId']:r['hash'] for r in json.loads((ROOT/'audit/runs/next-shard-0030-reviews.json').read_text(encoding='utf-8'))}
for qid,(types,reason) in classes.items():
    prior=ledger['changeClassifications'].get(str(qid),{})
    if prior.get('hash')==review_hashes[qid] and set(prior.get('types',[]))==set(types.split()):
        continue
    args=['classify',qid]
    for kind in types.split(): args += ['--type',kind]
    run(*args,'--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0030-reviews.json')

reasons = {
(2047,2446): 'First taking the dropped wand and receiving the altered slipper fitting are different actions. Knowing who takes the wand does not establish whom Tremaine later selects for the slipper.',
(2064,2066): 'Garderobe’s transformation is a wardrobe; her dog becomes a stool. Knowing the owner’s enchanted form does not identify the dog’s form.',
(2055,2178): 'Frida Kahlo’s own artist/performance cameo differs from Héctor impersonating her at the bridge. Identifying the real artist does not establish whose disguise Héctor chooses.',
(2047,2049): 'Anastasia taking the wand in Cinderella III and loving the baker in Cinderella II are separate events and films. Neither action establishes the other relationship.',
(2061,2063): 'One asks who leads the meeting; the other asks its venue. The venue was removed from 2061’s final stem, preserving independent facts.',
(2049,2446): 'Anastasia’s baker romance in Cinderella II is distinct from Tremaine altering a slipper to fit her in Cinderella III. Neither relationship establishes the other action.',
(1204,2031): 'The same war affected studio revenue and provides this sequel’s story setting. A studio business-history fact does not identify a fictional film’s setting.',
(2064,2065): 'Garderobe and Cadenza are different people transformed into different objects. Knowing wardrobe for one does not establish harpsichord for the other.',
(2065,2066): 'Cadenza becomes a harpsichord and the dog a stool; each question tests a separate character-to-object transformation.',
(33,2043): 'The original film’s English love interest and the sequel’s hooded rescuer are different scene relationships. A character’s romance does not establish his later rescue role.',
(2042,): 'England is the destination shared by the alternatives’ context, not proof of a peace mission. Identifying a destination does not determine why she travels.',
(2039,): 'Beast appears in the film title and identifies the person valuing Forte’s music. The repeated name does not reveal Forte’s motivation; other listed motives remain grammatically possible.',
(2059,): 'Light in the title Lightyear does not establish the story’s time-dilation explanation. The title is necessary film context and the mechanism is explicitly explained in dialogue.',
}
report=json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
catalog={}
for path in (ROOT/'questions').glob('q-*.json'):
    for q in json.loads(path.read_text(encoding='utf-8')): catalog[q['id']]=q
records=[]
for f in report['openFindings']:
    ids=tuple(f['questionIds'])
    if set(ids)&set(range(2018,2068)):
        if ids not in reasons: raise ValueError(f'Unreviewed finding: {f}')
        records.append(dict(findingId=f['id'],questions=[catalog[i] for i in ids],
            reviewer='Codex',at='2026-11-08',decision='accepted',reason=reasons[ids]))
reference='audit/runs/next-shard-0030-final-comparisons.json'
(ROOT/reference).write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for r in records:
    run('decide',r['findingId'],'accepted','--reviewer','Codex','--reason',r['reason'],'--reference',reference)
run('sync')
run('report','--out','artifacts/question-audit.json','--brief','--since','artifacts/question-audit.json')
run('check')
run('close','audit/runs/next-shard-0030-plan.json','--reviewer','Codex','--out','audit/runs/next-shard-0030-result.json')
