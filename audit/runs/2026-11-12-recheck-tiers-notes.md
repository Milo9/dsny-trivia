# Recheck tiers — 2026-11-12 (backlog #5)

Reviewer: Claude. Owner approved tiering, date-anchoring, retiring listing-type
questions and staggering on 2026-11-12.

## Problem

The November 2026 audit gave every changeable fact a 90-day recheck (old rule 7).
220 questions (137 parks, 81 cruise, 2 walt), all reviewed 2026-11-02..12, fell due
together (9 in 2027-01, 211 in 2027-02), and would repeat every 90 days (~880/year).
Most were long-standing names, locations and designs that do not change on that
timescale (e.g. #2222 Rose & Crown's pavilion, #88 Cinderella Castle).

## Policy (QUESTION_AUDIT.md rule 7, now tiered)

- historical: wording anchored to a date ("In November 2026, ...") or a past event.
  No recheck.
- stable: long-standing names, locations, designs. Recheck within 12 months.
- changeable: offerings, schedules, policies, venues with announced changes.
  Recheck within ~90 days.

## How this wave was re-tiered

`question_audit.py reschedule audit/runs/2026-11-12-recheck-reschedule.json`.
Each new date is bounded by the tier interval from the **recorded evidence date**
(the earliest `checkedAt` of the review's sources), not from today. All sources were
inspected 3–10 days earlier, so re-inspecting them only to move a date would add
nothing. No source was re-inspected and no evidence changed; each review gains a
`schedule` record (tier, reason, actor, `sourcesReinspected: false`, previous dates)
and the prior review is kept in history.

Triage used the recorded evidence: notes mentioning announced maintenance,
refurbishment or mutable policy stay changeable. When unsure, the shorter tier was used.

- historical (48): every stem containing "November 2026", plus past events
  #433 (built in Italy), #968 (replaced Beat Street in 2013), #799 and #737
  (debuted on the Wish), #2511 (opened 2017), #2515 (opened 2016).
  #356 stays stable: "opened in 1999" alone does not exclude Journey Into Imagination.
- changeable (6, dates unchanged): #2222 (announced maintenance from 2027-01-11),
  #369 (2026-27 refurbishment), #424/#425 (advertised club ages), #430 (Palo meal
  periods), #916 (uncertain future plans).
- stable (163): staggered by topic so related questions (often sharing sources)
  come due together: Castaway Cay 2027-07, other DCL ships 2027-08, Magic Kingdom
  and international parks 2027-09, other WDW and Disneyland Resort 2027-10.
  About 50 per month, which is one session each.

## Retired without replacement (not worth their upkeep)

These ask about a specific November 2026 listing, not a lasting Disney fact.
Anchoring would keep them correct but stale once the listing changes:

- #2560 Halloween event listing: Minnie/Daisy/Clarabelle's Hocus Pocus costumes.
- #2561 Halloween event listing: name of the costume celebration.
- #2277 Aladdin musical listed for Disney Wish and which other ship (show
  assignments move between ships).

Snapshots are preserved in questions/retired.json (no `replacedBy`).
