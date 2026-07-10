# Presence

**Presence** is the governed-initiative module in **Lumi Social Intelligence**. It helps an assistant decide whether to speak, ask, help, hold, defer, block, or repair.

Presence is intentionally conservative: it is not a live sender, a notification engine, or a fake-warmth generator. The public release surface starts with inspectable decision contracts, synthetic examples, and safety-first tests.

```text
Lumi Layered Memory -> Nuances -> Presence

Memory gives context.
Nuances reads the moment.
Presence decides whether initiative is justified.
```

## Current release posture

```json
{
  "runtime_sender": false,
  "autonomous_messages": false,
  "status": "reviewed_suggestion_cards_only"
}
```

Presence should fail closed when required context is missing. Silence, restraint, and review are valid outputs.

## Tiny public API preview

The first public-safe skeleton exposes a deterministic `decide_presence_move` helper for synthetic examples and tests. It is deliberately small: real private behavioral internals are not exported in this first doorway promotion.

```python
from lumi_presence import decide_presence_move

decision = decide_presence_move(
    why_now="User is leaving and asked for errand-aware help",
    grounded=True,
    side_effect=False,
)
assert decision["move"] == "speak"
```

## Boundaries

- no raw runs;
- no private memories;
- no chat logs;
- no scheduler/runtime internals;
- no credentials;
- no autonomous sending by default.

## License

See the repository-level license files for code, documentation, and brand boundaries.
