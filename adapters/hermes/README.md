# Lumi for Hermes adapter

This directory is reserved for the first planned host adapter: **Lumi for Hermes**.

The adapter should bind **Lumi Layered Memory**, **Nuances**, and **Presence** into Hermes Agent through explicit configuration, review surfaces, and safety gates.

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
