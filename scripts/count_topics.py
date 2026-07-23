"""
Counts how many questions are about each Disney/Pixar film.
Counts against question text + correct answer (index 0) only — not distractors.
Run from the project root: python scripts/count_topics.py

Parent-film counts below EXCLUDE matches that belong to a tracked sequel/short
(see scripts/_common.py:SEQUELS_AND_SHORTS) so a "Saturated" label reflects the
base film, not the whole franchise. Sequels/shorts are reported separately.
"""
import json, re, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _common import SEQUELS_AND_SHORTS

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

film_keywords = {
    'Beauty and the Beast': r'beauty.*beast|lumiere\b|cogsworth\b|mrs.*potts\b|gaston\b.*belle|belle\b.*gaston',
    'The Little Mermaid': r'little mermaid|ariel\b|ursula\b|prince eric\b|sebastian\b.*crab|flounder\b|king triton\b|scuttle\b',
    'Frozen': r'\bfrozen\b|elsa\b|arendelle\b|kristoff\b|olaf\b|hans\b.*arendelle|sven\b.*reindeer|let it go\b',
    'The Lion King': r'lion king|simba\b|mufasa\b|scar\b.*lion|timon\b|pumbaa\b|rafiki\b|pride rock\b',
    'Moana': r'\bmoana\b|maui\b.*demigod|te fiti\b|te ka\b|tamatoa\b|heihei\b|motunui\b|gramma tala\b',
    'Finding Nemo/Dory': r'finding nemo\b|finding dory\b|marlin\b.*clown|nemo\b.*dentist|darla\b.*dentist|marine life institute\b|destiny\b.*whale shark|hank\b.*octopus',
    'Toy Story': r'toy story|woody\b.*sheriff|buzz lightyear|stinky pete\b|lotso\b|jessie\b.*cowgirl|bullseye\b.*horse|gabby gabby\b|forky\b',
    'Aladdin': r'\baladdin\b|genie\b.*lamp|jafar\b|jasmine\b.*agrabah|iago\b.*parrot|abu\b.*monkey|agrabah\b|cave of wonders\b',
    'Pocahontas': r'\bpocahontas\b|governor ratcliffe\b|meeko\b.*raccoon|grandmother willow\b|nakoma\b|john smith\b.*jamestown',
    'Encanto': r'encanto\b|madrigal\b|mirabel\b|luisa\b.*madrigal|isabela\b.*madrigal|dolores\b.*madrigal|camilo\b.*madrigal|casita\b',
    'Mulan': r'\bmulan\b|mushu\b.*dragon|shan yu\b|cri.kee\b|li shang\b|fa zhou\b',
    'Tangled': r'\btangled\b|rapunzel\b|flynn rider\b|mother gothel\b|snuggly duckling\b|pascal\b.*chameleon',
    'The Hunchback of Notre Dame': r'hunchback|quasimodo\b|esmeralda\b|frollo\b|phoebus\b|clopin\b|djali\b',
    'Tarzan': r'\btarzan\b|kerchak\b|kala\b.*gorilla|terk\b.*gorilla|jane.*porter\b|clayton\b.*hunter\b',
    'Inside Out': r'inside out\b|bing bong\b|core memories\b|hockey island\b',
    'The Incredibles': r'incredibles\b|mr.*incredible\b|elastigirl\b|edna mode\b|frozone\b|syndrome\b.*omnidroid|jack.jack\b',
    'Ratatouille': r'ratatouille\b|remy\b.*rat|linguini\b|gusteau\b|anton ego\b',
    'Monsters Inc/University': r'monsters.*inc\b|monsters university\b|sulley\b|mike wazowski\b|boo\b.*monster\b|randall\b.*monster|dean hardscrabble\b|oozma kappa\b',
    'Brave': r'\bmerida\b|king fergus\b|queen elinor\b|will o.*wisp\b|mor.du\b|dingwall\b.*clan',
    'WALL-E': r'wall.e\b|buy n large\b|m.o\b.*cleaning|axiom\b.*ship',
    'Cars': r'lightning mcqueen\b|mater\b.*tow truck|radiator springs\b|chick hicks\b|doc hudson\b|piston cup\b',
    'Zootopia': r'zootopia\b|judy hopps\b|nick wilde\b|bellwether\b|night howlers\b',
    "Emperor's New Groove": r'emperor.*groove\b|kuzco\b|yzma\b|kronk\b|pacha\b.*llama\b',
    'Big Hero 6': r'big hero 6\b|baymax\b|hiro\b.*baymax\b|tadashi\b.*baymax\b|san fransokyo\b',
    "A Bug's Life": r"bug.*life\b|flik\b.*ant\b|hopper\b.*grasshopper\b|princess atta\b|molt\b.*grasshopper\b|circus bugs\b",
    'Wreck-It Ralph': r'wreck.it ralph\b|vanellope\b|fix.it felix\b|sugar rush\b.*game\b',
    'Atlantis': r'atlantis.*lost empire\b|milo thatch\b|kida\b|commander rourke\b|vinny santorini\b',
    'Hercules': r'\bhercules\b.*disney|hades\b.*underworld|megara\b|philoctetes\b|pain and panic\b',
    'Coco': r'\bcoco\b.*pixar|miguel\b.*guitar\b|hector\b.*rivera\b|ernesto.*de la cruz\b|land of the dead\b.*coco',
    'Soul': r'\bsoul\b.*pixar|joe gardner\b|great before\b',
    'Inside Out 2': r'inside out 2\b|ennui\b.*inside out|envy\b.*inside out|embarrassment\b.*inside out|anxiety\b.*riley',
    'Up': r'carl fredricksen\b|ellie fredricksen\b|russell\b.*wilderness\b|dug\b.*talking dog\b|paradise falls\b',
    'Turning Red': r'turning red\b|meilin lee\b|4.town\b',
    'Elemental': r'\belemental\b|ember\b.*fire element|ember\b.*lumen|element city\b',
    'Onward': r'ian lightfoot\b|barley lightfoot\b|phoenix gem\b|manticore\b.*tavern\b',
    'Luca': r'\bluca\b.*italy|\bluca\b.*sea monster|alberto\b.*sea monster|portorosso\b|ercole\b.*visconti\b',
    'Cinderella': r'\bcinderella\b|fairy godmother\b.*cinderella|prince charming\b.*cinderella|lady tremaine\b|anastasia\b.*tremaine|drizella\b|glass slipper\b',
    'Bambi': r'\bbambi\b|thumper\b.*rabbit|flower\b.*skunk|great prince\b.*forest',
    '101 Dalmatians': r'101 dalmatians|dalmatians\b.*cruella|cruella de vil\b|pongo\b.*dalmatian|perdita\b.*dalmatian',
    'The Jungle Book': r'jungle book\b|mowgli\b|baloo\b|bagheera\b|shere khan\b|kaa\b.*snake',
    'The Fox and the Hound': r'fox and the hound\b|\btod\b.*fox|copper\b.*hound',
    'Brother Bear': r'brother bear\b|\bkenai\b.*bear|\bkoda\b.*bear',
}

all_questions = []
with open(os.path.join(BASE, 'questions', 'manifest.json'), encoding='utf-8') as f:
    manifest = json.load(f)
for shard_path in manifest['shards']:
    with open(os.path.join(BASE, shard_path), encoding='utf-8-sig') as f:
        all_questions.extend(json.load(f))

print(f'Total questions: {len(all_questions)}\n')

children_by_parent = {}
for entry in SEQUELS_AND_SHORTS:
    if entry['parent']:
        children_by_parent.setdefault(entry['parent'], []).append(entry['pattern'])

film_counts = []
for film, pattern in film_keywords.items():
    haystacks = [(q, q['question'] + ' ' + q['answers'][0]) for q in all_questions]
    matched = [q for q, h in haystacks if re.search(pattern, h, re.IGNORECASE)]
    child_patterns = children_by_parent.get(film)
    if child_patterns:
        combined_child = '|'.join(f'(?:{p})' for p in child_patterns)
        matched = [
            q for q in matched
            if not re.search(combined_child, q['question'] + ' ' + q['answers'][0], re.IGNORECASE)
        ]
    film_counts.append((film, len(matched)))

film_counts.sort(key=lambda x: -x[1])
print(f'{"Film (base film, sequels/shorts excluded)":<42} {"Count":>5}  {"Status"}')
print('-' * 65)
for film, count in film_counts:
    status = 'SATURATED (>=20)' if count >= 20 else ('well-covered (10-19)' if count >= 10 else 'under-covered (<10)')
    print(f'{film:<42} {count:>5}  {status}')

print(f'\n{"Sequel / Short":<42} {"Count":>5}  {"Status"}')
print('-' * 65)
seq_counts = []
for entry in SEQUELS_AND_SHORTS:
    count = sum(
        1 for q in all_questions
        if re.search(entry['pattern'], q['question'] + ' ' + q['answers'][0], re.IGNORECASE)
    )
    seq_counts.append((entry['title'], count))
seq_counts.sort(key=lambda x: -x[1])
for title, count in seq_counts:
    status = 'ZERO COVERAGE' if count == 0 else ('covered' if count >= 3 else 'thin')
    print(f'{title:<42} {count:>5}  {status}')
print('\n(For opportunity-sorted sequel/short + distractor-only gaps, run scripts/find_gaps.py)')
