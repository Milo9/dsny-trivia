# Sequential audit batch 23

Reviewer: Codex. Date: 2026-11-08. Scope: the saved 50-question plan in
`questions/q-005.json`, #1205 through #1255 (with the pre-existing ID gaps).
Result: **complete-for-scope**.

- Reviewed: 50. Current retained evidence records: 45. Approved: 45.
- Edited retained questions: 23. Retired duplicates: 5. Unresolved: 0.
- Change types overlap: clarification 23, distractors 4, difficulty 1;
  factual, explanation, category, scope and metadata 0.

## Findings and changes

Retirements preserve exact question snapshots and ledger history:
#1206 → #1388 (Sherman brothers/Mary Poppins); #1212 → #977 (Cookie's BBQ and
Family Beach); #1235 → #765 (Lumiere/candelabra); #1239 → #41 (Triton/Ariel's
father); #1245 → #1326 (the named unbirthday tea party).
Full question comparisons and reasons are in `next-shard-0023-comparisons.json`.
The #1245 review was recorded before retirement and is preserved in its ledger history.

Clarifications distinguish Walt's supervision from preliminary involvement, the
Star's lack of an art vacancy from the firing legend, exact ship room categories,
the physical cruise card from bands, and specific musical scenes. Cinderella's
later Dream reprise was removed as a distractor for the dressmaking question.
Ratigan's number is tied to the henchmen and Bartholomew interruption. The Rescuers
anthem now names the delegates without asserting Bernard sang with them.
Spring-a-Leak is distinguished by its storm-damaged design rather than generic
children's water play. #1250 is medium for its specific scene association.

All complete topic digests were read together using the saved combined context.
Additional cross-bank searches supplied missing Alice, Peter Pan, Lady and the
Tramp, Robin Hood, Rescuers and Oliver context. The later search identified the
#1245/#1326 duplication. Fifteen remaining applicable findings received specific,
hash-bound accepted decisions, recorded with comparison snapshots in
`next-shard-0023-finding-decisions.json`.

## Evidence and limits

Explicit final four-option rationales, locators and separate evidence challenges
are in `next-shard-0023-evidence-notes.json` and `next-shard-0023-reviews.json`.
Reusable passages were added to `audit/source-notes.json`. Disney/D23, the Walt
Disney Family Museum, shipbuilder records and institutional catalogs are used
where available. Film scenes rely on secondary transcriptions corroborated by
Disney music/catalog entries; no original-film or video playback is claimed.
The Star application uses Michael Barrier's scholarly biography and its account
of Walt's recollections. Limited indexed PDF/object passages are explicitly
identified in source-note limitations and corroborated elsewhere.

Current cruise venues/services have review dates of 2027-02-05. Attraction identity
does not promise that Pelican Plunge is operating on a particular sailing.

The player-flag export contains two old already-resolved complaints about #1230's
former wording. The current stem names concrete clubs; no production flags were
changed or resolved during this batch.

## Validation and progress

`validate_corpus.py`, audit sync/report and the audit gate passed with zero errors.
The saved close report confirms 50 reviewed, 45 approved, 23 retained edits,
five retirements and zero unresolved questions. The untouched legacy source
backlog remains 921 questions.

Current shard: **181/226 approved**. Whole bank: **954/1,875 approved**.
The next request begins with **#1256**, the final 45-question chunk of q-005.
No app/content publication was requested or performed.
