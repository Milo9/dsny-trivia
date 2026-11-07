"""Apply Codex's reviewed warning decisions and retained-edit classifications."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHANGES = {
304: (['clarification','distractors'], 'Specified the theatrical film and replaced unrelated comedy trios with overlapping Scottish character names.'),
305: (['clarification','category'], 'Bound sponsor identity to Cars (2006); brand trivia belongs in pixar, rather than character-name coverage.'),
311: (['clarification','distractors'], 'Specified 1970 film and replaced generic pet-name groups with plausible overlapping film-character lists.'),
313: (['clarification'], 'Specified the 1996 film and captain role; feelings for Esmeralda alone do not distinguish all men.'),
320: (['clarification','distractors'], 'Replaced ambiguous main title rival with a specific crash-causing action; removed the named victim from options and specified the original film.'),
328: (['clarification','distractors','difficulty'], 'Narrowed from a difficult surname claim to the first-name identity directly supported by the primary synopsis; four parallel names and medium difficulty. No claim that the former surname is false.'),
331: (['distractors'], 'Replaced implausible invented ghost trios with overlapping sets of plausible Haunted Mansion names.'),
340: (['clarification','distractors'], 'Used precise soft-serve terminology and historical Aloha Isle context; removed the colloquial ice-cream label without claiming the original keyed product was wrong.'),
346: (['clarification','distractors'], 'Asked historical building location and made all four options parallel building names; removed Town Hall/City Hall duplication.'),
347: (['clarification'], 'Bound district name to its 2015 renaming, avoiding an unbounded current-status claim.'),
349: (['clarification'], 'Added breakfast preparation that distinguishes waffles from other real Mickey-shaped foods; original wording had multiple defensible treats.'),
351: (['clarification'], 'Asked for the name Disney uses for a specific route, excluding generic water-taxi descriptions as alternative proper names.'),
352: (['clarification','distractors'], 'Used historical two-night Halcyon experience instead of loose hotel/date wording and removed an informal alias of the keyed experience.'),
355: (['clarification'], 'Specified orange rather than green destination, then removed Mission word overlap on final challenge.'),
356: (['factual','clarification'], 'Corrected simulated speeds to a real outdoor high-speed car loop, removed test title-word clue, and specified 1999 official opening context.'),
359: (['clarification','distractors'], 'Specified E coupon introduction in 1959; avoided original-system ambiguity with the 1955 A/B/C books and used parallel coupon options.'),
360: (['clarification','distractors'], 'Removed the Guardians title from the stem and supplied pavilion/year context with comparable real attraction titles.'),
361: (['clarification','distractors'], 'Replaced invented hotels with actual resort alternatives and distinguished the savanna design without repeating animal from the keyed name.'),
364: (['clarification'], 'Asked the beginning year; the original celebrate wording also fit 2022 during an 18-month event.'),
366: (['clarification'], 'Bound the land name to the documented Hollywood Studios 2019 opening event.'),
}
REASONS = {
(358,463): 'Different events sharing 1992: Paris park opening versus an Academy Award for a film song. Neither answer establishes the other event date.',
(336,1136): 'Magic Kingdom Big Thunder land assignment differs from Disneyland Frontierland overall Old West design. A general theme at another park does not locate this specific Florida attraction.',
(345,1477): 'Distinct park productions: Disneyland Rivers of America versus Hollywood Studios lagoon show. Knowing a show title at one park does not establish that it also runs at the other; retained explicit park-specific coverage.',
(357,394): 'Different 2006 events: Expedition Everest opening and Disney acquisition of Pixar. The common year is not shared event knowledge.',
(340,739): 'Aloha Isle 1984 pineapple soft-serve identification differs from Castaway Cay availability. An island menu fact does not establish the product original venue, date or flavor.',
(354,398): 'Magic Kingdom Haunted Mansion opening and Roy Disney death are different historical events that happen to share 1971.',
(336,1138): 'Distinct attractions in the same land: Big Thunder versus Country Bear. Knowing one location does not supply the other attraction location.',
(354,599): 'Different attributes of Haunted Mansion: opening year versus land. A Liberty Square location does not establish 1971.',
(325,2481): 'Different films and roles: Ratigan species versus the intruder in Lady and the Tramp. Sharing rat as an answer is insufficient for duplication.',
(336,2526): 'Different parks and attractions: Magic Kingdom Big Thunder versus Disneyland Paris Phantom Manor. Shared land label Frontierland does not locate either from knowledge of the other.',
(357,922): 'Different Everest facts: opening year and Asia land location. Neither establishes the other.',
(338,1193): 'Existing EPCOT World Showcase location differs from Walt last filmed planning concept. A conceptual-city presentation does not identify the current international-pavilion area.',
}

def run(args):
    r = subprocess.run([sys.executable, 'scripts/question_audit.py', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stdout+r.stderr)

for qid, (types, reason) in CHANGES.items():
    args = ['classify',str(qid)]
    for kind in types:
        args += ['--type',kind]
    run(args+['--reviewer','Codex','--reason',reason,'--reference',f'audit/runs/next-shard-0007-reviews/{qid}.json'])

report = json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
plan = json.loads((ROOT/'audit/runs/next-shard-0007-plan.json').read_text())
scope = set(plan['questionIds'])
bank = {q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
comparisons = []
for finding in report['openFindings']:
    if not scope.intersection(finding['questionIds']):
        continue
    if finding['kind'] == 'duplicate':
        reason = REASONS[tuple(sorted(finding['questionIds']))]
    elif finding['id'] == 'leak-470962a9cb331b5f3bfa':
        reason = 'Boat is the generic transport class, not the distinctive Friendship name. Water Taxis, Resort Launches and EPCOT Ferries also name watercraft; the stem does not reveal Friendship. Exact Disney route naming is supported by the official Swan amenities page.'
    else:
        raise ValueError(f'Unexpected finding requires new review: {finding}')
    reference = 'audit/runs/next-shard-0007-comparisons.json'
    comparisons.append({'findingId':finding['id'], 'questions':[bank[i] for i in finding['questionIds']], 'reviewer':'Codex', 'at':'2026-11-06', 'status':'accepted', 'reason':reason})
    run(['decide',finding['id'],'accepted','--reviewer','Codex','--reason',reason,'--reference',reference])
(ROOT/'audit/runs/next-shard-0007-comparisons.json').write_text(json.dumps(comparisons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Classified {len(CHANGES)} retained edits and decided {len(comparisons)} current warnings.')
