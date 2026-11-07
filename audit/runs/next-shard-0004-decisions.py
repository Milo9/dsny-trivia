"""Record individually read comparisons and final-hash edit classifications."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
report = json.loads((ROOT/'artifacts/question-audit.json').read_text(encoding='utf-8'))
plan = json.loads((ROOT/'audit/runs/next-shard-0004-plan.json').read_text(encoding='utf-8'))
bank = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
REASONS = {
 (188,1313): 'Sadness\u2019s blue design and Joy\u2019s yellow design are attributes of different characters; neither answer establishes the other color.',
 (175,634): 'Mr. Incredible\u2019s civilian name and his superpower require separate recall; Bob Parr does not establish super strength.',
 (204,1094): 'Judy\u2019s job and hometown are distinct attributes; knowing police officer does not establish Bunnyburrow.',
 (179,305): 'Racing number and sponsor are distinct facts; 95 does not establish Rust-eze.',
 (196,2633): 'Film restaurant identity versus a specific real park ride\u2019s claw-machine design reference. Knowing the film location alone cannot establish which reference Alien Swirling Saucers uses; retaining both distinct associations.',
 (206,1353): 'Poisoned fruit and the Queen\u2019s disguise are separate plot attributes. Knowing apple does not identify her peddler disguise; knowing peddler does not identify fruit. The contextual stem in the latter is not its tested answer.',
 (159,725): 'Menken\u2019s three-film composition credits and his Hunchback score credit concern different productions. His name alone does not establish every film in his career.',
 (191,520): 'Elinor\u2019s transformation in Brave and Kenai\u2019s transformation in Brother Bear are different stories and characters. Shared animal alone proves no duplicate.',
 (158,1537): 'The Little Mermaid\u2019s Under the Sea Oscar and its Disney Renaissance historical role are different facts, even though the film title matches.',
 (172,2433): 'The Ratatouille protagonist identity and the other question\u2019s claimed Onward cameo concern different scenes/films. This duplicate decision does not validate the out-of-scope cameo premise; it needs its own factual review.',
 (169,2087): 'The 1941 Oscar ceremony and the studio animators\u2019 strike are different historical events; sharing a year does not establish either event\u2019s date.',
 (191,859): 'Elinor\u2019s magically changed form and Little John\u2019s species in another film are unrelated character facts.',
 (203,231): 'Flynn\u2019s civilian name and the horse\u2019s name concern different characters; Eugene Fitzherbert and Maximus are not interchangeable facts.',
 (205,1313): 'Belle\u2019s ballroom gown color and Joy\u2019s design color are separate visual facts in different films; shared yellow is not duplication.',
}
CHANGES = {
 158: (['clarification'], 'Bound the song-film identification to its unique 1990 Oscar result; avoids sequel/compilation-reuse ambiguity.'),
 168: (['distractors'], 'Removed parenthetical first names from the correct option to balance length with the other songwriting pairs.'),
 169: (['factual','clarification','distractors'], 'Corrected answer from film year 1940 to ceremony year 1941; expressly asks ceremony year and retains 1940 as a plausible distractor.'),
 171: (['clarification'], 'Specified original 1995 film so Bonnie\u2019s later ownership cannot also fit.'),
 183: (['difficulty'], 'Prominent original-film antagonist identity fits easy rather than medium.'),
 186: (['difficulty'], 'Prominent child companion identity fits easy rather than medium.'),
 188: (['difficulty'], 'Basic emotion-color recognition fits easy rather than medium.'),
 189: (['clarification'], 'Specified Lotso escape episode; the original donation-endpoint wording also allowed Bonnie\u2019s final home.'),
 196: (['difficulty'], 'Named recurring film restaurant recall fits medium rather than hard.'),
 197: (['difficulty'], 'Main villain identity fits medium rather than hard.'),
 198: (['clarification'], 'Requested the island proper name to exclude the literally descriptive Syndrome\u2019s Island alternative.'),
 199: (['difficulty'], 'Prominent critic name fits medium rather than hard.'),
 205: (['clarification'], 'Specified 1991 animation and ballroom dance to distinguish Belle\u2019s other outfits and adaptations.'),
}

def run(*args):
    r = subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stdout+r.stderr)

comparisons=[]
for f in report['findings']:
    if not set(f['questionIds']).intersection(plan['questionIds']) or f.get('decision'):
        continue
    pair=tuple(f['questionIds'])
    reason=REASONS[pair]
    comparisons.append({'findingId': f['id'], 'questions':[bank[i] for i in pair], 'reviewer':'Codex','at':'2026-11-06','decision':'accepted','reason':reason})
ref='audit/runs/next-shard-0004-comparisons.json'
(ROOT/ref).write_text(json.dumps(comparisons,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for c in comparisons:
    run('decide', c['findingId'], 'accepted', '--reviewer','Codex','--reason',c['reason'],'--reference',ref)
for qid,(types,reason) in CHANGES.items():
    args=['classify',str(qid),'--reviewer','Codex','--reason',reason,'--reference',f'audit/runs/next-shard-0004-reviews/{qid}.json']
    for kind in types:
        args.extend(['--type',kind])
    run(*args)
print(f'Recorded {len(comparisons)} comparison decisions and {len(CHANGES)} change classifications.')
