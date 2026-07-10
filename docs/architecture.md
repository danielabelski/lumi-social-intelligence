# Architecture

Lumi Social Intelligence is a host-neutral social-intelligence layer composed of three cooperating products:

```text
Lumi Layered Memory -> Nuances -> Presence
```

```text
Lumi Layered Memory gives context.
Nuances reads the moment.
Presence decides whether to speak, wait, ask, act, repair, or stay quiet.
```

## Lumi Layered Memory

**Lumi Layered Memory** handles continuity.

It stores and retrieves useful context with review, citations, and inspectable state. Its job is not to make an assistant clingy or over-personalized. Its job is to preserve useful continuity while keeping boundaries visible.

Public contract:

- durable memory is reviewable;
- memory use can be explained with receipts;
- corrections and revocations matter;
- private runtime state does not become public release material;
- identity, preferences, and durable user facts are not silently rewritten.

## Nuances

**Nuances** handles moment-reading.

It appraises what a memory, correction, tone shift, uncertainty signal, or contextual cue might mean right now. Nuances proposes interpretations; it does not mutate durable behavior on its own.

Public contract:

- observations remain humble;
- ambiguity is preserved instead of flattened;
- consent, correction, and emotional weight are first-class signals;
- learning routes through review where appropriate;
- pattern recognition does not become hidden profiling.

## Presence

**Presence** handles governed initiative.

It decides whether the assistant should speak, wait, ask, act, repair, or hold silence. Presence is the fail-closed gate when continuity, memory, or context is uncertain.

Public contract:

- restraint is a supported outcome;
- action requires appropriate confidence and permission;
- repair is part of the loop;
- proactive behavior is reviewable before it becomes live behavior;
- warmth must not override safety or consent.

## Host adapters

Host adapters translate the Lumi Social Intelligence contract into a specific agent runtime.

Adapters also preserve the boundary between Lumi and the host's primary memory provider. Lumi Social Intelligence should not replace Obsidian-like vaults, Hermes memory providers, or other canonical stores. The provider remains authoritative; Lumi adds interpretation, restraint, review, and receipts above it.

Initial adapter:

- **Hermes Agent**

Deferred compatibility research:

- **OpenClaw** — possible future target, but not implemented or claimed here yet.

Memory-provider compatibility is specified in [Memory Provider Compatibility](memory-provider-compatibility.md).

## Release flow

```text
Private development repositories
  Lumi Layered Memory
  Nuances
  Presence
  Autoresearch
        |
        | tested, reviewed, public-safe promotion
        v
Lumi Social Intelligence
```

Autoresearch remains private harness and evidence infrastructure. It is not the public product surface.
