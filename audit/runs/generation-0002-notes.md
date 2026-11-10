# Question generation round 2 — November 10, 2026

Requested scope: **100 additional questions**, with topic selection delegated to
Codex. Reviewer: Codex. IDs **2696–2795**, following the first round's 40 questions.
All changes remain local and unpublished.

The starting bank contained 1,895 active questions. The selection used actual
four-option bank reads and additional key-term searches, not the old topic-count
tool's incomplete labels. This round broadens theatrical animation coverage,
especially older package features and less represented character, story, music,
literary-source and production facts. These are theatrical features, including
the theatrical compilations' component stories; no real TV-show trivia or
direct-to-video sequel additions were made.

| Film/topic | Added |
|---|---:|
| Dinosaur | 5 |
| Chicken Little | 5 |
| Raya and the Last Dragon | 5 |
| Alice in Wonderland | 5 |
| Lady and the Tramp | 5 |
| Robin Hood | 5 |
| The Sword in the Stone | 5 |
| Oliver & Company | 5 |
| Fantasia 2000 | 5 |
| The Three Caballeros | 5 |
| Saludos Amigos | 3 |
| Make Mine Music | 7 |
| Melody Time | 5 |
| Fun and Fancy Free | 5 |
| The Adventures of Ichabod and Mr. Toad | 5 |
| The Many Adventures of Winnie the Pooh | 5 |
| Peter Pan | 5 |
| Fantasia | 5 |
| The Rescuers | 5 |
| The Rescuers Down Under | 5 |
| **Total** | **100** |

Categories: **66 movies, 20 music, 14 characters**. Editorial difficulty:
**5 easy, 48 medium, 47 hard**. This round favors deeper gaps after the obvious
questions were already covered; it is not intended as an equal-difficulty quota.

All additions have four answers, a unique fact ID, film metadata, an explanation,
an HTTPS source and a verification date. Every review includes the exact premise,
all four option rationales, evidence bases and passage locators, all eight manual
checks, and a separate final wording/evidence challenge. These checks are human
editorial judgments; the validator does not prove factual support.

Research uses Disney's D23 encyclopedia and detailed character articles, and the
official Disney Movies synopsis for Chicken Little. The Buck Cluck relationship
uses a Disney Interactive Studios licensed manual's character biography, accessed
through a transcript mirror because the other PDF mirrors were inaccessible.
That limitation is explicit in the saved source note. The question uses the
film relationship, not game-specific plot. Pooh component-story reviews also cite
the feature's compilation description to establish the 1977 theatrical context.
No direct film viewing is claimed. Specific URLs and locators are preserved in
`generation-0002-sources.json` and in the expanded four-option reviews.

Draft review changes before import:

- Replaced the CinemaScope question after the additional key-term search found
  its inverse, existing #949. The replacement tests Tramp's railroad-yard home.
- Dropped an ambiguous Chicken Little acorn premise and used the directly
  supported alien-invasion threat instead.
- Avoided duplicating details already supplied by existing stems, including
  Pedro's mail route, Goofy's Argentine setting, the samba dance, and Happy Valley.
- Removed unnecessary answer-word overlaps and used parallel causal answers.
- Made the Pooh songwriting question use actual, comparable songwriting pairs.
- Avoided dependence on the disputed wording of the Ward Greene story title;
  the final question tests the credited author.

Duplicate checking covered full topic objects, extra character/production terms,
new-versus-bank and new-versus-new similarity at 0.35, and uncapped normalized
shared-answer groups. The 38 final audit warnings were read with all options and
individually decided. They concern independent cast credits, different family
relationships, conductor versus orchestra, a party host versus its occasion,
and unrelated facts sharing an answer. Full comparisons and specific rationales
are saved in `generation-0002-comparisons.json`. The imperfect text matcher also
misses some spelling variants, so key-term inspection checked names such as the
Shermans and CinemaScope separately.

Validation and preservation:

- Draft validation before append: zero errors. Remaining advisory answer-style
  notices concern initials/honorifics, proper composition titles, or intentionally
  parallel clauses; no final answer-leak warnings remained.
- Final structural validation: 1,995 questions in 10 shards, zero errors.
- Final audit gate: zero errors, zero missing source verification, no open findings.
- All 100 additions have current recorded evidence and completed approval.
- The 1,895 pre-round question objects are preserved, including generation round 1.
  Retired snapshots and the frozen audit baseline are unchanged; no IDs were reused.
- q-009 now contains 250 questions. The remaining 20 are in the new q-010 shard,
  which is included in the manifest. The next fresh ID is **2796**.

Final counts: **100 reviewed / 100 evidence-recorded / 100 approved / 100 added /
0 pre-existing questions edited / 0 retired / 0 unresolved**. Change type:
**100 new-content additions**, not factual corrections. The bank is now
**1,995 active questions**, with **185 preserved retired snapshots**.

The baseline and runtime were not changed. Structural and audit checks are the
relevant checks for this content-only update; no runtime tests, deployment,
player-data writes, or Firestore rules changes were performed.
