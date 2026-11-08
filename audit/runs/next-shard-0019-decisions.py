"""Record explicit editorial classifications and reviewed finding decisions."""
import subprocess

REF = 'audit/runs/next-shard-0019-reviews.json'
changes = {
 1005: (['clarification'], 'Bound the marketplace song to the original film and early escape.'),
 1007: (['clarification'], 'Specify first sung number, excluding overture and spoken narration.'),
 1008: (['clarification'], 'Identify the early wish for a day outside rather than a later romantic solo.'),
 1010: (['clarification'], 'Specify animated version and Matchmaker preparation.'),
 1011: (['clarification'], 'Use accompanies instead of an unbounded chronological follows.'),
 1012: (['clarification'], 'Name the ceremony and song award category; preserve the co-composer credit in evidence.'),
 1013: (['clarification'], 'Specify the original 2002 hula sequence.'),
 1014: (['clarification'], 'Identify the wants-versus-needs advice scene.'),
 1018: (['clarification'], 'The later I Am Moana also invokes ancestry; specify the cavern vision.'),
 1019: (['clarification'], 'Avoid repeating the distinctive song-title surname in the stem.'),
 1021: (['clarification'], 'Use the source-backed insecurity and toy identity without an unnecessary color cue.'),
 1022: (['clarification','distractors'], 'Use parallel occupations and avoid species-versus-occupation overlap.'),
 1023: (['clarification','scope'], 'Explicitly identify a fictional program inside a theatrical film.'),
 1025: (['clarification'], 'Bound the city question to the documented pre-wedding crime-fighting scene.'),
 1027: (['clarification'], 'Ask the hired job title, allowing that cleanup tasks may include dishwashing.'),
 1030: (['clarification'], 'The earlier shredder also threatens destruction; specify burning immediately before the rescue.'),
 1031: (['clarification'], 'Both spies fit the old wording; distinguish the veteran from the rookie.'),
 1032: (['factual','clarification'], 'The games are the suitor competition, not a preliminary competition deciding eligibility.'),
 1038: (['distractors'], 'Use comparably specific dog breeds and challenge other hairless breeds.'),
 1039: (['clarification','distractors'], 'Replace non-family Tony and specify newly developing unpredictable powers.'),
 1047: (['clarification'], 'Use explicit production-note size and color; remove unnecessary wide-eyed detail.'),
 1050: (['clarification','distractors','difficulty'], 'Remove unsupported recipe specificity, ask the supported dish-level fact and reduce difficulty.'),
}
decisions = {
 'duplicate-5d2f43767adb1e9ec28a': 'Rex as dinosaur and Hamm as piggy bank identify different toys and physical forms; knowing either does not establish the other.',
 'duplicate-6c04f05a2350c528cf9e': 'Naming the baby (#1276) does not establish his emerging unpredictable powers in the sequel (#1039); Violet also has multiple established powers, so the development distinction matters.',
 'duplicate-a1dab8c9e9b1e8a39daa': 'The fictional show title in Toy Story 2 and the real Shanghai attraction using that theme are different film and park mappings; the attraction fact requires independent location knowledge.',
 'duplicate-c8d4b7268a4029d70c8e': 'Mama Odie singing in the film and guests singing at a Disney Wonder restaurant parade are separate performer/event facts despite sharing a song title.',
 'leak-8f26c81dac61173cce07': 'Mother is part of the necessary character name Mother Gothel; it does not give the complete song title or distinguish her song from the other Tangled numbers by itself.',
 'leak-fe2e9228392aee8a1b89': 'Lilo is part of the film title; knowing that name does not supply He Mele No Lilo among these soundtrack options.',
 'scope-81932a7436f5d28a99ba': 'This is an in-universe fictional television program appearing in the theatrical Toy Story 2 plot, not real television-show trivia.',
}
for qid, (types, reason) in changes.items():
    args = ['python','scripts/question_audit.py','classify',str(qid)]
    for kind in types:
        args.extend(['--type',kind])
    args.extend(['--reviewer','Codex','--reason',reason,'--reference',REF])
    subprocess.run(args, check=True, capture_output=True, text=True)
for fid, reason in decisions.items():
    subprocess.run(['python','scripts/question_audit.py','decide',fid,'accepted',
        '--reviewer','Codex','--reason',reason,'--reference',REF],
        check=True, capture_output=True, text=True)
print(f'Classified {len(changes)} retained edits and decided {len(decisions)} findings.')
