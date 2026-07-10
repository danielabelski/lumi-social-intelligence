# Lumi for Hermes adapter

This directory contains the host-specific preview surface for **Lumi for Hermes**.

The adapter binds **Lumi Layered Memory**, **Nuances**, and **Presence** into Hermes Agent through explicit inputs, review surfaces, and safety gates. The current public surface is intentionally preview-only: it produces inspectable output and performs no runtime actions.

## Current public scope

Lumi for Hermes is currently a **dry-run/review-gated preview surface**.

It accepts explicit synthetic or host-selected input, normalizes it into public-safe Lumi records, and returns review card or receipt output that a human can inspect before anything is applied elsewhere.

The adapter does **not** claim an autonomous runtime, a live Telegram integration, or a durable memory writer. It is a public contract for safe review-gated behavior.

## Live-demo scope

The current safe live demo can show:

- local adapter execution from explicit input;
- generated review cards and receipts;
- fail-closed behavior when grounding or confidence is insufficient;
- private runtime field rejection at the contract boundary;
- `canonical_writes: 0` and empty runtime actions;
- the public v0.2 evidence artifacts under `docs/demos/`.

A presenter may say that the adapter demonstrates the review-gated flow and safety boundaries. Native outbound reaction delivery is not claimed live.

## Shadow-only scope

Reaction and emoji presence records remain preview evidence, not live delivery proof:

- reaction-aware Presence records are shadow-only;
- outbound emoji Presence records are shadow-only;
- records are built from explicit host-provided input;
- allowed outbound emoji choices are limited to `❤️ 😄 👍 👀 ✨`;
- tiny reply/reaction intent may be represented as a record;
- no Telegram API reads are performed;
- no Telegram sends or reactions are performed;
- no durable memory promotion is performed.

Shadow-only records are useful for reviewing how Lumi would reason about social signals without pretending that the host runtime already acted on them.

## Blocked side effects

The adapter must keep these side effects blocked in the public preview:

- no canonical writes;
- no Hermes memory writes;
- no Obsidian or vault edits;
- no scheduler, queue, or job changes;
- no Telegram API reads;
- no Telegram sends or reactions;
- no delivery-channel selection;
- no credential, token, or connection-string handling.

Any future mode that performs writes, sends, reactions, scheduling, or durable memory promotion must add an explicit consent path, a receipt, rollback notes where relevant, and tests before it ships.

## Operator rule

When presenting the adapter, say what the evidence proves and stop there:

> This demonstrates Lumi’s review-gated decision path and safety boundaries from explicit inputs. Live Telegram reaction delivery is not claimed until a real host-runtime run verifies it.

## Adapter contract

Input schema:

```json
{
  "schema": "lumi.hermes.adapter_input.v1",
  "mode": "dry_run",
  "memory_context": {
    "provider": "hermes-memory",
    "source_id": "synthetic://memory/context/1",
    "text": "Public-safe context summary.",
    "confidence": 0.9
  },
  "nuance_appraisal": {
    "why_now": "short reason this moment may matter",
    "grounded": true,
    "confidence": 0.8
  }
}
```

Output schema:

```json
{
  "schema": "lumi.hermes.review_card.v1",
  "status": "ready_for_review",
  "mode": "dry_run",
  "memory": {},
  "nuance": {},
  "decision": {},
  "safety": {
    "canonical_writes": 0,
    "runtime_actions": [],
    "requires_human_review": true
  }
}
```

Flow:

```text
memory context → compatibility packet → nuance appraisal → Presence decision → review card
```

## Modes

- `dry_run` — produce a review card only.
- `review_gated` — same zero-write behavior, but labeled for future human approval workflows.
- `reaction_presence_shadow` — reaction-aware Presence card from explicit host-provided reaction input; no Telegram API reads/sends and no memory promotion.
- `outbound_emoji_presence_shadow` — assistant-side emoji Presence card from explicit host-provided intent; reaction-only, throttled, shadow-only, and no memory promotion.

Both regular modes currently have:

- `canonical_writes: 0`
- `runtime_actions: []`
- `requires_human_review: true`

Reaction presence shadow mode additionally keeps:

- `telegram_reaction_ingestion_verified: false`
- `telegram_outbound_reaction_back_verified: false`
- `telegram_messages_sent: 0`
- `live_memory_writes: 0`
- reaction-back replies tiny, optional, and throttled

Outbound emoji presence shadow mode additionally keeps:

- allowed emoji palette: `❤️ 😄 👍 👀 ✨`
- `delivery_mode: shadow_only`
- `safe_to_claim_live_delivery: false`
- `telegram_reactions_sent: 0`
- `telegram_messages_sent: 0`
- `text_reply: ""`
- `max_text_words: 0`
- `durable_write: false`
- `outbound_reaction_is_not_consent: true`

## Fail-closed behavior

The adapter returns `status: fail_closed` and a `hold` Presence decision when confidence, grounding, or the why-now justification is insufficient.

The adapter rejects private Hermes runtime fields at the contract boundary:

- `chat_id`
- `job_id`
- `scheduler_queue`
- `runtime_state`
- `api_key`
- `token`
- `credential`
- `delivery_channel`
- `connection_string`
- `password`

## Memory-provider boundary

Hermes may use different durable memory setups, including built-in memory tooling, file-backed notes, Obsidian-like vault workflows, or future provider integrations. **Lumi for Hermes** must not assume it owns that memory layer.

Adapter stance:

- Hermes' selected memory provider remains authoritative.
- Lumi reads selected context only through explicit host configuration.
- Lumi preserves provenance and confidence for memory-derived context.
- Lumi emits proposals and receipts before any durable write.
- Lumi does not silently rewrite Hermes memory, Obsidian notes, vault files, or provider internals.
- If memory sources conflict, Lumi should preserve ambiguity and route to Presence for ask/wait/repair behavior.

Default preview mode is read-only plus reviewable proposal/receipt output.

See `docs/memory-provider-compatibility.md` for the shared contract.

Do not add OpenClaw support here. OpenClaw compatibility must be researched before any adapter, installer, or support claim is added.
