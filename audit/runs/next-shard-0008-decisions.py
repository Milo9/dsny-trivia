"""Codex's reviewed finding decisions and hash-bound change classifications."""
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def run(*args):
    r=subprocess.run([sys.executable,'scripts/question_audit.py',*args],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if r.returncode: raise SystemExit(r.stdout+r.stderr)

decisions={
 'duplicate-2a869c9772865c94ae5b':'Different clubs and full age ranges: Edge 11-14 versus Vibe 14-17. Either name/age association alone does not identify the other club; a shared endpoint at 14 does not merge the two facts.',
 'duplicate-3df1a45c7c73f1dd1ef0':'Treasure Island as the first wholly live-action Disney feature is a production milestone; Treasure Island as the novel adapted by Treasure Planet is a separate literary-source fact.',
 'duplicate-4c65f80adf986a43f8dc':'The same ship houses two differently themed restaurants. Knowing the Frozen venue Arendelle does not supply the Marvel venue Worlds of Marvel, or vice versa.',
 'duplicate-4cb3c9dafacdb6db4df7':'Six fleet ships at a December 2024 cutoff versus six selectable coaster songs: unrelated counted sets.',
 'duplicate-87b9179109bdab9c6803':'Flowers and Trees holds both a color-process first and an Oscar milestone. Final 396 removes the award clue and asks only Technicolor; the first Oscar alone does not establish a first color process.',
 'duplicate-a8cad0b27fe5a917beee':'Three Genie wishes versus three Wish rotational restaurants: unrelated film rule and ship dining count.',
 'duplicate-db49873a3d3c7ebb813d':'Disneyland the park Walt saw open is distinct from Disneyland the anthology-program title. This comparison does not approve 1374\'s TV scope or color claim.',
 'duplicate-e6ace83fa571a1820194':'Six ships versus six passenger seats in a Cars ride vehicle: unrelated counted sets.',
 'duplicate-ecd6d7e4cc8962b00bc9':'A 1950 feature-film milestone and the former name of a Florida wildlife island are different entities sharing Treasure Island.',
 'duplicate-f912e912e3049c9e47af':'Three Wish dining venues versus three Lion King song nominations: independent counts in unrelated subjects.',
}
for fid,reason in decisions.items():
    run('decide',fid,'accepted','--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0008-comparisons.json')

edits={
 367:(['clarification'],'Specified the Florida Tower version to avoid the Tokyo storyline.'),
 368:(['factual','clarification','distractors'],'Corrected lobby to the tower atrium/concourse; used complete parallel hotel names.'),
 369:(['clarification','difficulty'],'Specified family household technology and set recognizable attraction recall to medium.'),
 371:(['factual','clarification'],'Removed the false implication that the 1999 show was EPCOT\'s original lagoon spectacular.'),
 374:(['clarification','distractors'],'Asked the coined name and replaced generic tunnel descriptions that could also fit.'),
 376:(['clarification','distractors'],'Made the monorail record explicit and used four competing monorail systems to avoid a type-word giveaway.'),
 381:(['distractors'],'Replaced the Florida resort name with its actual Magic Kingdom theme park for parallel options.'),
 383:(['clarification'],'Narrowed broad design help to the sourced first-sketch attribution.'),
 387:(['clarification','distractors'],'Asked the public affectionate nickname; removed Mr. Disney, a genuinely used form of address.'),
 392:(['distractors'],'Made the four proposed concepts comparable in form and length.'),
 396:(['clarification','distractors'],'Specified three-strip Technicolor; removed the separate Oscar clue and parenthetical years.'),
 397:(['clarification','distractors'],'Asked city and removed the longer key-only Presidio parenthetical.'),
 405:(['clarification','distractors'],'Distinguished tracing as a movement aid from general reference and replaced the overlapping live-reference option.'),
 408:(['clarification'],'Bound ownership to 1928 and distinguished rights holder from distributor and later Disney ownership.'),
 412:(['clarification'],'Explicitly included Treasure at its December 2024 maiden-voyage cutoff in response to the player report.'),
 413:(['clarification'],'Specified the Wish nursery rather than an unbounded fleet generalization.'),
 414:(['clarification'],'Specified the Dream and removed salon from the stem after its giveaway warning.'),
 415:(['clarification'],'Specified Wish main rotational dinner restaurants rather than all venues or every ship.'),
 420:(['clarification','distractors'],'Asked the designed team-assignment policy with four parallel team arrangements.'),
 424:(['clarification'],'Specified Wish and the full advertised 11-14 age range to handle overlap at 14.'),
 425:(['clarification'],'Specified Wish and the full advertised 14-17 age range to handle overlap at 14.'),
}
for qid,(types,reason) in edits.items():
    args=['classify',str(qid)]
    for kind in types:args+=['--type',kind]
    run(*args,'--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0008-reviews.json')
print(f'Recorded {len(decisions)} individual comparison decisions and {len(edits)} edit classifications.')
