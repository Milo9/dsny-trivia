"""Save explicit comparisons and apply reviewed batch-11 decisions."""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(path): return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
def run(*args): subprocess.run([sys.executable,'scripts/question_audit.py',*args],cwd=ROOT,check=True)
catalog={q['id']:q for p in (ROOT/'questions').glob('q-*.json') for q in json.loads(p.read_text(encoding='utf-8'))}
reasons={
 (563,1117): 'Max the teenage son in A Goofy Movie and Max the dog in Little Mermaid are different characters and relationships; shared first name gives no identity fact.',
 (521,2407): 'Treasure Planet literary source versus the opening name of a Bay Lake preserve: separate adaptation and park-history facts.',
 (578,1132): 'Naveen is Tiana\'s frog love interest; Eudora is her mother. Knowing one relationship does not identify the other.',
 (515,636): 'Red paint on Alice\'s roses versus red paintwork on Lightning McQueen: distinct films, objects and contexts.',
 (510,1594): 'Robin Hood is a fox; Friar Tuck is a badger. Species of one character cannot establish the species of the other.',
 (520,859): 'Kenai becomes a bear through magic; Little John is depicted as a bear in Robin Hood. Distinct character/story facts.',
 (534,2499): 'Sherlock Holmes is the fictional inspiration for Basil; Eve Titus is the real author of the source books. Character model and book authorship are distinct facts.',
 (530,2380): 'Kuzco\'s llama transformation is separate from a llama outwitting Donald in Saludos Amigos; same species does not identify either event.',
 (510,859): 'Robin Hood is a fox and Little John is a bear. Each asks a different character\'s species; no inference connects those species.',
}
leaks={
 529:'Atlantis identifies the film and setting, but does not supply Heart; alternatives also sound like power-crystal names. The exact designation still must be recalled.',
 521:'Treasure in the adaptation title is a legitimate title resemblance. All choices are adventure novels and the question requires identifying the actual source, not just its genre.',
 517:'Restaurant is a common venue noun in the question and answer. All four options are Italian restaurant-style names; it does not identify Tony.',
 518:'Oliver is shared by the film and source-book titles because the protagonist is retained. All options are Dickens novels; the source relationship is legitimate content.'
}
scope=set(read('audit/runs/next-shard-0011-plan.json')['questionIds'])
report=read('artifacts/question-audit.json')
decisions=[]
for f in report['findings']:
    if not scope.intersection(f['questionIds']) or (f.get('decision') or {}).get('status') in ('accepted','fixed'):
        continue
    if f['kind']=='duplicate': reason=reasons[tuple(sorted(f['questionIds']))]
    elif f['kind']=='leak': reason=leaks[f['questionIds'][0]]
    else: raise ValueError(f)
    decisions.append(dict(findingId=f['id'],questionIds=f['questionIds'],questions=[catalog[i] for i in f['questionIds']],reason=reason))
retirement={
 'questionIds':[506,10], 'questions':[catalog[506],catalog[10]],
 'decision':'Retire 506 in favor of the earlier approved q10.',
 'reason':'Both test Dumbo\'s flying discovery that redeems his oversized ears. Q10 explicitly frames humiliation over ears and its flight payoff; q506 restates the same ear/flight connection. Retain the already verified earlier, scene-contextualized question.',
 'evidence':'https://d23.com/a-to-z/dumbo-film/',
 'challenge':'The feature-versus-result phrasing is reciprocal testing of the same ear/flight fact. Neither adds another event, character or production fact. Q10 is active and already approved.'
}
artifact={'reviewer':'Codex','at':'2026-11-07','retirement':retirement,'findingDecisions':decisions,
 'additionalComparisons':[
 {'questionIds':[541,2134,2135], 'questions':[catalog[i] for i in [541,2134,2135]], 'reason':'Final q541 asks which body part of Flynn is healed at the campfire. Generic healing ability or Pascal\'s separate injury cannot reveal hand; q2135 instead asks the result of cutting hair. The final wording adds the specific injury detail rather than repeating the general power.'},
 {'questionIds':[527,849,1098], 'questions':[catalog[i] for i in [527,849,1098]], 'reason':'Sisu is the sought dragon; Kumandra is the land and Heart is Raya\'s home region. Shared film vocabulary does not collapse these separate identity/geography facts.'}
 ]}
path='audit/runs/next-shard-0011-comparisons.json'
(ROOT/path).write_text(json.dumps(artifact,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for d in decisions:
    run('decide',d['findingId'],'accepted','--reviewer','Codex','--reason',d['reason'],'--reference',path)
print(f'Saved {len(decisions)} reviewed finding decisions and retirement comparison.')
