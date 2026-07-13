# Release Boundary

Lumi Social Intelligence is the public-facing release doorway for tested, curated updates from private development repositories.

## Private development repositories

Development happens in:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**
- **Autoresearch**

## Public release repository

Versioned releases are promoted into:

- **Lumi Social Intelligence**

Promotion should happen only when the update is tested, documented, reviewed, and safe for public-facing distribution.

## Product naming rule

Public-facing documentation should refer to the product components by their product names:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**

Avoid reducing the public story to internal folder names, module nicknames, or private harness language.

## Do not include

This repository must not contain:

- raw Autoresearch runs;
- private memories or diaries;
- chat logs;
- credentials, tokens, API keys, passwords, connection strings, or chat IDs;
- local runtime state;
- scheduler internals, cron/job IDs, queues, or wrappers;
- private coordinates or personal identifiers;
- unreviewed generated artifacts;
- host-specific claims that have not been verified.

## Release gate

Every release should pass:

```bash
./scripts/release_check.sh
```

Before publication, also run a clean-checkout smoke test from the release archive.

## Visibility rule

The repository stays private until:

- licensing is in place;
- public docs are product-consistent;
- release gates pass;
- secret/privacy scans pass;
- install artifacts are reviewed;
- host compatibility claims are verified;
- GitHub About metadata matches the public product story.
