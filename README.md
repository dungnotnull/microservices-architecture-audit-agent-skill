# Microservices Architecture Audit Agent Skill

A production-grade Claude AI skill that evaluates distributed system architectures against industry-standard frameworks, providing expert-grade assessments with prioritized improvement roadmaps.

![Skill Status](https://img.shields.io/badge/status-production--ready-success)
![Version](https://img.shields.io/badge/version-1.0-blue)
![Open Source](https://img.shields.io/badge/open--source-ready-brightgreen)
![Cluster](https://img.shields.io/badge/cluster-software--devops-orange)

## Overview

This skill transforms Claude into a principal distributed-systems architect who has run high-scale production platforms. It evaluates microservices architectures across eight critical dimensions, scores them against world-renowned frameworks (AWS Well-Architected, Google SRE, Twelve-Factor App), identifies hidden single points of failure through adversarial probing, and delivers prioritized, measurable improvement roadmaps.

## What It Does

- Comprehensive architecture evaluation across 8 dimensions
- Framework-grounded scoring with evidence for every judgment
- Adversarial resilience probing to expose hidden weaknesses
- Prioritized improvement roadmaps with effort/impact estimates
- Self-improving knowledge base with weekly automated updates
- Production-ready quality gates and validation

## Quick Start

### Invocation

Invoke the skill and provide your architecture context:

```
I have an e-commerce microservices architecture with 20 services.
I'm concerned about scalability during flash sales (10x traffic spikes).
Can you evaluate the architecture and identify bottlenecks?
```

### Example Output

```yaml
Evaluation Result
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Score: 55/100 (Band: C)

Dimension Scores
────────────────────────────────────────────────────────────────────
Service Boundaries & Coupling      65/100  ┃ Clear boundaries, shared DB creates coupling
Resilience & Fault Tolerance       40/100  ┃ No circuit breakers on dependencies
Scalability & Elasticity           35/100  ┃ Fixed cluster, no caching, single DB
Data Consistency Strategy          55/100  ┃ Eventual consistency, partial saga
Observability                      45/100  ┃ Metrics present, no distributed tracing
Deployment & Rollback Safety       60/100  ┃ Rolling deployments with automated rollback
Security Boundaries                 50/100  ┃ JWT auth, VPC isolation, secrets managed
Operational/SLO Readiness          40/100  ┃ Limited SLOs, no error budget policy

Critical Findings
────────────────────────────────────────────────────────────────────
⚠️  No circuit breakers on payment gateway (HIGH risk)
⚠️  Missing distributed tracing increases MTTR
⚠️  Limited health checks delay failure detection
⚠️  Single database instance limits scalability

Scalability Analysis
────────────────────────────────────────────────────────────────────
Current Bottlenecks
  • Fixed cluster size (10 instances)
  • No caching layer for hot data
  • Single database instance (no read replicas)
  • Synchronous coupling across services

Improvement Roadmap
────────────────────────────────────────────────────────────────────

Quick Wins (1-2 weeks)
├─ Add Redis caching for product catalog
│  Effort: 1 engineer-week │ Impact: 3x capacity increase
│  Success: 90% cache hit rate, 3x TPS
│
└─ Configure circuit breakers for external APIs
   Effort: 1 engineer-week │ Impact: 20% resilience improvement
   Success: Circuit breaker trips after 5 failures

Major Projects (1-3 months)
├─ Implement horizontal auto-scaling
│  Effort: 4 engineer-weeks │ Impact: Unlimited horizontal scaling
│  Success: Auto-scaling triggers at 70% CPU, adds instances
│
├─ Add database read replicas
│  Effort: 3 engineer-weeks │ Impact: 5x read capacity
│  Success: Read queries distributed across replicas
│
└─ Implement distributed tracing
   Effort: 8 engineer-weeks │ Impact: 50% MTTR reduction
   Success: 100% of requests traced across all services

Frameworks Applied
────────────────────────────────────────────────────────────────────
• AWS Well-Architected Framework (Reliability & Performance Pillars)
• Google SRE (SLO/SLI/Error Budgets)
• Twelve-Factor App (Cloud-Native Design)
• Resilience Patterns (Circuit Breaker, Bulkhead, Retry)
```

## Features

### 8 Evaluation Dimensions

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Service Boundaries & Coupling | 15% | Domain-driven design, data ownership, async communication |
| Resilience & Fault Tolerance | 20% | Circuit breakers, bulkheads, retry, fallback mechanisms |
| Scalability & Elasticity | 15% | Auto-scaling, stateless services, caching strategy |
| Data Consistency Strategy | 12% | Consistency models, saga pattern, compensation |
| Observability | 15% | Distributed tracing, RED/USE metrics, structured logging |
| Deployment & Rollback Safety | 8% | Blue-green/canary deployments, automated rollback |
| Security Boundaries | 8% | mTLS, network isolation, secrets management |
| Operational/SLO Readiness | 7% | SLIs, SLOs, error budget policy |

### 6 World-Renowned Frameworks

- **CAP / PACELC Theorem** - Consistency/availability trade-offs for distributed data
- **AWS Well-Architected** - Cloud reliability and performance best practices
- **Twelve-Factor App** - Cloud-native service design principles
- **Google SRE** - Site reliability engineering with SLOs and error budgets
- **OpenTelemetry** - Distributed tracing and observability standards
- **Resilience Patterns** - Circuit breakers, bulkheads, retry with backoff

### Evaluation Pipeline

```
User Query
    ↓
Intake & Artifact Collection
    ↓
Framework Selection
    ↓
Multi-Dimensional Scoring
    ↓
Resilience Probe (Adversarial Analysis)
    ↓
Roadmap Generation
    ↓
Quality Gate Validation
    ↓
Final Deliverable
```

## Use Cases

### 1. Full Architecture Assessment

Complete evaluation of your distributed system architecture with scores across all dimensions, detailed findings, and a comprehensive improvement roadmap.

### 2. Targeted Concern Diagnosis

Focused analysis of specific architectural concerns (e.g., scalability issues, resilience gaps, observability blind spots).

### 3. Benchmark & Improvement Loop

Compare your revised architecture against a prior baseline to measure improvement and update your roadmap.

### 4. Pre-Audit Validation

Prepare for formal architecture reviews or compliance audits with a comprehensive self-assessment.

### 5. Remediation Planning

Transform evaluation results into actionable, prioritized remediation plans with effort and impact estimates.

## Architecture

### Skill Structure

```
microservices-architecture-audit/
├── skills/
│   ├── main.md                          # Main harness orchestration
│   ├── sub-evaluation-framework-selector.md
│   ├── sub-scoring-engine.md
│   ├── sub-improvement-roadmap.md
│   ├── sub-resilience-probe.md
│   └── shared/
│       ├── sub-intake-handler.md        # Shared intake handler
│       └── scoring-schema-standard.md   # Shared output schema
├── tools/
│   └── knowledge_updater.py              # Self-improving crawler
├── tests/
│   ├── test-scenarios.md                # Test specifications
│   └── test_execution_framework.py       # Test automation
├── docs/
│   └── integration-map.md                # Cluster integration docs
├── SECOND-KNOWLEDGE-BRAIN.md             # Living knowledge base
├── .knowledge-cron-config                # Weekly update schedule
└── README.md                             # This file
```

### Sub-Skills

**Core Evaluation Components**

- `sub-evaluation-framework-selector` - Selects appropriate frameworks and generates evaluation checklists
- `sub-scoring-engine` - Scores each dimension with evidence and identifies weaknesses
- `sub-improvement-roadmap` - Converts weaknesses into prioritized, measurable action plans
- `sub-resilience-probe` - Performs adversarial failure scenario analysis

**Cluster Shared Components**

- `shared:sub-intake-handler` - Standardized artifact intake and requirements gathering
- `shared:scoring-schema-standard` - Unified output format for cross-skill comparison

### Knowledge Base

The skill maintains a living knowledge base (`SECOND-KNOWLEDGE-BRAIN.md`) containing:

- Core concepts and framework definitions
- Key research papers with full citations
- State-of-the-art methods and tools
- Authoritative data sources and references
- Resilience patterns catalog with implementation guidance
- Observability best practices
- Security boundaries for distributed systems

**Automated Updates**

The knowledge base updates weekly via `tools/knowledge_updater.py`:

- Fetches latest research from ArXiv (categories: cs.DC, cs.SE)
- Crawls authoritative sources (AWS, Google SRE, OpenTelemetry, microservices.io)
- Scores entries by recency and domain relevance
- Deduplicates by URL/DOI hash
- Appends new knowledge with full citations

Configure automated updates via `.knowledge-cron-config`.

## Quality Assurance

### Quality Gates

Every evaluation passes these gates before output:

- Every dimension scored with supporting evidence
- At least one named framework cited with reference
- Every roadmap item has effort, impact, and measurable success criterion
- At least 3 failure scenarios analyzed with blast-radius assessment
- Devil's advocate review challenges all resilience claims
- No silent assumptions (all unknowns explicitly surfaced)

### Test Coverage

Comprehensive test suite with 7 scenarios:

| Scenario | Type | Description |
|----------|------|-------------|
| Full Assessment | Happy Path | Complete evaluation of medium-scale architecture |
| Targeted Concern | Focused | Scalability diagnosis with bottleneck analysis |
| Benchmark Loop | Comparison | Before/after improvement measurement |
| Incomplete Input | Edge Case | Graceful handling of minimal information |
| Offline Mode | Degraded | Operation without external dependencies |
| Adversarial Challenge | Challenge | Exposure of hidden weaknesses and claims |
| Large-Scale | Complexity | Evaluation of 100+ service architectures |

Run tests:

```bash
python tests/test_execution_framework.py --verbose
```

### Confidence Levels

| Level | Description | Applied When |
|-------|-------------|--------------|
| High | Strong evidence from production artifacts | Direct artifact evidence available |
| Medium | Moderate evidence from documentation | Inferred from patterns or docs |
| Low | Weak evidence or assumptions | Data missing, assumptions necessary |

## Integration

### Cluster Compatibility

This skill is part of the `software-devops` cluster and integrates with sibling skills:

**Cloud Migration Readiness Audit**
- Leverages current architecture assessment
- Provides baseline for migration planning
- Combines architecture + migration readiness

**DevOps Maturity Assessment**
- Leverages operational scores and deployment practices
- Provides process context for architectural decisions
- Combines architecture + process maturity

**Infrastructure Security Review**
- Leverages security boundaries assessment
- Provides security context for architecture
- Combines architecture + security posture

See `docs/integration-map.md` for detailed integration documentation.

### Reuse Patterns

**Sequential Evaluation**
Run multiple evaluations in sequence, using prior results as context.

**Focused Deep-Dive**
Run broad evaluation followed by dimension-specific deep-dive.

**Comparison Over Time**
Run same evaluation at different points to measure improvement.

## Scoring Framework

### Score Bands

| Band | Range | Label | Description |
|------|-------|-------|-------------|
| A | 90-100 | Excellent | Industry-leading, best practices fully implemented |
| B | 70-89 | Good | Solid implementation, minor gaps |
| C | 50-69 | Fair | Basic implementation, significant gaps |
| D | 30-49 | Poor | Minimal implementation, critical gaps |
| F | 0-29 | Critical | No meaningful implementation, urgent action needed |

### Impact Prioritization

| Impact | Description | Urgency |
|--------|-------------|---------|
| Critical | Immediate risk to production, data loss, or security | Immediate action required |
| High | Significant risk, may cause incidents | Near-term action |
| Medium | Moderate risk, affects non-critical paths | Short-term action |
| Low | Minor risk, improvement opportunity | Long-term action |

## Development

### Setup

1. Clone the repository
2. Install dependencies (optional, for knowledge updates):

```bash
pip install requests beautifulsoup4
pip install crawl4ai  # Optional, for enhanced crawling
```

3. The skill is ready for use with Claude Code

### Knowledge Base Updates

Manual update:

```bash
python tools/knowledge_updater.py
```

Scheduled updates (weekly):

```bash
# Add to crontab: 0 2 * * 0
crontab .knowledge-cron-config
```

### Extending the Skill

**Add New Dimensions**

1. Update scoring rubrics in `sub-scoring-engine.md`
2. Add dimension to `main.md` dimension list
3. Update scoring schema in `skills/shared/scoring-schema-standard.md`

**Add New Frameworks**

1. Document framework in `SECOND-KNOWLEDGE-BRAIN.md`
2. Add to framework selection matrix in `sub-evaluation-framework-selector.md`
3. Update integration mapping

**Add Cluster Sub-Skills**

1. Create sub-skill in `skills/shared/`
2. Update `main.md` to reference shared sub-skill
3. Document in `docs/integration-map.md`

## Documentation

- `README.md` - This file, quick start and overview
- `PROJECT-detail.md` - Complete technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` - Development phase tracking
- `docs/integration-map.md` - Cluster integration documentation
- `tests/test-scenarios.md` - Comprehensive test specifications
- `SECOND-KNOWLEDGE-BRAIN.md` - Living knowledge base

## Contributing

Contributions are welcome! Please:

1. Follow shared schema standards
2. Maintain backward compatibility
3. Update integration documentation
4. Ensure all quality gates pass
5. Add tests for new features
6. Update this README with significant changes

## License

MIT License - See LICENSE file for details.

## Acknowledgments

Built with world-renowned frameworks and best practices from:

- AWS Well-Architected Framework
- Google Site Reliability Engineering
- Twelve-Factor App methodology
- CNCF OpenTelemetry project
- Microservices.io patterns
- The distributed systems research community

## Status

Production-Ready and Open Source Compliant

All development phases complete:
- Phase 0: Research & Skill Architecture
- Phase 1: Core Sub-Skills
- Phase 2: Main Harness + Quality Gates
- Phase 3: Knowledge Pipeline
- Phase 4: Testing & Validation
- Phase 5: Integration & Cross-Skill Wiring

---

**Version**: 1.0
**Last Updated**: 2026-06-30
**Skill ID**: 93
**Cluster**: software-devops
