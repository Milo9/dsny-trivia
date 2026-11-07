# Batch 6 content audit — 2026-11-06

Reviewer: Codex. Fixed scope: the 50 saved plan IDs (251–302 with gaps) in
`questions/q-002.json`. Result: **complete-for-scope**.

- Reviewed: 50, including documented duplicate comparisons for six retirements.
- Current four-option evidence recorded / source verified / approved: 44 / 44 / 44.
- Retained questions edited: 27. Retired duplicates: 6. Unresolved: 0.
- Edit types overlap: factual 3; clarification 25; distractors 10; difficulty 7;
  explanation/category/scope/metadata 0 each. Edited is not a factual-error count.

## Material findings

- **252:** Eli La Bouff and Big Daddy are the same person. Replaced the alias
  distractor with a different character and removed the shared-surname clue.
- **258:** Wendy offers a kiss and Tinker Bell interrupts; the question formerly
  described a completed gift and conflated the film with the thimble exchange.
  The final question names the nursery offer in the 1953 film.
- **263:** The screenplay reveals both Linguini's paternity and his restaurant
  ownership. The former broad secret question admitted both. The final question
  asks only who his biological father is.
- **291/292/300:** Clarified pre-exile playmate, Sulley's chosen nickname, and
  Disney's young human Pooh companion to exclude alternate literal readings.
- Specified film versions where remakes alter context, including the non-speaking
  dwarf and Scuttle's species. Revised animal-made dress context, nickname options,
  full-name options, and editorial difficulty where needed.

Retired, with exact snapshots retained through the supported `retire` command:
259 → 537 (Silver mentor identity), 261 → 279 (Sven/reindeer inverse),
265 → 1339 (Merryweather's curse mitigation), 269 → 514 (Dukas segment),
276 → 330 (Madam Mim inverse), 299 → 1458 (Kaa/python).

273 remains distinct from 1123: all four final answers share Professor/Porter,
so knowing the usual title/surname cannot identify the full first name and initial.
The Disney licensing handbook's discussion of film production supports that name.

## Evidence and limitations

Read all selected stems and options, topic digests, fallback category context,
ranked comparisons, and additional cross-bank matches. Source locators and specific
option challenges are preserved in `next-shard-0006-reviews/`; comparison snapshots
and reasons are in `next-shard-0006-comparisons.json` and the retirement directory.
The serialization helpers record the review; they do not perform research.

Most evidence is Disney/Pixar/D23 character material. The Ratatouille, Monsters,
Inc., and Zootopia studio screenplays were read through external hosts; the Tarzan
film-background material is a Disney Theatrical licensing handbook hosted by MTI.
Peter Pan's sequence combines an official quote with a third-party transcription.
Sleeping Beauty's exact narrated region uses two external transcriptions.
Big Hero 6's reveal uses a dialogue transcription and a separate plot account.
These are documented limitations; no direct viewing of original film scenes or
authenticated production scripts is claimed for the latter three reviews.
Oliver's secondary account corroborates the creditor/debtor/guard-dog roles.
The Frog official indexed character profiles are fuller than live page extraction;
the secondary cast account corroborates the family and alias relationships.

Player reports were fetched read-only to
`artifacts/question-audit/batch-6-player-flags.json`: 11 reports, no pagination token,
none for a planned ID. No production report was resolved or modified.

## Validation and progress

Structural validation passed: 1,987 active questions in nine shards, zero errors.
Supported bulk recording validated 44 final question hashes, snapshots and options.
The complete-for-scope close passed with no unclassified edits, undocumented
retirements, or unresolved questions/findings in this batch.

Current shard: 44/228 active questions approved, 184 remaining; six planned
questions retired. Whole bank: 245/1,987 approved (12.3%), 1,742 remaining.
The next request starts batch 7 in q-002, beginning at question 303. Preview only;
no next-batch plan was created.

The broader audit gate still fails on the pre-existing changed question 683 and
manual concern `manual-f3d837f37c46dfc67ab1` (two gate errors). This batch does not
resolve that separate release blocker. No commit, push, deployment or publication.
