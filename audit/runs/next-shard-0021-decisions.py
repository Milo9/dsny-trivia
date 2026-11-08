"""Batch 21's explicit pair decisions and classifications; uses audit CLI."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
def read(p):
    return json.loads((ROOT / p).read_text(encoding='utf-8'))
def save(p, x):
    (ROOT / p).write_text(json.dumps(x, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def run(*args):
    subprocess.run([sys.executable, 'scripts/question_audit.py', *map(str, args)], cwd=ROOT, check=True)

reasons = {
 (854,1104): 'George is Wendy\'s father; Mary is her mother. These are distinct family members and names.',
 (336,1138): 'Big Thunder Mountain and Country Bear are different attractions; knowing one Frontierland location does not place the other.',
 (536,1128): 'Sitka is Kenai\'s eldest brother; Tanana is the tribe\'s shaman. The distinct relationships require different names.',
 (578,1132): 'Naveen is Tiana\'s love interest; Eudora is her mother. Knowing one relationship does not identify the other.',
 (441,1102): 'Jiminy\'s song performance and his appointment as conscience are distinct roles. Knowing a singer does not prove his story office.',
 (888,1139): 'The greenhouse boat setting does not locate its pavilion. This question adds the Land pavilion and separately locates Soarin there.',
 (1124,2488): 'Kronk\'s Bucky conversation and Wart\'s transformed animal in another film are different facts despite both involving squirrels.',
 (1115,2500): 'Fidget\'s name and his peg leg are separate identity and physical-trait facts. His name alone does not establish his leg.',
 (1124,1433): 'Kronk speaks squirrel to Bucky; Up dogs interrupt speech when spotting squirrels. These are different actions in different films.',
 (1136,2526): 'Disneyland\'s broad Old West land theme does not locate Phantom Manor at Disneyland Paris.',
 (1111,1251): 'Sir Hiss\'s advisor identity does not name the song mocking Prince John\'s rule.',
 (1136,1138): 'Disneyland\'s western theme and Magic Kingdom\'s Country Bear location are park-specific facts; neither establishes the other.',
 (275,1131): 'Penny the rescued orphan and Penny the owner of Bolt are different characters in different films.',
 (1068,1114): 'Eilonwy is Taran\'s princess companion, Fflewddur his minstrel companion. Naming one does not name the other.',
 (1151,2241): '2001 is the entire DisneySea park opening; 2024 is the later Fantasy Springs expansion opening.',
 (336,1136): 'Magic Kingdom\'s Big Thunder land assignment differs from Disneyland\'s overall Old West theme.',
 (1139,1175): 'The Land\'s ride locations do not establish its Garden Grill restaurant location; different facilities are mapped to the pavilion.',
 (337,1143): 'The Magic Kingdom entrance avenue and the Disneyland Railroad entrance station are different park/facility mappings.',
 (1061,1108): 'Kay is Arthur\'s foster brother while Ector is his foster father. These are distinct relationships.',
 (1138,2526): 'Country Bear at Magic Kingdom and Phantom Manor in Paris have independent land assignments.',
 (882,1134): 'Wasabi\'s plasma equipment and Honey Lemon\'s chemistry spheres are different character/equipment mappings.',
 (563,1117): 'Goofy\'s son Max and Eric\'s pet dog Max are different characters in different films.',
 (282,1119): 'Sarabi is Simba\'s mother; Sarafina is Nala\'s mother. Similar spellings do not merge the two family relationships.',
 (1133,2303): 'The Duke\'s volunteering of bodyguards and the later Zootopia surname/voice-actor pun are separate story and production facts.',
}
retirements = {
 1123: (273, 'Both identify Jane\'s scientist father as Professor Porter. The full-name question includes the same title/surname and requires additional first-name recall; the shorter identity question adds no fact.'),
 1150: (1366, 'Both encode the Magic Kingdom Space Mountain opening in 1975, with identity and opening year reversed. Retain the dedicated historical-year question.'),
}
types = {
 1102:['clarification'], 1103:['clarification'], 1104:['clarification'],
 1105:['clarification'], 1106:['clarification'],
 1107:['clarification','difficulty'], 1109:['clarification','distractors'],
 1114:['clarification'], 1116:['distractors'], 1117:['clarification'],
 1118:['clarification'], 1119:['clarification'], 1120:['clarification'],
 1121:['clarification','distractors'], 1122:['clarification'],
 1124:['clarification'], 1126:['clarification','distractors'],
 1128:['clarification','distractors'], 1129:['clarification','difficulty'],
 1131:['clarification'], 1133:['clarification'], 1135:['clarification'],
 1136:['clarification'], 1137:['clarification'], 1138:['clarification'],
 1139:['clarification','distractors'], 1142:['clarification'],
 1143:['clarification','distractors'], 1145:['clarification'],
 1146:['factual','clarification','distractors'],
 1147:['clarification'], 1148:['factual','clarification'],
}

def comparisons():
    plan = read('audit/runs/next-shard-0021-plan.json')
    scope = set(plan['questionIds'])
    qs = {q['id']: q for f in (ROOT/'questions').glob('q-*.json') for q in read(str(f.relative_to(ROOT)))}
    report = read('artifacts/question-audit.json')
    pairs = []
    for finding in report['findings']:
        ids = tuple(finding['questionIds'])
        if not scope.intersection(ids) or finding['kind'] != 'duplicate' or ids == (1150,1366):
            continue
        pairs.append({'findingId': finding['id'], 'questions': [qs[i] for i in ids],
                      'verdict':'distinct', 'reason':reasons[ids]})
    for old, (keep, reason) in retirements.items():
        pairs.append({'questions':[qs[old],qs[keep]], 'verdict':'retire-first', 'reason':reason,
                      'evidence': ('https://en.wikipedia.org/wiki/Tarzan_(1999_film)' if old == 1123 else
                                   'https://disneyexperiences.com/disneyworld-press/release/walt-disney-world-celebrates-50-years-of-space-mountain/'),
                      'locator': ('Voice cast Professor Archimedes Q. Porter; Clayton is the escort' if old == 1123 else
                                  'Opening paragraph January 15, 1975; indoor coaster description'),
                      'optionChallenge': ('Professor Porter is the named father. Clayton is the hunter; Doctor Archimedes and Sir Porter alter his title. The retained full-name option alone matches Archimedes Q., excluding Augustus J., Alexander B. and Archibald M.' if old == 1123 else
                                          'Space Mountain is the named 1975 indoor coaster; TRON, Big Thunder and Barnstormer are different attractions. In the retained question, the recorded 1975 date excludes 1971, 1977 and 1980.')})
    pairs.extend([
        {'questions':[qs[1110],qs[2071],qs[2072]], 'verdict':'distinct',
         'reason':'Band leader identity, Hit Cat\'s guitar and Scat Cat\'s trumpet are three role/instrument mappings. Naming a leader does not establish either instrument.'},
        {'questions':[qs[1102],qs[556]], 'verdict':'distinct',
         'reason':'The conscience appointment and the gold certification badge at the ending are distinct events and facts.'},
        {'questions':[qs[1137],qs[624]], 'verdict':'distinct',
         'reason':'The 1959 original opening name and the 2007 Finding Nemo retheme name are different historical names and events.'}
    ])
    save('audit/runs/next-shard-0021-comparisons.json', {'reviewer':'Codex','at':'2026-11-08','comparisons':pairs})

def retire():
    for qid, (replacement, reason) in retirements.items():
        run('retire', qid, '--replaced-by', replacement, '--reviewer','Codex', '--reason',reason,
            '--reference','audit/runs/next-shard-0021-comparisons.json')

def decide():
    scope = set(read('audit/runs/next-shard-0021-plan.json')['questionIds'])
    report = read('artifacts/question-audit.json')
    for finding in report['findings']:
        ids = tuple(finding['questionIds'])
        if not scope.intersection(ids):
            continue
        if finding['kind'] == 'duplicate':
            reason = reasons[ids]
        elif finding['kind'] == 'leak' and ids == (1145,):
            reason = 'World is ordinary language in the attributed worldwide ranking; all four answers are Disney Springs shops. It does not repeat the distinctive shop name or decide which shop carries the advertisement.'
        else:
            raise ValueError(finding)
        run('decide', finding['id'], 'accepted', '--reviewer','Codex', '--reason',reason,
            '--reference','audit/runs/next-shard-0021-comparisons.json')

def classify():
    for qid, change_types in types.items():
        args = ['classify', qid]
        for change_type in change_types:
            args += ['--type',change_type]
        args += ['--reviewer','Codex','--reason',
                 ('Corrected obsolete present tense or show-description premise; renewed all four options.' if qid in (1146,1148) else
                  'Clarified version, scene, role or dated context and/or improved the explicitly classified options/difficulty; correct answer identity retained.'),
                 '--reference','audit/runs/next-shard-0021-reviews.json']
        run(*args)

if __name__ == '__main__':
    {'comparisons':comparisons,'retire':retire,'decide':decide,'classify':classify}[sys.argv[1]]()
