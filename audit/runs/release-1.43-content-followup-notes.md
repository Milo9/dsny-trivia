# v1.43 content release follow-up

Owner requested publication after the completed audit on 2026-11-07. This separate
two-question plan preserves batch 13's fixed scope and result.

Codex researched and challenged all four final options for both release blockers:

- #1374 now asks which park ABC helped finance in 1954. Removed the false color
  television premise and the real-series identity question; choices are four parks.
- #1492 now identifies the company incorporated in Kansas City in spring 1922,
  corroborated by the Walt Disney Family Museum and the studio preservation group.
  Earlier 1921 animation work is a different event.

Both concerns are marked fixed with renewed schema-2 reviews and final-content
classifications. The Disneyland shared-answer warning with #381 was individually
accepted: financing and a lifetime park opening are independent historical facts.
The follow-up result is complete-for-scope: two reviewed, evidence-recorded and
approved; two edited; none retired or unresolved. The bank now has 515 approved
active questions out of 1,920, with 1,405 remaining in the disclosed legacy backlog.
The audit gate passes with zero errors.

Release preparation synchronized v1.43 across the app, page, bootstrap, review page
and service-worker cache. Development documentation now reflects current active,
retired and explanation counts. No player accounts or passwords were introduced.

An isolated Chromium regression initially exposed a stale test fixture: question
#21 had been retired, so filtering the active pool by that ID left no questions.
The test now selects an actual active explanation/source question and explicitly
fails if none exists. No production behavior was changed for this fixture fix.
The network sandbox then blocked external resources; the required full dry run was
rerun outside that sandbox. Browser suites operate on isolated local copies and
Firestore tests explicitly target the demo-disney-trivia emulator.

The release includes accumulated content audits and their supporting queue/tooling
records. Unrelated APP_AUDIT.md deletion, .claude local configuration and debug.log
are excluded from staging. Production Firestore rules are unchanged.

The final `deploy.ps1 -DryRun -IncludeUntracked` passed: 48 JavaScript tests,
76 Python tests, 10 demo Firestore emulator tests, structural/content gates, and
the complete Chromium and WebKit browser suites including actual cached reload.
Home, settings, game, answered-game, results and daily-review screenshots were
visually inspected. The dry run performed no staging, commit or push.
