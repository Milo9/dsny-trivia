"""Record the reviewed classifications and finding decisions using supported commands."""
import json, subprocess, sys
from pathlib import Path
root=Path(__file__).resolve().parents[2]
changes={
802:(['clarification','distractors'],'Separate the initial acting lure from Pleasure Island and replace accomplice Gideon.'),
815:(['clarification'],'Fix the initial countryside guide encounter, excluding the band\'s later rescue.'),
825:(['clarification','difficulty'],'Fix the 1992 version and set full-name recall to medium.'),
826:(['clarification'],'Remove pride answer echo and state the original film version.'),
828:(['clarification'],'Ask about Quasimodo attending the celebration rather than the earlier opening prologue.'),
829:(['clarification','distractors'],'Exclude the defensible many-headed Cerberus option and specify head growth during the battle.'),
835:(['clarification','distractors'],'Distinguish the spherical object from its holographic projection and omit unnecessary color.'),
837:(['difficulty'],'Calibrate the main heroines\' basic animal type from hard to easy.'),
842:(['clarification','distractors'],'Ask whose birthday and use parallel possessive person options.'),
843:(['clarification'],'Remove game answer echo without changing the hub fact.'),
844:(['clarification'],'Ask for Elsa\'s home so the approach bridge cannot also answer.'),
846:(['clarification','distractors'],'Distinguish toxic flowers from manufactured serum and make all options flower names.'),
848:(['clarification'],'Name BuzzzTube and the head-algorithm role, excluding other genuine helpers.'),
}
for i,(types,reason) in changes.items():
    args=['classify',str(i)]
    for typ in types: args+=['--type',typ]
    args+=['--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0015-reviews.json']
    subprocess.run([sys.executable,'scripts/question_audit.py']+args,cwd=root,check=True)
decisions={
'duplicate-3517aecfb285341aa901':'#841 asks where Mama Odie lives, #1014 what song she sings. The boat-in-tree dwelling and Dig a Little Deeper are independent facts.',
'duplicate-93d32124a97ac91e69d2':'#833 asks Kida\'s first name Kidagakash; #2594 her father\'s name Kashekim Nedakh. Shared film and royal naming context do not supply the other person\'s identity.',
'duplicate-f0fedfabe192fa0069c3':'#810 identifies Lady\'s two neighbors Jock and Trusty; #2480 tests Jock\'s specific terrier breed. A name does not supply the breed, and the breed does not supply the pair.',
'duplicate-f4d609e2ad41d74a061f':'#849 asks the whole land Kumandra; #1098 asks Raya\'s region Heart. These are distinct geographic levels, with different answers and knowledge.',
}
for fid,reason in decisions.items():
    subprocess.run([sys.executable,'scripts/question_audit.py','decide',fid,'accepted','--reviewer','Codex','--reason',reason,'--reference','audit/runs/next-shard-0015-reviews.json'],cwd=root,check=True)
(root/'audit/runs/next-shard-0015-change-notes.json').write_text(json.dumps({str(k):{'types':v[0],'reason':v[1]} for k,v in changes.items()},indent=2)+'\n',encoding='utf-8')
