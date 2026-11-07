"""Codex's final content classifications and individually evaluated finding decisions."""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
reference='audit/runs/next-shard-0009-reviews.json'
changes={
432:(['factual','clarification','distractors','difficulty'],'Corrected the false white hull/yellow funnels answer; historical Dream scope and parallel color pairs; medium difficulty.'),
434:(['clarification'],'Specified Dream at its 2011 debut rather than imply a single current fireworks title across the fleet.'),
447:(['clarification'],'Asked which film introduced the song so later reprises cannot qualify.'),
451:(['clarification'],'Specified separate album pop recordings, avoiding conflation with real film vocal contributions by Lebo M.'),
456:(['clarification'],'Specified eight original songs, separating songwriter from orchestral score or incidental music.'),
459:(['distractors'],'Removed actor-only parenthesis from the correct answer to make all four choices parallel character names.'),
460:(['distractors'],'Corrected the wrong-option song title to The Bare Necessities; the keyed answer was unchanged.'),
461:(['factual','clarification','distractors'],'Mancina also co-wrote Moana songs; replaced this second valid answer with Elton John, specified the original 2016 film and which-of-these wording.'),
462:(['distractors','difficulty'],'Replaced invented Oscar categories with real award categories and calibrated recognition to medium.'),
466:(['difficulty'],'Calibrated familiar song/award-category recognition to medium.'),
468:(['factual','clarification'],'Corrected composer to lyricist and all-song implication to collaboration; removed overlapping death-date clue.'),
471:(['clarification'],'Replaced subjective main focus with Pixar’s precise anticipatory-planning behavior.'),
472:(['factual','clarification'],'Removed false implication that Luca discovers his sea-monster identity; the boys conceal already-known identities.'),
479:(['clarification','distractors','difficulty'],'Asked street address and city, removed addressee-only length clue, and set exact-address recall to medium.'),
480:(['factual','clarification'],'Removed the false monocle condition and substituted Pixar’s positively documented phone-app behavior.'),
}
reasons={
'answer-style-a46e9b6347ae44bc0310':'All four answers are authentic Lion King song titles. Preserving the full winning title is necessary and does not supply a grammatical or semantic answer clue. The Academy separately establishes winner versus nominees.',
(468,1392):'Different facts after removing the death-date clue: q468 tests the lyricist partnership on both Beauty and the Beast and Aladdin; q1392 asks which film was completed/released after the named writer died. Film completion does not establish the two-film writing collaboration.',
(441,993):'Different song-performance associations: When You Wish Upon a Star versus Give a Little Whistle. Knowing who performs one song does not establish who performs the other.',
(462,466):'Separate Academy events: the 2000 Tarzan song win versus the 2014 Frozen song win. The same category label is not a duplicate fact.',
(17,459):'Object transformation versus ballroom vocal performance. Mrs. Potts being a teapot does not establish that she sings the title song.',
(458,718):'Separate award winners and years: 1995 Lion King versus 1993 Aladdin. Similar award phrasing does not repeat an outcome.',
(481,1036):'Different named characters and species: Destiny is a whale shark, Hank an octopus. One classification does not establish the other.',
(457,1382):'Different Pocahontas songs: Savages versus Just Around the Riverbend. Shared film answer does not establish the other song association.',
(438,701):'Character identity Elsa versus the performer name Idina Menzel. An additional actor-to-character fact is required; retain both.',
(450,701):'Different original-film song recordings: Into the Unknown in Frozen 2 versus Let It Go in Frozen. Sharing Menzel does not establish both performance credits.',
(468,703):'Different film credits: q703 tests Little Mermaid lyrics, while q468 requires the collaboration on both Beauty and the Beast and Aladdin. A lyricist can differ across films; the additional credits are new facts.',
(441,1102):'Jiminy’s song performance versus his appointment as conscience. Knowing the appointment does not establish that he sings this song.',
(457,1241):'Different songs and films: Savages belongs to Pocahontas, With a Smile and a Song to Snow White. Generic song-to-film wording is not duplication.',
(433,902):'Original ship construction country versus the location of a park replica. Shared Italy answer is incidental.',
(457,2284):'Savages song attribution versus Pocahontas winning the Oscar against Randy Newman’s Toy Story nomination. The Oscar outcome does not establish Savages’s film credit.',
}
def run(args):
    r=subprocess.run([sys.executable,'scripts/question_audit.py',*args],cwd=ROOT,capture_output=True,text=True)
    if r.returncode: raise SystemExit(r.stdout+r.stderr)
for qid,(types,reason) in changes.items():
    run(['classify',str(qid),*[a for t in types for a in ('--type',t)],'--reviewer','Codex','--reason',reason,'--reference',reference])
report=json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
planned=set(json.loads((ROOT/'audit/runs/next-shard-0009-plan.json').read_text())['questionIds'])
qs={q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
evidence=[]
for f in report['findings']:
    if not planned.intersection(f['questionIds']): continue
    if f.get('decision') and f['decision']['status'] in ('accepted','fixed'): continue
    key=f['id'] if f['kind']=='answer-style' else tuple(sorted(f['questionIds']))
    reason=reasons[key]
    evidence.append({'finding':f,'questions':[qs[i] for i in f['questionIds']],'reason':reason})
    run(['decide',f['id'],'accepted','--reviewer','Codex','--reason',reason,'--reference',reference])
(ROOT/'audit/runs/next-shard-0009-finding-decisions.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Classified {len(changes)} retained edits; decided {len(evidence)} findings with full question comparisons.')
