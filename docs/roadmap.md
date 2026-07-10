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

**Goal:** Make each private product module independently promotable into the release doorway.

### Deliverables

- [ ] Rename or normalize the **Lumi Layered Memory** distribution to `lumi-layered-memory`.
- [ ] Rename or normalize the **Nuances** distribution to `lumi-nuances`.
- [ ] Add package metadata for **Presence** as `lumi-presence`.
- [ ] Ensure each private module has an executable release gate.
- [ ] Run **Lumi Layered Memory** release gate.
- [ ] Run **Nuances** release gate.
- [ ] Run **Presence** release gate.
- [ ] Confirm each module uses only synthetic or public-safe fixture data in release surfaces.
- [ ] Confirm each module has public-safe README/docs boundaries.

### Exit criteria

- All three module release gates pass locally.
- Package/distribution names match the 0.1.0 naming decision.
- Each module has a clear public export surface.

## Sprint 3 — Curated export and promotion scripts

**Goal:** Make promotion from private development repositories to **Lumi Social Intelligence** repeatable.

### Deliverables

- [ ] Add an export script for **Lumi Layered Memory**.
- [ ] Add an export script for **Nuances**.
- [ ] Add an export script for **Presence**.
- [ ] Define allowlists for promoted files.
- [ ] Exclude private runtime state, raw runs, local logs, credentials, and internal planning material.
- [ ] Copy curated exports into `core/` in **Lumi Social Intelligence**.
- [ ] Run doorway release check after import.
- [ ] Commit imports as release-candidate updates only after checks pass.

### Exit criteria

- A clean private-to-doorway promotion can be repeated without manual guessing.
- The doorway release check catches missing product names, missing licenses, private-path leaks, and secret-shaped material.

## Sprint 4 — Lumi for Hermes installable preview

**Goal:** Build the first host-specific preview: **Lumi for Hermes**.

### Deliverables

- [ ] Define the **Lumi for Hermes** adapter contract.
- [ ] Define adapter inputs and outputs.
- [ ] Connect the flow: memory context → nuance appraisal → presence decision → review card.
- [ ] Add dry-run mode.
- [ ] Add review-gated mode.
- [ ] Ensure fail-closed behavior when any dependency is missing or uncertain.
- [ ] Add installer path under `installers/lumi-for-hermes/`.
- [ ] Add uninstall or rollback notes.
- [ ] Add synthetic fixture tests for the adapter.
- [ ] Confirm the adapter does not expose private Hermes scheduler internals, job IDs, queues, chat IDs, or local runtime state.

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

- [ ] Add GitHub Actions release workflow.
- [ ] Run doorway release check in CI.
- [ ] Build release zip artifact.
- [ ] Build or collect Python package artifacts for:
  - `lumi-layered-memory`
  - `lumi-nuances`
  - `lumi-presence`
- [ ] Include **Lumi for Hermes** preview installer artifacts.
- [ ] Generate checksums.
- [ ] Attach artifacts to GitHub Release on tag.
- [ ] Add clean-checkout smoke test.
- [ ] Add release archive scan for private/local material.

### Exit criteria

- A `v0.1.0-rc.1` tag can build artifacts automatically.
- Release artifacts can be downloaded, inspected, and smoke-tested from a clean checkout.

## Sprint 6 — Public-readiness audit

**Goal:** Decide whether the repository and artifacts are safe to make public.

### Deliverables

- [ ] Audit tracked files.
- [ ] Audit ignored local artifacts separately.
- [ ] Run secret/privacy scan.
- [ ] Run naming scan for product-name consistency.
- [ ] Run host-claim scan.
- [ ] Verify OpenClaw remains deferred unless compatibility research is complete.
- [ ] Verify licenses and notice files.
- [ ] Verify GitHub About metadata.
- [ ] Verify release archive contents.
- [ ] Verify clean install or clean inspection path for **Lumi for Hermes**.

### Exit criteria

- No private or local operational material is present.
- No unsupported compatibility claim is present.
- The release artifact matches the stated 0.1.0 scope.

## Sprint 7 — 0.1.0 release

**Goal:** Publish the first installable Hermes preview release when all gates pass.

### Deliverables

- [ ] Tag `v0.1.0`.
- [ ] Publish GitHub Release notes.
- [ ] Attach release artifacts and checksums.
- [ ] Verify release page and assets.
- [ ] Decide whether to keep repository private, publish a private release candidate, or switch the repository public.

### Exit criteria

- `v0.1.0` is reproducible, documented, licensed, and public-safe.
- **Lumi for Hermes** is presented as an installable preview with review gates and fail-closed behavior.
- **Lumi Social Intelligence** remains the clean release doorway for **Lumi Layered Memory**, **Nuances**, and **Presence**.
