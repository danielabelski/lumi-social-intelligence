# Article Plan for NotebookLM

Before running the 0.1.0 implementation sprints, prepare three full-length articles that explain Lumi Social Intelligence from three different angles: product introduction, technical architecture, and creation story.

These articles are source material for NotebookLM and should be written as substantial, coherent essays rather than marketing snippets.

## Shared positioning

All three articles should preserve this human origin:

> Lumi Social Intelligence was conceived by one person building a full social-intelligence layer for Hermes Agent: a non-developer with a project-manager mindset, QA discipline, and music-producer sensitivity to timing, tone, dynamics, and emotional arc.

This framing matters because Lumi Social Intelligence did not start as a conventional software architecture project. It came from lived product sense, careful observation, QA-style failure analysis, creative pattern recognition, and repeated testing of how an assistant should remember, read the room, and decide whether to speak or stay quiet.

## Shared product definition

Lumi Social Intelligence is a social-intelligence layer for agents: adaptive memory, nuance, and presence with review, consent, and repair.

Core architecture:

```text
Lumi Layered Memory -> Nuances -> Presence
```

```text
Lumi Layered Memory gives context.
Nuances reads the moment.
Presence decides whether to speak, wait, ask, act, repair, or stay quiet.
```

Public-facing products:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**

0.1.0 Python package/distribution names:

- `lumi-layered-memory`
- `lumi-nuances`
- `lumi-presence`

Initial host target:

- **Lumi for Hermes**

## Article 1 — Introduction to Lumi Social Intelligence

### Working title

**Lumi Social Intelligence: Memory, Nuance, and Presence for AI Agents**

### Purpose

Introduce Lumi Social Intelligence to a non-specialist but intelligent reader. The article should explain why modern agents need more than memory, tools, and larger context windows. They need social judgment: what to remember, how to interpret it, when to use it, when to ask, when to repair, and when to stay quiet.

### Reader

- AI-curious product people
- agent builders
- technically literate non-developers
- early Hermes users
- people interested in safer, more humane personal AI

### Spine

1. **The problem:** assistants remember badly, act clumsily, and confuse context with judgment.
2. **The insight:** social intelligence is not one feature; it is a layered loop.
3. **The architecture:** Lumi Layered Memory → Nuances → Presence.
4. **The promise:** agents that remember carefully, read the room better, and know when not to act.
5. **The boundary:** review, consent, repair, and restraint are product features.
6. **The first doorway:** Lumi Social Intelligence as the release surface, with Lumi for Hermes as the first preview.
7. **The human origin:** one non-developer, PM, QA thinker, and music producer shaping a social-intelligence layer through observation, testing, and product discipline.

### Tone

Accessible, warm, clear, and grounded. No hype. No “AI companion will change everything” fog machine. It should feel like an intelligent product essay with a human pulse.

### Must include

- The phrase **social-intelligence layer for agents**.
- The three-product architecture.
- Why memory alone is not enough.
- Why restraint matters.
- Review/consent/repair as first-class design principles.
- The single public doorway: **Lumi Social Intelligence**.
- The first host target: **Hermes Agent**.
- The creator framing: non-developer, project manager, QA, music producer.

### Avoid

- Over-personifying Lumi as a public character.
- Claiming universal emotional understanding.
- Unsupported OpenClaw claims.
- Exposing private implementation details.
- Making it sound like a chatbot persona pack.

## Article 2 — Technical Article: Lumi Layered Memory, Nuances, and Presence

### Working title

**Inside Lumi Social Intelligence: Layered Memory, Nuances, and Presence**

### Purpose

Explain the technical design and research context behind Lumi Social Intelligence. This article should show how the architecture relates to known problems in agent memory, contextual AI, human-agent interaction, evaluation, consent, safety, and agent governance.

### Reader

- AI engineers and researchers
- agent framework developers
- Hermes contributors/users
- product-minded technical readers
- NotebookLM as a research synthesis target

### Spine

1. **Agents need more than retrieval.** Memory must be inspectable, correctable, and context-aware.
2. **Layer 1: Lumi Layered Memory.** Stores useful continuity with review, receipts, boundaries, and revocation.
3. **Layer 2: Nuances.** Appraises moment-level signals: correction, consent, tone, uncertainty, emotional weight, and context shifts.
4. **Layer 3: Presence.** Governs initiative: speak, wait, ask, act, repair, or stay quiet.
5. **Review-first architecture.** Durable changes and proactive behavior should be inspectable before becoming live behavior.
6. **Evaluation model.** Synthetic fixtures, anti-pattern tests, release gates, public/secret scans, fail-closed behavior.
7. **Release architecture.** Private repos promote curated files into Lumi Social Intelligence through scripted gates.
8. **Research context.** Connect to memory systems, RAG, personal information management, contextual bandits/decision policies, HCI, trust calibration, consent, human-agent interaction, affective computing, and AI safety/evaluation.
9. **0.1.0 installable Hermes preview.** Package names, Hermes preview, review-gated behavior.

### Research/reference lanes to collect

The article should include technical references from these areas:

- Agent memory and long-term personalization
- Retrieval-augmented generation and memory-augmented systems
- Human-agent interaction and mixed-initiative systems
- Trust calibration and explainable AI
- Human-centered AI and consentful design
- Affective computing, social signal interpretation, and its limitations
- AI safety evaluation, red-teaming, and fail-closed design
- Software release engineering, CI gates, provenance, and artifact hygiene

### Must include

- `lumi-layered-memory`, `lumi-nuances`, `lumi-presence` as distribution names.
- The private-to-doorway promotion mechanics:

```text
Private repo passes release gate
→ export curated files via script
→ copy into Lumi Social Intelligence
→ run doorway release check
→ commit as release candidate
```

- Why Nuances does not directly mutate durable memory.
- Why Presence is the action/restraint gate.
- Why Autoresearch remains private harness/evidence, not public product.

### Avoid

- Claiming Lumi solves emotion recognition generally.
- Claiming memory is always beneficial.
- Treating social intelligence as sentiment analysis.
- Treating proactivity as automatically good.
- Publishing private Hermes internals.

## Article 3 — Creation Story of Lumi Social Intelligence

### Working title

**How Lumi Social Intelligence Was Created: From One-Person Concept to Social-Intelligence Layer for Hermes**

### Purpose

Tell the full creation story: why it was needed, who made it, how the concept emerged, how research and concepting shaped it, how it was implemented, how it was tested, and who it was created for.

This should be the most human article. It should still be rigorous, but it should preserve the strange, real path: one person noticing the gaps in agents not as an abstract developer problem, but as a PM/QA/music-producer problem of timing, trust, tone, dynamics, and failure modes.

### Reader

- NotebookLM as a narrative source
- future users who want to understand the project’s values
- collaborators/investors/reviewers
- AI product people
- non-developers who need to see that product architecture can come from observation, not only code

### Spine

1. **The origin:** a personal Hermes agent became capable enough that the remaining failures were no longer only technical. They were social: timing, memory use, overreach, under-response, tone, and repair.
2. **The creator:** one non-developer, project manager, QA thinker, and music producer concepting a full layer through product judgment, sensitivity to timing, and ruthless testing of awkward edges.
3. **The method of concepting:** naming the failure modes, clustering them, separating memory from interpretation from initiative, and refusing fake warmth.
4. **Research loop:** comparing the idea against agent memory, RAG, HCI, trust, consent, social signal interpretation, evaluation, and safety practices.
5. **Implementation path:** three cooperating modules, private development repos, public release doorway.
6. **Testing discipline:** synthetic fixtures, anti-patterns, release gates, public/secret scans, fail-closed behavior, review cards, and no uncontrolled live autonomy.
7. **Why it exists:** to make agents more useful without making them invasive; warmer without being manipulative; proactive without being noisy; adaptive without silently rewriting the user.
8. **Who it is for:** people who need AI to work with them over time — creators, project managers, researchers, operators, sensitive high-context users, and anyone who wants an assistant that can learn carefully without becoming creepy.
9. **The release path:** Lumi Social Intelligence as doorway; Lumi for Hermes first; public release only after gates pass.

### Must include

- “one man concepting a full social-intelligence layer for Hermes Agent.”
- Non-developer origin.
- Project manager / QA / music producer perspective.
- Research and implementation as iterative loops, not one grand invention moment.
- Rigorous testing and release gates.
- Why it was created and for whom.

### Avoid

- Mythologizing the creator as a lone genius.
- Making it sound accidental or purely emotional.
- Hiding the QA/testing discipline.
- Turning private intimacy into public product copy.
- Exposing private chat details, memories, coordinates, or live-system internals.

## Suggested writing order

1. **Creation Story** — captures the soul, origin, and why.
2. **Introduction** — turns that into public product understanding.
3. **Technical Article** — anchors the idea in architecture and research.

Alternative order if research comes first:

1. **Technical Article research pack**
2. **Introduction**
3. **Creation Story**

## Research pack needed before drafting

Before drafting the technical article, collect a source pack with:

- 8–12 academic or technical references on agent memory/RAG/personalization.
- 5–8 references on human-agent interaction, mixed initiative, trust calibration, and explainability.
- 4–6 references on consent, privacy, human-centered AI, or contextual integrity.
- 4–6 references on evaluation, red-teaming, fail-closed systems, and release engineering.
- 3–5 practical references from agent frameworks/runtime documentation, including Hermes Agent where appropriate.

Each reference note should include:

- title
- authors/organization
- year
- URL/DOI/arXiv ID
- why it matters to Lumi Social Intelligence
- which article section it supports

## NotebookLM packaging

Recommended files to provide to NotebookLM:

```text
articles/
  01-introduction-lumi-social-intelligence.md
  02-technical-lumi-layered-memory-nuances-presence.md
  03-creation-story-lumi-social-intelligence.md
research/
  references.md
  source-notes/
    agent-memory.md
    human-agent-interaction.md
    trust-consent-safety.md
    release-engineering.md
```

## Pre-sprint writing gate

Before implementation sprints begin, complete:

- [ ] Article 1 outline approved.
- [ ] Article 2 research pack collected.
- [ ] Article 2 outline approved.
- [ ] Article 3 story spine approved.
- [ ] All three article drafts written.
- [ ] Private detail/public boundary review completed.
- [ ] NotebookLM source bundle prepared.

Only then move into the 0.1.0 implementation sprints.
