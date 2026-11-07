"""Explicit warning decisions and final-content change classifications."""
import json, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def run(*args):
    p=subprocess.run([sys.executable,'scripts/question_audit.py',*map(str,args)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8')
    print(' '.join(map(str,args[:3])),p.returncode)
    if p.returncode:raise RuntimeError(p.stdout+p.stderr)
reasons={
 (724,):'All four answers are genuine titles of Cinderella songs, quoted in full. The correct title is naturally longer; it does not echo the final stem or receive a uniquely explanatory suffix. The bedroom sequence, rather than title length, selects the answer.',
 (438,701):'q438 asks fictional character Elsa; q701 asks the real performer Idina Menzel. Knowing the character does not establish the real performer, especially with the separate Demi Lovato recording.',
 (458,718):'q458 asks The Lion King\'s winning song, Can You Feel the Love Tonight; q718 asks the 1993 winner, A Whole New World. Distinct films, songs and ceremonies.',
 (729,2352):'Wish\'s 2022 maiden voyage and Treasure\'s ship-class/size relationship are different facts. Identifying Wish by voyage date does not establish Treasure\'s class.',
 (468,703):'The original Little Mermaid lyric credit is a separate work from the Beauty and the Beast/Aladdin credits in q468. A known collaboration does not prove an individual film credit; the remake even has additional lyricists, so 1989 is explicit.',
 (718,719):'q718 asks Aladdin\'s 1993 winner; q719 asks the Mary Poppins winning song. Similar award wording, independent songs and film contexts.',
 (729,1223):'A 2022 maiden voyage does not establish which Grand Hall statue a ship has. Date identity and decorative statue assignment require different knowledge.',
 (743,2276):'Dream\'s January 2011 maiden voyage and a stage show debuting aboard it in 2017 are independent historical events.',
 (159,725):'q159 asks the composer shared by three other films; q725 asks the Hunchback orchestral score. A composer\'s earlier credits do not establish a later film assignment.',
 (729,743):'Same chronological question format but different ships and dates: Wish July 2022 versus Dream January 2011.',
 (743,1221):'Dream\'s maiden voyage date and Admiral Donald atrium statue are different ship attributes; one answer alone does not establish the other relationship.',
 (450,701):'These ask credits for two distinct recordings, Let It Go in Frozen and Into the Unknown in Frozen 2. Same role and performer do not guarantee a separate song\'s recording credit: Frozen also uses a different pop singer for its end-credit rendition. Retain the original-film recording fact separately from the sequel recording fact.',
 (716,1261):'The opening Tarzan montage uses Two Worlds; the childhood-growth montage uses Son of Man. Different scenes and songs; full music digest confirms distinct targets.'
}
scope=set(read('audit/runs/next-shard-0013-plan.json')['questionIds'])
report=read('artifacts/question-audit.json')
findings=[f for f in report['openFindings'] if scope.intersection(f['questionIds'])]
assert {tuple(f['questionIds']) for f in findings}==set(reasons)
records=[dict(finding=f,reviewer='Codex',reason=reasons[tuple(f['questionIds'])],reference='audit/runs/next-shard-0013-evidence-notes.json') for f in findings]
(ROOT/'audit/runs/next-shard-0013-finding-decisions.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for f in findings:run('decide',f['id'],'accepted','--reviewer','Codex','--reason',reasons[tuple(f['questionIds'])],'--reference','audit/runs/next-shard-0013-finding-decisions.json')
types={
698:['clarification'],699:['clarification'],701:['clarification'],703:['clarification'],
704:['factual','clarification','difficulty'],705:['factual','clarification','difficulty'],706:['clarification','difficulty'],708:['factual','clarification'],
713:['clarification','distractors','difficulty'],714:['clarification','difficulty'],715:['clarification'],716:['clarification','difficulty'],718:['clarification'],720:['clarification'],721:['clarification','difficulty'],722:['clarification','difficulty'],
724:['factual','clarification'],725:['clarification'],729:['clarification'],739:['factual','clarification','distractors','difficulty'],742:['clarification'],743:['clarification'],
746:['clarification','distractors','difficulty'],747:['clarification','distractors','difficulty'],750:['factual','clarification','distractors'],758:['factual','clarification','distractors'],760:['clarification','distractors','difficulty'],762:['clarification'],770:['clarification','difficulty'],772:['clarification','distractors'],773:['clarification']}
initial={r['questionId']:r['hash'] for r in read('audit/runs/next-shard-0013-initial-template.json')['reviews']}
final={r['questionId']:r['hash'] for r in read('audit/runs/next-shard-0013-evidence-notes.json')['reviews']}
assert {i for i,h in final.items() if initial[i]!=h}==set(types)
detail={704:'Removed false physical-solitude claim; the song is a vocal solo while companions are present.',705:'Restricted the originally multiple-answer household-object performance claim to Belle\'s elaborate dinner presentation.',708:'Both listed Bruno and A Whole New World reached No. 1. Replaced unique-highest implication with the exact 2022 first-since-1993 event.',724:'Corrected the chores scene to the opening attic-bedroom sequence; other listed song Sing Sweet Nightingale belongs to chores.',739:'Replaced unsupported Dole Whip availability claim with the positively documented soft-serve machine dessert. This does not assert Dole Whip is absent everywhere.',750:'Removed the unsupported Movies Under the Stars proper-title construction; the documented DCL screen is Funnel Vision.',758:'The trapped condition could include Arendellian soldiers and Forest People could describe Northuldra. Yelana leadership and separate named peoples now provide one answer.'}
for i,ts in types.items():
    args=['classify',i]
    for t in ts:args+=['--type',t]
    run(*args,'--reviewer','Codex','--reason',detail.get(i,'Clarified the final scene/version/historical event and improved option parallelism or difficulty where classified; see the question-specific evidence challenge.'),'--reference','audit/runs/next-shard-0013-evidence-notes.json')
