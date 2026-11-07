"""Hash-bound editorial classifications for the 26 retained batch edits."""
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
changes={
507:('clarification distractors','Removed overlapping human-artifact/coin answers and clarified the collection\'s subject.'),
510:('clarification difficulty','Clarified animated species rather than an animal actor; easy recall.'),
514:('clarification','Removed the composition title from the stem, using the broom scene instead.'),
515:('factual clarification','The gardeners conceal their planting mistake; the Queen did not request the deceptive painting.'),
526:('clarification distractors','Specified Tadashi\'s original design purpose to exclude later combat upgrades; parallel role answers.'),
527:('clarification','Anchored to Raya\'s quest rather than an unqualified last-dragon status at any point in the film.'),
530:('clarification','Specified the dinner outcome without attributing direct potion administration solely to Yzma.'),
534:('clarification difficulty','Asked the fictional inspiration more precisely and calibrated recognition to medium.'),
536:('clarification','Removed potentially misleading shorthand about the death to focus on eldest-brother identity.'),
538:('clarification distractors','Replaced the rare oracular term and joke answers with clearer wording and recognizable pig names.'),
541:('clarification distractors','Focused the healing question on Flynn\'s specific body part at the campfire; parallel body-part options distinguish it from generic healing facts.'),
543:('clarification distractors','Compared material pairs rather than purporting to establish an exhaustive list of abilities.'),
544:('clarification distractors','Asked the ability explaining a form-change rather than requiring an exhaustive limit on all hook powers.'),
556:('clarification difficulty','Specified the earned ending reward, distinct from initial appointment/outfit; medium recall.'),
563:('clarification scope','Anchored Max to the 1995 theatrical film, excluding earlier Junior incarnations and television-only interpretation.'),
567:('clarification','Clarified Maurice\'s ownership and Belle\'s use of the family horse.'),
569:('clarification distractors difficulty','Specified 1989 animation, replaced non-crustacean starfish with crayfish, and calibrated to easy.'),
573:('clarification category','Specified animated film and moved cave/location trivia from characters to movies.'),
576:('clarification','Replaced subjective useless description with the actual canoe-stowaway event and original-film year.'),
577:('clarification difficulty','Specified original 2016 film and calibrated prominent species recall to easy.'),
579:('clarification distractors','Queried a precise component of the full name with comparable single-word answers, removing the longest-answer giveaway.'),
580:('clarification distractors difficulty','Specified 1994 film and used competing mixed trios with equivalent form; medium recall.'),
583:('clarification difficulty','Specified 1999 film and calibrated prominent villain identification to medium.'),
588:('clarification distractors','Specified first Meg encounter rather than global first-monster chronology; used four centaur names.'),
589:('clarification difficulty','Specified original film and calibrated named-pet recall to medium.'),
597:('factual clarification','Current Soarin\' film availability has changed; anchored the global experience to its June 2016 debut.')
}
for qid,(types,reason) in changes.items():
    args=[sys.executable,'scripts/question_audit.py','classify',str(qid)]
    for kind in types.split(): args+=['--type',kind]
    args+=['--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0011-evidence-notes.json']
    subprocess.run(args,cwd=ROOT,check=True,capture_output=True,text=True)
print(f'Classified {len(changes)} final-hash edits.')
