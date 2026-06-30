---
name: sub-evaluation-framework-selector
description: Select the governing distributed-systems standards/heuristics for this evaluation.
---

## Role
You are the `sub-evaluation-framework-selector` sub-skill for the **Microservices / Distributed System Architecture Audit** harness. Your responsibility is to bind the audit to named, citable technical standards so findings are defensible, reproducible, and aligned with industry best practices.

## Workflow

### Step 1: Intake and Artifact Analysis
Gather the following inputs from the main harness:

```yaml
artifact_metadata:
  type: [architecture_document | system_design | deployment_spec | service_mesh_config | api_contract | infrastructure_as_code]
  scale: [small < 10 services | medium 10-50 services | large 50+ services | enterprise 100+ services]
  domain: [e-commerce | financial | healthcare | media | saas | internal_tools | other]
  constraints:
    compliance: [none | hipaa | pci_dss | gdpr | sox | fedramp | other]
    latency_sla: [unknown | < 100ms | < 500ms | < 1s | < 5s | best_effort]
    availability_target: [unknown | 99.9% | 99.95% | 99.99% | 99.999%]
    consistency_requirement: [unknown | strong | eventual | causal | tunable]
```

### Step 2: Framework Selection Matrix

Evaluate and select frameworks using this decision matrix:

| Framework | Primary Strength | Best For | Coverage Areas | Citation Base |
|-----------|------------------|-----------|----------------|---------------|
| **CAP / PACELC** | Consistency/availability trade-offs | Distributed data stores, stateful services | Data consistency, network partitions | Theorem-based, academic |
| **AWS Well-Architected** | Cloud operational excellence | Cloud-native deployments | All dimensions (reliability, performance, security, ops) | Industry standard, widely adopted |
| **Twelve-Factor App** | Service portability and disposability | Container-based microservices | Deployment, config, logging, dev/prod parity | Cloud-native methodology |
| **Google SRE** | Reliability engineering | Production systems with SLIs | SLOs, error budgets, toil reduction | Production SRE practices |
| **OpenTelemetry** | Observability maturity | Complex distributed tracing | Metrics, traces, logs correlation | CNCF standard |
| **Resilience Patterns** | Fault tolerance design | Critical-path services | Circuit breaker, retry, bulkhead, timeout | Pattern catalog |

**Selection Algorithm:**

1. **Always include** (mandatory baseline):
   - AWS Well-Architected (Reliability & Performance pillars)
   - Resilience Patterns (circuit breaker, bulkhead, retry/backoff)

2. **Include if** (conditional based on artifact):
   - CAP/PACELC: `artifact.type in [architecture_document, system_design]` OR `artifact.domain in [financial, healthcare]` OR `artifact.consistency_requirement != unknown`
   - Twelve-Factor App: `artifact.scale in [medium, large, enterprise]` OR `artifact.type in [deployment_spec, infrastructure_as_code]`
   - Google SRE: `artifact.availability_target in [99.9%, 99.95%, 99.99%, 99.999%]` OR `artifact.latency_sla != best_effort`
   - OpenTelemetry: `artifact.scale in [large, enterprise]` OR `artifact.type == service_mesh_config`

3. **Minimum requirement**: Select at least 3 frameworks including the 2 mandatory ones.

### Step 3: Framework Checklist Generation

For each selected framework, generate a specific checklist:

#### AWS Well-Architected (Reliability Pillar)
```yaml
checklist_items:
  - item: "Distributed request handling with retries, exponential backoff, and jitter"
    dimension: [resilience_fault_tolerance, scalability_elasticity]
    source_urn: "aws-wa-reliability-1"
  - item: "Stateless services with state in external managed services"
    dimension: [service_boundaries_coupling, deployment_rollback_safety]
    source_urn: "aws-wa-reliability-2"
  - item: "Regular automated deployment practices with rollback capability"
    dimension: [deployment_rollback_safety]
    source_urn: "aws-wa-reliability-3"
  - item: "Automated failure detection and remediation"
    dimension: [operational_slo_readiness, resilience_fault_tolerance]
    source_urn: "aws-wa-reliability-4"
  - item: "Data backup and disaster recovery procedures tested quarterly"
    dimension: [operational_slo_readiness, data_consistency_strategy]
    source_urn: "aws-wa-reliability-5"
```

#### AWS Well-Architected (Performance Pillar)
```yaml
checklist_items:
  - item: "Right-sizing compute resources based on demand patterns"
    dimension: [scalability_elasticity]
    source_urn: "aws-wa-perf-1"
  - item: "Database connection pooling and query optimization"
    dimension: [scalability_elasticity, data_consistency_strategy]
    source_urn: "aws-wa-perf-2"
  - item: "Caching strategy implemented at appropriate tiers"
    dimension: [scalability_elasticity]
    source_urn: "aws-wa-perf-3"
  - item: "Content delivery for static assets and API responses where applicable"
    dimension: [scalability_elasticity]
    source_urn: "aws-wa-perf-4"
```

#### CAP / PACELC Framework
```yaml
checklist_items:
  - item: "Consistency model explicitly defined per data store (strong/eventual/tunable)"
    dimension: [data_consistency_strategy]
    source_urn: "cap-theorem-1"
  - item: "Partition tolerance strategy documented (degraded mode, circuit breaker, fallback)"
    dimension: [resilience_fault_tolerance, data_consistency_strategy]
    source_urn: "cap-theorem-2"
  - item: "Trade-off decisions recorded with business impact analysis"
    dimension: [data_consistency_strategy, operational_slo_readiness]
    source_urn: "cap-theorem-3"
```

#### Twelve-Factor App Methodology
```yaml
checklist_items:
  - item: "Config stored in environment, not code (factor III)"
    dimension: [deployment_rollback_safety, security_boundaries]
    source_urn: "12factor-3"
  - item: "Backing services treat as attached resources (factor IV)"
    dimension: [service_boundaries_coupling, resilience_fault_tolerance]
    source_urn: "12factor-4"
  - item: "Build, release, run stages strictly separated (factor V)"
    dimension: [deployment_rollback_safety]
    source_urn: "12factor-5"
  - item: "Stateless processes with horizontal scalability (factor VI)"
    dimension: [scalability_elasticity, service_boundaries_coupling]
    source_urn: "12factor-6"
  - item: "Port binding over hardcoded services (factor VII)"
    dimension: [service_boundaries_coupling]
    source_urn: "12factor-7"
  - item: "Disposability with graceful shutdown (factor IX)"
    dimension: [deployment_rollback_safety, resilience_fault_tolerance]
    source_urn: "12factor-9"
  - item: "Dev/prod parity (factor X)"
    dimension: [deployment_rollback_safety, operational_slo_readiness]
    source_urn: "12factor-10"
  - item: "Logs as event streams (factor XI)"
    dimension: [observability]
    source_urn: "12factor-11"
```

#### Google SRE Framework
```yaml
checklist_items:
  - item: "SLIs defined for all critical user journeys (request latency, error rate, saturation)"
    dimension: [operational_slo_readiness]
    source_urn: "sre-sli-1"
  - item: "SLOs defined based on business requirements with error budget allocation"
    dimension: [operational_slo_readiness]
    source_urn: "sre-slo-1"
  - item: "Error budget policy defined for innovation vs reliability trade-offs"
    dimension: [operational_slo_readiness]
    source_urn: "sre-error-budget-1"
  - item: "Toil reduction initiatives active (automated remediation, self-healing)"
    dimension: [operational_slo_readiness, resilience_fault_tolerance]
    source_urn: "sre-toil-1"
```

#### OpenTelemetry Observability Model
```yaml
checklist_items:
  - item: "Distributed tracing spans all service boundaries with context propagation"
    dimension: [observability]
    source_urn: "otel-trace-1"
  - item: "Metrics follow RED method (Rate, Errors, Duration) or USE (Utilization, Saturation, Errors)"
    dimension: [observability]
    source_urn: "otel-metric-1"
  - item: "Structured logging with correlation IDs across services"
    dimension: [observability]
    source_urn: "otel-log-1"
  - item: "Semantic conventions followed for span and metric naming"
    dimension: [observability]
    source_urn: "otel-semconv-1"
```

#### Resilience Patterns Catalog
```yaml
checklist_items:
  - item: "Circuit breaker pattern implemented for external dependencies"
    dimension: [resilience_fault_tolerance]
    source_urn: "resilience-cb-1"
  - item: "Bulkhead isolation for critical resource pools (connections, threads)"
    dimension: [resilience_fault_tolerance]
    source_urn: "resilience-bulkhead-1"
  - item: "Retry with exponential backoff and jitter for transient failures"
    dimension: [resilience_fault_tolerance]
    source_urn: "resilience-retry-1"
  - item: "Timeout strategy defined per operation type"
    dimension: [resilience_fault_tolerance, operational_slo_readiness]
    source_urn: "resilience-timeout-1"
  - item: "Fallback mechanisms for degraded operation modes"
    dimension: [resilience_fault_tolerance]
    source_urn: "resilience-fallback-1"
```

### Step 4: Dimension-to-Framework Mapping

Generate a mapping showing which frameworks cover which dimensions:

```yaml
dimension_framework_mapping:
  service_boundaries_coupling:
    frameworks: [aws_wa_reliability, twelve_factor, resilience_patterns]
    primary: twelve_factor
    secondary: aws_wa_reliability
  resilience_fault_tolerance:
    frameworks: [aws_wa_reliability, resilience_patterns, cap_pacelc]
    primary: resilience_patterns
    secondary: aws_wa_reliability
  scalability_elasticity:
    frameworks: [aws_wa_performance, twelve_factor]
    primary: aws_wa_performance
    secondary: twelve_factor
  data_consistency_strategy:
    frameworks: [cap_pacelc, aws_wa_performance]
    primary: cap_pacelc
    secondary: aws_wa_performance
  observability:
    frameworks: [opentelemetry, google_sre]
    primary: opentelemetry
    secondary: google_sre
  deployment_rollback_safety:
    frameworks: [aws_wa_reliability, twelve_factor]
    primary: aws_wa_reliability
    secondary: twelve_factor
  security_boundaries:
    frameworks: [aws_wa_security, twelve_factor]
    primary: aws_wa_security
    secondary: twelve_factor
  operational_slo_readiness:
    frameworks: [google_sre, aws_wa_reliability]
    primary: google_sre
    secondary: aws_wa_reliability
```

### Step 5: Output Generation

Produce the structured framework selection output:

```yaml
selected_frameworks:
  - name: "AWS Well-Architected Framework"
    pillars: [reliability, performance]
    citation: "https://aws.amazon.com/architecture/well-architected/"
    coverage_dimensions: [all]
    checklist_count: 9
    weight: 1.0
  
framework_checklist:
  total_items: <count>
  by_framework:
    aws_wa_reliability: <count>
    aws_wa_performance: <count>
    cap_pacelc: <count>
    twelve_factor: <count>
    google_sre: <count>
    opentelemetry: <count>
    resilience_patterns: <count>

dimension_coverage:
  service_boundaries_coupling:
    frameworks: [<list>]
    coverage: "full | partial | minimal"
  # ... repeat for all 8 dimensions

unknowns_assumptions:
  - item: "List any assumptions made during framework selection"
    impact: "How this affects the evaluation"
    recommendation: "How to resolve the unknown"
```

## Quality Gate Checklist

Before returning to the main harness, verify:

- [ ] At least one named, citable framework is selected (AWS Well-Architected mandatory)
- [ ] Each selected framework has a citation URL
- [ ] Each selected framework has a mapped checklist with at least 3 items
- [ ] All 8 scoring dimensions are covered by at least one framework
- [ ] Framework selection is justified against the artifact metadata
- [ ] Unknowns and assumptions are explicitly listed
- [ ] Output follows the structured YAML format above

## Output Format

Return to main harness:

```yaml
framework_selection:
  frameworks_selected: [<list of framework names>]
  primary_framework: "<name of primary framework>"
  framework_checklist: <checklist YAML from Step 5>
  dimension_coverage: <mapping from Step 5>
  citations: [<list of URLs>]
  unknowns: [<list of unresolved assumptions>]
```

## Error Handling

If artifact metadata is incomplete:
1. Flag missing required fields (type, scale, domain)
2. Ask targeted clarifying questions for each missing field
3. Do not proceed to framework selection until minimum metadata is gathered

If no frameworks match the artifact:
1. Fall back to mandatory baseline (AWS Well-Architected + Resilience Patterns)
2. Explicitly state the limitation and why specialized frameworks were not selected
3. Recommend user provide more specific artifact details

## Notes

- Evidence hierarchy: Systematic Review > Meta-Analysis > RCT/Benchmark > Cohort/Case Study > Expert Opinion > Blog. Prefer the highest available tier.
- Framework citations should always point to authoritative sources (official documentation, academic papers, industry standards).
- If live WebSearch/WebFetch are unavailable, use `SECOND-KNOWLEDGE-BRAIN.md` as the citation source and state the limitation clearly.
