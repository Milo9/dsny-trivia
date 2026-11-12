# Improvement Backlog — holistic audit of 2026-11-11 (v1.50)

Produced by a whole-project audit (code, docs, repo hygiene, question bank, live
Firestore read-only probes), reviewed by an advisor pass. Numbers are stable IDs —
refer to them as "backlog #N". Mark items done here (with commit) as they land.

**Baseline health at audit time:** 48 JS unit tests, 76 Python tests, 10 Firestore
emulator tests, the isolated Chromium browser suite, `validate_corpus.py` (2,195
questions, 0 errors) and `question_audit.py check` (0 unverified) all passed. GitHub
CI green on the last 4 commits; live site serves v1.50; versioned Firestore rules are
deployed (unknown-collection read returns 403).

**Not checked:** real iPhone, the WebKit browser run, live player stats.

**Advisor corrections already applied:** "easy games will repeat" was wrong (423 easy
vs 300-question seen window always leaves ≥123 unseen); all 59 "As of November 2026"
anchors are parks/cruise and are deliberate under QUESTION_AUDIT.md rule 7 (not an
item); new-film clusters are a uniform ~5/film by design. **Any reword of a question
invalidates its ledger approval and needs a fresh four-option source review** —
factor that into every content-edit estimate.

---

## A. Safe cleanup — no decision needed (all done 2026-11-11)

Done: old CLAUDE.md archived to `docs/history/CLAUDE-through-v1.50.md`, new thin
CLAUDE.md; doc/script references repointed; Claude memory refreshed; APP_AUDIT.md
deletion committed; `debug.log` ignored; `artifacts/release-*-t(e)mp` pruned (245→99 MB);
two dead functions removed and two stale app.js comments corrected.

**1. ✅ DONE 2026-11-11 (v1.51) — CLAUDE.md is stale; make it a thin pointer file.** *Medium.*
545 lines / 115 KB, contradicts code: claims no service worker, no npm, open
`allow read, write: if true` rules, "append to q-009, IDs 2579+" (max ID 2995, q-010
current), 2,037 questions (actual 2,195), 2am MDT reset (code: 08:00 UTC), old
monthlyKey/prev model (now `monthlyTotals`), homework rollover "assumed watched"
(now explicit), file map missing bootstrap.js / data-logic.js / sw.js /
firestore.rules / audit tooling. Root cause: the audit agent ("Codex") maintains
AGENTS.md / DEVELOPMENT.md, nobody maintains CLAUDE.md. Fix: ~100-line CLAUDE.md
pointing at the shared docs; move history out; refresh Claude memory files.
Absorbs the doc-sprawl item (CLAUDE.md / AGENTS.md / DEVELOPMENT.md /
QUESTION_AUDIT.md / audit/README.md / EFFICIENT_WORKFLOW.md overlap; DEVELOPMENT.md
accumulating per-release notes).

**2. ✅ DONE 2026-11-11 (v1.51) — Dirty tree blocks the documented deploy path.** *Tiny.*
`APP_AUDIT.md` deletion uncommitted since ~v1.43; `debug.log` untracked (`.gitignore`
has `*-debug.log`, not `debug.log`). `deploy.ps1` does `git add -A`, so v1.44/v1.45
release notes record publishing via hand-picked file lists instead. Fix: commit the
deletion (findings addressed in v1.39), ignore/delete `debug.log`.

**3. ✅ DONE 2026-11-11 (v1.51) — Local `artifacts/` is 245 MB.** *Tiny.*
Mostly `release-*-tmp` / `release-*-temp` full site copies. Prune only those —
`artifacts/question-audit/` is read by `question_audit.py next`.

**4. ✅ DONE 2026-11-11 (v1.51) — Dead code.** *Tiny.*
`pickFromMoviePool` (app.js:312) and `upsertWatched` (app.js:912) are never called
(also not from scripts/ or test/).

## B. Needs owner OK / decision

**5. 220 scheduled rechecks fall due Jan–Feb 2027** (221 at audit; #976 retired in v1.52). *Large if done properly.*
`nextReviewAt`: 9 in 2027-01 (first 2027-01-08), 212 in 2027-02 — mostly parks/cruise
time-anchored facts. Once one is overdue, `question_audit.py check` fails, blocking
`deploy.ps1` and CI. Plan December recheck batches (or consciously re-date — not
recommended, it games the gate).

**6. ✅ DONE 2026-11-12 (v1.52) — Close the 6 open player flags + fix the answer-in-question pattern.**
Done: 10 rewords + #976 retired (audit/runs/release-1.52-flag-followup-notes.md); #138
left as is (Magic-class wording verified); flags closed in Firestore after publish
(see notes). Original item: *Small (flags) / Medium (rewords).*
Firestore flags on #911 (x2), #2432, #2080, #708, #138 have no `resolutions` records —
content was already reworded/retired but flags were never closed (production write,
needs OK; do it via review.html). Still worth a look: #2432's distractors
(B227/C118/T809) remain obviously fake; #138's reword may not settle "plays both
songs." Answer-in-question is the most-flagged complaint, and ~10 approved questions
still do it: #1355 (presidents → The Hall of Presidents — same shape as retired #911,
flagged twice in a day), #2243 (Frozen-themed → Frozen Kingdom), #2642 (Pixar Pier →
Pixar Promenade), #1236 (Mickey silhouettes → Hidden Mickeys), #976 (cruise ships →
Disney Cruise Line Navigator), #427 (Castaway Cay → Castaway Cay 5K), #2589
(Elemental → Element City), #518 (Oliver & Company → Oliver Twist), #521 (Treasure
Planet → Treasure Island), #925 (riverboat). Source: `find_leaks.py --tier2`.

**7. ✅ DONE 2026-11-12 (v1.52) — 144 MB of audit records tracked in git and publicly served on GitHub Pages.**
Done: `_config.yml` Jekyll `exclude` keeps audit/, docs/, scripts/, test/, *.md off
Pages (no settings change). Still public in the GitHub repo by design. Original item: *Medium.*
`audit/ledger.json` (28 MB, +~0.7 MB/release) is public at
`/dsny-trivia/audit/ledger.json`; each `audit/runs/*-result.json` embeds a ~1.4 MB
whole-bank `report`. Git pack is only 3 MB (compresses well) — this is Pages/checkout
weight and public exposure, not history size. Safest fix: exclude `audit/` from what
Pages publishes (Actions-based Pages deploy uploading only app files). Stripping
`report` blobs is technically safe (queue reads only status/plan/scopeHashes/removedIds)
but audit policy treats run records as history — leave them.

## C. Content direction — owner's call

**8. ✅ CLOSED 2026-11-12 — owner decision: fine as is.** The app is now a general
Disney trivia app (still used for cruise prep, but also for fun), so no rebalancing
toward cruise. Original item: Category mix drifting from cruise prep. Last 340 added: movies 217, characters
60, music 31, pixar 22, parks 5, cruise 5, walt 0. Totals: movies 661, characters 402,
pixar 315, parks 276, music 217, walt 170, cruise 154 (smallest). Audit retirements
also shrank parks (306→276), walt (207→170), cruise (167→154). Suggest next
generation round targets cruise/parks/walt.

**9. Thin easy coverage in some categories + suspect easy labels.** Easy by category:
walt 12, cruise 32, music 37, parks 44, characters 84, pixar 89, movies 125. Some new
"easy" labels look wrong (#2836 Kurt Russell in a 1969 film; #2846 Jodie Foster,
Freaky Friday 1976). Use admin difficulty hints once attempts accrue; target easy in
the thin categories.

**10. Formulaic cast questions.** ~31 "Who voices X in the original English-language
Y (year)?" + ~35 "Who plays X in Y (year)?", many on obscure 1960s–70s live-action
films. Decide if that's the desired flavor; if not, stop generating more rather than
retiring approved ones.

**11. Explanations/sources shown on only 347 of 2,195 questions.** Ledger holds
evidence for all; backfilling `explanation`/`source` is feasible. *Medium.*

## D. Verify before changing

**12. ✅ DONE 2026-11-12 (v1.53) — Offline fallback likely fails on stalled (not dead) wifi.**
Confirmed: with the old sw.js a stalled reload hung >30 s. Now 4 s network wait then cache
(300 ms while stalled); stalled-wifi browser test added; also fixed a boot race where
the practice button opened settings and boot sent it back home. Original item: `sw.js` is
network-first with no timeout. `fetchWithTimeout` (app.js ~1799) aborts at 10 s, which
probably surfaces the load error before the SW cache fallback runs. Browser tests only
cover an unavailable origin. Verify with a throttled/stalled connection; fix by racing
network vs ~4 s then cache in sw.js. *Small–Medium; most cruise-relevant item.*

**13. ✅ DONE 2026-11-12 (v1.53) — Firebase SDK mismatch.** Emulator tests now use
`firebase-cdn` (npm:firebase@10.12.0) and assert it matches the CDN URLs. Original item: Production CDN 10.12.0 (bootstrap.js, review.html);
emulator tests use firebase 13.1.0; browser tests stub the CDN. Production SDK path
never exercised. Prefer pinning the dev dependency to 10.12 over bumping production
before the cruise. *Small.*

**14. ✅ DONE 2026-11-12 (v1.53) — Home screen at 375×667: player list below the fold.**
Hero tightens under 760 px tall; browser check asserts both players are above the fold.
Original item: Belle hero card fills the
first viewport; "Who's playing?" sits at the bottom edge, Cara is off-screen. Confirm
on a real phone; shrink hero on small heights. Only 2 of 19 screenshots were viewed —
a fuller visual pass may find more. *Small.*
