# Technical References for Lumi Social Intelligence

This source pack supports the NotebookLM articles on **Lumi Social Intelligence**, especially the technical article on **Lumi Layered Memory**, **Nuances**, and **Presence**. The references are used as grounding lanes, not as claims that the project implements a specific paper exactly.

## Agent memory, RAG, and personalization

1. **Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks** — Patrick Lewis et al., 2020. arXiv:2005.11401. https://arxiv.org/abs/2005.11401
   Supports the distinction between retrieval as a capability and Lumi Social Intelligence’s additional need for reviewable memory use, contextual appraisal, and action governance.

2. **Reflexion: Language Agents with Verbal Reinforcement Learning** — Noah Shinn et al., 2023. arXiv:2303.11366. https://arxiv.org/abs/2303.11366
   Relevant to agent self-reflection and learning loops; Lumi’s boundary is that social learning should route through review and receipts before becoming durable behavior.

3. **Generative Agents: Interactive Simulacra of Human Behavior** — Joon Sung Park et al., 2023. arXiv:2304.03442. https://arxiv.org/abs/2304.03442
   Useful comparison point for memory, reflection, and planning in agent behavior, while Lumi focuses on personal-agent boundaries, consent, and restraint.

4. **MemGPT: Towards LLMs as Operating Systems** — Charles Packer et al., 2023. arXiv:2310.08560. https://arxiv.org/abs/2310.08560
   Supports the idea that long-running agents need explicit memory management rather than relying only on context windows.

5. **Toolformer: Language Models Can Teach Themselves to Use Tools** — Timo Schick et al., 2023. arXiv:2302.04761. https://arxiv.org/abs/2302.04761
   Useful background for tool-using agents. Lumi’s contribution is not tool use itself, but the social decision layer around when an agent should act, ask, wait, or repair.

6. **ReAct: Synergizing Reasoning and Acting in Language Models** — Shunyu Yao et al., 2022. arXiv:2210.03629. https://arxiv.org/abs/2210.03629
   Background for reasoning/action loops. Presence can be understood as a social and safety gate around such loops.

## Human-agent interaction, mixed initiative, trust, and explainability

7. **Guidelines for Human-AI Interaction** — Saleema Amershi et al., 2019. ACM CHI. DOI:10.1145/3290605.3300233. https://doi.org/10.1145/3290605.3300233
   Supports the need for interaction norms such as showing uncertainty, allowing correction, and supporting graceful recovery.

8. **Mixed-Initiative User Interfaces** — Eric Horvitz, 1999. CHI. DOI:10.1145/302979.303030. https://doi.org/10.1145/302979.303030
   Relevant to Lumi’s Presence layer: initiative should be governed, contextual, and interruptible, not treated as inherently good.

9. **Some Requirements for Human-like Robots: Why the Recent Over-Emphasis on Autonomy and Emotion is a Distraction** — Kerstin Dautenhahn, 2007. Philosophical Transactions of the Royal Society B. DOI:10.1098/rstb.2007.2059. https://doi.org/10.1098/rstb.2007.2059
   Useful caution against equating social intelligence with emotion-performance or autonomy theater.

10. **Why Should I Trust You? Explaining the Predictions of Any Classifier** — Marco Tulio Ribeiro, Sameer Singh, Carlos Guestrin, 2016. DOI:10.1145/2939672.2939778. https://doi.org/10.1145/2939672.2939778
   Background for explainability. Lumi applies the same spirit to memory and action: show receipts and reasons, not hidden drift.

## Consent, privacy, and human-centered AI

11. **Privacy as Contextual Integrity** — Helen Nissenbaum, 2004. Washington Law Review. https://crypto.stanford.edu/portia/papers/RevnissenbaumDTP31.pdf
   Supports the idea that whether information use is appropriate depends on context, relationship, purpose, and transmission norms — central to Nuances.

12. **Human-Centered AI** — Ben Shneiderman, 2020. Oxford University Press / related HCAI work. https://hcil.umd.edu/human-centered-ai/
   Supports a design stance where automation, human control, reliability, and accountability are balanced rather than collapsed into autonomy.

13. **The Consentful Tech Project** — Una Lee, Dann Toliver, and Allied Media Projects, 2017. https://www.consentfultech.io/
   Practical design lens for consent, agency, and respectful defaults; useful for memory review, correction, and revocation boundaries.

## Safety, evaluation, and release engineering

14. **Artificial Intelligence Risk Management Framework (AI RMF 1.0)** — NIST, 2023. https://www.nist.gov/itl/ai-risk-management-framework
   Supports the framing of risk management, measurement, governance, and documentation around AI systems.

15. **Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned** — Ganguli et al., 2022. arXiv:2209.07858. https://arxiv.org/abs/2209.07858
   Background for adversarial and anti-pattern testing; Lumi uses anti-pattern fixtures and release gates to catch unsafe social behavior before runtime.

16. **SLSA: Supply-chain Levels for Software Artifacts** — OpenSSF, specification v1.0. https://slsa.dev/spec/v1.0/
   Supports artifact provenance, build hygiene, and release discipline.

17. **Hermes Agent Documentation** — Nous Research, current docs. https://hermes-agent.nousresearch.com/docs
   Practical reference for the first planned host target, **Lumi for Hermes**. The articles should not expose private Hermes runtime state; they should discuss Hermes as a host runtime and adapter target.
