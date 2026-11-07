"""Record individually reviewed findings and retained-edit classifications."""
import json
from pathlib import Path
from subprocess import run
import sys

ROOT = Path(__file__).resolve().parents[2]
P = json.loads((ROOT/'artifacts/question-audit/current.json').read_text(encoding='utf-8'))
REASONS = {
 (110,1155): 'Different castle/location facts: California Sleeping Beauty Castle versus Shanghai Enchanted Storybook Castle. Knowing one does not identify the other.',
 (118,926): 'Birth city and full birth date are different biographical facts; neither answer supplies the other.',
 (111,358): 'Different resorts and different opening years: Shanghai 2016 versus Paris 1992.',
 (111,2259): 'Shanghai park opening in 2016 is different from a later Zootopia land opening in 2023.',
 (119,935): 'Studio first-feature chronology and the venue of a particular premiere are different facts. Knowing the first feature does not establish the Carthay Circle venue.',
 (120,2422): 'Character creation and the Up villain naming allusion are different facts; identifying Mickey does not establish the Charles Mintz/Charles Muntz connection.',
 (148,2433): 'Remy restaurant identity and an alleged film cameo are different subjects. The identical string is not evidence of the same fact; the out-of-scope cameo is not approved by this decision.',
 (138,696): 'Magic-class horn repertoire and the identity of a Pinocchio song are different facts; film-song knowledge does not prove the ship-specific horn association.',
 (123,661): 'Oscar count and Soul character identifier merely share 22; they are unrelated facts.',
 (105,2249): 'Shanghai park official name and the original location of the TRON attraction are different facts; geography/name recognition does not establish TRON history.',
 (149,2254): 'Cruise-ship maiden-voyage year and Hong Kong land opening merely share 2012; different events.',
 (149,1609): 'Fantasy maiden voyage and Lucasfilm acquisition merely share 2012; different events.',
 (149,2240): 'Fantasy maiden voyage and Cars Land opening merely share 2012; different events.',
 (136,964): 'First fleet-ship identity and the ship carrying AquaDunk are different facts; knowing which ship was first does not locate the slide.',
 (148,172): 'A ship restaurant and a film character share a name, but restaurant cuisine/ship placement is a new fact beyond character identity.',
 (119,440): 'First-feature chronology is different from a particular song appearing in that film; either fact requires separate knowledge.',
 (137,2568): 'Cruise operations commencement and the private island opening are different events, even though both occurred in 1998.',
 (151,1392): 'The 1992 film introducing a particular Rice song is distinct from Ashman death/completion history. The out-of-scope question is not source-approved here.',
 (119,1241): 'First-feature chronology is different from the With a Smile and a Song film association.',
 (114,2256): 'The dated resort renaming event is different from the location of a Ratatouille attraction.',
 (120,1195): 'Walt\'s mouse creation identity is different from the character specifically recognized by an honorary Academy award in 1932.',
 (119,991): 'First-feature chronology is different from the Whistle While You Work film association.',
 (138,717): 'The ship-class horn melody is distinct from the first Disney song to win an Oscar; the award fact does not establish a horn repertoire.',
}
CLASSIFY = {
106: (['clarification'], 'Bound operating-resort count to November 2026; exclude an announced future resort.'),
109: (['clarification'], 'Distinguish adult public gate admission from child prices, preview day and ride bundles.'),
110: (['clarification','difficulty'], 'Ask the official castle name and calibrate iconic-name recall to easy.'),
113: (['clarification'], 'Replace the answer-name giveaway with the source-backed 1966 dedication event; retain hard historical recall.'),
114: (['clarification'], 'Separate the 1994 official naming event from the original Euro Disney name.'),
122: (['clarification','distractors'], 'Pin the theatrical period and use four rabbit names instead of giving away the answer with two cats.'),
123: (['factual','clarification'], 'Correct the lifetime/all-awards premise to competitive wins including the posthumous credit.'),
128: (['clarification'], 'Attribute the naming account as Disney\'s traditional story, matching the source\'s legend qualification.'),
129: (['clarification'], 'Ask for the railroad name, not its type; distinguish the locomotive from the railway.'),
130: (['clarification'], 'Specify the 1922 fairy-tale shorts rather than all work from a vaguely defined first studio.'),
134: (['clarification','distractors'], 'Pin evening classes and replace the second Art Institute alias with a distinct institution.'),
135: (['factual','clarification','difficulty'], 'Remove the incorrect last-major-production implication and make straightforward Mary Poppins recognition easy.'),
138: (['clarification'], 'Restrict the horn question to original Magic-class ships, excluding later multi-song repertoires.'),
139: (['clarification','difficulty'], 'Replace unbounded current majority/homeport claim with the maiden-voyage port; use medium for historical recall.'),
140: (['clarification','difficulty'], 'Ask the ship-specific Marvel Academy association, date-bound to November 2026, rather than generic kids-space naming.'),
146: (['clarification'], 'Replace fleet-wide changing registration claim with Destiny\'s documented 2025 flag.'),
147: (['factual','clarification','distractors','difficulty'], 'Remove separate-private-island premise; test the precise first-preview date with parallel date options, preserving a distinct fact from destination-name questions.'),
149: (['clarification','difficulty'], 'Distinguish maiden voyage from launch/float-out and calibrate year recall to medium.'),
151: (['clarification'], 'Specify the 1992 animated introduction rather than an unbounded appearance claim.'),
}

def cli(*args):
    r=run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    if r.returncode:
        print(r.stdout,r.stderr)
        raise SystemExit(r.returncode)

if __name__=='__main__':
    saved=[]
    for finding in P['openFindings']:
        kind=finding['kind']
        ids=tuple(sorted(finding['questionIds']))
        if kind=='duplicate':
            reason=REASONS[ids]
        elif kind=='answer-style' and ids==(119,):
            reason='These are unembellished official film titles. Snow White\'s title is inherently longer; it is not padded with a correct-only explanation. All four are credible early Disney features.'
        elif kind=='leak' and ids==(129,):
            reason='Railroad describes the object being asked for. All four options are parallel railway/train names; this shared object word does not identify Carolwood Pacific.'
        else:
            raise RuntimeError(f'Unreviewed finding: {finding}')
        cli('decide',finding['id'],'accepted','--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0003-reviews')
        saved.append({'findingId':finding['id'],'questionIds':list(ids),'reason':reason,'decision':'accepted'})
    (ROOT/'audit/runs/next-shard-0003-decisions.json').write_text(json.dumps(saved,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for qid,(types,reason) in CLASSIFY.items():
        args=['classify',str(qid),'--reviewer','Codex','--reason',reason,'--reference',f'audit/runs/next-shard-0003-reviews/{qid}.json']
        for typ in types:
            args.extend(['--type',typ])
        cli(*args)
    print(f'Recorded {len(saved)} reviewed finding decisions and {len(CLASSIFY)} retained-edit classifications.')
