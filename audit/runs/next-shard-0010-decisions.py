"""Classify retained edits and record Codex's inspected finding comparisons."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
reference = 'audit/runs/next-shard-0010-reviews.json'
changes = {
 483: (['clarification','difficulty'], 'Used the official film title/year and specified the mastermind rather than a controlled decoy; medium twist recall.'),
 484: (['difficulty'], 'Hal is an obscure proper name not spoken in the film; changed easy to hard.'),
 485: (['difficulty'], 'Calibrated the fictional town name to medium.'),
 486: (['clarification'], 'Years apart distinguishes Bo Peep from reunions after shorter separations with Buzz or Jessie.'),
 491: (['clarification','distractors'], 'Asked the specific model animal and supplied four parallel shapes; avoids needing to exclude every simultaneous trap invention.'),
 495: (['clarification'], 'Removed unsupported all-remaining-humans quantifier and identified the Captain\'s particular ship.'),
 496: (['factual','clarification','distractors'], 'Removed the unsupported disappear-forever assertion: Héctor says nobody knows where the soul goes. Ask his explicit term with parallel alternatives.'),
 497: (['clarification','distractors'], 'Accounted for partial wet transformations and asked visible form; replaced unrelated abilities and sole long answer with parallel appearances.'),
 498: (['clarification','difficulty'], 'Replaced astronaut-program label with the documented mission organization and specified the original film; medium recall.'),
 499: (['difficulty'], 'Calibrated the colony setting name to medium.'),
 500: (['clarification','distractors','difficulty'], 'Removed before from the stem and unique parenthetical alias from the answer, used Great Beyond as a relevant distractor, and calibrated central realm recall to medium.'),
 326: (['clarification'], 'Specified Ratigan\'s pet cat rather than an unqualified pet, clearly separating Felicia from henchman Fidget.'),
 375: (['clarification'], 'Specified the historical pay-cut demand and distributor; separated the negotiation from Universal\'s legal ownership.'),
 427: (['factual','clarification'], 'Replaced vague runDisney/select-sailing framing with the documented self-paced run/walk, dated November 2026.'),
 436: (['clarification','distractors'], 'Specified Disney Cruise Line and followed Disney\'s long-pole derivation; corrected Enchanté spelling.'),
}
reasons = {
 (309,1284): 'Different color-character associations: Fear is purple and Disgust green. Learning one does not supply the other\'s color.',
 (309,1313): 'Different color-character associations: Fear-purple and Joy-yellow; shared emotion-color phrasing does not repeat a fact.',
 (272,1063): 'Roquefort\'s mouse/rescuer identity differs from Madame Bonfamille\'s ownership of the cats. Neither answer supplies the other relationship.',
 (329,531): 'Separate song-film credits: Good Company versus Once Upon a Time in New York City. One film can contain many songs; knowing one attribution does not establish the other.',
 (499,1272): 'Ant Island is a location name; the other question asks the princess\'s identity. Place name and royal character are separate facts. The outside-scope Atta/Dot ambiguity is not approved by this comparison.',
 (317,947): 'Disneyland caterpillar vehicles versus the Lewis Carroll source of the animated feature. Ride design is a separate fact from literary adaptation.',
 'leak-719701852b0ba93e7b743fd7676e1d2aac1f0f3cf719a03ecb43100e6d6b8441': 'Company is a necessary word in the actual song and film titles. The shared word alone does not establish a recording credit; three other animal films remain plausible. Preserve exact titles.',
 'leak-a07611ace1e3d4a60f1c2681bd558b3adb52b4b8580f9815bf8d75ac0f0404c0': 'Castaway Cay supplies necessary island context; other choices use island places Pelican Plunge and Serenity Bay, and a plausible Disney running-event name. Exact 5K identity remains required.',
}

def run(args):
    r = subprocess.run([sys.executable,'scripts/question_audit.py',*args],cwd=ROOT,capture_output=True,text=True)
    if r.returncode:
        raise SystemExit(r.stdout+r.stderr)

for qid,(types,reason) in changes.items():
    run(['classify',str(qid),*[x for t in types for x in ('--type',t)],'--reviewer','Codex','--reason',reason,'--reference',reference])
report = json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
planned = set(json.loads((ROOT/'audit/runs/next-shard-0010-plan.json').read_text())['questionIds'])
qs = {q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
evidence = []
for f in report['findings']:
    if not planned.intersection(f['questionIds']):
        continue
    if f.get('decision') and f['decision']['status'] in ('accepted','fixed'):
        continue
    key = tuple(sorted(f['questionIds'])) if f['kind']=='duplicate' else f['kind']+'-'+f['signature']
    reason = reasons[key]
    evidence.append(dict(finding=f,questions=[qs[i] for i in f['questionIds']],reason=reason))
    run(['decide',f['id'],'accepted','--reviewer','Codex','--reason',reason,'--reference',reference])
(ROOT/'audit/runs/next-shard-0010-finding-decisions.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Classified {len(changes)} retained edits and decided {len(evidence)} findings.')
