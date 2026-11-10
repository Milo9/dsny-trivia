# Release v1.50

Prepared November 10, 2026. This release publishes [generation round 4](generation-0004-notes.md), adding 100 source-reviewed questions on 16 live-action Disney films, two Pixar films, Disneyland Paris and Disney Adventure.

The bank contains 2,195 active questions, all approved, and 185 preserved retired snapshots. The 2,095 existing questions were preserved. The ten-shard manifest now loads 220 questions from q-010. Versioned assets and the offline cache use v1.50 so installed clients can refresh the bank.

The release dry run passed corpus validation, the question audit gate, 48 JavaScript tests, 76 Python tests, the isolated Chromium and WebKit suites (including offline practice), and 10 demo Firestore emulator tests. The unrelated APP_AUDIT.md deletion and debug.log are outside this release.
