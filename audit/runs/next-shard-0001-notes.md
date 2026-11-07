# Sequential question audit: batch 1

Reviewer: Codex. Review date: 2026-11-02 UTC (the owner's local session is November 1).

Post-pass evidence challenge (2026-11-02 UTC): the initial complete close was superseded by a partial report. Questions 7 and 10 were reopened because their cited sources establish the correct answer but their recorded rationales do not independently exclude potentially compatible distractor claims. These are evidence-quality concerns, not newly established factual errors. At that point, queue completion was 44/241 in this shard and 44/2,033 bank-wide; 46 retained reviews remained structurally recorded, but two had unresolved manual concerns. The subsequent tooling update below adds three candidate comparisons to the same fixed batch.

Subsequent tooling update (2026-11-02 UTC): reciprocal answer/stem detection adds three advisory comparisons: #4/#941, #27/#1511 and #45/#939. These are candidates, not confirmed duplicates; no disposition was inferred. Current completed approval is 41/241 in this shard and 41/2,033 bank-wide. There are 46 current evidence records, 44 without an open manual evidence concern, and five questions awaiting approval (#4, #7, #10, #27, #45). All 46 records retain their legacy evidence standard; no new premise/challenge attestations were invented. The four existing retirement decisions have been documented using `record-retirement`, without changing their preserved snapshots.

Fixed scope: the 50 IDs 1-50 in the saved `next-shard-0001-plan.json`, all originally in `questions/q-001.json`. Related questions were read to resolve duplicate candidates; their inclusion did not expand this batch. No deployment, production flag decisions, or runtime/storage changes were made.

## Outcome

50 questions reviewed, 46 retained with recorded four-option reviews, 16 retained questions edited, four retired. The initial close reported zero unresolved concerns; the post-pass evidence challenge above reopens two. Each retained question has an individual final-content review in `next-shard-0001-reviews/`. The retirement reviews preserve the rejected editorial decision and option evidence separately; they are not passing manual attestations.

The factual/editorial corrections include:

| IDs | Decision |
| --- | --- |
| 1 | Specify the 1950 gown's creation scene; silver is correct there. Blue is its later moonlit appearance. Replace the unrelated release-date explanation and change easy to medium for this less familiar scene detail. |
| 11 | Replace the unrelated animal-friends explanation with the lost glass slipper and midnight departure. |
| 15 | Specify the animated 1989 Ariel. Inspect an official Disney film still and corroborate the sea-green tail in the character reference. |
| 20 | Ask which object identifies the fairest person, rather than broadly asking what the Queen consults. Remove the magical/magic answer echo. |
| 22 | Specify Maui's opening theft from Te Fiti, distinguishing it from later boat events. |
| 26 | Specify animated Mulan (1998). Replace generic/external dragon-name distractors with Cri-Kee, Shang and Ping, whose roles are documented in Disney's synopsis. |
| 27 | Specify the main villain and replace Lawrence, who is also an antagonist. Use villains from other films and an explanation of Facilier's actual role. |
| 32, 33 | Specify the Disney film/year to distinguish the 1996 Frollo from the novel and the fictional 1995 romance from history or the sequel. |
| 37 | Correct the false family-mausoleum premise. Ask whose tomb Miguel enters, which is Ernesto's, without conflating location with the guitar's original ownership or Miguel's mistaken ancestry. |
| 39 | Restrict the no-gift comparison to the four named Madrigals. The prior only-family-member claim excluded in-laws incorrectly. |
| 46, 47 | Replace weak unrelated/invented names with actual characters whose roles/allegiances are documented. #46 changes from hard to medium. |
| 48, 50 | Change hard to medium for straightforward character identification. |
| 49 | Ask for the loyal mouse friend instead of exclusively attributing flight encouragement. Use three other Disney-film mice as distractors; shorten the correct name to Timothy to remove a new asymmetric Mouse echo. Change hard to medium. |

## Retirements

Original objects, including their original answers and metadata, were copied intact to `questions/retired.json`, with only `replacedBy` added. No ID is reused. Existing ledger entries, evidence and decision history remain.

| Retired | Retained | Reason |
| --- | --- | --- |
| 9 | 58 | Maleficent/ Sleeping Beauty identification is the same fact in reverse. |
| 16 | 543 | Elsa's ice-and-snow power is asked twice. The retained question has concise parallel power options. |
| 21 | 700 | The transformation spell and the Fairy Godmother's magic-word song both target Bibbidi-Bobbidi-Boo. Keep the music-category question with other real song titles as distractors. |
| 25 | 765 | Lumiere's enchanted form is the same fact in reverse. The retained question uses the more precise candelabra rather than candlestick. |

## Sources and limitations

Read Disney Movies character profiles and scene captions, D23's Disney A to Z entries, Disney Princess's archival storybook gallery, Pixar's individual character profiles, the Coco Academy screenplay, and AFI's Fantasia catalog entry. Locators and individual reasons for the correct answer and all three distractors are stored with each review. These are source-based editorial judgments, not results inferred from structural checks or pre-existing source metadata.

Key evidence:

- [Disney restoration interview](https://d23.com/as-brilliant-as-ever-the-restoration-of-cinderella/), Silver Meddle: Eric Goldberg distinguishes silver at transformation from blue in moonlight.
- [Coco original screenplay](https://www.dicacademy.com/_files/ugd/7a859e_f9530329bda9418f8dc451fcf5cede61.pdf), printed pages 28-30: de la Cruz's mausoleum, portrait, crypt and guitar removal. The Academy script is hosted by a third-party academy; no generic movie homepage was substituted for this scene evidence.
- [Encanto character profiles](https://d23.com/meet-the-characters-of-encanto/): Mirabel's lack of gift and the distinct powers of Luisa, Isabela and Julieta.
- [Computer Graphics World creator interview](https://web.engr.oregonstate.edu/~mjb/cs557/moana.pdf), printed page 9: Maui stole the jade-like heart. Corroborated by Disney Princess's return-the-heart scene captions. This is a 2016 creator interview, not evidence borrowed from the 2026 remake.
- [Disney Princess Jasmine](https://princess.disney.com/jasmine), Aladdin synopsis: three wishes. Independently compared with the Genie introduction in the [Aladdin transcript](https://imsdb.com/scripts/Aladdin.html). The transcript host is unofficial; that limitation is recorded.
- [AFI Fantasia entry](https://catalog.afi.com/Film/27633-FANTASIA?cp=1&pos=2&sid=c5193785-56fd-4d16-90b9-0410b9dfa091&sr=2.8317978) and [Disney A to Z](https://d23.com/a-to-z/fantasia-film/): the original 1940 premiere, distinct from development beginning in 1937 or later reissues.
- [Official Ariel film still](https://lumiere-a.akamaihd.net/v1/images/gallery_princess_ariel_1_bc7355f9_b75f8a55.jpeg?region=3%2C0%2C2175%2C1223), reached from the first Ariel Photos item at Disney Princess, was downloaded and visually inspected. The visible tail is teal-green below lavender shells, with red hair. [Secondary character text](https://en.wikipedia.org/wiki/Ariel_(The_Little_Mermaid)#Development) explicitly corroborates sea-green. No unseen film documentary is claimed as evidence.

All retained facts concern fixed film content or historical releases; they have `timeSensitive: false` and no scheduled recheck. An edit or a new concern still invalidates the applicable approval through the content hashes.

## Distinctness, scope and player reports

Read the full matching topic digests across all nine shards, with correct answers shown, in these groups: Cinderella/Lion King/Little Mermaid/Bambi/Aladdin/Pinocchio/Toy Story/Sleeping Beauty/Dumbo (280 matches); Frozen/Beauty and the Beast/Tangled/Moana/Encanto (178); Nemo/Mulan/Princess and the Frog/WALL-E/Tarzan/Brave (124); Ratatouille/Hercules/Coco/Up (145); Hunchback/Pocahontas/Lilo & Stitch/Jungle Book/Fantasia/Great Mouse Detective/Black Cauldron/Aristocats/Emperor's New Groove (164); Snow White/Queen/mirror (24). Candidate pairs and retained replacements were then read as full four-option objects from the shards. Shared-answer detector candidates were evaluated in addition to the semantic digest review.

Sharing a color, year or number was rejected as a duplicate criterion. Father/mother, villain/hero, bird/explorer and different robot-name expansions are different facts. Same identity/form/power pairs were retired. Knowing an original-film character does not establish a new sequel event, casting fact, song title or later coronation. Specific decisions are retained in the ledger. Related-question concerns, including any questionable dates or TV-scope claims encountered in digests, remain outside this batch and are not implicitly approved.

A read-only Firestore flags query returned 11 reports with no next page. None concerned IDs 1-50. Four other-bank reports remained unresolved (138, 708, 2080, 2432); seven had existing legacy resolved markers. No report or resolution was changed. The private response is under ignored `artifacts/`, not the versioned audit notes.

All eight retained Pixar-film questions remain in `pixar`; other questions in this scope concern Disney films. No question was added, and no sequel/short/TV coverage was expanded. The four retirements preserve historical-game recovery snapshots.

## Validation and continuation

After each question mutation/retirement, `sync` reran structural validation and `report` refreshed detector findings. Final reviews use the final hashes; the new #49 leak was recorded unresolved and then fixed. Before the post-pass challenge, structural validation of 2,033 active questions, the audit gate, all 30 existing audit/queue unit tests, and `git diff --check` passed. Those checks establish record/structure consistency, not source sufficiency. The saved `next-shard-0001-result.json` is now partial because of the two evidence concerns described above. The other 566 advisory findings remain in the unaudited backlog.

Current continuation: resume the evidence concerns on #7/#10 and duplicate comparisons involving #4/#27/#45 within batch 1. Once all are decided and the report closes again, the next batch is questions 51-100 in `questions/q-001.json`. Current completed approval is 41/241 in this shard (200 remain) and 41/2,033 bank-wide (1,992 remain). Four retired questions have preserved snapshots and recorded duplicate decisions.

The final content-hash-bound edit classifications record two factual corrections
(#37's location and #39's overbroad family assertion), 12 clarifications, six
distractor changes, three explanation changes, five difficulty changes and three
metadata changes. Types overlap; there were 16 edited retained questions, not 16
established factual errors. All 66 Python tests pass after the tooling changes.
The current content gate intentionally remains blocked by the two manual evidence
concerns and the new comparison involving edited #27. The other two comparisons
also block batch approval, even though their questions are untouched baseline
content. Previous saved result contents are preserved in the result-history folder.
