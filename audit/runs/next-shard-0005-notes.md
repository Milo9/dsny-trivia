# Sequential question audit: batch 5

Reviewer: Codex. Date: 2026-11-06. Fixed scope: 45 IDs from the saved plan,
the final queued questions in `questions/q-001.json`. No additional question
was edited or retired outside that scope.

## Result

Complete for scope: 45 reviewed, 40 current schema-2 evidence records and approvals,
15 retained questions edited, five duplicates retired, zero unresolved.
Nonexclusive change types: factual 2, clarification 14, distractors 6, difficulty 2;
all other change types zero. See the result JSON for hash-bound details.

The factual-premise corrections are #228 (original Maleficent death curse versus
Merryweather's mitigation; now tests the spindle trigger) and #231 (Maximus is a
palace guard horse pursuing Flynn, not Flynn's horse). Other edits do not mean
the previous correct answer was factually wrong. #229's squash distractor also
described a pumpkin; #210's Casa Madrigal could describe the family house.
#249's film title gave away Atlantis. #247 now has parallel proper-name pairs.

Retired only planned IDs: #208 -> #526, #213 -> #576, #242 -> #656,
#244 -> #2179, #248 -> #1252. Exact original snapshots and both comparison
questions are preserved in the retirement artifacts and retired bank.

## Evidence and challenge

Individually saved final-wording reviews include premises, all four option
rationales, evidence bases, HTTPS sources, locators and separate final challenges.
Full topic digests, category context and ranked comparison questions informed
distinctness review; detector similarity was not treated as duplication by itself.
Nine remaining in-scope advisory comparisons received specific accepted decisions.
Existing accepted decisions remained current where content did not change.

Primary evidence principally came from Disney/D23, Pixar, Disney Books,
Disneyland Paris, the Walt Disney Family Museum and licensed Disney publications.
The new D23 Sugar Rush article was read after the book page returned 403; the
review uses the accessible primary article, not the blocked book's search snippet.
Perdita's separate official entry corroborates the exact 15-puppy count and the
film synopsis distinguishes it from 99 rescued puppies and 101 total dogs.

Documented limitations:

- #126: an Ask Dave reply says gloves were added in When the Cat's Away.
  The independently read museum account explicitly distinguishes Opry House's
  stage-costume debut from the following short's permanent design, and D23's
  Opry release history separately identifies that debut. This supports introduction
  under the question's wording; the conflicting reply is preserved in its sources.
- #220: the specific fork utterance uses a secondary dialogue transcription,
  corroborated by a separate character account. No primary film playback claimed.
- #219: the tower action uses Disney's licensed junior novelization hosted by a
  school, corroborated by the official film still gallery identifying the pan.
- #142: official DCL live page was inaccessible. Disney News reproduced in a
  contemporary magazine, an independent 2013 report and a dated 2014 atrium
  photograph support the historically bounded redesign question. No current ship
  configuration claim or firsthand visit is implied.

## Reports and checks

Read-only Firestore export: `artifacts/question-audit/batch-5-player-flags.json`.
Eleven reports returned, no pagination token and no planned question IDs. No
production report decisions were changed. The read was completed after batch
selection; that ordering deviation did not alter the fixed plan.

Structural validation: 1,993 active questions in nine shards, zero errors.
Audit close: complete-for-scope. Release gate remains blocked by the pre-existing
#683 missing current review and its unresolved manual concern. Neither was
expanded into this batch. No commit, push or publication was performed.

Final progress: q-001 is 201/201 active questions approved. Whole bank is
201/1,993 approved, 1,792 remaining. The next request begins batch 6 with 50
questions in q-002; no new plan was created beyond this batch.
