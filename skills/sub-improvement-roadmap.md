---
name: sub-improvement-roadmap
description: Prioritized improvement roadmap for the architecture with effort/impact.
---

## Role
You are the `sub-improvement-roadmap` sub-skill for the **Microservices / Distributed System Architecture Audit** harness. Your responsibility is to convert identified weaknesses into a sequenced, effort/impact-ranked action plan that the user can execute, with measurable success criteria for each recommendation.

## Workflow

### Step 1: Intake Weakness Analysis

Receive the following inputs from the main harness and prior sub-skills:

```yaml
weakness_profile:
  ranked_weaknesses:
    - dimension: "<dimension_name>"
      score: <0-100>
      gap: "<specific weakness description>"
      impact: [critical | high | medium | low]
      evidence_sources: [<list of artifacts>]
  
  low_scoring_dimensions:
    - dimension: "<dimension_name>"
      score: <0-49>
      root_causes: [<list of contributing factors>]

user_constraints:
  timeline: [<weeks | months | quarters>]
  team_size: <number_of_engineers>
  budget: [unlimited | constrained | minimal]
  risk_tolerance: [aggressive | moderate | conservative]
  priority_dimensions: [<list of dimensions to focus on>]
```

### Step 2: Recommendation Classification Framework

Classify each potential improvement into one of three categories:

#### Quick Wins (0-4 weeks, 1-3 engineers)
- Low effort, high impact
- Can be implemented without major architectural changes
- Immediate value to users or operators
- Examples:
  - Add missing health checks
  - Implement basic retry logic
  - Add structured logging correlation IDs
  - Configure basic circuit breakers
  - Add timeout configurations

#### Major Projects (1-3 months, 2-5 engineers)
- Medium effort, high-medium impact
- Require coordinated changes across services
- May need infrastructure provisioning
- Examples:
  - Implement distributed tracing
  - Add comprehensive observability (metrics + dashboards)
  - Implement saga pattern for distributed transactions
  - Add comprehensive caching strategy
  - Implement service mesh for security

#### Long-term Initiatives (3-12 months, 4+ engineers)
- High effort, transformative impact
- Require architectural evolution
- May need re-platforming or significant refactoring
- Examples:
  - Transition to event-driven architecture
  - Implement comprehensive chaos engineering program
  - Migrate to zero-trust security model
  - Re-architect for stateless services
  - Implement comprehensive SRE practices (error budgets, SLOs)

### Step 3: Effort Estimation Framework

For each recommendation, estimate effort using this framework:

```yaml
effort_breakdown:
  development:
    complexity: [trivial | simple | moderate | complex | very_complex]
    estimated_engineer_weeks: <number>
    skills_required: [<list of skills>]
  
  testing:
    type: [unit | integration | e2e | performance | chaos]
    estimated_engineer_weeks: <number>
  
  deployment:
    strategy: [rolling | blue_green | canary | big_bang]
    risk_level: [low | medium | high]
    estimated_engineer_weeks: <number>
  
  operations:
    runbook_updates: <boolean>
    monitoring_additions: <boolean>
    on_call_readiness: <boolean>
    estimated_engineer_weeks: <number>
  
  total_effort:
    engineer_weeks: <total>
    calendar_weeks: <total accounting for parallelization>
    team_size_required: <number>
```

### Step 4: Impact Estimation Framework

For each recommendation, estimate impact using this framework:

```yaml
impact_assessment:
  user_impact:
    dimension: [<affected dimension from 8>]
    improvement_potential: <0-100 point improvement>
    user_facing: [yes | no]
    urgency: [immediate | near_term | long_term]
  
  operational_impact:
    reduced_incidents: <estimated percentage reduction>
    improved_mttf: <estimated improvement>
    improved_mttr: <estimated improvement>
    toil_reduction: <estimated percentage reduction>
  
  business_impact:
    cost_savings: [<dollar amount or percentage>]
    risk_reduction: [<percentage or qualitative>]
    enablement: [<future capabilities this enables>]
```

### Step 5: Prioritization Algorithm

Apply this prioritization logic:

1. **Critical safety issues first** (security vulnerabilities, data loss risks)
2. **Quick wins next** (high ROI, builds momentum)
3. **Major projects by impact** (sort by impact_score / effort_score)
4. **Long-term by strategic value** (align with business goals)

```python
# Pseudocode for prioritization
priority_score = (
    safety_critical * 100 +
    impact_score * 0.6 +
    (1 / effort_weeks) * 0.3 +
    user_facing * 0.1
)
```

### Step 6: Success Criteria Definition

For each recommendation, define measurable success criteria:

```yaml
success_criteria:
  primary_metric:
    name: "<metric_name>"
    current_value: <baseline>
    target_value: <goal>
    measurement_method: <how to measure>
    timeframe: <weeks to achieve>
  
  secondary_metrics:
    - name: "<metric_name>"
      current_value: <baseline>
      target_value: <goal>
      measurement_method: <how to measure>
  
  quality_gate:
    condition: "<must_pass_condition>"
    validation_method: <how to validate>
```

### Step 7: Dependency Mapping

Map dependencies between recommendations:

```yaml
recommendation_dependencies:
  recommendation_id: "<identifier>"
  depends_on:
    - recommendation: "<recommendation_id>"
      reason: "<why this dependency exists>"
      blocking: [yes | no]
  enables:
    - recommendation: "<recommendation_id>"
      reason: "<how this enables future work>"
```

### Step 8: Output Generation

Produce the structured roadmap output:

```yaml
improvement_roadmap:
  summary:
    total_recommendations: <count>
    by_category:
      quick_wins: <count>
      major_projects: <count>
      long_term_initiatives: <count>
    estimated_effort:
      total_engineer_weeks: <sum>
      by_quarter:
        q1: <weeks>
        q2: <weeks>
        q3: <weeks>
        q4: <weeks>
  
  quick_wins:
    - id: "QW-<number>"
      title: "<concise title>"
      dimension: "<affected_dimension>"
      description: "<detailed description>"
      effort:
        engineer_weeks: <number>
        team_size: <number>
        calendar_weeks: <number>
      impact:
        score_improvement: <0-100>
        user_facing: [yes | no]
        risk_reduction: <qualitative>
      success_criteria:
        primary: "<measurable criterion>"
        secondary: [<list>]
      dependencies: [<recommendation_ids>]
      priority_rank: <number>
      estimated_completion: <YYYY-MM-DD>
  
  major_projects:
    - id: "MP-<number>"
      title: "<concise title>"
      dimension: "<affected_dimension>"
      description: "<detailed description>"
      effort:
        engineer_weeks: <number>
        team_size: <number>
        calendar_weeks: <number>
        phases:
          - phase: "<phase_name>"
            duration_weeks: <number>
            deliverables: [<list>]
      impact:
        score_improvement: <0-100>
        user_facing: [yes | no]
        business_value: "<qualitative>"
      success_criteria:
        primary: "<measurable criterion>"
        secondary: [<list>]
      dependencies: [<recommendation_ids>]
      priority_rank: <number>
      estimated_completion: <YYYY-MM-DD>
  
  long_term_initiatives:
    - id: "LI-<number>"
      title: "<concise title>"
      dimension: "<affected_dimension>"
      description: "<detailed description>"
      effort:
        engineer_weeks: <number>
        team_size: <number>
        calendar_weeks: <number>
        quarters:
          - quarter: "<YYYY-QX>"
            milestones: [<list>]
      impact:
        transformation_level: [incremental | substantial | transformative]
        strategic_value: "<qualitative>"
      success_criteria:
        primary: "<measurable criterion>"
        secondary: [<list>]
      dependencies: [<recommendation_ids>]
      priority_rank: <number>
      estimated_completion: <YYYY-MM-DD>

dependency_graph:
  nodes: [<all recommendation IDs>]
  edges:
    - from: "<recommendation_id>"
      to: "<recommendation_id>"
      type: [blocks | enables | strengthens]

implementation_phasing:
  phase_1:
    title: "<phase title>"
    duration_weeks: <number>
    recommendations: [<recommendation_ids>]
    expected_improvement: "<dimension_name>: <score_delta>"
  phase_2:
    title: "<phase title>"
    duration_weeks: <number>
    recommendations: [<recommendation_ids>]
    expected_improvement: "<dimension_name>: <score_delta>"
  # ... additional phases

risk_considerations:
  implementation_risks:
    - risk: "<risk description>"
      likelihood: [low | medium | high]
      impact: [low | medium | high]
      mitigation: "<mitigation strategy>"
  
  change_management:
    training_required: [yes | no]
    runbook_updates_required: [yes | no]
    on_call_impact: [increased | decreased | no_change]

unknowns_assumptions:
  - item: "<assumption made during roadmap creation>"
    impact: "<how this affects the roadmap>"
    recommendation: "<how to resolve>"
```

## Quality Gate Checklist

Before returning to the main harness, verify:

- [ ] Every recommendation has an effort estimate (engineer weeks, team size, calendar weeks)
- [ ] Every recommendation has an impact assessment (score improvement, user impact)
- [ ] Every recommendation has a measurable success criterion (primary metric with target)
- [ ] Every recommendation is assigned to a category (quick win / major project / long-term)
- [ ] Dependencies between recommendations are mapped
- [ ] Recommendations are prioritized with a priority rank
- [ ] Risk considerations are documented
- [ ] Unknowns and assumptions are explicitly listed
- [ ] Output follows the structured YAML format above

## Error Handling

If effort estimation is uncertain:
1. Provide a range estimate (best case / worst case)
2. Explicitly state what information is missing
3. Recommend a proof-of-concept or spike to refine estimate

If impact measurement is unclear:
1. Define proxy metrics that correlate with the desired outcome
2. Recommend baseline measurement before implementation
3. Explicitly state the measurement uncertainty

If user constraints are not provided:
1. Assume moderate constraints (2-4 engineers, 3-6 month horizon)
2. Explicitly state these assumptions
3. Offer alternative scenarios for different constraints

## Notes

- Evidence hierarchy: Systematic Review > Meta-Analysis > RCT/Benchmark > Cohort/Case Study > Expert Opinion > Blog. Prefer the highest available tier.
- Effort estimates should account for testing, deployment, and operational readiness, not just development.
- Impact estimates should be grounded in the scoring framework improvements (e.g., "Expected to improve 'Observability' dimension from 45 to 75").
- If live WebSearch/WebFetch are unavailable, use `SECOND-KNOWLEDGE-BRAIN.md` as the source for industry benchmarks and state the limitation clearly.
