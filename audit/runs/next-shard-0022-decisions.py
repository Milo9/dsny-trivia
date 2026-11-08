"""Apply explicit batch-22 findings and hash-bound change classifications."""
import json
import subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def run(*args): subprocess.run(['python','scripts/question_audit.py',*map(str,args)],cwd=R,check=True)
ref='audit/runs/next-shard-0022-reviews.json'
decisions={
 'answer-style-4c1f173c8e824e0a1a07': 'The answer is the attraction’s complete licensed title, parallel to three other attraction titles. Its extra words are naming, not an explanation or added hint. California replacement evidence explicitly names this predecessor.',
 'duplicate-36df460f4a0845a0c6ff': 'Mexico pyramid architecture and the location of Gran Fiesta Tour are separate facts. Neither question supplies the other attraction/building relationship.',
 'duplicate-38176784e1e075650555': 'Garden Grill restaurant location is separate from Soarin and greenhouse-boat location. A shared pavilion does not supply the independently named restaurant location.',
 'duplicate-8d9354f8a1cf1de4930e': 'The 1966 Florida Project film development and the later theme park containing World Showcase are different history facts; EPCOT is shared but the film association is new knowledge.',
 'duplicate-b9eb644709b09dca8996': 'The animated 1950 return to single-story features and the live-action 2015 Frozen Fever pairing concern different Cinderella films and different release facts.',
 'duplicate-c68d4b8e9c8386195434': 'The Academy’s 1932 creation citation and the Mintz contract dispute are separate Mickey history facts. Knowing the dispute’s result does not identify the honorary award citation.',
 'duplicate-d92e03cbf0ec3ae9fea0': 'Carolwood Pacific is the railroad, while Lilly Belle is its engine. Memorizing the railway name does not supply the locomotive name; final wording explicitly distinguishes the component from the system.',
 'duplicate-f68c00ad3029aab606ef': 'These are separate original English voice credits for different princesses and different films. Caselotti and Woods cannot be swapped; knowing one film’s credit cannot identify the other.',
}
for fid,reason in decisions.items():
    run('decide',fid,'accepted','--reviewer','Codex','--reason',reason,'--reference',ref)
for fid,reason in {
 'leak-729c75d43636fe45bfee':'Final stem uses carries by rail instead of repeating train, and the destination is the currently documented Conservation Station. All four options were rechecked against the official route description.',
 'leak-60d89987eb15d2af6b50':'Final stem says central landmark and supplies the historical 2007 opening. Four parallel accommodation names were reviewed against the castle-suite opening and name records.',
 'leak-be2f1711f6a08f0ab976':'Final stem no longer contains Liberty. All four answers remain parallel bell names; the source explicitly identifies the Liberty Bell replica.',
}.items():
    run('decide',fid,'fixed','--reviewer','Codex','--reason',reason,'--reference',ref)

classifications={
 1156:(['clarification','distractors'],'Dated the property location and replaced off-island distractors with Oahu areas.'),
 1157:(['clarification'],'Dated the reviewed mountain identity.'),
 1158:(['clarification'],'Dated the reviewed Tomorrowland ride configuration.'),
 1159:(['clarification','distractors'],'Asked the 2018 retheme name so the prior name of the same physical coaster cannot also fit; used parallel candidate names.'),
 1164:(['clarification'],'Dated the route and specified TTC-to-Magic Kingdom ferryboats, distinguishing Bay Lake resort launches.'),
 1165:(['clarification'],'Dated the reviewed TTC-to-EPCOT route.'),
 1166:(['factual','clarification'],'Updated the current destination naming to Conservation Station and removed repeated train wording.'),
 1167:(['clarification'],'Dated the reviewed land identity.'),
 1170:(['clarification','distractors'],'Specified the 2007 accommodation opening and balanced the four accommodation names while removing castle from the stem.'),
 1171:(['clarification'],'Dated the configuration and specified the main building rather than implying the entire pavilion is enclosed.'),
 1172:(['factual','clarification'],'Removed the erroneous grouping of Splash Mountain as a coaster and replaced an unattributed description with a verifiable opening-date comparison.'),
 1173:(['clarification'],'Bound the building association to the 2020 Florida opening, excluding the later California theater.'),
 1174:(['clarification'],'Dated the replica question and removed Liberty from its stem.'),
 1175:(['clarification'],'Dated the reviewed restaurant location.'),
 1178:(['clarification'],'Specified the 1923 Alice pilot rather than potentially implying one performer throughout the series.'),
 1182:(['clarification','distractors'],'Specified the theatrical color milestone and used four competing color processes instead of mixing color, widescreen and depth attributes.'),
 1183:(['clarification'],'Specified the original English Donald performance.'),
 1184:(['clarification'],'Specified initial newspaper-strip naming rather than imprecise earliest appearances.'),
 1185:(['clarification'],'Distinguished the bloodhound prototype debut from the later named Pluto.'),
 1187:(['clarification'],'Specified Walt’s backyard locomotive, distinguishing resort railroad engines.'),
 1191:(['clarification'],'Replaced unbounded today wording with the documented 1986 rename.'),
 1192:(['clarification'],'Narrowed general Haunted Mansion contribution fame to the documented bust-illusion discovery with Crump.'),
 1193:(['clarification','difficulty'],'Specified the 1966 film without an absolute final-appearance claim; calibrated to medium recognition.'),
 1194:(['clarification'],'Restricted closest-city comparison to the listed cities, avoiding smaller unlisted municipalities.'),
 1200:(['clarification'],'Specified original English Pinocchio and release year for the Jiminy credit.'),
 1201:(['clarification'],'Specified original English Snow White voice credit.'),
 1202:(['clarification'],'Specified original English Cinderella voice credit.'),
 1204:(['difficulty'],'Set easy because the early-1940s date strongly distinguishes the conflicts.'),
}
plan=json.loads((R/'audit/runs/next-shard-0022-plan.json').read_text())
reviews=json.loads((R/ref).read_text())
changed={r['questionId'] for r in reviews if r['hash'] != plan['startingHashes'][str(r['questionId'])]}
assert changed==set(classifications),(changed ^ set(classifications))
for i,(types,reason) in classifications.items():
    args=['classify',i]
    for t in types: args.extend(['--type',t])
    run(*args,'--reviewer','Codex','--reason',reason,'--reference',ref)
