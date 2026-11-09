"""Hash-bound change classifications for the final retained batch 31 wording."""
import json
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[2]
rows = {
2068: ('clarification,distractors', 'Ask the explicitly stated rule list; use the stated refusal rather than an unsupported absolute inability.'),
2069: ('clarification', 'Specify the 1951 adaptation and shorten the transformation prompt.'),
2074: ('clarification', 'Remove the correct song title from the stem while retaining the beach-fantasy scene.'),
2075: ('clarification,difficulty', 'Remove duration and title-paraphrase clues; identify the Sven-voice scene and set medium difficulty.'),
2076: ('factual,clarification', 'Replace each sneeze with repeatedly because the final alphorn sneeze makes a giant snowball.'),
2080: ('clarification,difficulty', 'Remove unnecessary award/nationality claims and parenthetical title repetition; basic object recognition is easy.'),
2082: ('clarification,distractors', 'State documented low riding from passenger loading rather than imply literal sinking; parallel causal answers.'),
2083: ('clarification,distractors', 'Remove the unestablished evacuation count; keep the documented Fantasyland gas-leak closure.'),
2084: ('clarification,distractors', 'Focus on the original storyline contribution; give all four names without unequal occupational labels.'),
2085: ('clarification,distractors', 'Combine Bell System and AT&T, which are overlapping opening-sponsor identities, and replace that competing distractor.'),
2089: ('clarification', 'Remove redundant year and resort description from the date prompt.'),
2090: ('clarification,distractors', 'Date the current lounge claim, remove rose from the stem, and use real Wish lounges as alternatives.'),
2091: ('clarification', 'Bound the show description to Disney\'s documented 2025 version rather than an unbounded nightly schedule.'),
2093: ('factual,clarification,distractors,difficulty', 'Correct Ranjan from Shanti\'s brother to Mowgli\'s adoptive brother; renew options and set medium difficulty.'),
2095: ('clarification', 'Describe hollow-tree voice amplification rather than suggest a physical monster disguise.'),
2096: ('clarification,distractors', 'Narrow the broad weakness claim to the sourced running-speed difficulty; use parallel physical limitations.'),
2101: ('clarification,distractors', 'Shorten the father-son premise and make all alternatives relationships.'),
2102: ('clarification', 'Remove unnecessary regional first-park claim from the opening-year question.'),
2103: ('clarification,distractors', 'Ask final nominal production cost; remove disputed initial-budget precision and use comparable numeric forms.'),
2104: ('clarification,distractors', 'Ask the specific final-lap pass and remove unsupported footage provenance; use comparable actions.'),
2105: ('clarification,distractors', 'Ask the explicit college-arrival relationship; remove unneeded study-partner and rivalry generalizations.'),
2106: ('clarification', 'Remove unestablished top-student ranking and ask the named fraternity presidency.'),
2107: ('clarification', 'Remove singing stray dogs, which paraphrased the band name in the stem.'),
2108: ('clarification,distractors', 'Ask the scout\'s venue affiliation using four venues, rather than mixing events and a person\'s visit.'),
2109: ('clarification,distractors,difficulty', 'Change why to what false claim to match the answers; remove stray title leak and set medium difficulty.'),
2110: ('clarification,distractors,difficulty', 'Replace speculative laughing-gas language with the observable laughter trigger; parallel trigger options and easy difficulty.'),
2111: ('factual,clarification,distractors', 'Remove the false claim that Mary rises by laughing; ask the actual tea guests in parallel complete groups.'),
2114: ('clarification,distractors', 'Avoid the title giveaway and unsupported instant-anywhere wording; ask Paul\'s enchanted object using short parallel objects.'),
2115: ('clarification,difficulty', 'Specify the 1954 film and simplify the commander prompt; basic character recall is easy.'),
2116: ('clarification,distractors', 'Specify Vulcania\'s bomb and replace the potentially overlapping defensive-trap answer with distinct motives.'),
2117: ('clarification,distractors', 'Ask the immediate grounding event rather than competing storm/pirate chain-of-causation explanations.'),
}
reference = 'audit/runs/next-shard-0031-reviews.json'
for qid, (types, reason) in rows.items():
    ledger = json.loads((root/'audit/ledger.json').read_text(encoding='utf-8'))
    existing = ledger['changeClassifications'].get(str(qid), {})
    if existing.get('reference') == reference and set(existing.get('types', [])) == set(types.split(',')):
        continue
    cmd = [sys.executable,'scripts/question_audit.py','classify',str(qid),'--reviewer','Codex','--reason',reason,'--reference',reference]
    for kind in types.split(','):
        cmd.extend(['--type',kind])
    for attempt in range(4):
        result = subprocess.run(cmd,cwd=root,capture_output=True,text=True)
        if result.returncode == 0 or '[WinError 5]' not in result.stdout + result.stderr:
            break
        time.sleep(0.5)
    if result.returncode:
        raise RuntimeError(result.stdout+result.stderr)
print(f'Classified {len(rows)} retained edits with individual evidence references.')
