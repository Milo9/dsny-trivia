"""Record the individually evaluated comparisons and final-hash edit types."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
report = json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
plan = json.loads((ROOT/'audit/runs/next-shard-0005-plan.json').read_text(encoding='utf-8'))
bank = {q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
REASONS = {
 (232,2204): 'Original-film ice-harvester/search companion identity versus the particular decoration-guard assignment in Frozen Fever. Knowing Kristoff’s trade does not establish the short’s party assignment.',
 (223,2453): 'Bagheera as Mowgli’s original panther guardian versus Baloo’s assignment to protect Ranjan during a specific sequel rescue. Different child, film and event; knowing original guardian does not establish sequel assignment.',
 (225,634): 'Different characters in different films. Luisa and Mr. Incredible both having strength does not establish either character’s power from the other.',
 (217,725): 'Quasimodo is the fictional protagonist; Alan Menken is the score composer. Separate character and production facts.',
 (226,999): 'Identifying Cruella as puppy-fur villain does not establish that a song named for her is actually in the film. Character role versus song-film association; retain both.',
 (245,1049): 'Ray is a Cajun firefly in Princess and the Frog; Mr. Ray is Nemo’s teacher in another film. Shared partial name does not connect the facts.',
 (217,1075): 'Character identity versus the specific cathedral where he lives. The title is context in the protagonist question; the home relationship is the tested fact in 1075. Quasimodo as a name alone does not identify a cathedral.',
 (84,249): 'Milo’s linguist/cartographer identity versus his expedition’s destination. The destination question omits its giveaway film title; these are separate person and geography facts.',
 (239,262): 'Zero is the ghost dog; Sally is the ragdoll love interest. Same Jack framing but different characters and roles.',
}
CHANGES = {
 210: (['clarification','distractors'], 'Use established house nickname Casita; replace Casa Madrigal, a defensible literal description, and keep parallel name alternatives.'),
 216: (['clarification'], 'Pin the Pumpkin King title to his own town rather than vague control of a holiday, avoiding Christmas takeover ambiguity.'),
 219: (['clarification'], 'Scope weapon identification to the tower knockout in the original film, avoiding claims about every object used in combat.'),
 220: (['clarification'], 'Specify 1989 animation, where Scuttle is a seagull, and ask the actual fork nickname.'),
 221: (['clarification'], 'Specify original 1992 film and third granted wish rather than unspecified final franchise wish. Avoid mentioning Genie in the stem because it gives the answer.'),
 222: (['clarification'], 'Ask the explicitly built self-taught guitar, avoiding unbounded claims that Miguel never plays another instrument.'),
 228: (['factual','clarification','distractors'], 'Original answer attributed sleep to Maleficent’s original curse, though she curses death and Merryweather mitigates it. Test the unambiguous spindle trigger with balanced sharp-object options.'),
 229: (['clarification','distractors'], 'Specify 1950 animation and replace squash, which also describes a pumpkin, with cabbage.'),
 231: (['factual','clarification','distractors'], 'Correct false premise that Maximus belongs to Flynn; ask the pursuing palace horse and replace human Phillip with horse Samson.'),
 236: (['clarification','distractors'], 'Pin the villain question to 2016 predator conspiracy and use on-screen Bellwether rather than unnecessary first name.'),
 240: (['clarification'], 'Replace ambiguous best friend with the human confidante about John Smith, excluding animal companions and tree mentor.'),
 247: (['distractors','difficulty'], 'Use comparable Disney character-name pairs instead of generic animal labels; central protagonist recall is easy.'),
 249: (['clarification','difficulty'], 'Remove answer Atlantis from film title in stem and calibrate basic title/destination association to easy.'),
 250: (['clarification'], 'Use companion rather than unsupported pet ownership, and specify the 1995 film.'),
 142: (['clarification'], 'Bind statue identification to the 2013 atrium redesign, avoiding an indefinitely current-status claim.'),
}

def run(*args):
    r = subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stdout+r.stderr)

comparisons=[]
for finding in report['findings']:
    if not set(finding['questionIds']).intersection(plan['questionIds']) or finding.get('decision'):
        continue
    pair=tuple(finding['questionIds'])
    reason=REASONS[pair]
    comparisons.append({'findingId':finding['id'],'questions':[bank[i] for i in pair],'reviewer':'Codex','at':'2026-11-06','decision':'accepted','reason':reason})
ref='audit/runs/next-shard-0005-comparisons.json'
(ROOT/ref).write_text(json.dumps(comparisons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for comparison in comparisons:
    run('decide',comparison['findingId'],'accepted','--reviewer','Codex','--reason',comparison['reason'],'--reference',ref)
for qid,(types,reason) in CHANGES.items():
    args=['classify',str(qid),'--reviewer','Codex','--reason',reason,'--reference',f'audit/runs/next-shard-0005-reviews/{qid}.json']
    for kind in types:
        args.extend(['--type',kind])
    run(*args)
print(f'Recorded {len(comparisons)} comparison decisions and {len(CHANGES)} classifications.')
