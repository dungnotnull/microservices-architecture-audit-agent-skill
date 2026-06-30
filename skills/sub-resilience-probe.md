---
name: sub-resilience-probe
description: Stress-test the design against failure scenarios (Socratic devil's advocate).
---

## Role
You are the `sub-resilience-probe` sub-skill for the **Microservices / Distributed System Architecture Audit** harness. Your responsibility is to walk through partition, dependency-failure, and load-spike scenarios to expose hidden single points of failure, challenging the architecture's resilience claims through adversarial analysis.

## Workflow

### Step 1: Intake Architecture Mapping

Receive the following inputs from the main harness and prior sub-skills:

```yaml
architecture_map:
  services:
    - name: "<service_name>"
      criticality: [critical | important | optional]
      dependencies: [<list of service names>]
      data_stores: [<list of databases>]
      external_dependencies: [<list of third-party services>]
      sla_target: <percentage>
      bottleneck_risk: [high | medium | low]
  
  communication_graph:
    - source: "<service_name>"
      destination: "<service_name>"
      protocol: [synchronous_http | asynchronous_message | grpc | websocket]
      reliability_features: [retry | circuit_breaker | timeout | bulkhead | fallback]
      single_point_of_failure: [yes | no]
  
  data_layer:
    - name: "<data_store_name>"
      type: [sql | nosql | message_queue | cache | search | blob]
      availability_pattern: [single_instance | primary_replica | multi_primary | geo_distributed]
      consistency_model: [strong | eventual | causal | tunable]
      partition_handling: [stop_the_world | degraded_mode | read_only | continue_with_stale]

failure_mode_assumptions:
  acceptable_downtime: [<duration>]
  acceptable_data_loss: [<volume>]
  degraded_mode_requirements: [<list of minimum viable features>]
```

### Step 2: Failure Scenario Generation

Generate and analyze failure scenarios across these categories:

#### Scenario Category 1: Network Partition Failures

**Scenario 1.1: Service-to-Service Partition**
```yaml
scenario_id: "PARTITION-001"
scenario_name: "Network partition between critical service and its primary dependency"
description: "A network partition occurs between Service A and Service B, preventing all communication for 5 minutes"
failure_mode:
  partition_type: [complete | intermittent | latency_spike]
  affected_services: [<service_names>]
  partition_duration: <minutes>
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      impact: [unavailable | degraded | functional]
      user_impact: [critical | moderate | minimal]
      cascading_failures: [<list of downstream services>]
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [circuit_breaker | fallback | retry | timeout | bulkhead]
      effective: [yes | no]
      gap: "<description of gap if protection is missing or ineffective>"
  
  recovery_assessment:
    automatic_recovery: [yes | no]
    recovery_time: <seconds>
    manual_intervention_required: [yes | no]
    data_consistency_impact: [none | minor | major | critical]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 1.2: Database Connection Partition**
```yaml
scenario_id: "PARTITION-002"
scenario_name: "Network partition between service and its primary database"
description: "Service loses network connectivity to its primary database instance"
failure_mode:
  database_type: [sql | nosql | cache]
  partition_type: [complete | intermittent]
  affected_operations: [read | write | both]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      write_path_handling: [stop | queue | fallback_to_cache | local_buffer]
      read_path_handling: [stop | fallback_to_replica | fallback_to_cache | serve_stale]
      data_integrity_risk: [none | minor | moderate | severe]
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [connection_pooling | retry | circuit_breaker | fallback_replica | local_cache]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_recovery: [yes | no]
    recovery_time: <seconds>
    manual_intervention_required: [yes | no]
    data_reconciliation_needed: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 1.3: Cross-AZ/Region Partition**
```yaml
scenario_id: "PARTITION-003"
scenario_name: "Network partition between availability zones or geographic regions"
description: "A complete network partition separates AZs or regions, affecting cross-region communication"
failure_mode:
  partition_scope: [cross_az | cross_region | partial_region]
  partition_duration: <minutes>
  affected_services: [<service_names>]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      impact: [unavailable | degraded | functional]
      cross_region_replication: [halted | delayed | unaffected]
      geo_routing: [broken | fallback_to_local | manual_intervention]
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [multi_region_deployment | geo_dns | active_active | active_passive]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_failover: [yes | no]
    failover_time: <seconds>
    manual_intervention_required: [yes | no]
    data_divergence_risk: [none | minor | moderate | major]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

#### Scenario Category 2: Dependency Failures

**Scenario 2.1: Critical Service Failure**
```yaml
scenario_id: "DEPEND-001"
scenario_name: "Complete failure of a critical dependency service"
description: "A service that multiple other services depend on fails completely"
failure_mode:
  failed_service: "<service_name>"
  failure_type: [crash_loop | resource_exhaustion | deadlock]
  downstream_consumers: [<list of services>]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      impact: [unavailable | degraded | functional]
      has_fallback: [yes | no]
      fallback_mechanism: "<description>"
      cascading_failure_risk: [high | medium | low]
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [circuit_breaker | fallback_service | degraded_mode | local_cache]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_recovery: [yes | no]
    recovery_time: <seconds>
    manual_intervention_required: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 2.2: Third-Party Service Outage**
```yaml
scenario_id: "DEPEND-002"
scenario_name: "Third-party API or SaaS service becomes unavailable"
description: "A critical external dependency (payment gateway, identity provider, etc.) fails"
failure_mode:
  external_service: "<service_name>"
  outage_type: [complete | degraded | rate_limited]
  outage_duration: <minutes>
  affected_operations: [<list of operations>]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      business_impact: [revenue_loss | customer_impact | operational_impact | minimal]
      has_fallback: [yes | no]
      fallback_mechanism: "<description>"
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [circuit_breaker | fallback_provider | queue_for_retry | degraded_mode]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_recovery: [yes | no]
    recovery_time: <seconds>
    manual_intervention_required: [yes | no]
    data_consistency_impact: [none | minor | moderate | major]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 2.3: Database Failure**
```yaml
scenario_id: "DEPEND-003"
scenario_name: "Primary database instance failure"
description: "The primary database instance fails, requiring failover to a replica"
failure_mode:
  database_type: [sql | nosql]
  failure_type: [crash | corruption | resource_exhaustion]
  has_replica: [yes | no]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      write_path_impact: [stop | queue | local_buffer]
      read_path_impact: [unavailable | fallback_to_replica | serve_stale]
      rpo_rto_impact: "<data_loss_and_recovery_time_estimate>"
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [automated_failover | manual_failover | multi_primary | local_cache]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_failover: [yes | no]
    failover_time: <seconds>
    manual_intervention_required: [yes | no]
    data_reconciliation_needed: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

#### Scenario Category 3: Load Spike Scenarios

**Scenario 3.1: Sudden Traffic Surge**
```yaml
scenario_id: "LOAD-001"
scenario_name: "Sudden traffic surge (5-10x normal load)"
description: "A sudden increase in traffic, potentially from viral content, marketing campaign, or DDoS"
failure_mode:
  surge_magnitude: [2x | 5x | 10x | 50x]
  surge_duration: <minutes>
  affected_services: [<service_names>]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      bottleneck_resource: [cpu | memory | database_connections | api_limits | network_bandwidth]
      current_headroom: <percentage>
      auto_scaling_triggered: [yes | no]
      auto_scaling_response_time: <seconds>
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [auto_scaling | rate_limiting | load_shedding | caching | queueing]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_scaling: [yes | no]
    scaling_time: <seconds>
    manual_intervention_required: [yes | no]
    degraded_mode_available: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 3.2: Resource Exhaustion**
```yaml
scenario_id: "LOAD-002"
scenario_name: "Resource exhaustion (connection pool, memory, disk)"
description: "A resource limit is reached, causing service degradation or failure"
failure_mode:
  resource_type: [connection_pool | memory | disk | file_handles | threads]
  exhaustion_cause: [leak | surge | misconfiguration | limit_too_low]
  affected_services: [<service_names>]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      failure_mode: [slow_crash | instant_crash | degrade | queue_reject]
      detection_time: <seconds>
      isolation_available: [yes | no]
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [resource_limits | health_checks | circuit_breaker | bulkhead | monitoring_alerts]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_recovery: [yes | no]
    recovery_time: <seconds>
    manual_intervention_required: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 3.3: Cache Stampede or Thundering Herd**
```yaml
scenario_id: "LOAD-003"
scenario_name: "Cache stampede or thundering herd on cache expiration"
description: "Multiple requests simultaneously miss cache and hit the backend, overwhelming it"
failure_mode:
  cache_type: [redis | memcached | cdn | application_cache]
  trigger: [simultaneous_expiration | cold_cache | hot_key]
  affected_backend: <database_or_service_name>
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      backend_impact: [overwhelmed | degraded | unaffected]
      user_impact: [high_latency | errors | timeout | unaffected]
      cache_warmup_time: <seconds>
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [cache_lock | probabilistic_expiration | pre_warming | request_coalescing]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_recovery: [yes | no]
    recovery_time: <seconds>
    manual_intervention_required: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

#### Scenario Category 4: Data Consistency Failures

**Scenario 4.1: Distributed Transaction Rollback**
```yaml
scenario_id: "CONSIST-001"
scenario_name: "Distributed transaction rollback with partial completion"
description: "A multi-service transaction fails mid-flow, leaving some services committed and others rolled back"
failure_mode:
  transaction_type: [saga | two_phase_commit | eventual_consistency]
  failure_point: <service_name>
  compensating_actions: [defined | undefined | partial]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      state: [committed | rolled_back | indeterminate]
      compensation_needed: [yes | no]
      compensation_logic_exists: [yes | no]
      data_inconsistency_risk: [high | medium | low]
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [saga_compensation | transactional_outbox | idempotency | reconciliation_jobs]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
    automatic_compensation: [yes | no]
    manual_reconciliation_required: [yes | no]
    reconciliation_time: <minutes | hours | days>
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

**Scenario 4.2: Replication Lag or Divergence**
```yaml
scenario_id: "CONSIST-002"
scenario_name: "Database replication lag causing stale reads"
description: "Replication lag causes users to read stale data, potentially causing inconsistencies"
failure_mode:
  replication_type: [async | semi_sync | sync]
  lag_duration: <seconds>
  lag_cause: [network | load | misconfiguration]
  
blast_radius_analysis:
  immediate_impact:
    - service: "<service_name>"
      read_consistency: [strong | eventual | stale]
      business_impact: [data_corruption | user_confusion | lost_updates | minimal]
      users_affected: <percentage>
  
  defense_in_depth:
    - layer: "<layer_name>"
      protection: [read_from_primary | sticky_sessions | lag_monitoring | grace_period]
      effective: [yes | no]
      gap: "<description of gap>"
  
  recovery_assessment:
  automatic_detection: [yes | no]
  manual_intervention_required: [yes | no]
  
  severity: [critical | high | medium | low]
  confidence: [high | medium | low]
```

### Step 3: Single Point of Failure Identification

Identify and document all single points of failure:

```yaml
single_points_of_failure:
  - component: "<component_name>"
    type: [service | database | message_queue | cache | load_balancer | network_link]
    failure_impact:
      services_affected: [<list>]
      business_impact: [critical | high | medium | low]
      user_facing: [yes | no]
    redundancy_exists: [yes | no]
    redundancy_type: [active_active | active_passive | none]
    recommended_mitigation: "<description of how to eliminate this SPoF>"
    severity: [critical | high | medium | low]
```

### Step 4: Cascading Failure Analysis

Analyze potential cascading failure paths:

```yaml
cascading_failure_paths:
  - path_id: "CASCADE-<number>"
    initiating_failure: "<component_name>"
    cascade_path:
      - step: 1
        component: "<component_name>"
        failure_mode: "<description>"
        time_to_failure: <seconds>
      - step: 2
        component: "<component_name>"
        failure_mode: "<description>"
        time_to_failure: <seconds>
      # ... additional steps
    
    total_impact:
      services_affected: <count>
      user_facing_outage_duration: <seconds>
      business_impact: [critical | high | medium | low]
    
    break_points:
      - component: "<component_name>"
        protection: "<protection that could break the cascade>"
        exists: [yes | no]
```

### Step 5: Devil's Advocate Challenge

Challenge the architecture's resilience claims through adversarial questioning:

```yaml
devils_advocate_challenges:
  - claim: "<architecture's resilience claim>"
    challenge: "<adversarial question that exposes weakness>"
    evidence_required: "<what would need to be proven to refute the challenge>"
    current_evidence: [strong | moderate | weak | missing]
  
  # Example challenges:
  # - claim: "We have circuit breakers so cascading failures won't happen"
  #   challenge: "Circuit breakers are only as good as their thresholds. 
  #               When was the last time you tuned them? Have you tested 
  #               them under production-like load?"
  #   evidence_required: "Recent circuit breaker tuning records and 
  #                       chaos engineering test results"
  #   current_evidence: weak
```

### Step 6: Output Generation

Produce the structured resilience probe output:

```yaml
resilience_probe_results:
  summary:
    scenarios_analyzed: <count>
    critical_findings: <count>
    single_points_of_failure: <count>
    cascading_failure_paths: <count>
    overall_resilience_assessment: [strong | moderate | weak | critical]
  
  failure_scenarios:
    - scenario_id: "<id>"
      scenario_name: "<name>"
      scenario_category: [partition | dependency | load | consistency]
      severity: [critical | high | medium | low]
      blast_radius: <assessment from analysis>
      defense_gaps: [<list of gaps>]
      recommendations: [<list of mitigations>]
  
  single_points_of_failure:
    critical: [<list of critical SPoFs>]
    high: [<list of high-priority SPoFs>]
    medium: [<list of medium-priority SPoFs>]
    low: [<list of low-priority SPoFs>]
  
  cascading_failure_analysis:
    total_paths_identified: <count>
    critical_paths: [<list of most dangerous cascade paths>]
    recommended_break_points: [<list of places to break cascades>]
  
  devils_advocate_findings:
    challenges_issued: <count>
    claims_with_weak_evidence: <count>
    recommended_validations: [<list of tests or evidence to gather>]

priority_recommendations:
  immediate: [<recommendations for critical SPoFs>]
  short_term: [<recommendations for high-severity gaps>]
  long_term: [<recommendations for architectural improvements>]

unknowns_assumptions:
  - item: "<assumption made during analysis>"
    impact: "<how this affects the findings>"
    recommendation: "<how to resolve>"
```

## Quality Gate Checklist

Before returning to the main harness, verify:

- [ ] At least 3 failure scenarios have been analyzed (covering different categories)
- [ ] Each scenario includes a blast radius assessment
- [ ] Each scenario identifies defense gaps
- [ ] Single points of failure are documented with mitigation recommendations
- [ ] Cascading failure paths are mapped
- [ ] Devil's advocate challenges are issued against resilience claims
- [ ] Severity is assessed for each finding
- [ ] Unknowns and assumptions are explicitly listed
- [ ] Output follows the structured YAML format above

## Error Handling

If architecture map is incomplete:
1. Flag missing critical information (service dependencies, data stores)
2. Make reasonable assumptions for analysis but explicitly state them
3. Request clarification before finalizing critical recommendations

If failure scenario analysis requires assumptions:
1. Document all assumptions clearly
2. Assess confidence level for each scenario
3. Recommend chaos engineering tests to validate assumptions

## Notes

- Evidence hierarchy: Systematic Review > Meta-Analysis > RCT/Benchmark > Cohort/Case Study > Expert Opinion > Blog. Prefer the highest available tier.
- Failure scenarios should be grounded in real production incidents from industry sources when available.
- If live WebSearch/WebFetch are unavailable, use `SECOND-KNOWLEDGE-BRAIN.md` as the source for industry incident patterns and state the limitation clearly.
- The goal is not to prove the architecture is fragile, but to stress-test it objectively and identify areas for improvement.
