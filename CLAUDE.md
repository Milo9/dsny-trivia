# Disney Trivia App — Claude Reference

## What This Is
A static single-page trivia app built for Kristen and Cara to practice before a Disney Cruise. No build step, no framework, no package manager.

**Live URL:** https://milo9.github.io/dsny-trivia/
**GitHub repo:** https://github.com/Milo9/dsny-trivia

## File Map
| File | Role |
|---|---|
| `index.html` | Single-page shell. All 6 screens live here as hidden divs. |
| `style.css` | All styling. Dark Disney theme, mobile-first, CSS variables at the top. |
| `app.js` | All game logic. Loaded last. Depends on `storage.js` and the `questions/` shards. |
| `storage.js` | Storage abstraction. `FirebaseAdapter` is active. `LocalStorageAdapter` is kept below it as a fallback. |
| `questions/manifest.json` | Lists the shard filenames. `app.js` fetches this first, then fetches each shard. |
| `questions/q-001.json` | Questions 1–250 (249 active). |
| `questions/q-002.json` | Questions 251–500 (245 active). |
| `questions/q-003.json` | Questions 501–799 (222 active; gaps from audit and dedup passes). |
| `questions/q-004.json` | Questions 801–1050 (246 active). |
| `questions/q-005.json` | Questions 1051–1300 (247 active). |
| `questions/q-006.json` | Questions 1302–2017 (250 active). |
| `questions/q-007.json` | Questions 2018–2267 (250 active). |
| `questions/q-008.json` | Questions 2268–2524 (250 active). |
| `questions/q-009.json` | Questions 2525–2655 (131 active). |
| `movies.json` | Weekly Homework movie pool — flat array of `{id, title, year, studio}`, Disney animated + Pixar canon. Fetched by `app.js` at boot alongside questions. |
| `review.html` | Standalone admin page for reviewing flagged questions. Shares the same Firestore `flags` collection. |
| `scripts/count_topics.py` | Counts questions per Disney/Pixar film (question + correct answer only, not distractors); parent-film counts exclude sequel/short matches, which are reported separately. Run from project root: `python scripts/count_topics.py`. Re-run after large batches of additions to update the Per-film coverage map in this file. |
| `scripts/_common.py` | Shared helpers (corpus loader, text normalization, the `SEQUELS_AND_SHORTS` registry) used by the scripts below. Not run directly. |
| `scripts/recon.py` | Compact `id + question` dump for a keyword/film — token-cheap alternative to reading full Grep hits during pre-draft recon. See Question-Bank Tooling below. |
| `scripts/find_gaps.py` | Novelty gap-finder: distractor-only entities and sequel/short coverage, lowest-covered first. See Question-Bank Tooling below. |
| `scripts/find_near_dupes.py` | Lexical near-duplicate detector, whole-corpus or `--new` against a draft batch. See Question-Bank Tooling below. |
| `scripts/validate_batch.py` | Pre-append sanity check for a drafted batch (IDs, enums, exact dupes, answer-format heuristics). See Question-Bank Tooling below. |

## The 6 Screens
Screens are `<div class="screen">` elements that get `.hidden` toggled. Only one is visible at a time. Navigation is handled by `showScreen(id)` in `app.js`.

1. `screen-home` — player selection, add new player; shows today's and yesterday's daily challenge comparison cards, plus the Weekly Homework card (this week's assigned movie)
2. `screen-settings` — difficulty, categories, question count; daily button becomes "Review Today's Questions" after the player has played
3. `screen-game` — active game
4. `screen-results` — score, category breakdown, missed question review; shows "Review All Questions" button for daily games
5. `screen-daily-review` — all 10 daily questions with each player's answer and the correct answer; reachable from results (after playing today), settings daily button (once played today), or the "View Questions →" link on yesterday's home card; title updates dynamically (Today's Review / Yesterday's Review)
6. `screen-leaderboard` — all players ranked by total points (lifetime)

## Question Format
```js
{
  id: 1,                        // unique integer, never reuse
  question: "Question text?",
  answers: ["Correct", "Wrong1", "Wrong2", "Wrong3"],  // correct answer is always index 0; app.js shuffles display order
  difficulty: "easy",           // "easy" | "medium" | "hard"
  category: "movies"            // see categories below
}
```

**Categories:** `movies` | `characters` | `parks` | `walt` | `cruise` | `music` | `pixar`

**No TV shows** — the requirement explicitly excludes Disney Channel, streaming series, etc. This is easy to accidentally violate (Mandalorian, WandaVision, DuckTales reboot, etc.) — hold the line.

**Shard format:** Each shard is a JSON array with **one question object per line** (compact, not pretty-printed). `app.js` loads shards via `r.json()` so indentation is irrelevant to the app. The compact format means each line contains the full question + all answers, making Grep results immediately useful for duplicate checking without reading whole files.

Example line:
```
{"id": 1, "question": "What color is Cinderella's iconic ball gown?", "answers": ["Blue", "Pink", "Yellow", "White"], "difficulty": "easy", "category": "movies"},
```

**Adding questions:** Append to the last shard (`questions/q-009.json` is current), one object per line, no pretty-printing. Use the next available integer ID (2579+). Correct answer must be at index 0. When a shard reaches ~250 questions, create the next shard (`q-010.json`, etc.) and add it to `questions/manifest.json` — no change to `index.html` needed.

**Dedup workflow (grep-first, mandatory):** Before writing any new question, grep all shards for 2–3 key terms from the topic. Because each question is one line, a Grep hit returns the entire question + all answers — eyeball it immediately to confirm it's a true duplicate or a distinct angle. Do not read whole shard files for dedup. For the initial "has this stem/angle been asked at all" scan on a saturated film, `scripts/recon.py` is a cheaper first pass (compact one-line-per-question digest instead of full Grep hits) — but it hides the correct answer by default (`--show-answer` adds only answers[0], never distractors), so once a candidate stem looks close, confirm with a real Grep hit or `--show-answer` before judging it a true duplicate; recon narrows the search, it doesn't replace the eyeball. Before appending a drafted batch, run `scripts/validate_batch.py` (format/enum/exact-dup checks) and `scripts/find_near_dupes.py --new` (lexical near-duplicate check, new-vs-existing and new-vs-new) — see Question-Bank Tooling below for the full workflow.

**Current count:** 2,050 questions (IDs 1–2655, with gaps from removed duplicates/errors). Distribution (exact, via count_topics.py):
- movies 465, characters 370, pixar 307, parks 310, music 221, walt 209, cruise 168

**Per-film coverage map** (questions that are *about* this film — correct answer or question text, not distractors). **The counts below are a rough signal, not a cap.** A film at 30 can still take a 31st question if the fact is genuinely un-asked — the real gate is always "is this a distinct fact, verified against a grep of the existing stems," never "is the count already high." Treat "Saturated" as "the obvious tier-1 facts are probably taken, go deeper (secondary characters, specific scenes/songs, production trivia, direct-to-video sequels, shorts) rather than skip the film," not as "stop." Under-covered rows are just as likely to reflect the count_topics.py regex undercounting (see note below) as genuinely thin coverage — grep the real stems before assuming either way.

| Film | Count | Status |
|---|---|---|
| Toy Story | 56 | Saturated |
| Frozen | 55 | Saturated |
| Beauty and the Beast | 35 | Saturated |
| The Little Mermaid | 30 | Saturated |
| The Lion King | 30 | Saturated |
| Moana | 30 | Saturated |
| Finding Nemo / Finding Dory | 30 | Saturated |
| Cinderella | 29 | Saturated |
| Aladdin | 27 | Saturated |
| Zootopia | 26 | Saturated |
| Encanto | 24 | Saturated |
| Inside Out | 22 | Saturated |
| The Incredibles | 22 | Saturated |
| Tangled | 21 | Saturated |
| Pocahontas | 20 | Saturated |
| Ratatouille | 19 | Well-covered |
| The Emperor's New Groove | 19 | Well-covered |
| Cars | 18 | Well-covered |
| The Hunchback of Notre Dame | 17 | Well-covered |
| Tarzan | 17 | Well-covered |
| Monsters Inc. / Monsters University | 17 | Well-covered |
| Bambi | 17 | Well-covered |
| The Jungle Book | 17 | Well-covered |
| Mulan | 16 | Well-covered |
| Wreck-It Ralph | 15 | Well-covered |
| Atlantis: The Lost Empire | 15 | Well-covered |
| Elemental | 15 | Well-covered |
| A Bug's Life | 14 | Well-covered |
| 101 Dalmatians | 14 | Well-covered |
| Brother Bear | 14 | Well-covered |
| Brave | 13 | Well-covered |
| Big Hero 6 | 13 | Well-covered |
| Turning Red | 13 | Well-covered |
| The Fox and the Hound | 13 | Well-covered |
| WALL-E | 12 | Well-covered |
| Soul | 12 | Well-covered |
| Inside Out 2 | 11 | Well-covered |
| Hercules | 9 | Under-covered (unreliable — see note) |
| Coco | 9 | Under-covered (unreliable — see note) |
| Up | 7 | Under-covered (unreliable — see note) |
| Onward | 7 | Under-covered (unreliable — see note) |
| Luca | 7 | Under-covered (unreliable — see note) |

**Note on Hercules/Coco/Onward/Luca/Up specifically:** the 2026-07-24 batch added 5–7 new questions to each of these per the table above, but a fork's recon during that batch found 30–38 *existing* Grep hits per film — 3–5x what this regex-based table shows. The count_topics.py regex undercounts these five badly (likely a phrasing/keyword-co-occurrence gap in the script, not a real coverage gap). Treat these five rows as especially unreliable; grep the actual stems before assuming they're wide open. **Reconfirmed 2026-07-29:** a fork targeting exactly these five films for the 100-question batch below recon'd all five and found Hercules, Coco, Onward, and Soul (also mistakenly assumed under-covered) fully saturated on every fresh angle it tried — it added zero questions to any of them and redirected its budget to Up, A Bug's Life, Brave, Elemental, Fox and the Hound, and Atlantis instead. Up still took only 3 clean new questions before thinning out. **These five rows should be treated as effectively saturated already, not as open opportunities**, despite what the table's raw number suggests.

These counts still fold numbered theatrical sequels into their parent row (Frozen includes Frozen II, Toy Story includes 2–4, etc.) since that's one continuously-active franchise, not a stale catalog title. **Direct-to-video sequels and shorts are excluded from the parent row and tracked separately** — run `python scripts/count_topics.py` for their counts or `python scripts/find_gaps.py --sequels` for the same list sorted lowest-coverage-first; see `scripts/_common.py:SEQUELS_AND_SHORTS` for the tracked list (Lion King II, Return of Jafar, King of Thieves, Little Mermaid II, Mulan II, Pocahontas II, Hunchback II, Cinderella II/III, Brother Bear 2, 101 Dalmatians II, Jungle Book 2, Tarzan II, Fox and the Hound 2, Kronk's New Groove, Bambi II, Frozen Fever, Olaf's Frozen Adventure, Geri's Game, Piper, Bao). **These titles are soft-capped, not a priority vein — see "Content balance" rule 10 below; a low/zero count here is no longer, by itself, a reason to draft for one.**

**Content policy (2026-07-29): sequels/shorts/made-for-TV soft-capped.** Earlier batches (2026-07-21 through 2026-07-24, see the dated notes below) explicitly hunted for zero-coverage direct-to-video sequels and shorts because they were the easiest source of "genuinely novel" facts, and this worked — but repeated often enough that it risked pulling the bank's balance away from theatrical/main-canon content over time. As of this date, sequels/shorts/made-for-TV movies sit at ~126 questions across 20 tracked titles (~6.4% of the corpus, averaging ~6.3/title) against theatrical films running 6–55 (most "well-covered" titles at 15–20+) — not yet imbalanced, but the old framing ("richest under-mined vein," "wide open") actively pulled future batches toward growing this bucket further just because it scores low on the gap-finder, not because the fact is actually important to the bank. Going forward: soft-cap each sequel/short/made-for-TV title at ~8–10 questions (roughly today's average), and prefer theatrical/main-canon gaps first when choosing what to research next. See rule 10 below.

This table is updated manually; re-run `scripts/count_topics.py` to regenerate it after large batches of additions. Note: the script's keyword regexes only match question text + correct answer, and require fairly specific phrase co-occurrence (e.g. Coco requires `coco`+`pixar` or `miguel`+`guitar` etc. in the same string) — some films are likely undercounted relative to their true coverage; treat this table as a floor, not an exact census.

**Duplicate audit (2026-07-21):** Players reported near-duplicate questions — same fact tested with reworded question text (not exact text matches). Ran a script-assisted audit: grouped all questions by normalized correct answer (ignoring honorifics/articles) plus a film/category-blocked word-overlap pass, then manually reviewed ~150 candidate clusters to separate true duplicates (same fact, reworded) from coincidental matches (different facts that happen to share an answer, e.g. two unrelated questions both answering "1971"). Removed 116 true duplicates, always keeping the better-worded/more-accurately-categorized copy. This is a one-time cleanup — the existing grep-first dedup workflow above remains the process for preventing new duplicates.

**Content generation strategy (2026-07-21, revised same day):** An initial attempt to add 250 questions from memory recall landed at only 72 clean ones — memory of "obvious" facts per film runs out fast in a bank this size. Revised approach, which then added a further 135 questions cleanly in one sitting: **generate WebSearch-primary, not memory-primary.** Research a film/topic's plot, characters, and production details via search, then harvest the facts not already in the bank from that same reading — the source you're reading from doubles as the verification, so this is nearly free of the hallucination risk memory-only drafting carries. One search reliably yields enough material for 5–10 questions. The richest under-mined veins turned out to be: direct-to-video sequels (The Lion King II, Return of Jafar/King of Thieves, Little Mermaid II, Mulan II, Pocahontas II, Hunchback II, Cinderella III, Brother Bear 2, 101 Dalmatians II, Jungle Book 2, Tarzan II, Fox and the Hound 2, Kronk's New Groove, Bambi II — nearly all had zero prior coverage), theatrical shorts (Frozen Fever, Olaf's Frozen Adventure, Geri's Game, Piper, Bao), classic package-film segments (Three Caballeros, Fun and Fancy Free, Fantasia/Fantasia 2000 segments beyond the two or three already covered), specific songs that only ever appeared as wrong-answer distractors and were never the actual target of a question, and verified post-2023 park/cruise facts. Still corroborate surprising specifics (dates, "first/only" claims, exact figures) — two invented-sounding facts were caught and fixed this way before deploy (see git log). The dedup gate is unchanged and non-negotiable: recon-first grep, then an end-of-batch answer-normalized pass covering new-vs-new AND new-vs-existing, PLUS an ignore-thresholds same-answer0 dump (a real duplicate — WALL-E's Axiom ship name — slipped past the thresholded pass in the first round and was only caught this way).

**Content expansion (2026-07-21):** Added 72 new questions (IDs 1553–1624, gaps intentional) after discovering the bank is far more comprehensively mined than raw per-film counts suggest — grepping candidate films before drafting repeatedly turned up existing coverage of the "obvious" facts, even for films the coverage table shows as under-covered. The effective workflow that worked: grep/dump existing coverage for a whole category or film *before* drafting a single question (not after), harvest only facts you're fully certain of, and WebSearch-verify anything post-2023 (new cruise ships, recent park changes) rather than guessing. A dedup pass (answer-normalized, new-vs-new and new-vs-existing) at the end caught 3 genuine duplicates a per-topic grep had missed. This is why the batch landed at 72 rather than a pre-set target — see the deploy notes/commit for the honest accounting.

**Content expansion (2026-07-23):** User asked for 500 new questions; landed at 183 clean (IDs 2136–2318) after generating 185 and cutting 2 true near-duplicates at the merge gate — 500 was never realistic for a single sitting given how mined the bank already was (see the 72/135 precedents above), and padding toward a number would have meant shipping unverified or duplicate content, which the project's dedup gate exists to prevent. **Parallelized via 10 fork agents**, each given a disjoint topic bucket (under-covered classics: Bambi/Brother Bear/Hercules/Fox and the Hound; under-covered Pixar: Soul/Onward/Luca/Coco/Up; direct-to-video sequels & shorts, including Cinderella II: Dreams Come True which had zero prior coverage; parks split three ways — WDW Magic Kingdom+EPCOT, WDW Hollywood Studios+Animal Kingdom+Disneyland/DCA, international parks; Walt/company history; Disney Cruise Line; music; and a secondary-character deep dive using the distractor-only gap report) so each fork's WebSearch-verify-then-draft work stayed independent and out of the main context. **Coordination lesson:** parallel forks can't see each other's drafts, so new-vs-new duplication across forks — not new-vs-existing — was the real risk; each fork wrote to its own scratch file with non-colliding placeholder IDs (bucket-prefixed, e.g. 91000s, 92000s), and the dedup/validation gate ran exactly once on the concatenated union of all 10 files before any renumbering or shard append, which is what caught the two cross-fork-adjacent true duplicates (a Carousel of Progress identification question redundant with existing #369, and a Grimsby/Vanessa question redundant with existing #822 — both same fact as an existing question, different surface wording). Also fixed two pre-existing miscategorized entries found incidentally by a fork during recon (#2076 Frozen Fever and #2133 The Emperor's New Groove were tagged `pixar`; both are Disney, not Pixar — corrected to `movies`). Added a new shard, `questions/q-008.json`, since q-007 filled to 250. Category "walt" and cruise-ship-restaurant/venue trivia were confirmed as the most heavily mined non-film categories — clean yield there came from corporate-history and stage-show angles rather than core biography/ship-amenity facts, which are close to exhausted.

**Content expansion (2026-07-23, single-session no-subagent batch):** User asked for 150 more questions in one sitting, explicitly without forking subagents. First pass landed at 76 clean; an advisor review before declaring done flagged that "the bank is saturated" wasn't fully earned yet — several productive veins (the distractor-gap report, package-film segments, brand-new films) were still untapped, and stopping at 76 without surfacing the shortfall would have quietly under-delivered. A second pass mined those veins further — Disney Legend/Imagineer bios (Sterling Holloway, Ward Kimball, John Hench), two more Melody Time segments, and, richest of all, films with **zero prior coverage**: Zootopia 2 (2025, released 8 months before this session) and Pixar's Elio (2025) — and landed the total at 93 clean (IDs 2319–2417, gaps from 7 questions cut at the dedup/quality gates across both passes; one of those cuts was a Mickey Mouse Club question pulled proactively for brushing against the project's no-TV-shows rule even though a same-topic precedent existed). Still short of 150, but every additional pass was still finding genuine, verified, non-duplicate facts when it stopped — the honest read is that a single non-parallel session has a real but not-yet-found ceiling above 93 for this corpus, not that 93 is the wall. The same lessons as the 2026-07-21 and prior 2026-07-23 batches held: worked through topic buckets sequentially (sequels/shorts, cruise, walt history, music, secondary characters, package films, then a second round of Imagineer bios + brand-new-film coverage), recon-checked every topic before drafting, and ran `find_near_dupes.py --new` once per merged batch. That end-of-batch pass caught 6 true "same fact, different wording" duplicates in the first round alone — two near-identical to existing question phrasing (Wendy's brothers' names, Simba/Nala's daughter Kiara) and four with different wording but the same correct answer (Bruno and Pepa's Madrigal gifts, Ray the firefly, Geri's Game dentures/teeth) — reconfirming the answer-normalized Pass B is load-bearing every batch, not just an edge case. Also caught and fixed a real categorization bug the advisor review found post-hoc: three drafted Zootopia questions were mistagged `pixar` (Zootopia is Walt Disney Animation, not Pixar; existing corpus already tags it `characters`) — `validate_batch.py` only checks enum membership, not semantic correctness, so a wrong-but-valid category sailed through undetected.

**Content expansion (2026-07-24):** User asked for another 150 questions. Landed at 161 clean (IDs 2418–2578, one gap from a cut duplicate) via **6 parallel fork agents** on disjoint buckets: under-covered core films (Hercules/Onward/Luca/Coco/Up), low-tier direct-to-video sequels & shorts, classic lesser-mined films with no dedicated coverage row (Black Cauldron, Lady and the Tramp, Robin Hood, Sword in the Stone, Rescuers, Oliver & Company, Great Mouse Detective, Aristocats — a genuinely fresh vein, all previously under 15 questions each), international parks (Tokyo DisneySea, Shanghai Disneyland, Disneyland Paris, Hong Kong Disneyland), a music deep dive, and cruise/Walt history. Raw yield was 162; the merge-gate `find_near_dupes.py --new` pass on the concatenated union caught exactly one true cross-fork duplicate (Walt's 22-Oscar record, same fact as existing #679, asked two ways). Two buckets came in under their 28-question target for reasons worth keeping: music (22) and cruise/Walt (24) are — as the 2026-07-23 note below already flagged — the most heavily-mined non-film territory in the bank; both forks explicitly reported hitting saturation on the obvious angles and pivoted to genuinely fresh but narrower veins (real-world pop cover versions of film songs, cut songs, and awards trivia for music; the newest ships/venues — Disney Treasure, Disney Adventure, Disney Destiny, Lookout Cay — for cruise). **New finding that revises the coverage table's reliability further:** the Bucket A fork's recon turned up 30–38 existing Grep hits for Up/Coco/Hercules/Onward/Luca — several times what count_topics.py's regex reports — confirming the table undercounts these films specifically; see the note added to the Per-film coverage map. This pushed q-008.json to its 250-question cap; the overflow (54 questions) started a new shard, `questions/q-009.json`.

**Quality audit (2026-07-29):** Full-corpus pass looking for duplicates, factual drift, and poorly-worded questions (not a content-expansion batch). `find_near_dupes.py`'s Pass A (raised to `--threshold 0.75` to cut noise) and Pass B were both run whole-corpus and read in full; nearly every Pass B cluster was the expected false-positive pattern (different facts sharing a one-word answer, e.g. two questions both answering "1971") — only one true duplicate surfaced this way (#132/#1496, Walt's 1939 honorary Snow White Oscar, reworded; #132 removed). A second true duplicate (#2310/#2402, Big Hero 6's "Fred's family is secretly wealthy" fact) was caught only by manually reading a cluster the scripts couldn't group, because the two answer strings ("They are extremely wealthy" vs "His family is enormously wealthy") don't normalize to the same text — a reminder that Pass B's answer-normalization can still miss same-fact/different-wording pairs when the answer itself is reworded, not just the question. Removed #2402. Separately ran a scratch script (not checked in) applying `validate_batch.py`'s sentence-like-answer and answer-leaked-in-question heuristics across all 1,973 questions instead of just a draft batch, plus a category-consistency check against a Pixar-film-title allowlist. Findings and fixes: **20 category bugs** — #2402/#2403 (Big Hero 6, Walt Disney Animation not Pixar) were tagged `pixar`; #2403 recategorized to `characters`. Separately, 19 questions whose core subject is a Pixar film were tagged `movies` instead of `pixar` per rule 9 — #8, #12, #19, #28, #30, #35, #37, #214, #222, #242, #244, #263 (all from the original q-001/q-002 shards, predating rule 9's codification) plus #1540, #1572–#1576, #2024 (Incredibles 2 and Cars 2, from later batches — showing the rule 9 bug recurs, not just legacy drift); all recategorized to `pixar`. **1 stale superlative** — #1614 called the Disney Destiny "Disney Cruise Line's newest ship as of 2026"; confirmed via WebSearch that Disney Adventure's maiden voyage slipped from December 2025 to March 2026, making Destiny no longer the newest ship — reworded to drop the claim entirely rather than re-pin it to a date that will just rot again. **3 answer-leaked-in-question fixes** — #1386 ("boasting about his collection of shiny objects" → answer "Shiny"), #1590 ("small, star-shaped magical being" → answer "Star"), and #2027 (question named the film's full subtitle, *101 Dalmatians II: Patch's London Adventure*, which contains the answer "Patch" outright) — all reworded to remove the giveaway phrase/title while preserving the fact tested. The sentence-like-answer heuristic itself threw ~350 hits but nearly all were legitimate multi-part names ("Huey, Dewey, and Louie") or intentionally explanatory answers to "why"/"what happens" questions — an established, accepted style in this bank, not a defect; it was not worth a bulk rewrite and none were changed. Net: corpus went from 1,975 to 1,973 questions (two true duplicates removed); category distribution shifted (movies 464→445, pixar 279→296, characters 354→355, walt 203→202) — table above and this file updated in the same commit as the fixes, per the project's always-keep-docs-current rule.

**Follow-up not yet done — distractor correctness:** This pass verified that correct answers (answers[0]) hold up, but did not verify rule 5 ("wrong answers must be wrong") at scale — the ~5,900 distractors across the corpus were never systematically fact-checked, only the ones noticed incidentally while reading for other issues. This needs real per-question verification (no script can judge whether a wrong answer is secretly also true), so it's slow and was deliberately deferred rather than rushed. Next time quality-auditing this bank, budget time for it separately — likely scoped to high-risk categories first (walt/music "first to win X" and similar record-claim questions, where a distractor can accidentally also be a true fact about a different film/person).

**Superlative sweep (2026-07-29):** Grepped all shards for "first/only/largest/biggest/smallest/longest/record/unprecedented/ever made" in question text — 137 hits. Nearly all were permanently-true historical facts (e.g. "first Mickey Mouse cartoon," "Walt's father's first name") that can't rot regardless of what launches later, so they needed no check. WebSearch-verified the ~10 that were genuinely current-record claims about an active/ongoing category (World of Disney "world's largest Disney character store," World of Frozen "world's first and largest Frozen-themed land," Germaine Franco "first woman to score a WDAS feature," Barlow & Bear "first all-female songwriting team" for Moana 2, Disney Adventure's "cruises to nowhere" itinerary) — all still hold up as of today. **Found one genuine factual error this way:** #2364 asked how many artists share the Billboard-record credit on 'We Don't Talk About Bruno,' with "Six" as the stored correct answer — multiple sources (Forbes, Billboard) confirm the actual record-breaking count is **seven** (six named performers plus the ensemble "Encanto cast" credit). Fixed to "Seven." This was not a stale-superlative case (nothing changed over time) — the fact was wrong from whenever it was drafted, only surfaced by actually checking a "record" claim instead of assuming a stored number was right. Worth remembering: a "current record" claim needs the same real verification as a "first/only" claim, even if it isn't the time-sensitive-superlative pattern rule 6 warns about.

**Content expansion (2026-07-29, first batch under the rule 10 sequel/short soft cap):** User asked for 100 new questions. Landed at 77 clean (IDs 2579–2655, one gap from a cut duplicate) via **4 parallel fork agents** on disjoint buckets, explicitly excluding direct-to-video sequels/shorts per the same-day rule 10 policy: (A) the five films CLAUDE.md's table calls "under-covered" — Hercules/Coco/Onward/Luca/Up/Soul, landed 20/25 after confirming on recon that Hercules, Coco, Onward, Soul, and Luca are already fully saturated (redirected to Up/A Bug's Life/Brave/Elemental/Fox and the Hound/Atlantis instead); (B) films with no row at all in the coverage table, confirmed genuinely thin via an advisor-recommended pre-dispatch recon spot-check (4–14 existing hits vs. the corpus's 15–40 norm) — Home on the Range, Chicken Little, Dinosaur, Bolt, Treasure Planet, Lilo & Stitch, Rescuers Down Under, Winnie the Pooh, Dumbo — landed the full 25/25, confirming this was the strongest vein in the batch; (C) parks (secondary/lesser attractions plus international-park depth), landed 22/25 after cutting 5 drafts that turned out to be true duplicates caught during the fork's own recon; (D) music/walt/cruise/secondary characters, landed only 11/25 — recon confirmed this territory (already flagged as heavily-mined in the 2026-07-23 and -24 notes) is now close to exhausted on any angle other than individual Imagineer biographies, which is where this fork's yield came from. Raw yield across all 4 files was 78; the merge-gate `find_near_dupes.py --new` pass caught one true duplicate (Up's Best Original Score composer, Michael Giacchino — same fact as existing #410 and #1502, just phrased with an added "first Pixar win" qualifier that didn't change the underlying tested fact) among several coincidental shared-answer matches (different facts that happen to share a one-word answer, e.g. multiple unrelated questions all answering "Six") that were correctly not duplicates. **This batch is the first real-world test of the rule 10 soft cap** — zero sequel/short questions were drafted by design, and the fork-A recon reconfirmed (a third time now, after 2026-07-24 and this same batch) that the coverage table's "under-covered" label on Hercules/Coco/Onward/Luca/Soul is actively misleading; the table and its reliability note above were updated in the same commit as this batch to say so plainly rather than just flag it as "unreliable."

**Removing a question:** Delete its object from the shard JSON. IDs do not need to be contiguous — gaps are fine.

**Local testing note:** `fetch()` is blocked on `file://`. Run a local server to test (`python -m http.server 8000`). On GitHub Pages it works fine.

## Question-Bank Tooling (scripts/)
All scripts are read-only against the shards — they print reports/candidates for a human to eyeball, they never edit shard JSON (adding/removing a question is still always a manual shard edit, per the rule below). Run from the project root with `python scripts/<name>.py`.

| Script | Purpose |
|---|---|
| `recon.py <regex>` | `id + question` dump for a keyword/film — a token-cheap first pass over full Grep hits during the mandatory pre-draft recon scan. Hides answers by default (`--show-answer` adds only the correct answer, never distractors) — good for "has this stem/angle been asked," not a substitute for a real Grep hit when judging whether a specific fact+answer is already covered. `--all-fields` also searches wrong answers. **Read the full digest for the topic you're drafting about, not just what `find_near_dupes.py` algorithmically flags** — a film is usually 15–40 lines, cheap to read end-to-end with semantic intent. This is the actual catch for "same fact, different answer wording" (e.g. "What weapon is X skilled with? → Bow and arrow" vs. "X's signature skill? → Archery") — no lexical script can judge that two answer strings mean the same thing, only a read can. |
| `find_gaps.py` | Two novelty reports: distractor-only entities (names/terms that have appeared as a wrong answer but never as a correct one — candidate seeds for new questions) and sequel/short coverage counts, lowest first. Run before drafting to find genuinely unmined material instead of relying on memory for what's "obviously" missing. `--distractors` / `--sequels` isolates one report; `--min-count`/`--limit` tune the distractor report (expect some noise — generic words and colors show up; it's advisory, not a verdict). **The `--sequels` report is a coverage census, not a to-do list** — a low count there means a title is under the ~8–10 soft cap (rule 10), not that it's owed more questions; keep theatrical/main-canon gaps as the default target. |
| `find_near_dupes.py` | Lexical near-duplicate detector. No args = whole-corpus self-audit (same method as the 2026-07-21 audit below, but scriptable/repeatable) — groups above `--max-group-size` (default 6) are skipped as likely just a common name. `--new drafts.json` checks a drafted batch against the existing corpus and against itself before appending; Pass B is NOT size-capped in this mode, since output is already scoped to groups touching the draft — capping there would hide exactly the "draft answer matches a common existing answer, worded differently" case this pass exists to catch. Two passes: question-text Jaccard similarity (`--threshold`, default 0.5, tokens lightly stemmed so "kitten"/"kittens" or "sings"/"singing" count as the same token) catches reworded restatements; same-normalized-answer grouping catches same-fact-different-wording that a text-similarity threshold can miss (Pass B is also why this tool independently catches most "semantically equivalent, low word overlap" dupes — same fact usually means same correct answer, regardless of phrasing). Catches lexical overlap only — semantically-equivalent questions with **low word overlap AND a differently-worded answer** (e.g. "bow and arrow" vs. "archery") still need a human read; see the recon.py note below for how that residual case gets caught. Always eyeball flagged pairs; a shared answer or wording doesn't automatically mean duplicate (e.g. two different songs both answering "Pocahontas"). |
| `validate_batch.py drafts.json` | Pre-append sanity check: valid JSON, ID collisions (against the corpus and within the batch), next-available-ID, category/difficulty enum membership, exact-duplicate question text, and advisory heuristics for the Answer structure rules below (sentence-like answers, answer text leaking into the question). Exits non-zero on errors. |
| `count_topics.py` | Per-film coverage counts — see Per-film coverage map below. |

**Recommended batch workflow:** `recon.py` (and/or `find_gaps.py` for topic ideas) — read the full digest for the topic, not just a skim, since that's what catches same-fact-different-answer-wording duplicates no script can — to confirm a fact isn't already covered → draft the batch as a scratch JSON file → `validate_batch.py` → `find_near_dupes.py --new` → append the survivors to the current shard, bump IDs/counts in this file.

## Storage Layer — Firebase (active)
User stats and flags are stored in **Firestore**, project `disneytrivia-38ac6`.

Collections:
- `users` — one doc per player, keyed by user ID
- `flags` — one doc per flag report (auto-ID)
- `dailies` — one doc per calendar day, keyed by `"YYYY-MM-DD"` date key; stores `{ questionIds: [id, ...] }` written by the first player who plays that day
- `weeklyHomework` — single doc `state`; stores the current Weekly Homework movie pick (see below)

Document shape:
```js
// users/{userId}
{ id, name, totalAnswered, totalCorrect, gamesPlayed,
  totalPoints,        // accumulated lifetime points — PRIMARY STATE, not derived (sequence-dependent bonuses make it non-recomputable)
  dailyStreak,        // consecutive days with a daily challenge
  lastDailyDate,      // "YYYY-MM-DD" of last daily played
  lastDailyScore,     // correct count (0–10) in last daily
  lastDailyPoints,    // pts earned in last daily
  lastDailyAnswers,   // [{questionId, correct, selectedText}] — per-question picks from last daily; used by screen-daily-review
  prevDailyDate,      // "YYYY-MM-DD" of the daily before last (populated when day rolls)
  prevDailyScore,     // correct count (0–10) for prevDailyDate
  prevDailyPoints,    // pts earned for prevDailyDate
  prevDailyAnswers,   // [{questionId, correct, selectedText}] — per-question picks shifted from lastDailyAnswers when day rolls
  categoryStats,      // { movies: {answered, correct}, characters: ..., ... } — per-category counters, absent on old docs (treated as {})
  recentQuestionIds } // [id, ...] — mirror of this device's local disney_seen_{userId} list (capped at SEEN_MAX, see below), synced on every
                       // completed/exited game; unioned across all users to exclude recently-played questions when generating a new day's
                       // daily-challenge pin. Absent on old docs (treated as []). See "Regular Game: Answer Order & Repeat Avoidance" below.

// flags/{autoId}
{ questionId, questionText, correctAnswer, allAnswers, difficulty, category,
  reportedBy, comment, timestamp, _resolved? }

// weeklyHomework/state
{ weekKey,   // "YYYY-MM-DD" of the Thursday this pick belongs to, from homeworkWeekKey()
  movieId,   // id into movies.json for the current pick
  pickedAt,  // ISO timestamp of the last pick/shuffle
  watched }  // [{id, watchedAt}, ...] movies already assigned in a past week, with the date
             // watched — excluded from future picks and rendered as watch history.
             // Older docs may have a bare `watchedIds:[id,...]` instead; app.js's
             // normalizeHomeworkState() upgrades that shape in memory on read.
             // NOT seed-derived like the daily challenge — watched-exclusion and the
             // shuffle veto make the pick stateful and non-reproducible. Do not "simplify"
             // this back to a deterministic weekly shuffle.
```

Stats stored as raw counters (`totalAnswered`, `totalCorrect`, `categoryStats`); percentages are always derived, never stored. `totalPoints` looks like a derived value but is **primary state** — streak and bonus mechanics make it non-recomputable from counters alone. `updateStats` uses a Firestore transaction to avoid race conditions when two players finish at the same time. The `dailyUpdate` payload (score, points, dateKey, streak, answers), the `catStats` per-category delta, and the optional `recentQuestionIds` seen-ids mirror are all written inside the same transaction so all fields are always consistent.

**Firebase console:** https://console.firebase.google.com/project/disneytrivia-38ac6

**Switching back to localStorage:** Change the last line of `storage.js` from `new FirebaseAdapter()` to `new LocalStorageAdapter()`. The rest of the app is unaffected.

**Firestore security rules** (currently set to open — URL is the only guard for this private family app):
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;
    }
  }
}
```

## Flag / Review System
- Players tap **👎 Flag** after answering to report a bad question
- Stored in Firestore `flags` collection via `storage.flagReport()`
- `review.html` is the admin triage page — open it at https://milo9.github.io/dsny-trivia/review.html
- After fixing a question in the appropriate shard JSON, mark the flag Resolved in `review.html`
- Flagging does NOT auto-remove the question; that's always a manual edit to the shard JSON

## Deploying Changes
The app is hosted on GitHub Pages from the `main` branch. Use the deploy script:

```powershell
.\deploy.ps1 -Message "your commit message"
```

`deploy.ps1` stages all changes, commits, and pushes in one step. Omitting `-Message` defaults to `"update app"`. GitHub Pages redeploys automatically within ~1 minute.

**Cache-busting for code files:** `index.html` loads `style.css`, `storage.js`, and `app.js` with a `?v=` query string matching `APP_VERSION` (currently 1.25). When making code changes, bump `APP_VERSION` in `app.js` **and** update the matching `?v=` strings in `index.html` so browsers discard their cached copies. Question shard files and `movies.json` (fetched via `fetch()`) use `{ cache: 'no-cache' }` and don't need manual versioning.

**Manual fallback:**
```
git add -A && git commit -m "your message" && git push
```

## Regular Game: Answer Order & Repeat Avoidance

**Answer order** is reshuffled fresh every time a question renders (`renderGameQuestion()` in `app.js`, `const indices = shuffle([0, 1, 2, 3])`), using the plain `shuffle()` Fisher-Yates (`Math.random()`-based). This is a correct, unbiased shuffle — verified 2026-07-29 by simulating the exact function 2,000,000 times, which landed the correct answer in each of the 4 display positions ~25.0% of the time. A player *feeling* like the correct answer lands in position A unusually often is expected perceptual pattern-matching on a genuinely random sequence, not a bug — true randomness clusters more than intuition expects. (The daily-review screen, `screen-daily-review`, uses a *different*, deterministic `seededShuffle([0,1,2,3], q.id)` so a question's displayed answer order is stable across repeated views of that review page — this only affects the review screen, not live gameplay, and does not correlate with what order players actually saw during the game.)

**Local per-player repeat avoidance** — `getSeenIds`/`computeSeenIds`/`saveSeenIds` in `app.js` track up to `SEEN_MAX` (currently 300, ~30 games' worth at the default 10 questions/game) most-recently-played question IDs per player in `localStorage` key `disney_seen_{userId}` — **per-device**, like the other `disney_*` localStorage keys; this is what **regular Play Game / Rematch** uses to pick its pool (post difficulty/category filter is split into fresh (unseen) vs. all — if enough fresh questions exist to fill the requested count, only fresh ones are used, otherwise **the exclusion is dropped entirely** for that game rather than partially topping off with repeats; a narrow filter well under ~300 matching questions can therefore serve repeats sooner than the default all-categories setting would). `SEEN_MAX` was 100 originally, raised to 300 on 2026-06-21 (commit `3339707`), briefly tried 500 on 2026-07-29 same-day, then reverted back to 300.

**Recording** happens for both regular games and daily challenges, on full completion (`endGame()`, unconditional) and on mid-game exit with ≥1 answered question — including a partial daily exit, fixed 2026-07-29 (previously only regular-game mid-exit recorded seen-ids; exiting a daily partway through saved progress for resuming but never marked the already-answered questions as seen, so one of them could still show up in a regular game played before the player went back to finish that day's daily).

**Cross-player daily exclusion (added 2026-07-29):** the daily challenge's own selection (`getDailyQuestions`) is deliberately deterministic and identical for every player, so it can't consult any one player's local seen-ids directly — but it needed *some* way to avoid repeating something any player just saw, in any mode. Solution: each player's capped seen-ids list is also mirrored to their own Firestore user doc as `recentQuestionIds` (written inside the same `updateStats` transaction on full completion / regular-game exit; via the standalone `storage.saveRecentQuestionIds()` on a partial daily exit, since nothing else is committed to Firestore at that point). When a brand-new day's pin is generated — `getDailyQuestions(10, 0, excludeIds)` in the `btn-daily-challenge` handler, and the pin-backfill branch that tops up a shard-deleted pinned ID — `dailyExclusionSet()` builds the exclusion set, then that combined set is excluded from the day's pick (falling back to the unexcluded pool if exclusion would leave fewer than the requested count, same pattern as regular-game selection). This only runs at the moment a *new* pin is actually created for the day — every subsequent player that day just reads the already-pinned list, and the daily-review screen's "regenerate from live pool" last-resort fallback deliberately passes no `excludeIds`, since "what's recently seen right now" has no meaning when reconstructing a past day.

**Daily-pin history, independent of play (added 2026-07-31):** `recentQuestionIds`-only exclusion had two gaps — a pinned daily that nobody ever finishes or exits-with-progress never marks its questions seen anywhere, and `recentQuestionIds` is capped at `SEEN_MAX` per user, so heavy regular-game play (which shares the same capped list) can push a genuinely-recent daily question out of the window well before it should be eligible to repeat as a daily. Fix: every day's pinned IDs already live in Firestore `dailies/{dateKey}` regardless of whether anyone plays; `storage.getAllDailyQuestionIds()` reads the whole `dailies` collection and unions every past day's `questionIds` (cheap at this app's scale — the collection grows ~1 doc/day). `dailyExclusionSet()` (`app.js`, formerly `recentlySeenByAnyone()`) now unions this with the existing `recentQuestionIds` union before excluding from a new day's pick. This uses the *pin*, not actual play, as the source of truth for "already used as a daily" — so unlike `recentQuestionIds`, it isn't bounded by `SEEN_MAX` and doesn't require anyone to have played.

Why per-user Firestore fields (mirroring each player's own list) rather than one shared "recently used" log: `updateStats` already runs each player's stat update inside its own per-user transaction (existing pattern, avoids the race two simultaneous finishes would hit if they both tried to append to one shared mutable document instead).

Known limitation, accepted rather than engineered around: `computeSeenIds` bases "already seen" purely on *this device's* local list, then overwrites the Firestore field wholesale — so a player switching devices doesn't merge histories, it resets what that device's plays contribute to the shared exclusion set going forward (the *other* player's contributions are untouched, since it's a separate document field). Consistent with this app's existing accepted per-device-state trade-offs (daily progress, mute state, etc.) rather than a new problem introduced here.

Seen-ids are recorded only after a *completed* game or a mid-game exit with at least one answered question — an unsaved/failed game leaves seen-ids untouched so its questions can come back around.

## Daily Challenge
A second game mode accessible from the settings screen. Always 10 questions, all categories, no difficulty filter. Uses a deterministic seeded shuffle so **all players see the same questions on a given calendar day**.

- Date key: `"YYYY-MM-DD"` via `dayKey(daysAgo=0)` (or the `todayKey()` wrapper), which subtracts 8h from UTC so the day rolls over at 2am MDT (Mountain Daylight Time) = 4am EDT. This ensures both Eastern and Alberta players always share the same question set. `dayKey(1)` gives yesterday using the same offset — do not compute yesterday via string arithmetic.
- **Pinned question IDs**: When the first player starts the daily challenge, the 10 question IDs are written to `dailies/{dateKey}` in Firestore. Every subsequent player (and the review screen) reads from this doc, so everyone plays the same questions regardless of question deploys that happen later in the day. `getDailyPins(dateKey)` / `saveDailyPins(dateKey, ids)` in `storage.js`.
  - If a pinned ID no longer exists in the shards by the time someone reads it (e.g. it was removed as a duplicate after being pinned), the game-start handler backfills the missing slot(s) from the live pool and re-saves the pins so the day stays at its original count; the review screen instead just omits the missing question (it can't reconstruct what a removed question's text/choices were, so a day whose pins referenced a since-deleted question may show fewer than 10 entries in review — this is expected, not a bug).
- Seed: `dateToSeed(key)` hashes the string; `seededShuffle()` uses an inline mulberry32 step
- Questions are stable-sorted by `id` before shuffling so shard load order doesn't affect results
- Streak (`dailyStreak`, `lastDailyDate`) stored in Firestore on the user doc — cross-device
- **Replay is blocked** — each player can play the daily exactly once per calendar day. The settings button becomes "📋 Review Today's Questions" after playing; the results-screen Rematch button is hidden for daily games.
- **Exit mid-daily → resume, don't restart.** Nothing is committed to Firestore stats until all 10 are answered. Exiting locks in the answered-so-far questions to `localStorage` (`disney_daily_progress_{userId}`, via `saveDailyProgress`/`getDailyProgress`/`clearDailyProgress` in `app.js`) — not Firestore, so this is per-device, like the other `disney_*` localStorage keys. Re-opening the Daily Challenge (`buildDailyGameState()`) resumes at the next unanswered question with the locked-in answers' score/streak already applied; those questions are never re-shown or re-editable. If a resume's saved answers no longer line up position-by-position with today's pinned questions (e.g. a backfill re-pinned the day after the exit), only the still-matching prefix is kept and the rest is treated as unanswered — never silently miscounted. Progress is cleared only after a successful Firestore save in `endGame()`; if that save fails (offline), progress is kept and the next "Daily Challenge" tap detects the already-complete answer set and retries `endGame()` directly instead of restarting the game. The settings screen shows a "▶️ Resume Daily Challenge (n/10)" state (reading the same localStorage progress) so a mid-exit isn't silently invisible. `endGame()` sets `gameState.ended` as a re-entrancy guard so a double-click on the final question (or two near-simultaneous resume-complete calls) can't double-commit stats.
- Per-question answers stored in Firestore as `lastDailyAnswers` on first play; shifted to `prevDailyAnswers` when the next day's challenge is played. Used by `screen-daily-review` for both today and yesterday views.
- Counts toward leaderboard stats just like a regular game
- `gameState.isDaily = true` when a daily challenge is active; `endGame()` checks this flag

New user doc fields (Firestore): `dailyStreak: number`, `lastDailyDate: "YYYY-MM-DD"`, `lastDailyAnswers: [{questionId, correct, selectedText}]`. Existing docs without these fields default gracefully.

## Weekly Homework
A tongue-in-cheek "assignment" feature: a Disney/Pixar movie is picked for family movie night, refreshed every Thursday. Movie pool lives in `movies.json`; pick state lives in Firestore `weeklyHomework/state` (see Document shape above). Card shows on `screen-home`.

- **Not seed-derived.** Unlike the daily challenge, the pick is not deterministic from a seed — watched-exclusion and the shuffle veto make it genuinely stateful. `rollHomeworkIfStale()` reads the stored state; if it's absent or belongs to a past week, it rolls to a new one.
- **Week boundary:** `homeworkWeekKey()` reuses the daily challenge's 8h-UTC-shift trick to roll over at 08:00 UTC = 3am EST / 4am EDT **Thursday**, returning that Thursday's date key. Like the daily challenge, this is a client-triggered check on app load — there is no server-side cron. The new week's movie is picked (and written to Firestore) by whichever player's device happens to load the app first after the boundary passes.
- **Rollover vs. shuffle — two separate code paths, not a shared helper:**
  - `rollHomeworkIfStale()` (boot-time, automatic): the outgoing movie is assumed watched ("homework complete") and pushed onto `watchedIds`, then a new movie is drawn from the unwatched pool.
  - `shuffleHomework()` (manual veto button): draws a new movie excluding `watchedIds` **and** the current pick, but does **not** touch `watchedIds` — a vetoed movie goes back into the pool for a future week.
- **Pool exhaustion:** if every movie is watched, `pickFromMoviePool()` resets and draws from the full pool again (`watchedIds` cleared in the caller).
- **Kristen-only shuffle:** the 🔀 Shuffle button (`#btn-shuffle-homework`) is shown only when `currentUser.id === 'kristen'` — i.e. she has actually selected her own card *this session*. It deliberately does not key off `localStorage.disney_last_user`, since that persists across sessions on a shared device and would show the button to anyone opening the app after Kristen last used it, before they'd selected a player at all this session (this caused an accidental shuffle). Still a loose, client-side-only gate consistent with the rest of the app's security model — it's a light veto-power joke for a 2-person household, not access control.
- **Full movie list:** a `🎬 View Full Movie List` toggle (`#btn-toggle-watched`) expands `#homework-watched-list`, showing the *entire* pool as two groups (current week's pick is excluded from both — it's already shown above):
  - **✅ Watched** — sorted newest-watched first (`watchedAt` descending), each row has an ✕. Clicking it calls `removeFromWatched(movieId)`, pulling that entry out of `watched` and saving — the movie goes back in the pool for future picks/shuffles.
  - **🍿 Not Yet Assigned** — everything else, alphabetical, read-only.
  - **Open to any player, no Kristen gate** on the ✕ (unlike shuffle).
- Graceful degradation: if `movies.json` or the Firestore read fails, the card just stays hidden (`init()` catches the error separately from question loading so a homework failure never blocks the trivia app itself).

## Sound Effects
Web Audio API (synthesized, no audio files). Wrapped in the `sounds` IIFE in `app.js`:

- `sounds.correct()` — two-note ascending chime (C5 → E5)
- `sounds.wrong()` — single low triangle-wave thud (A3)
- `sounds.fanfare()` — C major arpeggio (C5→E5→G5→C6), plays at results screen
- `sounds.toggle()` — flip muted state; persists in `localStorage` key `disney_sound_muted`
- Mute button (🔊/🔇) is in the game screen top bar next to Exit

## Scoring System
Points are computed by `scoreBreakdown(answers, earnDailyBonus, dailyStreak, awardPerfect = true)` in `app.js` and stored atomically to Firestore inside the `updateStats` transaction. `awardPerfect` is passed `false` only from the mid-game exit handler — otherwise "all answered so far were correct" on a partial (unfinished) set would incorrectly earn the perfect-game bonus. Earning formula:

| Component | Value |
|---|---|
| Correct answer — easy | 100 pts |
| Correct answer — medium | 150 pts |
| Correct answer — hard | 200 pts |
| In-game streak bonus (run ≥ 3) | +25 per correct while streak holds |
| Perfect game (all correct) | +500 pts |
| Daily challenge completion (first play of day) | +200 pts flat |
| Daily streak scaling (first play of day) | +10 × min(dailyStreak, 30) |

- `SCORING` constant object in `app.js` holds all values — edit there to rebalance
- `scoreBreakdown()` returns `{ base, streakBonus, perfectBonus, dailyBonus, total }`
- Leaderboard sorts by `totalPoints` descending; percentage is the secondary tiebreaker
- Results screen shows full breakdown when more than one component contributed
- Exiting mid-game awards base + streak bonus for answered questions only, no perfect/daily bonus

## Key app.js Globals
| Variable | What it holds |
|---|---|
| `QUESTIONS` | Flat array of all question objects, populated at boot by `loadQuestions()` |
| `MOVIES` | Flat array of all movie objects, populated at boot by `loadMovies()` |
| `currentUser` | The user object selected on the home screen |
| `gameSettings` | `{ difficulty, categories[], questionCount }` — set on settings screen |
| `gameState` | `{ questions[], currentIndex, answers[], score, currentStreak, isDaily, pointsEarned, scoreBreakdown }` — active game |
| `shuffledOpts` | `[{text, originalIndex}]` — display order for current question's answers |
| `homeworkState` | `{ weekKey, movieId, pickedAt, watched: [{id, watchedAt}] }` — this week's Weekly Homework pick, mirrors Firestore `weeklyHomework/state` |

## Styling Conventions
- CSS variables defined in `:root` at the top of `style.css` — use these, don't hardcode colors
- Key variables: `--bg`, `--bg-card`, `--bg-hover`, `--border`, `--primary`, `--gold`, `--green`, `--red`, `--text`, `--muted`
- Border-radius variables: `--r` (cards), `--r-sm` (buttons/inputs)
- All new screens follow the pattern: `.screen` div → `screen-header` → content → actions at bottom
- Mobile-first. Max width 480px centered. Test at 375px (iPhone SE) as the floor.

## Players
Default users seeded on first load: **Kristen** and **Cara**. Seeding is in `FirebaseAdapter._seed()` — it checks if the doc exists before writing, so it's safe to run on every page load. Do not remove them from the seed.

## Question Quality Rules (Lessons from Audits)

These rules were derived from real mistakes found during shard audits. Follow them every time questions are generated.

**Before adding any new question:**
1. **Cross-shard duplicate check** — Grep all shard files for key terms (character name, attraction name, film title) before writing. Because shards are one-question-per-line, each Grep hit shows the full question + answers — no need to open the file. Questions about the same topic often exist already. Easy/obvious topics (Mickey's dog, Donald's nephews, Tinker Bell's dress color, Simba's father) are almost certainly covered — check first. Also check the Per-film coverage map above: if a film is Saturated (≥20), skip it unless the angle is clearly distinct from what's there.

**Answer structure:**
2. **Never embed the answer in the question text.** If the question says "What type of animal is Geppetto's cat?" and the answer is "Figaro is a kitten," the word "cat" telegraphs the answer. Ask "What is the name of Geppetto's kitten?" instead.
3. **Never include explanatory prose in answer strings.** Answers must be short noun phrases, not sentences. Bad: `"Figaro is a kitten"`. Good: `"Figaro"`.
4. **Never use "All of the above" as a wrong answer** if all the listed options could plausibly be correct. Verify that wrong answers are actually wrong before using them.
5. **Wrong answers must be wrong.** If a question lists three "wrong" options and all three happen to be correct real-world answers, the question is broken. Replace them with genuinely incorrect options.

**Factual accuracy:**
6. **Avoid time-sensitive superlatives.** Phrases like "newest," "latest," or "most recent" become false when new things launch. Name the specific year instead: "the ship that launched in 2022" rather than "the newest ship."
7. **Verify ride/attraction names and statuses.** Brandings change — Rock 'n' Roller Coaster dropped "Starring Aerosmith" at WDW in 2024; Splash Mountain became Tiana's Bayou Adventure in 2024. Check before writing.
8. **Verify ship-specific facts.** DCL restaurant and venue names vary by ship (After Hours on Magic/Wonder, The District on Dream, Europa on Fantasy, Enchanté on Wish). Never write a question about "the adult area on Disney ships" — pin it to a specific ship.

**Category:**
9. **Pixar films use `pixar`, not `movies`.** Brave, Coco, Up, Inside Out, Finding Dory, Onward, Luca, Elemental, Toy Story, Monsters Inc., A Bug's Life, Cars, Ratatouille, WALL-E — all are `pixar`. If in doubt, check whether Pixar Animation Studios is the credited studio.

**Content balance:**
10. **Direct-to-video sequels, shorts, and made-for-TV movies are secondary content — soft-capped at ~8–10 questions per title**, not a floor to fill just because they're unmined. `find_gaps.py --sequels` (or the tracked list in `scripts/_common.py:SEQUELS_AND_SHORTS`) showing a title at or near zero is not, by itself, a reason to draft for it — a title already near the cap should only take another question for a fact that's clearly exceptional, the same bar a Saturated theatrical film gets under rule 1. When choosing what to research next, default to theatrical/main-canon gaps (going deeper on a Saturated film per rule 1, or filling an Under-covered one) over topping up a low-coverage sequel/short. See the Per-film coverage map's 2026-07-29 policy note for the rationale.

## What NOT to Do
- Do not introduce a build step, bundler, or npm unless explicitly asked
- Do not add a backend or server — this is intentionally fully static
- Do not store derived values (percentages) — always compute from raw counters
- Do not add TV show questions
- Do not reuse question IDs
