# Lumi Social Intelligence

**Memory, nuance, and presence for AI agents.**

Lumi Social Intelligence is the public-facing release doorway for three cooperating products:

```text
Lumi Layered Memory -> Nuances -> Presence
```

It gives agent runtimes a social-intelligence layer: adaptive memory, nuance, and presence with review, consent, and repair.

> **Status:** private playground. This repository is being shaped before public release. Do not treat it as install-ready yet.

## Why it exists

Modern assistants do not only need more context. They need better judgment about what context means, when it should matter, and whether acting on it would be helpful, invasive, unsafe, or just socially clumsy.

Lumi Social Intelligence is built around a simple promise:

> Agents that remember carefully, read the room better, and know when not to act.

## The product layer

| Product | Role | Public promise |
|---|---|---|
| **Lumi Layered Memory** | Context and continuity | Useful continuity. Clean boundaries. Receipts. No silent rewrites. |
| **Nuances** | Contextual appraisal | Notice lightly. Invite clearly. Repair quickly. Leave room. |
| **Presence** | Governed initiative | Soft presence. Clean boundaries. Quick repair. No stealing the feeling. |

### Lumi Layered Memory

Lumi Layered Memory gives an assistant inspectable continuity: durable facts, preferences, project context, and memory receipts without silent identity rewrites or hidden behavioral drift.

### Nuances

Nuances reads the moment around the memory: corrections, consent signals, tone, uncertainty, emotional weight, context shifts, and whether an observation should become a durable adaptation at all.

### Presence

Presence decides what the assistant should do with that understanding: speak, wait, ask, act, repair, or hold silence. Presence is where restraint becomes a feature, not a missing capability.

## Repository role

This repository is the curated release surface for Lumi Social Intelligence.

Development happens in private repositories:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**
- **Autoresearch**

Tested, reviewed, public-safe updates are promoted here as release candidates. This keeps the public doorway clean while the private workshop can stay messy, experimental, and properly fenced.

## Initial host target

The first planned distribution is **Lumi for Hermes**.

A future **Lumi for OpenClaw** distribution may be explored after compatibility research, but this repository intentionally does **not** include OpenClaw folders, installers, or support claims yet.

## Project layout

```text
core/
  layered-memory/      # curated Lumi Layered Memory release surface
  nuances/             # curated Nuances release surface
  presence/            # curated Presence release surface
adapters/
  hermes/              # Hermes-specific integration boundary
installers/
  lumi-for-hermes/     # first host-specific distribution target
examples/
  synthetic-memory-pack/
docs/
scripts/
tests/
```

## Public-release boundary

This repository must never include:

- raw Autoresearch runs;
- private memories, diaries, chat logs, or personal coordinates;
- credentials, tokens, API keys, passwords, connection strings, or chat IDs;
- local runtime state, scheduler internals, cron/job queues, or wrappers;
- unreviewed generated artifacts;
- host-specific compatibility claims that have not been verified.

Every release candidate must pass the local release gate:

```bash
./scripts/release_check.sh
```

## Documentation

- [Product brief](docs/product-brief.md)
- [Architecture](docs/architecture.md)
- [Release boundary](docs/release-boundary.md)
- [Host compatibility](docs/host-compatibility.md)
- [Licensing](docs/licensing.md)
- [Release checklist](docs/release-checklist.md)

## License

Code is licensed under the [MIT License](LICENSE).

Documentation, specifications, examples, diagrams, written explanations, and other non-code project materials are licensed under [CC BY 4.0](LICENSE-DOCS.md), unless a file states otherwise.

Project names, logos, branding, and trademarks are not granted by the code or documentation licenses except for normal nominative reference. See [NOTICE](NOTICE.md).
