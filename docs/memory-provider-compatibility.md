# Memory Provider Compatibility

Lumi Social Intelligence is not a competing memory backend. It is a higher social-intelligence layer that can run above an agent host's chosen memory provider.

The user should be able to keep their existing memory system — including file-backed systems such as Obsidian vaults, Hermes memory providers, or future host-specific stores — while adding Lumi's review, nuance, and presence gates around how remembered context is interpreted and acted on.

Short promise:

```text
Keep your memory. Add social intelligence.
```

## Layer boundary

```text
Host memory provider / vault / notes / memory API
        |
        | explicit read adapter
        v
Lumi Layered Memory compatibility view
        |
        v
Nuances appraisal
        |
        v
Presence initiative gate
        |
        | explicit proposal / receipt / reviewed write adapter
        v
Host review surface or memory provider, only when allowed
```

The underlying memory provider remains authoritative for storage, retrieval, deletion, and user-visible source material.

Lumi may:

- read selected context through a host adapter;
- cite where context came from;
- normalize context into a temporary compatibility view;
- appraise ambiguity, consent, emotional weight, corrections, and timing;
- decide whether to speak, wait, ask, repair, or stay quiet;
- create reviewable proposals or receipts;
- write only through explicit host-approved interfaces.

Lumi must not:

- silently rewrite another memory provider's files, notes, database rows, or canonical records;
- assume ownership of an Obsidian vault or Hermes memory provider internals;
- bypass the user's primary memory configuration;
- turn inferred patterns into durable facts without review;
- hide provenance from the user or host;
- promote runtime/social observations into public release material.

## Adapter contract

A memory-provider adapter has four narrow responsibilities.

| Responsibility | Required behavior |
|---|---|
| Read | Fetch selected context without mutating the provider. |
| Provenance | Preserve source type, location, timestamp when available, and confidence. |
| Proposal | Express any desired write as a reviewable proposal, not an automatic mutation. |
| Receipt | Record what was considered, what was decided, and whether anything was written. |

Adapters should be thin. The adapter translates between the host and Lumi; it should not become an invisible second memory system.

## Read policy

Reads are allowed when all of the following are true:

1. The host or user has made the source available to the adapter.
2. The adapter can preserve enough provenance for review.
3. The context is relevant to the current task or configured Lumi review surface.
4. The read does not broaden into unrelated private material.

For Obsidian-like systems, the safest first implementation is read-only vault access to explicitly configured folders, tags, or exported review bundles.

## Write policy

The default write mode is **no write**.

Allowed write levels:

| Level | Meaning | Example |
|---|---|---|
| `none` | No provider writes. Lumi only reads and reasons. | Default preview mode. |
| `proposal` | Lumi writes a review card outside canonical memory. | A suggested note update in a review folder. |
| `receipt` | Lumi records its own decision trace without altering source memory. | “Used note X; chose not to act.” |
| `reviewed-write` | A host/user-approved operation updates memory through the provider's public interface. | User accepts a proposed preference update. |

Disallowed in the public preview:

- direct silent edits to Obsidian notes;
- direct silent edits to Hermes durable memory files;
- hidden background consolidation of personal facts;
- inferred preference writes without a review trail.

## Conflict matrix

| Scenario | Expected behavior |
|---|---|
| Obsidian is the main memory store | Obsidian remains authoritative; Lumi reads configured context and creates proposals/receipts only. |
| Hermes built-in memory is active | Hermes memory remains authoritative; Lumi uses adapter boundaries and does not bypass memory tools. |
| Multiple memory providers disagree | Lumi preserves ambiguity, cites both sources, and asks or stays quiet instead of flattening conflict. |
| User deletes or corrects memory in the provider | Provider correction wins; Lumi must not resurrect stale facts from receipts. |
| Lumi detects a possible new durable preference | Create a review proposal; do not silently write. |
| Host denies write permission | Fail closed and keep a receipt/proposal only if the configured mode permits it. |
| Source provenance is missing | Treat context as low confidence; do not promote to durable memory. |
| Public release export runs | Exclude vault content, private memory, runtime state, logs, and raw evidence. |

## Main-memory-authoritative invariant

Compatibility tests should enforce this invariant:

```text
A Lumi compatibility run must not change the canonical memory provider unless the test explicitly enables a reviewed write path.
```

Minimum verification:

- read-only adapters do not mutate source fixtures;
- proposed writes are represented as proposals, not source edits;
- receipts are separate from provider data;
- conflict cases preserve both sides and do not invent a merged fact;
- release scans reject private memory/vault/runtime material.

## First release stance

For Lumi for Hermes 0.1.0, memory-provider compatibility should ship as a documented and tested boundary before deep provider-specific automation.

That means:

- read-only by default;
- proposal/receipt surfaces before live writes;
- explicit adapter modes;
- Obsidian coexistence documented but not overclaimed;
- no OpenClaw adapter until compatibility is researched.
