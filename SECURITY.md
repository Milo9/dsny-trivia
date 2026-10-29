# Password-free access

The owner explicitly chose to keep player selection without accounts or passwords.
The versioned Firestore rules validate documents, deny unknown collections, protect
published daily snapshots and game receipts from replacement, and prevent deleting
players or reset backups. They do not authenticate players or administrators.
Someone with the public app configuration can still submit valid-looking scores,
read player data, reset stats, and manage flags. A hidden review URL is not access control.

Rules in this checkout have no effect until deployed. Check the Firebase console's
Rules tab for the currently deployed policy. No authenticated Firebase session was
used during this work; production deployment is separate:

```
npm ci
npx firebase login
npx firebase deploy --only firestore:rules --project disneytrivia-38ac6
```

Deploy the updated app together with these rules. Old app versions cannot create
new ID-only daily pins under this policy; existing ID-only pins can be upgraded
once, preserving their IDs. Published snapshots remain immutable.

Run emulator checks against a demo project, never the production project:

```
npm run test:emulator
```

The admin page downloads a data backup, and each score reset keeps an immutable
pre-reset snapshot. Undo reset restores the snapshot and increments the player's
reset revision, invalidating unfinished games from before the restore. Downloaded
backup restore intentionally restores player stats only; daily pins and flags stay
unchanged. Full exports include daily snapshots, flags, homework and game receipts
for archival use. Keep backups private.
