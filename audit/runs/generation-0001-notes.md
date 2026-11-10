# Question generation round 1 — November 10, 2026

Completed locally by Codex. Added 40 questions, IDs **2656–2695**, to
`questions/q-009.json`. No app publication was requested or performed.

The starting bank contained 1,855 active questions, all approved. Selection used
category/difficulty totals, the existing coverage report, full four-option topic
reads and cross-bank searches. The old coverage tool omits several films and
underreports others (notably Onward, Luca and Soul); its apparent gaps were not
treated as reliable quotas. This round prioritizes original theatrical films
with modest existing coverage. Existing crowded titles and secondary shorts or
direct-to-video sequels received no additions.

| Film | Before | Added | After |
|---|---:|---:|---:|
| The Good Dinosaur | 3 | 6 | 9 |
| Lightyear | 4 | 6 | 10 |
| Strange World | 3 | 6 | 9 |
| Wish | 7 | 5 | 12 |
| Meet the Robinsons | 6 | 5 | 11 |
| Bolt | 7 | 4 | 11 |
| Home on the Range | 8 | 4 | 12 |
| Treasure Planet | 10 | 4 | 14 |

Counts describe the selected film-specific title matches, with false matches
such as Disney Wish, Thunderbolt, Michael Bolton, and Toy Story's Buzz Lightyear
excluded. Unnamed references elsewhere may be missed; these remain editorial
coverage signals. Full existing topic questions are saved in
`generation-0001-coverage.json`.

The additions cover story premises, character relationships, occupations,
locations, plot triggers, creature designs, cast credits, music and production.
Difficulty: **8 easy, 19 medium, 13 hard**. Categories: **20 movies, 12 Pixar,
5 characters, 3 music**. All 40 carry a unique fact ID, film tag, explanation,
HTTPS source and verification date.

Evidence was researched in Pixar's detailed character/world pages, Disney's
official D23 encyclopedia and feature articles, and Walt Disney Records' original
soundtrack listing. No direct film viewing is claimed. Each review records the
located premise, all four option rationales, inference bases, eight editorial
checks and a separate final challenge on the final wording. Evidence and full
reviews are saved alongside this note and imported through `record-many`.

Primary passages:

- [Pixar: The Good Dinosaur](https://www.pixar.com/the-good-dinosaur)
- [Pixar: Lightyear](https://www.pixar.com/lightyear)
- [D23: An Inside Look at Strange World](https://d23.com/an-inside-look-at-strange-world/)
- [D23: Wish characters](https://d23.com/meet-the-characters-of-disney-animations-wish/)
- [D23: Meet the Robinsons](https://d23.com/a-to-z/meet-the-robinsons-film/)
- [D23: Bolt](https://d23.com/a-to-z/bolt-film/)
- [D23: Home on the Range](https://d23.com/a-to-z/home-on-the-range-film/)
- [D23: Treasure Planet](https://d23.com/a-to-z/treasure-planet-film/)
- [D23: Treasure Planet details](https://d23.com/7-things-we-love-about-treasure-planet/)
- [Walt Disney Records: Treasure Planet soundtrack](https://disney.go.com/disneyrecords/Soundtracks/treasureplanet/index.html)

Draft review removed a book-title giveaway and unnecessary answer-word overlaps.
Final revision made Meridian's question ask her profession rather than imply
that evidence of one skill excludes every other skill; the crop-failure question
received more plausible parallel distractors. Final evidence was renewed after
these revisions. The draft validator's remaining Mrs. Caloway punctuation warning
is a name-format false positive. Clause-form answers in the crop-failure question
are parallel, comparable and appropriate to a causal question.

Duplicate review included whole-topic reads, key-term searches, new-vs-existing
and new-vs-new scans at both 0.50 and 0.35 similarity, and uncapped shared-answer
groups. Five audit findings were individually accepted with specific rationales:
Sabino versus Sakina tests different relatives; New York tests different events;
Pearl names unrelated entities; BEN and Jim test different actor credits; Wilbur
names different characters in different films. Final four-option comparisons and
decisions are retained in `generation-0001-comparisons.json`. No duplicates were
retired or reinstated, and no retired ID was reused.

Validation completed:

- Draft structural validation before append: zero errors.
- Whole-corpus validation after final wording: 1,895 questions, zero errors.
- Audit report and release gate: 1,895 approved, zero missing source reviews,
  zero open findings, zero gate errors.
- Sequential audit status: 1,895/1,895 complete; q-009 is 170/170 complete.
- Compared against Git HEAD: all 1,855 existing question objects unchanged;
  retired snapshots, frozen baseline and shard manifest unchanged.

Scope result: **40 reviewed / 40 evidence-recorded / 40 approved / 40 added /
0 existing questions edited / 0 retired / 0 unresolved**. Change type is new
content, not factual correction. Runtime tests were unnecessary for a content-only
change; no runtime, storage or scoring code changed. Two transient Windows ledger
replace denials were retried through the supported commands and the final gate
confirmed the persisted reviews and decisions.

The bank now has **1,895 active questions** and **185 preserved retired snapshots**.
This is one generation round, not a claim that every film now has sufficient
coverage. Later rounds should repeat full-topic research for other theatrical
gaps, check actual coverage for omitted titles such as Dinosaur and Chicken
Little, and consider older package features without treating counts as quotas.
The next fresh ID is **2696**; q-009 has room before its approximate 250-question
shard limit. All changes remain local and unpublished.
