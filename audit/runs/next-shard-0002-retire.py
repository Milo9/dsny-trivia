"""Save authored duplicate decisions and invoke the supported retirement command."""
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
packet = json.loads((root / 'audit/runs/next-shard-0002-reviews/starting-packet.json').read_text(encoding='utf-8'))
bank = {}
for path in (root / 'questions').glob('q-*.json'):
    bank.update({q['id']: q for q in json.loads(path.read_text(encoding='utf-8'))})
decisions = {
    60: (569, 'Both test Sebastian being the crab in The Little Mermaid, reversing name and animal. Retain the explicit crustacean question; original q60 snapshot preserves the name question.', 'https://d23.com/a-to-z/little-mermaid-the-film/', 'Opening synopsis: Sebastian the crab is sent by King Triton to watch Ariel.'),
    61: (684, 'Both ask for the original Mickey Mouse voice performer, Walt Disney. The nearly-20-years context does not add a different requested answer. Preserve q61 and retain the existing same-fact question without approving its other options.', 'https://d23.com/a-to-z/mickey-mouse/', 'Voice-history paragraph beginning Walt Disney provided Mickey Mouse’s voice.'),
    79: (546, 'Inverse Meeko/raccoon relationship. Knowing that Meeko is Pocahontas’s raccoon solves both; retain the character-name question.', 'https://d23.com/a-to-z/pocahontas-film/', 'Opening synopsis identifies Meeko as a raccoon and Flit as a hummingbird.'),
    80: (1345, 'Inverse Iago/parrot relationship. Retain the more specific character-name question. Original q80 also has a nested animal option: a macaw is a kind of parrot; it must not be approved as single-answer.', 'https://d23.com/a-to-z/aladdin-film/', 'Cast identifies Iago; compare full q1345 which identifies the parrot. Retirement is a content-overlap decision, not verification of all q1345 options.'),
    82: (328, 'Both request the identity of The Aristocats butler Edgar; the retained surname question requests the more specific name. q82’s inheritance premise also needs the cats-first condition. Retiring avoids retaining the less precise question.', 'https://d23.com/a-to-z/aristocats-the-film/', 'Opening synopsis identifies Edgar and the inheritance left to Madame Bonfamille’s cats; this source does not establish the surname in q328.'),
    87: (602, 'The retained Anaheim, California location answer includes the entire California fact requested here and adds the city. Preserve the broader state-only question as retired.', 'https://d23.com/a-to-z/disneyland/', 'Opening sentence locates Disneyland in Anaheim, California.'),
    89: (687, 'The retained exact opening-date answer October 1, 1971 includes the entire year fact requested here. Preserve the less specific year question as retired.', 'https://d23.com/a-to-z/walt-disney-world-resort/', 'Opening sentence: resort opened near Orlando, Florida on October 1, 1971.'),
    93: (600, 'Inverse Haunted Mansion/999 happy haunts recall. The explicit haunt-count question retains the same fact. q93 is preserved intact, including its attraction-name answer.', 'https://disneyworld.disney.go.com/attractions/magic-kingdom/haunted-mansion/', 'Haunted Mansion attraction identity and Ghost Host description; q600 asks the count embedded in q93. No claim that the current webpage itself states 999.'),
    96: (683, 'The exact opening-date answer in q683 contains the entire 1955 year fact requested here. Preserve the broader year-only question. q683’s wording incorrectly says public opening for the invitation day; record that separate context concern, do not silently approve the replacement.', 'https://d23.com/a-to-z/disneyland/', 'Opening sentence explicitly distinguishes invitation opening July 17, 1955 and public opening the next day.'),
    99: (618, 'The pair supply the 1989 opening event and Disney-MGM Studios name in reverse. Retain q618; the requested old name is already given there. Neither needs both directions of the same opening-event identification.', 'https://d23.com/a-to-z/disney-mgm-studios/', 'Opening sentence gives May 1, 1989 and original Disney-MGM Studios Theme Park name; final paragraph gives 2008 renaming.'),
}
out = root / 'audit/runs/next-shard-0002-retirements'
out.mkdir(exist_ok=True)
for old, (new, reason, url, locator) in decisions.items():
    reference = out / f'{old}-{new}.json'
    reference.write_text(json.dumps({'reviewer': 'Codex (OpenAI)', 'questions': [bank[old], bank[new]], 'decision': reason, 'evidence': [{'url': url, 'locator': locator}], 'replacementApproved': False}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    result = subprocess.run(['python', 'scripts/question_audit.py', 'retire', str(old), '--replaced-by', str(new), '--reviewer', 'Codex (OpenAI)', '--reason', reason, '--reference', str(reference.relative_to(root))], cwd=root, capture_output=True, text=True, encoding='utf-8')
    print(f'{old} -> {new}: {result.returncode}')
    if result.returncode:
        print(result.stdout, result.stderr)
        raise SystemExit(result.returncode)
