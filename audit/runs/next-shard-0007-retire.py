"""Record Codex's batch-7 duplicate comparisons using the supported retire command."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAIRS = {
    307: (1259, "The retained question explicitly identifies Phil performing the Hercules training song and asks its title. This supplies the same trainer identity while testing the additional song fact."),
    324: (2101, "The retained Bambi II relationship question explicitly names Bambi's father as the Great Prince. That directly supplies the paternal title asked here; retain the additional father-son story context."),
    342: (1624, "The retained Riviera Resort question explicitly describes a Skyliner gondola stop at Walt Disney World. Its stem supplies the system's name and transport type, directly answering this simple system identity question."),
    365: (1156, "Inverse Aulani/Hawaiian location identity. The retained question names Disney's Aulani and locates it on Oahu, then asks the Ko Olina location. Memorizing that complete question answers 365 and includes more precise geography."),
    303: (1530, "Same Toy Story 3 strawberry-scented villain identification. The retained question supplies Sunnyside context; knowing either complete question supplies the same Lotso fact."),
    308: (647, "The retained question explicitly names Bing Bong as Riley's imaginary friend and asks his composition. That stem directly answers 308; retain the question that asks an additional design fact."),
    327: (751, "The original group question permits several options: Bambi meets Friend Owl and the Great Prince while young too. Its intended answer merely aggregates the character associations already covered by 751 (Thumper), 218 (Flower), and 1055 (Faline). Retain those more precise individual facts; 751 is the primary replacement pointer, not a claim that it alone covers all three names."),
    330: (2490, "The retained Wizard's Duel question names Madam Mim and Merlin in its stem, directly disclosing the answer here, and asks the additional dragon transformation fact. Original 330 snapshot is preserved, including as the historical replacement snapshot for retired 276."),
    332: (1120, "Inverse Percy/pampered pug identification. The retained question explicitly supplies the species and owner and asks the name; memorizing its complete wording answers 332."),
    335: (1150, "The retained Space Mountain question explicitly supplies Magic Kingdom and Tomorrowland while asking the attraction and its 1975 opening context. Its complete wording directly answers the simpler land association here."),
    341: (609, "Inverse Tower of Terror/Hollywood Studios association. The retained question identifies the drop tower from its park, directly supplying the same park-attraction link."),
    350: (1355, "Inverse Hall of Presidents/Liberty Square association. The retained question names the land and asks the presidential attraction; there is no new fact needed for 350."),
    362: (1368, "The retained question identifies Tokyo Disneyland as the park that opened in 1983 outside the US. The place-name answer directly supplies the intended Tokyo park identity; original 362 additionally misstates the actual location, Urayasu, and ignores Tokyo DisneySea. Retain the historically precise question."),
    363: (2102, "The retained Hong Kong Disneyland opening-year question supplies the entire park name in its stem, directly answering this name-only question. Retain the opening-year fact, avoiding place-name giveaway options."),
}
bank = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in json.loads(f.read_text(encoding='utf-8'))}
out = ROOT/'audit/runs/next-shard-0007-retirements'
out.mkdir(exist_ok=True)
for old, (replacement, reason) in PAIRS.items():
    related = [bank[i] for i in (218, 1055) if old == 327]
    ref = out/f'{old}-{replacement}.json'
    ref.write_text(json.dumps({'reviewer': 'Codex', 'at': '2026-11-06', 'retired': bank[old], 'retained': bank[replacement], 'additionalComparisons': related, 'rationale': reason, 'scope': 'Only the planned question is retired. Comparing a replacement does not approve its factual review.'}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    r = subprocess.run([sys.executable, 'scripts/question_audit.py', 'retire', str(old), '--replaced-by', str(replacement), '--reviewer', 'Codex', '--reason', reason, '--reference', str(ref.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    if r.returncode:
        raise SystemExit(r.stdout+r.stderr)
    print(f'Retired {old}; retained {replacement}')
