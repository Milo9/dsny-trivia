# Batch 7: complete for scope

Reviewer: Codex. Review date: 2026-11-06.

Fixed scope: the 50 IDs in `next-shard-0007-plan.json`, physical shard
`questions/q-002.json`. Related questions were read for comparison, not added to
the audit. The full character and parks digests, film topic digests, ranked
comparisons, and additional cross-bank title/name searches were inspected.

## Results

- 50 reviewed, including 14 documented duplicate retirements.
- 36 retained questions have final-wording schema-2 evidence and approval.
- 20 retained questions edited; 14 original snapshots preserved by `retire`.
- Zero unresolved questions/findings within this plan.
- Overlapping edit classifications: factual 1, clarification 19, distractors 11,
  difficulty 1, category 1; explanation/scope/metadata 0.
- The factual edit is 356: Test Track's outdoor speed is real, not simulated.
  Clarifying an ambiguous question does not mean its old keyed answer was false.
- `validate_corpus.py`: 1,973 active questions, zero errors.
- `question_audit.py check`: zero errors; 1,691 active questions remain without
  current source verification. A passing gate does not approve that legacy backlog.
- Active approval: q-002 is 80/214; whole bank is 282/1,973.
- Next request: batch 8, q-002, starting at question 367. The read-only status
  preview did not create a new batch plan.

The closing report is `next-shard-0007-result.json`; per-question evidence is in
`next-shard-0007-reviews/`. Current warning comparisons and their complete option
sets are in `next-shard-0007-comparisons.json`. Retirement snapshots, counterpart
questions, and individual rationales are in `next-shard-0007-retirements/`.

## Evidence and final challenges

Retained questions each record the source locator, evidence basis, rationale for
every option, and Codex's separate challenge of the final wording. Historical
date claims were corroborated; mutable park offerings have a 2027-02-04 recheck.
The Cars sponsor/crash and Ratigan-species records explicitly disclose their
secondary evidence and the limits of unavailable primary extraction. No video
viewing is claimed from a clip title. An indexed Edgar Balthazar merchandise PDF
was not fully retrievable, so 328 was narrowed to the primary-supported Edgar
identification; the old surname is not labeled false.

The new Mission word-overlap warning on 355 was recorded unresolved before the
stem was revised. Its final evidence was renewed and the warning marked fixed
only after it disappeared. The remaining boat classifier warning is accepted
because it does not reveal the distinctive Friendship name and all alternatives
describe watercraft. Duplicate warnings were decided individually; common
years/animals and separate park locations were not automatically treated as dupes.

Retirement source checks supplement the saved full-question comparisons:

| Retired IDs | Evidence locator and challenge |
| --- | --- |
| 303 | [Pixar Toy Story 3](https://www.pixar.com/toy-story-3), Lotso profile identifies the strawberry bear; Big Baby and Ken have separate doll profiles. The name fact is repeated by 1530, whose stem gives the more precise Sunnyside context. No additional bear identity is learned. |
| 307 | [Disney Hercules profiles](https://www.disney.co.jp/fc/hercules), Philoctetes/Phil is the satyr trainer; Zeus is the father, Hades the underworld ruler, Pegasus the winged horse. Question 1259 explicitly gives Phil's training context and asks an additional song fact. |
| 308 | [Pixar Inside Out](https://www.pixar.com/inside-out), Bing Bong profile explicitly identifies Riley's imaginary friend; the three alternative names are not that identity. Question 647 supplies Bing Bong's name in its stem. Comparison does not approve 647's separate composition claim. |
| 324 | [Disney Bambi II](https://movies.disney.com/bambi-2), synopsis and Great Prince profile establish the father/title association, also expressly given in 2101. Other invented royal titles do not create another identity. |
| 327 | [Disney Bambi](https://movies.disney.com/bambi/), character profiles and childhood gallery include Friend Owl, Thumper, Flower, Faline and the Great Prince. The original broad young-fawn wording cannot exclude the other three sets. Intended names also aggregate facts in 751, 218 and 1055. Retirement avoids falsely approving a single-answer claim; 751 is the main replacement pointer, not an assertion it covers all three names. |
| 330 | [D23 Madam Mim](https://d23.com/a-to-z/madam-mim/) identifies the film witch; [D23 snake article](https://d23.com/celebrate-the-year-of-the-snake-with-9-ssssensational-disney-snakes/) describes her duel with Merlin. The complete 2490 stem names both participants, directly supplying 330's answer. The alternatives do not identify that witch. |
| 332 | [D23 Percy](https://d23.com/a-to-z/percy/) identifies Ratcliffe's dog, excluding parrot, cat and ferret. The complete 1120 question explicitly supplies the same pampered-pug association in reverse. This duplicate review does not independently approve its separate breed wording. |
| 335 | [D23 Space Mountain](https://d23.com/a-to-z/space-mountain/), opening sentence explicitly assigns Magic Kingdom Space Mountain to Tomorrowland, excluding the three other land options. The complete 1150 question already states that park/land association. |
| 341 | [D23 Tower of Terror](https://d23.com/a-to-z/twilight-zone-tower-of-terror-the/), original Disney-MGM Studios location; [official current page](https://disneyworld.disney.go.com/attractions/hollywood-studios/twilight-zone-tower-of-terror/) is under Hollywood Studios. Question 609 reverses the same park/attraction link; the other Florida parks are not the stated location. |
| 342 | [D23 Disney Skyliner](https://d23.com/a-to-z/disney-skyliner/), named gondola network and parks/hotels list. The other three invented system names are not the named network. Question 1624 expressly names a Skyliner gondola stop, disclosing the identity. |
| 350 | [D23 Liberty Square](https://d23.com/a-to-z/liberty-square/), explicitly locates Hall of Presidents in Liberty Square rather than the other listed lands. The complete 1355 question supplies the inverse link and adds the presidential figures fact. |
| 362 | [Tokyo resort FAQ address](https://faq-en.tokyodisneyresort.jp/answer/686a27edc1f34019065e0eb9/) is Urayasu, Chiba; [official park site](https://www.tokyodisneyresort.jp/en/tdl/) distinguishes Tokyo Disneyland and Tokyo DisneySea. The original Tokyo-city/singular-park premise is imprecise. The intended name is already supplied by 1368; invented alternatives do not cure the premise. |
| 363 | [Hong Kong Disneyland official site](https://www.hongkongdisneyland.com/) establishes the proper name rather than the three invented alternatives. The complete 2102 question states that name and asks its opening year. |
| 365 | [Aulani official site](https://www.disneyaulani.com/), brochure section gives Aulani, A Disney Resort & Spa in Ko Olina, Hawaii. The three alternative names are not that property's name. Question 1156 already states Disney's Aulani/Oahu association and adds Ko Olina geography. |

The earlier retirement of 276 into 330 retains its original replacement snapshot;
330's later retirement into 2490 preserves that evidence history. No IDs were
reused and no baseline was regenerated.

## Player reports and boundaries

Fresh read-only player report snapshot:
`artifacts/question-audit/batch-7-player-flags.json`. Eleven documents were
returned, with no further page token and no question IDs in this plan. No player
report resolution was written. In particular the earlier 138 report is outside
this batch and was not closed. No production mutation, commit or publication
was performed.

The existing unrelated working-tree changes were retained. This audit's content
changes are confined to its planned questions and preserved retired snapshots.
