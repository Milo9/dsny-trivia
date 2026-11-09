"""Apply individually reasoned warning decisions and final edit classifications."""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))
def run(*args):
    for attempt in range(3):
        result = subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True)
        if result.returncode == 0 or 'WinError 5' not in result.stdout + result.stderr:
            break
        time.sleep(0.3)
    if result.returncode:
        print(result.stdout,result.stderr)
        raise SystemExit(result.returncode)

reasons = {
 (1384,2420): 'Gaston soundtrack attribution is separate from Beauty and the Beast earning a Best Picture nomination; neither answer establishes the other fact.',
 (1384,2577): 'The song Gaston and the first Broadway production are different music/theater facts; a shared film title does not determine both.',
 (1401,2211): 'Turning Red and Bao are different works; each independently requires knowing its Canadian setting. Shared Toronto answer is not a duplicate fact.',
 (1383,2653): 'Be Prepared soundtrack attribution and Mayor Lionheart species are unrelated. The Lion King title is normalized like lion by the detector, but the facts differ.',
 (1382,2284): 'Just Around the Riverbend belongs to Pocahontas; the 1996 Oscar defeat of Toy Story is a separate award fact about Colors of the Wind.',
 (1397,1620): 'March 3 arrival at Singapore is not the date of beginning regular passenger sailings. Knowing a 2026 sailing year cannot establish the earlier arrival date.',
 (1383,1453): 'Song-film attribution for Be Prepared does not establish Prince John being a lion in Robin Hood; shared normalized lion tokens are incidental.',
 (1397,2569): 'Singapore arrival date and the ship carrying Toy Story Place are distinct events/design facts; identifying one feature does not supply an arrival date.',
 (1124,1433): 'Kronk speaking squirrel and Up dogs being distracted by squirrels concern different films, characters and actions.',
 (698,1391): 'Circle of Life is the opening song title; Nants ingonyama is its opening phrase. Knowing the title does not establish the non-English opening words.',
 (151,1392): 'A Whole New World film association is different from the Ashman-to-Rice transition after a death; the common Aladdin title does not establish the production history.',
 (1433,2488): 'The Up dog distraction cue and Wart becoming a squirrel during a lesson are independent facts from different films.',
 (1420,2063): 'Bad-Anon is the support group name; the Pac-Man ghost pen is its meeting location. The group name does not establish which arcade game hosts it, and the location answer alone does not name the group.',
}

all_questions={}
for path in (ROOT/'questions').glob('q-*.json'):
    all_questions.update({q['id']:q for q in json.loads(path.read_text(encoding='utf-8'))})
plan=read('audit/runs/next-shard-0026-plan.json')
report=read('artifacts/question-audit.json')
comparisons=[]
for f in report['openFindings']:
    if not set(f['questionIds']).intersection(plan['questionIds']):
        continue
    pair=tuple(f['questionIds'])
    reason=reasons[pair]
    comparisons.append(dict(findingId=f['id'],questions=[all_questions[i] for i in pair],decision='accepted',reason=reason))
if comparisons:
    (ROOT/'audit/runs/next-shard-0026-comparisons.json').write_text(json.dumps(dict(reviewer='Codex',at='2026-11-08',comparisons=comparisons),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for c in comparisons:
    run('decide',c['findingId'],'accepted','--reviewer','Codex','--reason',c['reason'],'--reference','audit/runs/next-shard-0026-comparisons.json')

changes={
1388:('clarification distractors','Removed the brothers giveaway and made all options songwriting duos.'),
1389:('clarification category','Replaced awkward Oscar-negative premise with a precise studio release-order question; moved chronology to movies.'),
1390:('clarification','Removed unsupported most-covered superlative and bounded to the original animated performance.'),
1391:('factual clarification','Removed unsupported Sotho language claim and ambiguous first-two-words framing; asks opening phrase.'),
1392:('factual clarification','Original allowed both Beauty and the Beast and Aladdin; added 1992 and documented Tim Rice transition.'),
1394:('clarification','Dated current program name and removed incomplete tier list.'),
1396:('factual clarification','Corrected outdated ages 3-12 to ages 3-10 and specified supervised programming and date.'),
1399:('factual clarification distractors','Corrected obsolete delivered-paper premise and formal name Personal Navigator; parallel alternatives.'),
1400:('clarification distractors','Removed nightly guarantee; made the material identification and all sculpture options parallel.'),
1407:('clarification distractors','Removed overlapping lunar-eclipse and blood-moon alternatives; attributed red moon terminology to Ming.'),
1410:('clarification','Used building inspector and removed shared city token while preserving job fact.'),
1413:('factual clarification distractors','Replaced inevitable physical incompatibility with Ember\'s stated pre-touch fear; parallel exclusive alternatives.'),
1417:('factual clarification','Corrected initial detention location to the Vault and identified the jar rather than Back of the Mind.'),
1420:('factual clarification','Removed wrong Game Central Station meeting location, preserving support-group-name fact.'),
1421:('clarification','Attributed numeric height to Ralph\'s opening introduction rather than an unverified in-game description.'),
1422:('clarification','Removed answer from stem, shortened answer, and avoided unsupported permanence/no-visits implication.'),
1423:('clarification distractors','Specified initial hilltop summer-home project and made all proposed building projects parallel.'),
1424:('clarification distractors','Removed very-start and on-a-whim overstatements; shortened all firing/revenge alternatives.'),
1426:('clarification distractors','Specified rescue dilemma, removed whenever absolute and shoulder giveaway; parallel conscience pairs.'),
1429:('factual clarification distractors difficulty','Love motivates the explicit 24-hour bargain rather than mechanically removing strength; renewed mechanism/options and set medium.'),
1430:('clarification difficulty','Added Achilles\' heel detail so other former trainees cannot fit; calibrated obvious mythological cue to medium.'),
1432:('clarification distractors difficulty','Shortened explicit vindication motive and parallel alternatives; plot-recall difficulty set medium.'),
1433:('clarification','Removed universal all-dogs/whenever claim while preserving the recurring squirrel cue.'),
1434:('clarification distractors','Shortened all three-item bundles and used precise visitation-spell name; removed unrelated portkey wording.'),
}
for i,(types,reason) in changes.items():
    current = read('audit/ledger.json')['changeClassifications'].get(str(i),{})
    review_hash = next(r['hash'] for r in read('audit/runs/next-shard-0026-final-notes.json')['reviews'] if r['questionId']==i)
    if current.get('hash') == review_hash and set(current.get('types',[])) == set(types.split()):
        continue
    args=['classify',i,'--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0026-reviews.json']
    for kind in types.split(): args+=['--type',kind]
    run(*args)
print(f'Resolved {len(comparisons)} applicable findings and classified {len(changes)} retained edits.')
