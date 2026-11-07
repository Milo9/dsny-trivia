"""Record Codex's individually assessed final-hash findings and edit types."""
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
report=json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
plan=json.loads((ROOT/'audit/runs/next-shard-0006-plan.json').read_text(encoding='utf-8'))
bank={q['id']:q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
REASONS={
 (256,531): 'Story location versus association of the particular song Once Upon a Time in New York City with its film. Knowing story geography alone does not establish that song appears; knowing its film does not establish where the story primarily occurs. Separate geography and musical fact.',
 (258,2338): 'A nursery offer in Peter Pan versus an actual climactic kiss in Hunchback II. Different characters, film and event; common action does not connect these facts.',
 (284,705): 'Cogsworth enchanted-object identity versus the title of an ensemble song. Knowing clock does not establish Be Our Guest; song title alone does not establish Cogsworth transformation.',
 (185,263): 'Gusteau motto authorship versus his biological relationship to Linguini. The common person has two independently learned facts; neither stem supplies the other answer.',
 (282,1119): 'Two different mother-child relationships: Sarabi/Simba versus Sarafina/Nala. Similar wording does not make the mothers interchangeable.',
 (288,290): 'Different named friends and species: Flounder/fish versus Scuttle/seagull. Learning one identity alone does not establish the other among the four choices.',
 (256,2162): 'Oliver and Company versus Soul geography. A shared New York setting does not establish one film location from the other.',
 (275,1131): 'Penny rescued by Bernard/Bianca versus a different Penny who owns Bolt. Shared first name, different fictional people and relationships.',
 (256,953): 'A fictional story setting versus the actual city hosting the 1964 Worlds Fair. Common answer is coincidental; neither relationship proves the other.',
 (268,516): 'Arthur nickname Wart versus mentor wizard Merlin. Learning a pupil nickname does not give the teacher identity, or vice versa.',
 (254,2438): 'Marahute species in Rescuers Down Under versus eagle-derived body parts of Coco hybrid Pepita. The creature identity does not establish the hybrid design relationship.',
 (251,807): 'Bruno the human Madrigal prophet versus Cinderella dog Bruno. Same name belongs to unrelated characters with different roles in different films.',
 (256,): 'City is the requested answer type and is a generic noun; it does not give New York. All four answers are city names with comparable granularity, so the mechanical overlap is necessary context rather than an answer leak.',
}
CHANGES={
252: (['factual','clarification','distractors'],'Remove Eli alias of correct father, replace with distinct characters, specify 2009 and drop shared surname from correct option.'),
253: (['clarification'],'Specify Disney 1950 adaptation for the two stepsisters.'),
254: (['clarification','distractors'],'Ask named Marahute species with parallel animal options; remove named-answer cue and unnecessary rarity/golden claim.'),
255: (['clarification'],'Specify 1998 animated Hun leader to distinguish live-action villain.'),
258: (['factual','clarification','distractors'],'Correct completed-gift premise to an interrupted offer, remove thimble conflation, and identify nursery scene with parallel actions.'),
260: (['clarification'],'Use central glitch/ally role rather than unbounded befriending of any racer.'),
263: (['factual','clarification','distractors'],'Original secret wording admits both paternity and ownership. Ask only father identity with four comparable people.'),
264: (['difficulty'],'Calibrate main story city recall from hard to medium.'),
266: (['clarification','difficulty'],'Specify 1940 and set central donkey-island location recall to medium.'),
268: (['clarification','distractors','difficulty'],'Name Arthur in stem, ask his nickname, replace his actual name as an alternative with comparable nickname labels, medium recall.'),
270: (['clarification','difficulty'],'Specify 1941 and calibrate maternal name recall to medium.'),
271: (['clarification'],'Use owl friend instead of unsupported ownership/pet framing.'),
273: (['clarification','distractors'],'Specify 1999 and balance all four full names, titles and initials; shared Porter surname makes exact full-name recall distinct from q1123.'),
274: (['clarification','difficulty'],'Specify 1961, remove unnecessary dimwitted wording, and calibrate familiar henchman pair to medium.'),
275: (['clarification','difficulty'],'Specify 1977 original rescue and calibrate orphan name recall to medium.'),
278: (['clarification','distractors'],'Ask specifically narrator mountain region, use plural wording of narration and parallel mountain-region names; distinguish common singular location shorthand.'),
281: (['clarification'],'Scope magical home land to Disney 1953 film.'),
285: (['clarification'],'Scope fairy name to Disney 1953 film.'),
286: (['clarification'],'Scope non-speaking dwarf to 1937 animation, avoiding remake differences and unbounded never claim.'),
287: (['clarification','distractors'],'Identify animal-made first outfit before Fairy Godmother; parallel sewn-garment options remove ball repetition and distinguish later magic dress.'),
290: (['clarification'],'Specify 1989 seagull rather than later live-action gannet.'),
291: (['clarification'],'Specify playmate before flight from Pride Lands so Timon and Pumbaa befriending him as cub after exile cannot fit.'),
292: (['clarification'],'Ask Sulley chosen nickname, excluding Mary as possible real-name interpretation.'),
294: (['difficulty'],'Set obscure Fauntleroy middle-name recall from easy to hard.'),
300: (['clarification','distractors'],'Scope young human friend to Disney films, replace real-world Billy Moon ambiguity and animal alternatives with human characters.'),
301: (['clarification'],'Identify exact apparent-son role in 2016 ice-pop scam instead of vague small criminal partnership.'),
302: (['clarification','distractors'],'Improve grammar, scope 2014 feature, use comparable names and replace TV-only Granville option with Tadashi.'),
}
def run(*args):
    r=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if r.returncode: raise SystemExit(r.stdout+r.stderr)

comparisons=[]
for f in report['findings']:
    if not set(f['questionIds']).intersection(plan['questionIds']) or f.get('decision'): continue
    pair=tuple(f['questionIds'])
    reason=REASONS[pair]
    comparisons.append({'findingId':f['id'],'questions':[bank[i] for i in pair],'reviewer':'Codex','at':'2026-11-06','decision':'accepted','reason':reason})
# Additional full-digest comparisons, even where final wording no longer triggers a detector.
for pair,reason in {
 (273,1123):'Exact first name and initial versus usual title/surname. Four final options all say Professor ... Porter, so memorizing Professor Porter cannot choose Archimedes Q. Genuine additional name detail.',
 (280,300):'Tiger Tigger versus human Christopher Robin: different Pooh companions; common framing does not supply either identity from the other.',
 (278,323):'Maleficent domain versus raven identity: different place and character facts.',
 (287,1244):'Garment made by animals versus the song they sing during making. Identifying dress alone does not name The Work Song.',
}.items():
    comparisons.append({'questions':[bank[i] for i in pair],'reviewer':'Codex','at':'2026-11-06','decision':'distinct-context','reason':reason})
ref='audit/runs/next-shard-0006-comparisons.json'
(ROOT/ref).write_text(json.dumps(comparisons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for c in comparisons:
    if c.get('findingId'):
        run('decide',c['findingId'],'accepted','--reviewer','Codex','--reason',c['reason'],'--reference',ref)
for finding,qid,reason in [
 ('manual-cff7b36d85588d3555fa',252,'Removed Eli alias; final alternatives are distinct people. Current schema-2 review challenges all four including James, Tiana father.'),
 ('manual-cad86f7121003baa7f5f',263,'Restricted final question to biological father; removed ownership alternative. Current schema-2 screenplay review establishes paternity and separately acknowledges ownership.'),
]:
    run('decide',finding,'fixed','--reviewer','Codex','--reason',reason,'--reference',f'audit/runs/next-shard-0006-reviews/{qid}.json')
for qid,(types,reason) in CHANGES.items():
    args=['classify',str(qid),'--reviewer','Codex','--reason',reason,'--reference',f'audit/runs/next-shard-0006-reviews/{qid}.json']
    for kind in types: args.extend(['--type',kind])
    run(*args)
print(f'Recorded {len(comparisons)} comparisons, 2 fixed concerns, {len(CHANGES)} classifications.')
