"""Apply explicitly reviewed finding decisions and final edit classifications."""
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
def read(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def run(*args): subprocess.run([sys.executable,'scripts/question_audit.py',*args],cwd=ROOT,check=True)
reasons={
 (924,1168):'Roger Rabbit attraction location and Toontown opening/design history are different facts; knowing the 1993 land history does not locate that ride.',
 (938,1199):'Second animated-feature chronology and competitive song/score Oscars are different production facts.',
 (935,1241):'Carthay Circle premiere venue and With a Smile and a Song placement require different knowledge.',
 (948,996):'Barrie source-play attribution and Second Star to the Right song placement are different facts.',
 (317,947):'Alice attraction caterpillar vehicles and Lewis Carroll authorship of the 1951 film source are different facts.',
 (935,991):'Carthay Circle premiere venue and Whistle While You Work placement require different knowledge.',
 (938,993):'Second-feature chronology and Give a Little Whistle placement require different knowledge.',
 (922,1621):'Everest land location and the continent of a cruise deployment are unrelated uses of Asia.',
 (927,928):'Father and mother are separate named parents; knowing one first name does not establish the other.',
 (951,999):'Feature-wide xerography introduction and Cruella de Vil song placement are independent production/music facts.',
 (948,2242):'J. M. Barrie adaptation and Tokyo DisneySea area inspiration are different facts.',
 (940,2262):'Economical rapid production and a labor-strike production context are different historical relationships; knowing the budget story does not establish the strike.',
}
singles={
 ('answer-style',935):'All answers are actual film titles. Snow White and the Seven Dwarfs is naturally longer; it adds no explanation or unique grammatical form that reveals the premiere venue.',
 ('leak',905):'Ride is generic attraction vocabulary, not the character identity. All four choices are Disneyland dark rides; the amphibian motorcar story still has to be known.',
 ('leak',909):'All four listed attractions involve boat travel. The identifying fact is the tour of miniature animated-film settings, not the generic word boat.',
 ('leak',925):'Liberty Belle and Admiral Joe Fowler are also riverboats, while Columbia follows the same route. Paddle-wheel vessel is the relevant factual distinction, not a word-match giveaway.',
}
report=read('artifacts/question-audit.json')
scope=set(read('audit/runs/next-shard-0017-plan.json')['questionIds'])
decisions=[]
for f in report['openFindings']:
    if not scope.intersection(f['questionIds']): continue
    reason=reasons.get(tuple(f['questionIds'])) if f['kind']=='duplicate' else singles.get((f['kind'],f['questionIds'][0]))
    if not reason: raise RuntimeError('Unreviewed finding '+f['id'])
    run('decide',f['id'],'accepted','--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0017-reviews.json')
    decisions.append({'id':f['id'],'status':'accepted','reason':reason})
(ROOT/'audit/runs/next-shard-0017-finding-decisions.json').write_text(json.dumps(decisions,indent=2)+'\n',encoding='utf-8')
changes={
907:(['clarification'],'Bound the show identification to its historical 2010 debut rather than a changing current version.'),
910:(['clarification'],'Removed tiki word echo while retaining the tropical bird-and-flower chorus.'),
913:(['clarification','distractors'],'Asked for the coaster system name; replaced mixed vehicle names with parallel ride-system alternatives.'),
914:(['clarification'],'Removed gorilla word echo; used the source-backed Pangani Forest identity.'),
916:(['clarification'],'Removed Tomorrowland word echo and specified guest steering of gas-powered miniature cars.'),
917:(['clarification'],'Replaced carousel-with-only-one-carousel giveaway with documented 1917 manufacturer provenance.'),
918:(['factual','clarification','distractors','difficulty'],'Replaced outdated present-tense riverboat claim with documented 1996 renaming; excluded the former-name ambiguity; calibrated hard historical recall.'),
919:(['clarification'],'Scoped vehicle terminology to Magic Kingdom rather than assuming every international version.'),
923:(['factual','clarification'],'Replaced unsupported chalet-entry description with the documented elevated home and salvaged wreckage, removing answer words.'),
925:(['clarification','distractors'],'Specified paddle-wheel vessel to distinguish Columbia on the same route and standardized Sailing Ship Columbia.'),
929:(['clarification','distractors'],'Asked for surname and made all four answers parallel surnames instead of repeated full names.'),
933:(['clarification'],'Removed the series-label elimination clue and specified the theatrical debut.'),
937:(['clarification','distractors'],'Removed Fantasia/Fantasound stem echo; replaced invented Disneyphonic with a real film presentation term and standardized CinemaScope.'),
943:(['clarification'],'Removed the release-year shortcut so identification rests on the two segments.'),
947:(['clarification'],'Specified the 1951 animated adaptation and removed an unnecessary first claim.'),
949:(['clarification'],'Specified animated feature filmed in CinemaScope, avoiding a broad first-Disney-film claim and removing the year shortcut.'),
951:(['factual','clarification'],'Corrected introduced to first feature-wide use because Sleeping Beauty already tested xerography.'),
952:(['clarification'],'Removed the release-year shortcut while preserving released-during-lifetime versus personally-supervised distinction.'),
}
for i,(types,reason) in changes.items():
    args=['classify',str(i)]
    for t in types: args+=['--type',t]
    run(*args,'--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0017-reviews.json')
(ROOT/'audit/runs/next-shard-0017-change-notes.json').write_text(json.dumps({str(i):{'types':v[0],'reason':v[1]} for i,v in changes.items()},indent=2)+'\n',encoding='utf-8')
