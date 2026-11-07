"""Apply authored warning decisions and final-content edit classifications."""
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
report = json.loads((ROOT / 'artifacts/question-audit.json').read_text(encoding='utf-8'))
bank = {}
for path in (ROOT / 'questions').glob('q-*.json'):
    bank.update({q['id']: q for q in json.loads(path.read_text(encoding='utf-8'))})
reasons = {
 (59,300): 'Eeyore’s donkey identity and Christopher Robin’s human-friend identity are different characters and relationships. The shared Pooh wording does not supply the other answer.',
 (66,67): 'Timon is a meerkat and Pumbaa is a warthog. Knowing either character’s animal type does not establish the other’s; both final option sets avoid nested animal labels.',
 (97,687): 'EPCOT’s 1982 opening and the resort’s October 1, 1971 opening concern different establishments and events. They share date-question syntax, not a requested fact.',
 (78,2451): 'The original film’s bear identity and Baloo’s particular action in the sequel are different facts. Merely knowing Baloo is a bear does not establish who enters the village in the sequel.',
 (15,54): 'Ariel’s tail and Tinker Bell’s dress are different character attributes in different films. Green is a common color, not a shared underlying fact. Renewing this hash-bound decision restores q15’s existing coverage without changing its review.',
 (97,102): 'EPCOT opened in 1982; Animal Kingdom opened in 1998. Different parks and opening events require independent knowledge.',
 (91,103): 'Animal Kingdom’s defining wildlife/conservation theme and the location of Pandora are separate facts. Wildlife theming alone does not establish the Avatar land’s park.',
 (56,1384): 'Gaston courting Belle is a character relationship; attribution of the song Gaston to its film is a soundtrack fact. Knowing the suitor’s name alone does not identify the song’s film.',
 (56,567): 'Belle’s suitor Gaston and her horse Philippe are different characters and relationships; neither answer solves the other identity.',
 (90,692): 'The singing-children ride experience and its 1964 World’s Fair origin are separate facts. Present ride content does not establish the production/exhibition history.',
 (100,886): 'Pirates at Magic Kingdom and Indiana Jones Adventure at Disneyland are separate attraction-location facts. The two parks each having an Adventureland does not establish either ride’s location in the other park.',
 (91,348): 'Animal Kingdom’s overall wildlife purpose and Na’vi River Journey’s location are different facts. The overall theme does not tell a player where this specific Avatar attraction is.',
 (58,950): 'Maleficent’s film identity and the Super Technirama 70 production process require different knowledge. A shared Sleeping Beauty answer does not establish both requested facts.',
 (100,2525): 'Magic Kingdom Pirates and Disneyland Paris Skull Rock concern separate attractions at separate parks. Shared land names are not duplicate attraction-location facts.',
 (94,779): 'Cinderella Castle’s location and the small-world boat ride’s location are different attraction-location facts. A shared Fantasyland answer does not establish both.',
 (57,2364): 'Seven dwarfs and seven Billboard credited artists concern entirely unrelated sets. The common number is not a repeated fact.',
 (51,): 'Mouse is Mickey’s ordinary surname and a shared surname with Minnie, not a revealed partner’s first name. Fictional characters’ relationships are not determined by matching species; the question still requires identifying Minnie, appropriate for easy recognition.',
}

comparisons = []
for finding in report['findings']:
    ids = tuple(finding['questionIds'])
    if ids not in reasons or finding.get('decision'):
        continue
    comparisons.append({'finding': finding, 'questions': [bank[qid] for qid in ids], 'decision': 'accepted', 'reason': reasons[ids], 'reviewer': 'Codex (OpenAI)'})
reference = ROOT / 'audit/runs/next-shard-0002-comparisons.json'
reference.write_text(json.dumps(comparisons, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def run(args):
    result = subprocess.run(['python', 'scripts/question_audit.py'] + args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        print(result.stdout, result.stderr)
        raise SystemExit(result.returncode)

for comparison in comparisons:
    run(['decide', comparison['finding']['id'], 'accepted', '--reviewer', 'Codex (OpenAI)', '--reason', comparison['reason'], '--reference', str(reference.relative_to(ROOT))])
print(f'Applied {len(comparisons)} specific warning decisions.', flush=True)

types = {
 54: ['clarification'], 58: ['clarification'],
 66: ['distractors'], 67: ['distractors'],
 69: ['clarification'], 70: ['clarification','distractors'],
 72: ['clarification','difficulty'], 73: ['clarification'],
 74: ['clarification'], 77: ['clarification'],
 81: ['difficulty'], 83: ['clarification','difficulty'],
 84: ['difficulty'], 85: ['clarification'],
 90: ['clarification'], 92: ['clarification'], 98: ['clarification'],
}
edit_reasons = {
 54: 'Specify the 1953 animated Peter Pan character design rather than every costume or adaptation.',
 58: 'Remove the unnecessary first-appearance chronology and identify the animated villain’s film directly.',
 66: 'Replace Mongoose, a defensible broader family label for a meerkat, with Otter. Correct answer remains Meerkat.',
 67: 'Replace overlapping Pig and broad Wild boar labels with disjoint animal choices. Correct answer remains Warthog.',
 69: 'Ask for the musical Greek chorus rather than all narrators, distinguishing the credited opening spoken narrator.',
 70: 'Replace place/generic-description alternatives with character names; ask the directly sourced Lalotai residence instead of unlocated fishhook evidence.',
 72: 'Identify the exact bedpost-jump line rather than a subjective famous catchphrase; label familiar scene recall easy.',
 73: 'Distinguish originating the Rivera music ban from enforcing it in later generations.',
 74: 'Specify animated 2002 context and describe the social worker’s assessment accurately.',
 77: 'Replace awkward best friend gorilla wording with the source-backed talkative gorilla companion description.',
 81: 'Basic seven-dwarf membership recognition is easy rather than hard; answers and fact unchanged.',
 83: 'Use the source-backed muscular helper description instead of unqualified loyalty/intelligence judgments; main sidekick recognition is medium.',
 84: 'Lead-character name recognition is medium rather than hard; wording and answers unchanged.',
 85: 'Use pet reptiles because two Disney encyclopedia entries disagree on crocodile versus alligator. No confirmed wrong name or species correction is claimed.',
 90: 'Specify Magic Kingdom and the singing-children boat experience; remove world/world lexical echo.',
 92: 'Specify official attraction name so informal Epcot Globe is not a competing naming standard.',
 98: 'Describe the runaway Himalayan train/Yeti experience without echoing expedition from the answer.',
}
for qid, kinds in types.items():
    args = ['classify', str(qid)]
    for kind in kinds:
        args += ['--type', kind]
    run(args + ['--reviewer', 'Codex (OpenAI)', '--reason', edit_reasons[qid], '--reference', f'audit/runs/next-shard-0002-reviews/{qid}.json'])
print(f'Classified {len(types)} edited retained questions.', flush=True)
