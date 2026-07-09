# Host Compatibility

Lumi Social Intelligence is host-neutral. Runtime-specific adapters provide installation, context injection, review surfaces, and safety gates for a given agent host.

## Compatibility matrix

| Host | Status | Notes |
|---|---|---|
| **Hermes Agent** | Planned first | First intended host-specific distribution: **Lumi for Hermes**. |
| **OpenClaw** | Research needed | Do not add folders, installers, or support claims until its architecture and extension points are verified. |

## Shared Lumi contract

A compatible host should provide or allow:

- context injection with clear precedence;
- file-backed or API-backed review cards;
- explicit dry-run, review, and live-mode boundaries;
- safe tool/action gating;
- rollback or reversible write records;
- public/private boundary separation;
- secret and local-state hygiene before release.

## Adapter rule

Adapters are thin runtime bindings. The public product components remain the same across hosts:

- **Lumi Layered Memory** for continuity and receipts;
- **Nuances** for contextual appraisal;
- **Presence** for governed initiative;
- review gates;
- receipts;
- fail-closed behavior.

## Deferred host rule

A host-specific adapter or installer should not be added merely because the product concept seems portable. Add one only after compatibility research identifies the host's extension points, configuration model, safety boundaries, and installation path.
