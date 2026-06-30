# CLAUDE.md — Microservices / Distributed System Architecture Audit

**Skill name:** `microservices-architecture-audit`
**Tagline:** Audit distributed-system architecture for resilience, scalability, and observability.
**Source idea:** #93 (cluster: `software-devops`)
**Current phase:** Phase 4 — Testing & Validation (initial build complete)

## Problem This Skill Solves
Engineering teams accumulate architectural debt — chatty services, missing circuit breakers, weak observability — that surfaces only during incidents. They need a rigorous, standards-based audit.

## Harness Flow Summary
1. **sub-evaluation-framework-selector** → Bind the audit to named, citable technical standards so findings are defensible.
2. **sub-scoring-engine** → Produce a transparent, dimension-by-dimension score (0-100 or band) with evidence for every sub-score.
3. **sub-improvement-roadmap** → Convert weaknesses into a sequenced, effort/impact-ranked action plan the user can execute.
4. **sub-resilience-probe** → Walk through partition, dependency-failure, and load-spike scenarios to expose hidden single points of failure.
5. **main (synthesis)** → assemble the scored deliverable + prioritized roadmap and run final quality gates.

## Gates
No safety/compliance gate applies to this cluster; standard quality gates still apply.

## Sub-skills
- `skills/sub-evaluation-framework-selector.md` — Select the governing distributed-systems standards/heuristics for this evaluation.
- `skills/sub-scoring-engine.md` — Multi-dimensional scoring of the architecture against the selected framework.
- `skills/sub-improvement-roadmap.md` — Prioritized improvement roadmap for the architecture with effort/impact.
- `skills/sub-resilience-probe.md` — Stress-test the design against failure scenarios (Socratic devil's advocate).

## Tools Required
WebSearch, WebFetch, Read, Write, Bash

## Knowledge Sources
- [AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)
- [Google SRE Books](https://sre.google/books/)
- [CNCF / OpenTelemetry](https://opentelemetry.io)
- [Microservices.io patterns](https://microservices.io)

ArXiv / research categories crawled: cs.DC, cs.SE

## Supporting Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that refreshes `SECOND-KNOWLEDGE-BRAIN.md` weekly from the sources above.

## Active Development Tasks
- [x] Scaffold deliverables and sub-skills
- [x] Define scoring dimensions against named frameworks
- [ ] Expand `SECOND-KNOWLEDGE-BRAIN.md` with first crawl batch
- [ ] Add 3 more adversarial test scenarios
- [ ] Wire shared cluster sub-skills for reuse

## Reference Docs
- `PROJECT-detail.md` — full technical spec
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — phase roadmap
- `SECOND-KNOWLEDGE-BRAIN.md` — living domain knowledge base
