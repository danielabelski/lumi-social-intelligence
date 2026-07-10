# Release Roadmap

Lumi Social Intelligence is the public-facing release doorway for tested, curated updates from the private Lumi development repositories.

## 0.1.0 scope

**0.1.0 target:** installable Hermes preview.

The first release should include public-safe documentation, curated module release surfaces, synthetic examples, repeatable release artifacts, and the first **Lumi for Hermes** installer/adapter path.

0.1.0 should remain review-gated and fail-closed. It should not introduce uncontrolled live autonomous behavior.

## Product components

Public-facing product names:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**

Python package/distribution names:

- `lumi-layered-memory`
- `lumi-nuances`
- `lumi-presence`

## Promotion mechanics

Development happens in private repositories:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**
- **Autoresearch**

Release promotion follows this path:

```text
Private repo passes release gate
→ export curated files via script
→ copy into Lumi Social Intelligence
→ run doorway release check
→ commit as release candidate
```

The release doorway should contain only reviewed, public-safe files. It must not include raw runs, private memories, diaries, local runtime state, scheduler internals, credentials, chat IDs, private coordinates, or unverified host claims.

## Pre-sprint — NotebookLM article foundation

**Status:** Complete.

**Goal:** Write the source essays that explain Lumi Social Intelligence before implementation sprints begin.

These articles should establish the public narrative, technical research context, and creation story before the 0.1.0 release machinery hardens.

### Deliverables

- [x] Full-length Introduction article: **Lumi Social Intelligence**.
- [x] Full-length Technical article: **Lumi Social Intelligence — Lumi Layered Memory, Nuances, and Presence**.
- [x] Full-length Creation Story: concepting, research, implementation, testing, purpose, and audience.
- [x] Technical reference pack for NotebookLM.
- [x] Public/private boundary review for all article drafts.
- [x] NotebookLM source bundle.

### Framing requirement

The articles should clearly explain that Lumi Social Intelligence was conceived by one person building a full social-intelligence layer for Hermes Agent: a non-developer with a project-manager mindset, QA discipline, and music-producer sensitivity to timing, tone, dynamics, and emotional arc.

### Exit criteria

- The three articles are drafted and reviewed.
- Technical claims are backed by references where needed.
- No private Hermes runtime details, memories, chat logs, credentials, coordinates, or scheduler internals leak into the public narrative.

See [Article Plan for NotebookLM](article-plan.md).

## Sprint 0 — Release doorway foundation

**Goal:** Establish the private release doorway and make the public story coherent before any release artifacts exist.

**Status:** Mostly complete.

### Deliverables

- [x] Create private **Lumi Social Intelligence** repository.
- [x] Define **Lumi Social Intelligence** as the public release doorway.
- [x] Keep private development repositories separate.
- [x] Document the product relationship: **Lumi Layered Memory** → **Nuances** → **Presence**.
- [x] Add public-safe README and documentation.
- [x] Add license, documentation license, and notice files matching related Lumi repositories.
- [x] Add release boundary documentation.
- [x] Add host compatibility documentation.
- [x] Keep OpenClaw deferred until compatibility research is complete.
- [x] Add local doorway release check.
- [x] Verify local release check passes.

### Remaining

- [ ] Keep this roadmap updated as release scope changes.
- [ ] Keep GitHub About metadata aligned with the public product story.

## Sprint 1 — Memory-provider compatibility boundary

**Status:** Complete.

**Goal:** Prove and document that **Lumi Social Intelligence** operates as a higher social-intelligence layer above existing memory providers, so Hermes memory, Obsidian, or another main memory backend can keep functioning normally.

### Deliverables

- [x] Add a public architecture note explaining that **Lumi Social Intelligence** is not a competing memory backend.
- [x] Define the adapter boundary between memory providers and Lumi:
  - memory provider = durable storage/retrieval;
  - Lumi Layered Memory = continuity policy, citations, receipts, review;
  - Nuances = contextual appraisal;
  - Presence = action/silence decision gate.
- [x] Document Obsidian as an example backend: vault notes remain user-owned source material, while Lumi consumes selected context through explicit adapter packets.
- [x] Define allowed effects:
  - read selected context;
  - produce compact context packets;
  - generate receipts;
  - create review proposals if configured.
- [x] Define blocked effects:
  - no silent rewrites of Obsidian/Hermes memory;
  - no hidden promotion of inferred emotional state;
  - no adapter claiming exclusive memory authority;
  - no uncontrolled live writes or sends.
- [x] Add synthetic fixture tests for provider-neutral context packets.
- [x] Add one Obsidian-shaped fixture and one Hermes-memory-shaped fixture proving both can feed the same Lumi decision path.
- [x] Add fail-closed tests for missing provider data, ambiguous authority, stale context, and blocked write attempts.
- [x] Update **Lumi for Hermes** adapter docs to state that Hermes' configured memory provider remains authoritative unless an explicit reviewed apply path is configured.

### Exit criteria

- **Lumi Social Intelligence** can be explained as: “Keep your memory model. Add better memory judgment.”
- Obsidian/Hermes/other memory providers remain compatible by contract.
- Tests prove the Lumi path consumes provider-neutral context and does not mutate provider-owned memory by default.
- The release doorway docs clearly distinguish storage/retrieval from continuity/appraisal/presence decisions.

## Sprint 2 — Module release gates and package names

**Status:** Complete for the public doorway machinery; no private module candidate has been exported yet.

**Goal:** Make each private product module independently promotable into the release doorway.

### Deliverables

- [x] Normalize public package naming decisions:
  - **Lumi Layered Memory** → `lumi-layered-memory`
  - **Nuances** → `lumi-nuances`
  - **Presence** → `lumi-presence`
- [x] Define module release gates and public export allowlists.
- [x] Add read-only module export audit.
- [x] Add non-mutating reviewed copy-plan generator.
- [x] Add explicit reviewed apply command for human-approved plans.
- [x] Document the private-to-doorway module promotion workflow.
- [x] Add synthetic end-to-end audit → plan → apply coverage without private sources.
- [x] Confirm public module surfaces use synthetic or public-safe fixture data only.
- [x] Confirm each module has public-safe README/docs boundaries.

### Exit criteria

- Package/distribution names match the 0.1.0 naming decision.
- Each module has a clear public export surface and fail-closed allowlist.
- Promotion follows the reviewed airlock: read-only audit → review-only plan → explicit reviewed apply.
- The doorway release check catches missing product names, private-path leaks, and secret-shaped material.

## Sprint 3 — First curated module promotion

**Status:** Complete for the first tiny Presence doorway candidate.

**Goal:** Promote the first intentionally small public-safe module candidate into **Lumi Social Intelligence**.

### Deliverables

- [x] Choose the first candidate module: **Presence**.
- [x] Prepare a tiny public-safe candidate: README, package skeleton, synthetic examples, and synthetic tests only.
- [x] Run the candidate's own release gate.
- [x] Run the doorway read-only export audit.
- [x] Review the generated copy plan.
- [x] Apply the reviewed plan with `--apply-reviewed-plan`.
- [x] Run doorway release check after import.
- [x] Commit imports as release-candidate updates only after checks pass.

### Result

The first Presence promotion imports a deliberately small governed-initiative skeleton into `core/presence/`:

- `lumi-presence` package metadata;
- deterministic `decide_presence_move` public API preview;
- synthetic example;
- synthetic tests;
- public overview documentation;
- `.lumi-export-manifest.json` recording the reviewed import.

No private Presence internals, raw runs, memories, chat logs, scheduler/runtime details, credentials, or Autoresearch evidence are included.

### Exit criteria

- A real private-to-doorway promotion completes without manual guessing.
- The first module export contains no private internals, raw runs, logs, credentials, or unreviewed generated artifacts.
- The release doorway remains private until the full public-readiness audit passes.

## Sprint 4 — Lumi for Hermes installable preview

**Goal:** Build the first host-specific preview: **Lumi for Hermes**.

### Deliverables

- [x] Define the **Lumi for Hermes** adapter contract.
- [x] Define adapter inputs and outputs.
- [x] Connect the flow: memory context → nuance appraisal → presence decision → review card.
- [x] Add dry-run mode.
- [x] Add review-gated mode.
- [x] Ensure fail-closed behavior when any dependency is missing or uncertain.
- [x] Add installer path under `installers/lumi-for-hermes/`.
- [x] Add uninstall or rollback notes.
- [x] Add synthetic fixture tests for the adapter.
- [x] Confirm the adapter does not expose private Hermes scheduler internals, job IDs, queues, chat IDs, or local runtime state.

### Non-goals for 0.1.0

- No uncontrolled live autonomous sending.
- No unreviewed writes to private memory or runtime state.
- No OpenClaw support claim.

### Exit criteria

- A user can install or inspect **Lumi for Hermes** as a preview.
- The adapter can produce reviewable decisions from synthetic fixtures.
- The adapter fails closed instead of acting when confidence, configuration, or safety state is insufficient.

## Sprint 5 — Release artifacts and GitHub automation

**Goal:** Produce repeatable 0.1.0 release artifacts from the release doorway.

### Deliverables

- [x] Add GitHub Actions release workflow.
- [x] Run doorway release check in CI.
- [x] Build release zip artifact.
- [x] Build or collect Python package artifacts for:
  - `lumi-layered-memory`
  - `lumi-nuances`
  - `lumi-presence`
- [x] Include **Lumi for Hermes** preview installer artifacts.
- [x] Generate checksums.
- [x] Attach artifacts to GitHub Release on tag.
- [x] Add clean-checkout smoke test.
- [x] Add release archive scan for private/local material.

### Exit criteria

- A `v0.1.0-rc.1` tag can build artifacts automatically.
- Release artifacts can be downloaded, inspected, and smoke-tested from a clean checkout.

## Sprint 6 — Public-readiness audit

**Goal:** Decide whether the repository and artifacts are safe to make public.

### Deliverables

- [x] Audit tracked files.
- [x] Audit ignored local artifacts separately.
- [x] Run secret/privacy scan.
- [x] Run naming scan for product-name consistency.
- [x] Run host-claim scan.
- [x] Verify OpenClaw remains deferred unless compatibility research is complete.
- [x] Verify licenses and notice files.
- [x] Verify GitHub About metadata recommendation.
- [x] Verify release archive contents.
- [x] Verify clean install or clean inspection path for **Lumi for Hermes**.
- [x] Add public README positioning for human-shaped, governed self-improvement.
- [x] Add repeatable public-readiness audit to the release gate.

### Exit criteria

- No private or local operational material is present.
- No unsupported compatibility claim is present.
- The release artifact matches the stated 0.1.0 scope.

## Sprint 7 — 0.1.0 release

**Goal:** Publish the first installable Hermes preview release when all gates pass.

### Deliverables

- [x] Tag `v0.1.0`.
- [x] Draft GitHub Release notes.
- [x] Attach release artifacts and checksums.
- [x] Verify release page and assets.
- [x] Add non-mutating release-candidate plan that blocks dirty trees and existing tags.
- [x] Keep repository private while publishing the private v0.1.0 release.

### Exit criteria

- `v0.1.0` is reproducible, documented, licensed, and public-safe.
- **Lumi for Hermes** is presented as an installable preview with review gates and fail-closed behavior.
- **Lumi Social Intelligence** remains the clean release doorway for **Lumi Layered Memory**, **Nuances**, and **Presence**.
