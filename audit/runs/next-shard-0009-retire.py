"""Execute Codex's individually reviewed duplicate decisions with preserved snapshots."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
questions = {q['id']: q for f in (ROOT/'questions').glob('q-*.json')
             for q in json.loads(f.read_text(encoding='utf-8'))}
rows = [
 (437, 2283, "Both expose the You've Got a Friend in Me–Toy Story association; retain the composer/score-career question with additional production context."),
 (439, 792, "Same I Just Can't Wait to Be King–Lion King association in reverse; retain the specific Simba/Zazu musical-number question."),
 (440, 1390, "Same Some Day My Prince Will Come–Snow White association; retain the character-performance question rather than the film-title version."),
 (442, 714, "Same opening number Belle–Beauty and the Beast fact in reverse; retain the song-identification question."),
 (443, 458, "The Oscar question already gives the Can You Feel the Love Tonight–Lion King association and tests the award; retain its additional award distinction."),
 (444, 722, "Same Almost There–Princess and the Frog association in reverse; retain the question locating Tiana's dream song."),
 (445, 711, "Same Go the Distance–Hercules association in reverse; retain the question describing Hercules's yearning."),
 (449, 723, "Same Zero to Hero–Hercules association in reverse; retain the Muses/rise-to-fame question."),
 (452, 791, "Same Phil Collins–Tarzan song attribution. Original overclaims the entire soundtrack: Mark Mancina scored it and other performers also sing. Retain the question separating songs from score; its all-five performance wording should be checked when its own scope is audited."),
 (454, 703, "Question 703 supplies Alan Menken as composer and tests Howard Ashman as lyricist, covering the same pair and roles; retain its shorter parallel answers."),
 (464, 2313, "Same Hellfire–Hunchback association in reverse; retain the specific Frollo/fireplace musical-number question."),
 (465, 709, "Same Lion King songwriting partnership: the team question covers the Elton John/Tim Rice attribution; retain the pair question rather than repeat one partner."),
 (467, 717, "Same first Disney Best Original Song Oscar for When You Wish Upon a Star; retain the shorter song-title question."),
 (475, 482, "Same Soul–jazz protagonist association in reverse; retain the film-identification question with its afterlife premise."),
 (476, 786, "Same Toy Story 4 spork-turned-toy fact in reverse; retain the question asking what utensil Bonnie crafts. Forky spelling checked against Pixar, including the resolved historical player flag."),
]
out = ROOT/'audit/runs/next-shard-0009-comparisons.json'
out.write_text(json.dumps({'reviewer':'Codex','at':'2026-11-07','comparisons':[
 {'retiredId':a,'replacementId':b,'question':questions[a],'replacement':questions[b],
  'reason':r,'challenge':'Read both complete questions and all eight options. The retained wording already exposes the association needed to answer the removed question; no distinct fact is lost.'}
 for a,b,r in rows]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for a,b,r in rows:
    result = subprocess.run([sys.executable,'scripts/question_audit.py','retire',str(a),
        '--replaced-by',str(b),'--reviewer','Codex','--reason',r,'--reference',str(out.relative_to(ROOT))],cwd=ROOT,capture_output=True,text=True)
    print(a, result.returncode, result.stdout.splitlines()[-1] if result.stdout else result.stderr)
    if result.returncode:
        raise SystemExit(result.stdout+result.stderr)
