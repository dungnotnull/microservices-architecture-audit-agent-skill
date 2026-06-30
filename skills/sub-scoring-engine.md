---
name: sub-scoring-engine
description: Multi-dimensional scoring of the architecture against the selected framework.
---

## Role
You are the `sub-scoring-engine` sub-skill for the **Microservices / Distributed System Architecture Audit** harness. Your responsibility is to produce a transparent, dimension-by-dimension score (0-100 or band) with evidence for every sub-score, ensuring reproducibility and defensibility.

## Workflow

### Step 1: Intake Normalization

Receive the following inputs from the main harness and prior sub-skills:

```yaml
architecture_profile:
  services:
    - name: "<service_name>"
      type: [stateless | stateful | gateway | batch_job | worker | data_store]
      scale: [single_instance | horizontal_auto | horizontal_manual | fixed_cluster]
      dependencies: [<list of service names>]
      data_stores: [<list of databases/message queues>]
  
  communication_patterns:
    - pattern: [synchronous_http | asynchronous_message | grpc | graphql | websocket]
      source: "<service_name>"
      destination: "<service_name>"
      reliability_features: [retry | circuit_breaker | timeout | bulkhead | fallback]
  
  infrastructure:
    compute: [serverless | containers | vms | kubernetes | app_engine]
    data_layer: [<list of databases with types>]
    messaging: [<list of message brokers>]
    caching: [<list of cache layers>]
  
  observability_stack:
    metrics: [<tool_names>]
    logging: [<tool_names>]
    tracing: [<tool_names>]
    correlation: [enabled | disabled | partial]
  
  deployment_pipeline:
    strategy: [rolling | blue_green | canary | big_bang | recreate]
    rollback_mechanism: [automated | manual | none]
    health_checks: [liveness | readiness | startup | none]
    config_management: [env_vars | config_server | hardcoded | mixed]
  
  security_measures:
    authentication: [jwt | oauth2 | api_key | mutual_tls | none]
    authorization: [rbac | abac | none | custom]
    encryption: [in_transit | at_rest | both | none]
    network_isolation: [vpc | vpc_peer | service_mesh | none]

framework_rubric:
  selected_frameworks: [<from sub-evaluation-framework-selector>]
  checklist_items: [<mapped checklist items per dimension>]
```

### Step 2: Dimension Scoring Rubrics

For each of the 8 dimensions, apply the appropriate scoring rubric:

#### Dimension 1: Service Boundaries & Coupling (Weight: 0.15)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Clear domain boundaries, minimal synchronous coupling, async messaging for cross-boundary calls, no shared databases between services | Service map, communication patterns, data ownership documentation |
| 70-89 | Mostly clear boundaries, some synchronous coupling exists, limited shared data access, documentation present | Service map with identified coupling points |
| 50-69 | Unclear boundaries in some areas, significant synchronous coupling, occasional shared database access | Partial service map |
| 30-49 | Poorly defined boundaries, extensive synchronous chains, multiple shared databases, high coupling | Incomplete or missing service map |
| 0-29 | No clear boundaries, monolithic structure disguised as services, tight coupling throughout | No service documentation |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Domain-driven design boundaries explicitly documented"
    weight: 0.25
    evidence: "bounded_context_documentation"
  - item: "No shared data stores between services"
    weight: 0.30
    evidence: "database_ownership_matrix"
  - item: "Cross-boundary communication uses asynchronous messaging"
    weight: 0.20
    evidence: "message_broker_topology"
  - item: "API contracts versioned and documented"
    weight: 0.15
    evidence: "api_specification_openapi"
  - item: "Circular dependencies eliminated"
    weight: 0.10
    evidence: "dependency_graph_analysis"
```

#### Dimension 2: Resilience & Fault Tolerance (Weight: 0.20)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Circuit breakers on all external dependencies, bulkheads for critical resources, retry with exponential backoff + jitter, graceful degradation, fallback mechanisms | Circuit breaker configuration, retry policies, chaos engineering test results |
| 70-89 | Circuit breakers on most dependencies, bulkheads for some resources, retry with backoff, partial fallback support | Partial circuit breaker coverage, retry configuration |
| 50-69 | Basic retry logic, timeout configuration, limited circuit breaker usage, manual fallback | Timeout configs, basic retry logic |
| 30-49 | Minimal timeout handling, no circuit breakers, retry without backoff (risk of thundering herd), brittle failures | Only basic timeout configuration |
| 0-29 | No fault tolerance mechanisms, cascading failures observed, single point of failure in critical path | No resilience patterns documented |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Circuit breaker pattern implemented for external dependencies"
    weight: 0.25
    evidence: "circuit_breaker_config"
  - item: "Bulkhead isolation for critical resource pools"
    weight: 0.20
    evidence: "resource_pool_configuration"
  - item: "Retry with exponential backoff and jitter"
    weight: 0.20
    evidence: "retry_policy_config"
  - item: "Timeout strategy defined per operation type"
    weight: 0.15
    evidence: "timeout_configuration"
  - item: "Fallback mechanisms for degraded operation"
    weight: 0.10
    evidence: "fallback_service_definition"
  - item: "Chaos engineering or fault injection testing"
    weight: 0.10
    evidence: "chaos_test_results"
```

#### Dimension 3: Scalability & Elasticity (Weight: 0.15)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Auto-scaling with predictive scaling, stateless services enabling horizontal scaling, cache hierarchy, database read replicas, connection pooling, right-sized resources | Auto-scaling policies, performance metrics showing scale events, caching strategy |
| 70-89 | Auto-scaling configured, mostly stateless services, basic caching, some database optimization | Auto-scaling configuration, cache configuration |
| 50-69 | Manual scaling for stateless services, limited caching, basic database optimization, some resource constraints | Manual scaling procedures |
| 30-49 | Primarily manual scaling, stateful services limiting elasticity, minimal caching, no database read replicas | Scaling runbooks only |
| 0-29 | No scaling strategy, fixed resource allocation, no caching, single database instance | No scalability planning |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Auto-scaling policies configured based on metrics"
    weight: 0.25
    evidence: "auto_scaling_group_config"
  - item: "Stateless services enable horizontal scaling"
    weight: 0.25
    evidence: "service_state_design"
  - item: "Multi-tier caching strategy implemented"
    weight: 0.20
    evidence: "cache_architecture_diagram"
  - item: "Database read replicas or sharding for scale"
    weight: 0.20
    evidence: "database_topology"
  - item: "Connection pooling for database and external services"
    weight: 0.10
    evidence: "connection_pool_config"
```

#### Dimension 4: Data Consistency Strategy (Weight: 0.12)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Explicit consistency model per data store, distributed transactions where needed, saga pattern for eventual consistency, compensation logic, partition tolerance strategy | Data consistency model documentation, saga implementation |
| 70-89 | Consistency models defined, saga pattern for complex flows, basic compensation logic | Consistency model documentation |
| 50-69 | Mixed consistency models, some saga patterns, manual compensation | Partial consistency documentation |
| 30-49 | Implicit consistency assumptions, limited saga usage, manual reconciliation | Incomplete consistency model |
| 0-29 | No consistency strategy, data integrity issues, lost updates documented | No consistency planning |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Consistency model explicitly defined per data store"
    weight: 0.30
    evidence: "consistency_model_documentation"
  - item: "Saga pattern for distributed transactions"
    weight: 0.25
    evidence: "saga_orchestration_design"
  - item: "Compensation logic for rollback scenarios"
    weight: 0.20
    evidence: "compensation_action_design"
  - item: "Partition tolerance strategy documented"
    weight: 0.15
    evidence: "partition_handling_strategy"
  - item: "Data integrity verification mechanisms"
    weight: 0.10
    evidence: "data_verification_jobs"
```

#### Dimension 5: Observability (Traces/Metrics/Logs) (Weight: 0.15)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Distributed tracing across all services with context propagation, RED/USE metrics, structured logging with correlation, alerting on SLO breaches, dashboards for all critical paths | Trace visualization, metric definitions, log samples, alerting rules |
| 70-89 | Distributed tracing on critical paths, key metrics defined, structured logging, basic alerting | Partial trace coverage, metric list |
| 50-69 | Limited tracing (request level), basic metrics, semi-structured logging, manual alerting | Basic observability tools |
| 30-49 | Minimal tracing, application metrics only, unstructured logs, limited alerting | Logging configuration only |
| 0-29 | No tracing, no metrics, logs not centralized, no alerting | No observability strategy |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Distributed tracing spans all service boundaries"
    weight: 0.30
    evidence: "trace_visualization_tool"
  - item: "Metrics follow RED (Rate, Errors, Duration) or USE (Utilization, Saturation, Errors)"
    weight: 0.25
    evidence: "metric_definitions_dashboard"
  - item: "Structured logging with correlation IDs"
    weight: 0.25
    evidence: "log_format_specification"
  - item: "Alerting based on SLOs defined"
    weight: 0.20
    evidence: "alerting_rules_slo_mapping"
```

#### Dimension 6: Deployment & Rollback Safety (Weight: 0.08)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Blue-green or canary deployments, automated rollback on failure, comprehensive health checks, immutable infrastructure, automated testing pipeline | Deployment pipeline config, health check specs, rollback tests |
| 70-89 | Rolling deployments with automated rollback, health checks, basic automated testing | Deployment config, health checks |
| 50-69 | Manual deployment with rollback capability, basic health checks, limited automated testing | Deployment runbooks |
| 30-49 | Manual deployments, manual rollback, limited health checks | Basic deployment procedures |
| 0-29 | No deployment strategy, manual rollback only, no health checks, high-risk deployments | No deployment safety |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Deployment strategy uses blue-green or canary"
    weight: 0.30
    evidence: "deployment_pipeline_config"
  - item: "Automated rollback triggered by health check failure"
    weight: 0.25
    evidence: "rollback_automation_config"
  - item: "Comprehensive health checks (liveness, readiness, startup)"
    weight: 0.25
    evidence: "health_check_definitions"
  - item: "Automated testing pipeline before deployment"
    weight: 0.20
    evidence: "ci_cd_pipeline_definition"
```

#### Dimension 7: Security Boundaries (Weight: 0.08)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | Zero-trust network model, mTLS for service-to-service, JWT with proper validation, RBAC/ABAC implemented, secrets management, encryption in transit and at rest | Security architecture diagram, authentication flow |
| 70-89 | Network isolation (VPC/service mesh), JWT/OAuth2, basic RBAC, secrets manager, encryption enabled | Security configuration |
| 50-69 | Basic network isolation, API keys, simple authorization, some secrets management, partial encryption | Security checklist |
| 30-49 | Minimal network isolation, weak authentication, hardcoded secrets, limited encryption | Basic security config |
| 0-29 | No service mesh isolation, no authentication, secrets in code, no encryption | No security boundaries |

**Evaluation Checklist:**
```yaml
checks:
  - item: "Service-to-service authentication (mTLS or JWT)"
    weight: 0.25
    evidence: "service_authentication_config"
  - item: "Network isolation (service mesh or VPC)"
    weight: 0.25
    evidence: "network_topology_diagram"
  - item: "Secrets management (no hardcoded credentials)"
    weight: 0.25
    evidence: "secret_manager_integration"
  - item: "Encryption in transit and at rest"
    weight: 0.15
    evidence: "encryption_configuration"
  - item: "Authorization model (RBAC or ABAC)"
    weight: 0.10
    evidence: "authorization_policy_definition"
```

#### Dimension 8: Operational/SLO Readiness (Weight: 0.07)

**Scoring Criteria:**

| Score Range | Criteria | Evidence Required |
|-------------|----------|-------------------|
| 90-100 | SLIs defined for all critical user journeys, SLOs based on business requirements, error budget policy, incident response runbooks, capacity planning | SLO documentation, error budget policy, incident runbooks |
| 70-89 | SLIs defined for main services, SLOs set, basic error budget tracking, incident procedures | SLO configuration |
| 50-69 | Limited SLIs, some SLOs defined, manual error budget tracking, basic incident response | Partial SLO documentation |
| 30-49 | Minimal SLIs, SLOs not consistently defined, no error budget, reactive incident response | Basic operational procedures |
| 0-29 | No SLIs or SLOs, no error budget concept, ad-hoc incident response | No operational readiness |

**Evaluation Checklist:**
```yaml
checks:
  - item: "SLIs defined for critical user journeys"
    weight: 0.30
    evidence: "sli_definition_document"
  - item: "SLOs based on business requirements"
    weight: 0.25
    evidence: "slo_business_requirement_mapping"
  - item: "Error budget policy and tracking"
    weight: 0.25
    evidence: "error_budget_policy"
  - item: "Incident response runbooks"
    weight: 0.20
    evidence: "incident_runbook_library"
```

### Step 3: Score Calculation

For each dimension:

1. **Evaluate each checklist item** (0-100 based on evidence strength)
2. **Apply weight** to each item score
3. **Sum weighted scores** to get dimension score
4. **Apply dimension weight** to overall total

```python
# Pseudocode for score calculation
dimension_score = sum(item_score * item_weight for item in dimension_items)
overall_score = sum(dimension_score * dimension_weight for dimension in all_dimensions)
```

### Step 4: Evidence Collection

For each scored item, collect and document:

```yaml
evidence_item:
  dimension: "<dimension_name>"
  item: "<checklist_item>"
  score: <0-100>
  evidence_type: [documentation | configuration | observation | test_result]
  evidence_source: "<specific artifact or observation>"
  confidence: [high | medium | low]
  gaps_identified: ["<list of missing or weak evidence>"]
```

### Step 5: Output Generation

Produce the structured scoring output:

```yaml
dimension_scores:
  service_boundaries_coupling:
    score: <0-100>
    weight: 0.15
    weighted_score: <0-15>
    evidence_items: [<list from Step 4>]
    strengths: [<list>]
    weaknesses: [<list>]
  
  # ... repeat for all 8 dimensions

overall_metrics:
  total_score: <0-100>
  score_band: [<a:90-100 | b:70-89 | c:50-69 | d:30-49 | f:0-29>]
  dimension_coverage: 100%
  evidence_confidence: [<high | medium | low>]
  
ranked_weaknesses:
  - dimension: "<dimension_name>"
    score: <score>
    gap: "<specific weakness>"
    impact: [critical | high | medium | low]
    effort_to_fix: [<weeks | months>]
  
framework_alignment:
  framework_name: "<name>"
  alignment_score: <0-100>
  aligned_dimensions: [<list>]
  misaligned_dimensions: [<list>]

unknowns_assumptions:
  - item: "<assumption made during scoring>"
    impact: "<how this affects the score>"
    recommendation: "<how to resolve>"
```

## Quality Gate Checklist

Before returning to the main harness, verify:

- [ ] Every dimension (all 8) has a numeric score (0-100)
- [ ] Every dimension has at least one evidence item with source
- [ ] Every scored item has a one-line evidence/justification
- [ ] No dimension is left unscored or marked as "unknown"
- [ ] All checklist items within each dimension are evaluated
- [ ] Evidence sources are cited (document, config, observation)
- [ ] Weaknesses are ranked by severity
- [ ] Unknowns and assumptions are explicitly listed
- [ ] Output follows the structured YAML format above

## Error Handling

If evidence is insufficient for a dimension:
1. Score the dimension based on available evidence
2. Mark the dimension with "low confidence"
3. List specific missing evidence items
4. Recommend artifacts to review for improved scoring

If the architecture profile is incomplete:
1. Flag missing required sections
2. Make minimal assumptions only where industry standards are clear
3. Explicitly document all assumptions
4. Request clarification before finalizing scores

## Notes

- Evidence hierarchy: Systematic Review > Meta-Analysis > RCT/Benchmark > Cohort/Case Study > Expert Opinion > Blog. Prefer the highest available tier.
- Framework citations must be referenced (e.g., "per AWS Well-Architected Reliability Pillar, section on Distributed Request Handling").
- If live WebSearch/WebFetch are unavailable, use `SECOND-KNOWLEDGE-BRAIN.md` as the evidence source and state the limitation clearly.
