# Brief for generation round 5: 200 easy questions (backlog #18)

Prepared by Claude 2026-11-24, after v1.59, from the #17 difficulty audit. This is a
starting point; QUESTION_AUDIT.md remains the procedure. Recompute counts before use.

## Start state (2026-11-24)

- 2,191 active, 189 retired. Audit 2191/2191 complete, gate 0 errors. **Next ID 2996.**
- 396 easy / 1,071 medium / 724 hard. Easy by category: movies 108, pixar 85,
  characters 79, parks 44, music 37, cruise 31, walt 12.
- q-009 has 248 questions and q-010 has 220, so add a new shard, `questions/q-011.json`,
  and list it in `questions/manifest.json`. sw.js reads the manifest; no change needed.

## Do this first: the new-question cap would hide the batch

`MAX_NEW_PER_DAILY` (1) applies to every ID >= `NEW_QUESTION_MIN_ID` (2656) in
game-logic.js, so IDs 2996+ would share one slot a day with the round it paces. The
cap exists to pace 2656-2995. Give it an upper bound (2995), adjust the cap test
(it generates IDs 2656 to 3075), update DEVELOPMENT.md, and rerun a simulation with
the new bank. Without this the 200 easy questions barely reach the daily. If the
simulation shows the easy batch itself flooding the daily, raise pacing with the owner.

With 596 easy, 2 a day (360 per 180-day window) has ample room. 3 a day (540) becomes
possible but tight; the mix stays 2/5/3 unless the owner asks.

## What "easy" must mean here

The previous rounds' labels failed (new "easy" 40% correct vs 64% for older easy on the
same days). Target what casual family fans would get about 80% of the time.

- **The film or place must be famous.** No 1950s-70s live action, no Strange World /
  Wish / Good Dinosaur-tier titles, no very recent releases (Elio and Hoppers missed).
- Ask the headline: main characters, sidekicks, villains, the big song, the famous
  object/place/catchphrase, the premise. No cast, crew, director, year or
  production-credit questions, no secondary-character names, no exact numbers.
- Keep real distractors. Easy means a familiar fact, not joke options.
- **All four players right:** #212 Moana's pet pig, #206 the poisoned fruit,
  #809 what chases Captain Hook, #438 who sings Let It Go, #826 Pride Rock,
  #338 the park with World Showcase, #1064 Robin Hood's love interest.
- **Easy label but 0-1 right:** #210 Casita, #1131 Bolt's owner, #1274 "camouflage",
  #418 AquaMouse, #2329 Piper's feature. (Tiny samples; hints only.)

## Where the room is

Famous titles with few easy questions (approximate, stems naming the title, total/easy):
Aristocats 16/0, Big Hero 6 12/0, Lady and the Tramp 17/1, Mulan 20/1, Tarzan 18/1,
Hunchback 19/1, A Bug's Life 13/1, Onward 20/1, Mary Poppins 5/1, Dumbo 11/2,
Pocahontas 19/2, Ratatouille 18/2, WALL-E 12/2, Brave 14/2, Luca 22/2,
Wreck-It Ralph 13/2, Nightmare Before Christmas 5/2, Coco 29/3, Jungle Book 21/3,
Lilo & Stitch 12/3, Turning Red 13/3, Soul 16/3, Hercules 30/4, Pinocchio 17/4,
101 Dalmatians 18/4, Sleeping Beauty 13/4, Zootopia 22/4.

Many headline facts already exist as *medium*: read the full topic first, and never
write an easier rewording of an existing question (that is a duplicate). Relabelling
such a medium is a separate, re-reviewed edit. If room runs out, propose relabels to
the owner rather than going obscure.

Categories: give walt, music, parks and cruise a real share (walt 12 and cruise 31 are
thinnest) with famous facts only. Pin cruise venues to a ship, anchor changeable park or
cruise facts to a date with a recheck tier (rule 7), and prefer lasting facts. The owner
does not want content skewed toward cruise.

## Process reminders

- WebSearch-first, with sources read for every option. D23 a-to-z and Pixar pages load
  with plain `curl`, so they can be read in bulk (33 pages this way for #17).
- Each question needs a schema-2 review before release: plan, `sync`, source notes,
  `build-reviews` or an author script, `record-many`, `report`, decide each finding,
  `close`, `check`. generation-0003/0004 files show the artifacts;
  `release-1.59-difficulty-author.py` is a recent scripted example.
- Any edit to an existing question, even only its difficulty, reopens hash-bound
  duplicate decisions on both sides (41 reopened for 79 relabels). Read and decide each.
- Dedup: `recon.py` / `question_audit.py view` per topic before drafting, then
  `validate_batch.py`, `find_near_dupes.py --new`, `find_leaks.py`. Check retired.json
  too, so a retired fact is not rewritten.
- Use `python -X utf8` on Windows, and write long scripts with the Write tool: long Bash
  heredocs failed twice with "unexpected EOF".
- Ship with `deploy.ps1 -IncludeUntracked -MessageFile <path outside repo>` in the
  background. The cap change triggers the version bump by itself.

## After shipping

Check accuracy around 2026-12-15 (backlog #17): read-only receipts under
`users/{id}/games`, joined to `dailies/{date}` snapshots. Baselines: 59% for 10-29 to
11-10, 43% for 11-11 to 11-24. Confirm dailies picked by v1.59 devices hold at most one
ID in 2656-2995 (the 2026-11-25 pick may still come from a v1.58 phone).
