# Lumi Social Intelligence

**Memory, nuance, presence, and review-gated Live Surface for AI agents.**

Lumi Social Intelligence is the public-facing release doorway for three cooperating products plus Live Surface, which lets a host agent keep safe context warm without turning every available tool into an automatic side effect:

```text
Lumi Layered Memory -> Nuances -> Presence -> Live Surface
```

It gives agent runtimes a governed reflection layer: adaptive memory, nuance, and presence with confidence scoring, contradiction handling, user approval, skill evaluation, review, consent, repair, and explicit control boundaries for live host surfaces.

> **Status:** latest public release is **`v0.4.0`** — real, review-gated Live Surface natural-language controls. The original track began as a private, review-gated `v0.1.0` preview release; `v0.2` is a demo-evidence path, not a live automation claim. Native Telegram reactions are not claimed until verified by a real host-runtime run. `v0.4.0` claims review-gated public Live Surface control cards and zero-write safety counters, not autonomous private runtime automation.

## Why it exists

Modern assistants do not only need more context. They need better judgment about what context means, when it should matter, and whether acting on it would be helpful, invasive, unsafe, or just socially clumsy.

Lumi Social Intelligence is built around a simple promise:

> Agents that remember carefully, read the room better, and know when not to act.

It is also built around a stricter self-improvement boundary:

> We are making the self-improvement loop something that is human-shaped.

That means **Lumi Social Intelligence** is not an auto-personality-rewriter. It is a governed reflection layer around agent self-improvement: observations can be scored, contradicted, reviewed, rejected, repaired, or promoted with explicit approval. The agent does not freely rewrite its identity after every interaction.

## Latest release: v0.4.0

**v0.4.0** adds the first real public release of review-gated **Live Surface natural-language controls**.

Live Surface is the capability boundary between “the assistant has safe, warmed context” and “the assistant is allowed to act.” It is designed for host integrations where a tool or surface may be present, but action still needs explicit review, membership, or approval.

In this release, the public API can produce review-gated control cards for safe session-readiness state and fail closed when a requested personal-data surface is not available.

### What v0.4.0 offers

- Semantic Live Surface intent parsing — ordinary phrases, not magic keywords.
- Safe session-readiness review cards.
- Explicit `review_required` handling for personal-data surfaces.
- Fail-closed behavior for unavailable surfaces such as Calendar.
- Zero side-effect counters for the public control path:
  - `canonical_writes: 0`
  - `external_writes: 0`
  - `private_runtime_reads: 0`
  - `scheduler_mutations: 0`
- A clearer split between warmed context and approved action.

### What v0.4.0 does not claim

- Autonomous private runtime automation.
- Telegram sends or native reactions.
- Calendar or email reads without explicit reviewed surface membership.
- Runtime config or scheduler mutation.
- Durable memory writes.
- Raw private Hermes runtime access.

See the [v0.4.0 release notes](docs/releases/v0.4.0.md) and [release evidence](docs/evidence/v0.4.0-real-controls-evidence.md).

## The short concept

Lumi Social Intelligence helps an assistant answer four questions before it does anything socially meaningful:

1. **What do I know?** — governed memory and continuity.
2. **What does this moment mean?** — nuance, uncertainty, consent, and contradiction.
3. **Should I speak, wait, ask, or repair?** — presence and restraint.
4. **Is this context only warm, or is action approved?** — Live Surface.

The result is a safer path toward assistants that feel more socially aware without becoming unbounded, invasive, or weirdly overconfident.

## The product layer

| Product | Role | Public promise |
|---|---|---|
| **Lumi Layered Memory** | Context and continuity | Useful continuity. Clean boundaries. Receipts. No silent rewrites. |
| **Nuances** | Contextual appraisal | Notice lightly. Invite clearly. Repair quickly. Leave room. |
| **Presence** | Governed initiative | Soft presence. Clean boundaries. Quick repair. No stealing the feeling. |
| **Live Surface** | Review-gated host readiness | Warm safe context. Fail closed. Separate readiness from action. |

### Lumi Layered Memory

Lumi Layered Memory gives an assistant inspectable continuity: durable facts, preferences, project context, and memory receipts without silent identity rewrites or hidden behavioral drift.

### Nuances

Nuances reads the moment around the memory: corrections, consent signals, tone, uncertainty, emotional weight, context shifts, and whether an observation should become a durable adaptation at all.

### Presence

Presence decides what the assistant should do with that understanding: speak, wait, ask, act, repair, or hold silence. Presence is where restraint becomes a feature, not a missing capability.

### Live Surface

Live Surface keeps host capabilities legible and review-gated. It lets a host say, for example, “keep this ready,” “only surface this if relevant,” or “add Calendar later,” while preserving hard boundaries around personal data, external sends, durable memory, scheduler changes, and runtime mutation.

## Repository role

This repository is the curated release surface for Lumi Social Intelligence.

Development happens in private repositories:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**
- **Autoresearch**

Tested, reviewed, public-safe updates are promoted here as versioned releases. This keeps the public doorway clean while the private workshop can stay messy, experimental, and properly fenced.

## Initial host target

The first planned distribution is **Lumi for Hermes**.

A future **Lumi for OpenClaw** distribution may be explored after compatibility research, but this repository intentionally does **not** include OpenClaw folders, installers, or support claims yet.

## Quickstart

Run the local release gate:

```bash
./scripts/release_check.sh
```

Use the public Live Surface control API:

```python
from lumi_social_intelligence import apply_review_gated_control

card = apply_review_gated_control(
    "keep this ready for when I leave",
    now="2026-07-11T17:00:00+07:00",
    source="host_public_api",
)

print(card["ack"])
print(card["side_effects"])
```

The API returns a review card plus side-effect counters. Safe readiness controls can be represented without private runtime reads or writes; personal-data requests fail closed until the surface is explicitly added and reviewed.

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

Every release must pass the local release gate:

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
- [Module promotion workflow](docs/module-promotion-workflow.md)
- [v0.1.0 release notes](docs/releases/v0.1.0.md)
- [0.1.0 Preview + Research Harness](docs/preview-0.1.0-research-harness.md)
- [0.1.0 Officialization Notes](docs/releases/v0.1.0-officialization-notes.md)
- [Release roadmap, including v0.2 demo/productization sprints](docs/roadmap.md)
- [v0.2 Demo Index](docs/demos/v0.2-demo-index.md)
- [v0.2 Demo Evidence Path](docs/demos/README.md)
- [Live Surface natural-language controls](docs/live-surface-natural-language-controls.md)
- [v0.4.0 release notes](docs/releases/v0.4.0.md)
- [v0.4.0 release evidence](docs/evidence/v0.4.0-real-controls-evidence.md)

## Find it

- Repository: <https://github.com/markoaamunkajo/lumi-social-intelligence>
- Latest release: <https://github.com/markoaamunkajo/lumi-social-intelligence/releases/tag/v0.4.0>

## License

Code is licensed under the [MIT License](LICENSE).

Documentation, specifications, examples, diagrams, written explanations, and other non-code project materials are licensed under [CC BY 4.0](LICENSE-DOCS.md), unless a file states otherwise.

Project names, logos, branding, and trademarks are not granted by the code or documentation licenses except for normal nominative reference. See [NOTICE](NOTICE.md).
