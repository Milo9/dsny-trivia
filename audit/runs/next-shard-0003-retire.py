"""Apply explicitly reviewed batch-3 duplicate decisions via the supported CLI."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAIRS = {
    116: (668, 'The full-name question repeats the middle-name recall tested by 668 with three Walter alternatives; retain the focused Elias question rather than testing the same name component twice.'),
    107: (377, 'Both establish TRON Lightcycle / Run as the Magic Kingdom coaster opening in 2023; the retained version directly tests the opening year rather than including it as a name clue.'),
    102: (1141, 'The full April 22, 1998 opening date already supplies the year; retain the more precise opening-date question.'),
    103: (1359, 'Both test Pandora being the Avatar land at Animal Kingdom, in opposite directions; retain the fuller land question.'),
    108: (366, 'Same Hollywood Studios Star Wars land-name fact and same distractors; retain the version using the full Star Wars: Galaxy\'s Edge name.'),
    115: (773, 'Both test the Splash Mountain to Tiana\'s Bayou Adventure replacement, in reverse; retain the dated Magic Kingdom version.'),
    117: (926, 'The full December 5, 1901 birth date contains this birth-year answer; retain the more precise date question.'),
    124: (2271, 'Both test the Walt Disney Productions to The Walt Disney Company rename, in reverse; retain the version anchored to 1986.'),
    125: (1487, 'Both test Walt\'s World War I ambulance service; the retained question specifies his age constraint, the Red Cross, and France.'),
    133: (408, 'Both test Oswald and Universal ownership in the same loss-of-control event, in reverse; retain the question explicitly stating original ownership.'),
    143: (430, 'Both test the Disney Magic Palo adults-only Italian dining association, in reverse; retain the version additionally specifying brunch and dinner.'),
    144: (743, 'Both test the Disney Dream and 2011 service-debut association, in reverse; retain the version with fleet-history context.'),
    150: (420, 'The central defining fact is servers accompanying guests through the dining rotation; retain the focused servers question rather than the overbroad different-restaurant-every-night formulation.'),
    153: (698, 'The opening-song question already establishes Circle of Life belongs to The Lion King; retain that more specific musical-context question.'),
    152: (704, 'Both test Ariel singing Part of Your World, in reverse; retain the question locating her solo in her collection grotto.'),
}

def run(*args):
    result = subprocess.run([sys.executable, 'scripts/question_audit.py', *map(str, args)], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if result.returncode:
        print(result.stdout, result.stderr)
        raise SystemExit(result.returncode)
    return result.stdout

if __name__ == '__main__':
    bank = {q['id']: q for f in (ROOT / 'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
    retired = {q['id'] for q in json.loads((ROOT / 'questions/retired.json').read_text(encoding='utf-8'))}
    out = ROOT / 'audit/runs/next-shard-0003-retirements'
    out.mkdir(exist_ok=True)
    for old, (replacement, rationale) in PAIRS.items():
        if old in retired:
            continue
        reference = out / f'{old}-{replacement}.json'
        reference.write_text(json.dumps({'reviewer': 'Codex', 'at': '2026-11-06', 'retired': bank[old], 'retained': bank[replacement], 'rationale': rationale, 'scope': 'Only the planned question is retired; the replacement is context and is not newly approved.'}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        run('retire', old, '--replaced-by', replacement, '--reviewer', 'Codex', '--reason', rationale, '--reference', reference.relative_to(ROOT))
        print(f'Retired {old}; retained {replacement}')
