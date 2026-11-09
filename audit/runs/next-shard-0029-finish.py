"""Record explicit editorial decisions after the batch-29 final evidence review."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'scripts/question_audit.py'

def run(*args):
    subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=ROOT, check=True)

run('record-many', 'audit/runs/next-shard-0029-reviews.json')

classifications = {
    1596: ('factual clarification distractors', 'Removed a second defensible bully answer; specified the film version.'),
    1597: ('factual', 'Corrected the character surname to Disney’s Caloway spelling.'),
    1600: ('clarification', 'Kept the Ahtohallan scene and removed the literal mother-spirit interpretation.'),
    1601: ('clarification difficulty', 'Shortened the power-ballad context and calibrated medium recall difficulty.'),
    1602: ('factual clarification', 'Corrected chronology: Anna sings after Olaf disappears, not before.'),
    1605: ('clarification', 'Asked the supported soundtrack recording without asserting montage/end-credit placement.'),
    1610: ('clarification distractors', 'Dated the star count to the two 1960 dedications and made options parallel.'),
    1611: ('scope clarification distractors', 'Replaced a real television-show title fact with Walt’s dated business/network transition.'),
    1614: ('clarification', 'Asked the official overall theme at the historical debut.'),
    1615: ('clarification', 'Specified fictional nation and debut; removed the Black Panther giveaway.'),
    1616: ('clarification', 'Dated the restaurant offering and removed the exact Lion King title echo.'),
    1617: ('clarification difficulty', 'Used the official show title and dated exclusivity; removed Greek-mythology hint.'),
    1618: ('clarification distractors', 'Asked the shared design fuel without a broad emissions comparison; parallel fuel options.'),
    1619: ('clarification', 'Dated the suite design and removed the unneeded top-tier ranking.'),
    1621: ('clarification', 'Historical first-homeport claim; removed Singapore-to-continent giveaway.'),
    1622: ('clarification', 'Specified inaugural Singapore round trips rather than an unbounded future itinerary.'),
    1623: ('clarification', 'Concise historical debut wording.'),
    1624: ('clarification', 'Precise opening month and design inspiration; removed ongoing gondola detail.'),
    2002: ('factual clarification', 'Corrected Chuckles’s story location to Bonnie’s house; removed clown clue.'),
    2003: ('clarification', 'Removed the unsupported pocket-riding detail.'),
    2004: ('clarification', 'Removed unneeded county-fair specificity.'),
    2005: ('clarification distractors', 'Asked a specific commercial-performance limitation and excluded simultaneous-trait ambiguities.'),
    2006: ('clarification distractors', 'Asked the studio-named dummy leader instead of an uncertain collective name and night restriction.'),
    2011: ('clarification', 'Focused the romance attribution and removed an unnecessary claim about the first film.'),
    2013: ('clarification', 'Asked the distinct sequel lava action instead of repeating the original sidekick identity.'),
    2015: ('distractors', 'All options now share Thieves, removing the film-title giveaway.'),
}
for qid, (types, reason) in classifications.items():
    args = ['classify', qid]
    for kind in types.split():
        args += ['--type', kind]
    run(*args, '--reviewer', 'Codex', '--reason', reason,
        '--reference', 'audit/runs/next-shard-0029-reviews.json')

decisions = {
    'duplicate-66496ebf9369d4154a49': '1607 tests Eisner’s CEO tenure; 2269 tests the target of Roy E. Disney’s 2003 campaign. Shared person, different historical relationships; knowing a CEO tenure does not establish who the campaign sought to oust.',
    'duplicate-9784a0f0f4cde2cef174': '1609 asks the Lucasfilm acquisition year; 2254 asks Grizzly Gulch opening year. Sharing 2012 does not establish either unrelated event from the other.',
    'duplicate-b3d31c4c12fa1238f93d': '1609 asks the Lucasfilm acquisition year; 2240 asks Cars Land opening year. Sharing 2012 does not establish either unrelated event from the other.',
}
compact = json.loads((ROOT / 'artifacts/question-audit/current-compact.json').read_text(encoding='utf-8'))
comparisons = []
for finding in compact['openFindings']:
    if finding['id'] in decisions:
        comparisons.append({'findingId': finding['id'], 'questions': [compact['catalog'][str(i)] for i in finding['questionIds']],
                            'decision': 'accepted', 'reviewer': 'Codex', 'at': '2026-11-08', 'reason': decisions[finding['id']]})
reference = 'audit/runs/next-shard-0029-resume-comparisons.json'
(ROOT / reference).write_text(json.dumps(comparisons, indent=2) + '\n', encoding='utf-8')
for finding, reason in decisions.items():
    run('decide', finding, 'accepted', '--reviewer', 'Codex', '--reason', reason, '--reference', reference)
run('decide', 'manual-eb23fdafcc14c37947f9', 'fixed', '--reviewer', 'Codex',
    '--reason', 'Final wording places Anna’s cave song after Olaf disappears. Rechecked the farewell-to-song sequence at transcript lines 1202-1250 and the separate song synopsis; renewed all four options and final challenge.',
    '--reference', 'audit/runs/next-shard-0029-reviews.json')
run('sync')
run('report', '--out', 'artifacts/question-audit.json', '--brief', '--since', 'artifacts/question-audit.json')
run('check')
run('close', 'audit/runs/next-shard-0029-plan.json', '--reviewer', 'Codex', '--out', 'audit/runs/next-shard-0029-result.json')
