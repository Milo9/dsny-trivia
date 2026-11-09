# Batch 27 content audit

Reviewer: Codex. Date: 2026-11-08. Status: complete-for-scope.

Fixed scope: the 50 IDs in `next-shard-0027-plan.json`, in
`questions/q-006.json` (#1435 through #1537, with manifest-order gaps).
Read the complete deduplicated topic catalogs (1,499 context questions, all four
options) and searched additional cross-shard film/character/answer terms. Context
questions did not expand the planned scope.

## Result

- Reviewed: 50, including three duplicate comparisons resulting in retirement.
- Current four-option evidence recorded: 47 retained questions.
- Approved: 47. Edited retained questions: 32. Retired: 3. Unresolved: 0.
- Change classifications overlap: factual 13, clarification 31, distractors 13,
  difficulty 3; explanation, category, scope and metadata 0 each.
- Shard progress: 147/243 approved. Bank progress: 1,142/1,868 approved;
  726 active questions remain without current source verification.
- The next request starts batch 28 in q-006, at #1538.

## Findings and decisions

Factual repairs include Luca's cycling event (not Vespa racing), Alberto's Roman
tower (not a lighthouse), Denahi's belief that Kenai was killed, Kenai's temporary
human restoration before his final choice, Shere Khan's additional fear of guns,
Bolt's changing beliefs and previously ambiguous alternatives, the captured
transport in Rise of the Resistance, Walt's post-armistice service in France,
Roy's pre-existing leadership, unsupported Walt-coined terminology, ungifted
Madrigal in-laws, the Dos Oruguitas flashback, and the Lookout Cay destination name.
These include premise/context problems, not just incorrect answer keys.

Disney's own 2013 Kaa profile inconsistently calls him both a python and a boa.
The final question asks the uncontested broad animal type, with four different
reptiles as options. This is classified as clarification/distractors, not proof
that every original python description was false.

Retirements, with preserved final snapshots, original batch snapshots and
replacement comparisons:

- #1477 -> #345: recognizing Fantasmic from Mickey battling villains is the same
  show-name fact; the park variation did not require a new fact to answer it.
- #1481 -> #104: Toy Story Land / Slinky Dog Dash association in reverse.
- #1484 -> #890: Harambe / Kilimanjaro Safaris association in reverse.

The Prince John / Mayor Lionheart shared lion answer is independent character
knowledge. The Brother Bear title echo does not establish Kenai's final choice.
Bolt's fictional in-universe show is acceptable theatrical-film context and does
not ask real television-show trivia. These three remaining applicable findings
were explicitly accepted after final-wording evidence review.

Removed the Dr. Facilier giveaway from #1511 so the song-film attribution requires
new knowledge beyond the existing villain-name question. Isolated the historical
Audio-Animatronics debut in #1475 from the separate singing-birds attraction fact.
Other retained edits improve mobile wording, parallel choices, and historical or
scene context. Current park/cruise offerings have November 2026 wording and a
2027-02-05 source recheck where applicable.

## Evidence and validation

`next-shard-0027-reviewed-notes.json` contains the explicit per-option rationales,
premise assessments, contexts and separate Codex challenges. The corresponding
`next-shard-0027-reviews.json` contains all 47 expanded reviews; four supplementary
renewals add track metadata and more precise source locators. Source passages and
access limitations are in `audit/source-notes.json` and embedded in the reviews.
Primary institutional, award and creator sources were preferred; detailed
secondary plot/dialogue accounts and corroboration are identified where needed.
No original film, audio or video playback is claimed.

Structural validation and the audit gate passed with zero errors after final
question changes. Sync/report were refreshed, applicable warnings were decided,
32 retained edits classified, and the saved result closed successfully. The 113
remaining open findings are outside this completed batch; the legacy evidence
backlog is explicitly disclosed by the gate.

Changes are local. No commit, push, release or deployment was requested or made.
