# Live Surface natural-language controls

Live Surface controls let a user steer warmed context with ordinary phrasing instead of magic commands. The public `v0.3` preview is intentionally **shadow-only**: it parses a request, returns a reviewable control state, and renders a tiny acknowledgement, but it does not mutate the host runtime or read personal integrations.

## Principles

1. Natural language, not keywords.
2. Safe, reversible, local controls should have almost no friction.
3. Ask only when ambiguity changes safety.
4. Review before durable personalization, personal-data surfaces, external writes, scheduler/config edits, or broad forgetting.
5. Refresh is not permission to speak: `refresh_policy` and `surfacing_policy` stay separate.
6. Silence can be a successful output.

## Intent families

| Intent | Meaning | Default scope | Confirmation | Example |
|---|---|---|---|---|
| `keep_fresh` | Keep safe derived state warm quietly | `session` | no | “keep an eye on this” |
| `only_on_request` | Answer only if asked | `session` | no | “only bring this up if I ask” |
| `do_not_surface` | Suppress this topic/context | `session` | no for narrow cases | “don’t surface this” |
| `capture_now_enrich_later` | Capture immediately, enrich later | `session` | no | “park this for later” |
| `show_status` | Show what is warm/blocked, without plumbing | `session` | no | “what are you keeping warm?” |
| `add_surface` | Add a personal-data surface | `review_required` | yes | “add Calendar free/busy” |
| `forget_pattern` | Remove a learned/reviewable pattern | `review_required` | yes | “forget that pattern” |
| `set_boundary` | Adjust a surfacing/refresh boundary | depends | maybe | “be quieter about rain” |

## Shadow-mode contract

`apply_control_shadow()` returns:

- a deterministic `control_id`;
- hashed raw text, with `raw_user_text_stored: false`;
- `surfacing_policy` separate from `refresh_policy`;
- review status and safety flags;
- zero side-effect counters.

Hard-gated requests include Calendar/email/photos/messages access, external sends/posts/replies, scheduler or runtime config edits, durable memory writes, and destructive broad forgetting.

## Example

```python
from lumi_social_intelligence.live_surface_controls import apply_control_shadow

card = apply_control_shadow(
    "keep this ready for when I leave",
    now="2026-07-11T17:00:00+07:00",
    source="host_shadow_surface",
)
assert card["state"]["intent"] == "keep_fresh"
assert card["ack"] == "Got it — I’ll keep it warm quietly."
assert all(value == 0 for value in card["side_effects"].values())
```

## Boundary example

A phrase such as “check my calendar and keep plans fresh” maps to `add_surface`, `review_required`, and a tiny confirmation-gate acknowledgement. The shadow model does **not** read Calendar free/busy until a host has explicitly added that surface under its own consent flow.
