# Release Checklist

Before Lumi Social Intelligence is made public or tagged for release, verify each gate.

## Product/documentation gates

- [ ] README presents **Lumi Social Intelligence** as the release doorway.
- [ ] Public-facing docs use **Lumi Layered Memory**, **Nuances**, and **Presence** as product names.
- [ ] Autoresearch is described only as private harness/evidence infrastructure.
- [ ] No OpenClaw adapter, installer, or support claim exists before compatibility research.
- [ ] GitHub About description and topics match the public product story.

## Safety/privacy gates

- [ ] No raw runs, private memories, diaries, or chat logs are tracked.
- [ ] No credentials, tokens, API keys, passwords, connection strings, or chat IDs are tracked.
- [ ] No local runtime state, scheduler internals, cron/job IDs, queues, or wrappers are tracked.
- [ ] No private coordinates or personal identifiers are tracked.

## Verification gates

Run:

```bash
./scripts/release_check.sh
```

The release gate currently checks:

- Python syntax for scripts and tests;
- repository structure tests;
- public/secret scan;
- whitespace/diff hygiene.

## Licensing gates

- [ ] `LICENSE` matches the related Lumi repositories.
- [ ] `LICENSE-DOCS.md` matches the related Lumi repositories.
- [ ] `NOTICE.md` matches the related Lumi repositories.
