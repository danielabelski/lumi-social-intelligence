# Inside Lumi Social Intelligence: Layered Memory, Nuances, and Presence

Lumi Social Intelligence is a social-intelligence layer for agents: adaptive memory, nuance, and presence with review, consent, and repair. It is built from three cooperating products:

```text
Lumi Layered Memory -> Nuances -> Presence
```

The simplest technical description is:

```text
Lumi Layered Memory gives context.
Nuances reads the moment.
Presence decides whether to speak, wait, ask, act, repair, or stay quiet.
```

This architecture starts from a limitation in many agent systems. Retrieval, memory, and tool use can increase capability, but they do not automatically create social judgment. A retrieval-augmented system may find the right fact and still use it at the wrong time. A memory system may store useful preferences but fail to distinguish durable preference from temporary mood. A tool-using agent may be able to act, but still lack a principled reason to decide whether acting is appropriate.

Lumi Social Intelligence treats memory, interpretation, and action as separate layers that must cooperate under review. This separation is the main technical idea.

## 1. Why agents need more than retrieval

Retrieval-augmented generation showed that language models can be grounded with external knowledge instead of relying only on model weights. That is useful, but personal agents need a stricter problem statement. They are not merely retrieving public facts. They are handling continuity about a person, a workflow, projects, preferences, corrections, private constraints, and sometimes emotionally weighted context.

That changes the requirements. Personal memory needs provenance. It needs revocation. It needs a difference between “the user said this once” and “this is a stable preference.” It needs a way to show why a memory was used. It needs boundaries around what should never become public release material. It also needs humility, because a remembered sentence is not the same thing as a full understanding of a person.

Agent memory projects such as Generative Agents, MemGPT, Reflexion, ReAct, and related long-context or tool-using agent work provide useful background. They show how memory, reflection, planning, and action can improve agent behavior. Lumi Social Intelligence borrows from that larger research landscape but focuses on a narrower public product question: how should an agent remember, interpret, and act around a real user without creating hidden personalization, unwanted intimacy, noisy initiative, or unreviewable drift?

## 2. Layer one: Lumi Layered Memory

**Lumi Layered Memory** is the continuity layer. Its role is not to remember everything. Its role is to preserve useful continuity with clean boundaries.

The public contract is:

- durable memory is reviewable;
- memory use can be explained with receipts;
- corrections and revocations matter;
- private runtime state does not become public release material;
- identity, preferences, and durable user facts are not silently rewritten.

A layered memory system should distinguish between different kinds of remembered information. A stable user preference is not the same as a project note. A project note is not the same as a private emotional signal. A correction is not automatically a personality rule. A transient context cue should not become durable memory without a reason.

This is why Lumi Layered Memory is designed as the first layer rather than the whole system. Memory supplies context, but it does not decide alone what the current moment means. It should provide candidate continuity, citations, and receipts. It should make memory visible enough to review. But it should not silently mutate the assistant’s behavior whenever it sees a signal.

## 3. Layer two: Nuances

**Nuances** is the contextual appraisal layer. It sits between memory and action.

Nuances asks what a memory, correction, tone shift, uncertainty signal, or contextual cue might mean right now. Its job is not to mind-read. Its job is to preserve ambiguity while noticing useful signals. That distinction is important. Social intelligence in agents should not become fake certainty about a user’s inner state.

Nuances handles questions such as:

- Is this correction likely a durable preference or a one-time adjustment?
- Is the user asking for action, reflection, silence, or a small answer?
- Is a remembered fact relevant here, or would using it feel invasive?
- Is the assistant about to over-explain, over-comfort, or over-personalize?
- Is there enough evidence to adapt, or should the system ask first?
- Does the moment carry emotional weight that should slow the assistant down?

Nuances does not directly mutate durable memory. That is a key boundary. It may propose an interpretation, mark uncertainty, suggest a review card, or route a signal toward a later decision. But durable learning should remain inspectable. Otherwise, nuance becomes hidden profiling.

In research terms, Nuances connects to human-agent interaction, mixed-initiative systems, trust calibration, explainability, affective computing, and contextual privacy. But it intentionally avoids the trap of treating social intelligence as sentiment analysis. A sentiment score cannot tell an agent whether it should speak, ask, repair, or leave a moment alone. Nuances is about contextual appraisal under uncertainty, not emotion detection as a product promise.

## 4. Layer three: Presence

**Presence** is the governed initiative layer. It decides whether the assistant should speak, wait, ask, act, repair, or stay quiet.

Presence exists because capability creates temptation. Once an agent can remember, infer, schedule, send, automate, and run tools, the question is no longer only “can it?” The question becomes “should it, now, with this confidence, under these permissions, and with this evidence?”

Presence is the action and restraint gate. It should support outcomes like:

- speak with a short answer;
- ask a clarifying question;
- wait because the user is focused;
- suggest but do not act;
- prepare a review card;
- repair a prior mistake;
- stay quiet because the moment is not asking for intervention;
- fail closed because memory, configuration, confidence, or permission is insufficient.

Presence treats restraint as a feature. This is a product decision and a safety decision. Proactive agents often fail not because they lack capability, but because they lack a good model of interruption, consent, timing, and social cost. Presence makes those costs explicit.

## 5. Review-first architecture

The core governance principle is review first. Durable memory changes and proactive behavior should be inspectable before they become live behavior.

This can be implemented through review cards, synthetic fixtures, dry-run mode, release gates, and visible receipts. A review card can show what the system thinks it noticed, what evidence supports it, what uncertainty remains, and what action Presence would choose. That makes the system correctable. It also separates evaluation from live side effects.

A review-first architecture is especially important for social-intelligence work because the system deals with high-context signals. A bug in a calculator is visible. A bug in a social memory system can become a quiet behavioral drift. The user may not immediately know what changed or why. Review surfaces make the hidden layer visible.

## 6. Evaluation model

Lumi Social Intelligence should be tested with synthetic fixtures, anti-pattern tests, public/secret scans, and release gates.

Synthetic fixtures allow the project to test social behavior without exposing private chat logs or personal memories. Anti-pattern tests can cover overfamiliarity, unsupported inference, fake warmth, noisy initiative, memory overreach, unreviewed adaptation, and failure to repair. Release gates can verify that public-facing files use the correct product names, include required licensing, and avoid private/local material.

For 0.1.0, the system should remain review-gated and fail-closed. It should not introduce uncontrolled live autonomous behavior. A safe preview is not the same thing as a fully live social agent. The first release target is inspectability and installable structure, not dramatic autonomy.

The release doorway currently expects package/distribution names:

```text
lumi-layered-memory
lumi-nuances
lumi-presence
```

The first planned host-specific distribution is **Lumi for Hermes**.

## 7. Release architecture

Development happens in private repositories:

- **Lumi Layered Memory**
- **Nuances**
- **Presence**
- **Autoresearch**

Release candidates are promoted into **Lumi Social Intelligence**, the public-facing release doorway.

The promotion path is:

```text
Private repo passes release gate
→ export curated files via script
→ copy into Lumi Social Intelligence
→ run doorway release check
→ commit as release candidate
```

This separation lets the private workshop remain experimental while the public doorway stays clean. It also protects against accidental exposure of raw runs, private memories, local runtime state, scheduler internals, credentials, chat IDs, coordinates, and unverified host claims.

**Autoresearch** remains private harness and evidence infrastructure. It is not the public product surface. That distinction is important: evidence-gathering machinery may contain internal experiments, local assumptions, evaluation data, and private iteration trails that should not be exposed as user-facing product.

## 8. Research context

Lumi Social Intelligence sits at the intersection of several research and engineering lanes.

From retrieval-augmented generation and memory-augmented agents, it takes the idea that models need external context and persistent state. From agent systems such as ReAct, Reflexion, MemGPT, and Generative Agents, it takes the observation that memory, reflection, and action loops can improve behavior over time. But it adds a product boundary: personal-agent memory should be reviewable, correctable, and context-aware.

From human-agent interaction and mixed-initiative research, it takes the importance of timing, initiative, uncertainty, and graceful handoff. Eric Horvitz’s mixed-initiative work is especially relevant because Presence is fundamentally a mixed-initiative gate. The assistant may initiate sometimes, but initiative must be governed.

From explainable AI and trust calibration, it takes the need for receipts. A user should be able to understand why a memory was used or why an action was proposed. Trust should not be produced by soothing language. It should be produced by visible behavior, correction paths, and recoverability.

From contextual integrity and consentful design, it takes the view that information use depends on context, purpose, and relationship. A fact being available does not mean it is appropriate to use. A memory being true does not mean it should be surfaced now. Nuances exists partly to handle that distinction.

From AI safety, red-teaming, and release engineering, it takes the habit of testing failure modes before runtime. Fail-closed behavior, anti-pattern fixtures, artifact hygiene, and public/secret scans are not separate from social intelligence. They are how social intelligence avoids becoming a nice story wrapped around unsafe automation.

## 9. Why this architecture is deliberately conservative

The conservative parts of Lumi Social Intelligence are not signs of weakness. They are the product.

A system that can remember a user over time should be slower to infer than a stateless chatbot. A system that can act should be more careful about permission than a system that only talks. A system that can adapt socially should show its reasoning and leave room for correction. The more personal the agent becomes, the more important it is that learning remains inspectable.

This is why the 0.1.0 scope is an installable Hermes preview with review gates, synthetic fixtures, and fail-closed behavior. The first milestone should prove the shape: memory provides context, Nuances appraises the moment, Presence governs initiative, and the release doorway keeps public artifacts clean.

Lumi Social Intelligence is not trying to make agents perform emotion. It is trying to make them safer and more useful at the boundary between memory and action. That is where many long-running assistants will either earn trust or lose it.

## References

The companion file `references.md` contains the technical reference pack used for this article, including work on retrieval-augmented generation, agent memory, mixed-initiative interaction, human-AI guidelines, contextual integrity, consentful design, AI risk management, red-teaming, supply-chain artifact hygiene, and Hermes Agent documentation.
