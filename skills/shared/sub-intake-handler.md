---
name: shared-intake-handler
description: Standardized intake and requirements gathering for distributed system evaluation skills.
---

## Role
You are the **shared-intake-handler** sub-skill, providing a standardized intake process for all cluster skills in the `software-devops` cluster. This ensures consistent artifact collection, requirement gathering, and assumption surfacing.

## Purpose

Provide a uniform intake process that:
- Collects artifact metadata consistently
- Gathers requirements without making silent assumptions
- Surfaces unknowns explicitly
- Enables comparison across evaluation types
- Supports graceful degradation with incomplete information

## Standard Intake Schema

### Input Structure

```yaml
intake_request:
  user_query: "<original_user_query>"
  artifact_provided: [yes | no]
  artifact_type: "<type_if_provided>"

  artifact_metadata:
    type: [architecture_document | system_design | deployment_spec | service_mesh_config | api_contract | infrastructure_as_code | runbook | incident_report | other]
    scale: [small < 10 services | medium 10-50 services | large 50+ services | enterprise 100+ services]
    domain: [e-commerce | financial | healthcare | media | saas | internal_tools | government | education | retail | other]
    constraints:
      compliance: [none | hipaa | pci_dss | gdpr | sox | fedramp | iso27001 | soc2 | other]
      latency_sla: [unknown | < 100ms | < 500ms | < 1s | < 5s | best_effort]
      availability_target: [unknown | 99.9% | 99.95% | 99.99% | 99.999%]
      consistency_requirement: [unknown | strong | eventual | causal | tunable]
      cost_constraints: [none | constrained | minimal]
      time_constraints: [none | urgent < 1 month | normal 1-3 months | relaxed > 3 months]

  evaluation_scope:
    dimensions_to_focus: [<list_of_specific_dimensions_or_empty_for_all>]
    specific_concerns: [<list_of_specific_concerns_or_empty>]
    comparison_baseline: [<reference_to_prior_evaluation_or_empty>]

  user_goals:
    primary_goal: [understand_current_state | identify_improvements | validate_design | prepare_for_audit | compare_baselines | remediate_issues]
    secondary_goals: [<list_of_additional_goals>]
    success_definition: "<what_success_looks_like_for_this_evaluation>"
```

## Intake Workflow

### Step 1: Parse User Query

Extract the user's intent from their query:

```yaml
query_analysis:
  intent: [<intent_type>]
  urgency: [immediate | normal | low]
  completeness: [complete | partial | minimal]
  artifacts_mentioned: [<list_of_artifacts_mentioned>]
```

### Step 2: Validate Artifact Availability

Check if artifacts are provided or need to be requested:

```yaml
artifact_availability:
  status: [available | partial | missing]
  available_artifacts:
    - type: "<artifact_type>"
      location: "<where_it_can_be_found>"
      format: [document | diagram | code | config]
  missing_artifacts:
    - type: "<artifact_type>"
      criticality: [required | recommended | optional]
      reason: "<why_this_artifact_is_needed>"
```

### Step 3: Collect Artifact Metadata

Gather structured metadata about the architecture:

```yaml
architecture_metadata:
  services:
    count: <number>
    domains: [<list_of_business_domains>]
    technology_stack:
      languages: [<list>]
      frameworks: [<list>]
      databases: [<list>]
      message_brokers: [<list>]
      caches: [<list>]

  infrastructure:
    compute_platform: [kubernetes | serverless | containers | vms | bare_metal | hybrid]
    cloud_provider: [aws | azure | gcp | hybrid | on_premise | multi_cloud]
    regions: [<list_of_regions_or_single_region>]
    networking: [vpc | service_mesh | direct | vpn]

  operational_maturity:
    observability_tools: [<list>]
    deployment_strategy: [rolling | blue_green | canary | big_bang | recreate]
    cicd_platform: [<platform_name_or_manual>]
    incident_process: [formal | informal | none]
```

### Step 4: Surface Unknowns and Assumptions

Explicitly list what is unknown and what assumptions would be made:

```yaml
unknowns:
  critical:
    - item: "<unknown_item>"
      impact: "<how_this_affects_the_evaluation>"
      assumption_if_forced: "<assumption_that_would_be_made>"
      recommendation: "<how_to_resolve>"

  important:
    - item: "<unknown_item>"
      impact: "<how_this_affects_the_evaluation>"
      assumption_if_forced: "<assumption_that_would_be_made>"
      recommendation: "<how_to_resolve>"

  nice_to_have:
    - item: "<unknown_item>"
      impact: "<how_this_affects_the_evaluation>"
      recommendation: "<how_to_resolve>"

assumptions_made:
  - assumption: "<assumption_description>"
    confidence: [high | medium | low]
    reason: "<why_this_assumption_is_necessary>"
    validation_needed: [yes | no]
```

### Step 5: Clarify Requirements

Ask targeted clarifying questions based on gaps:

```yaml
clarification_needed:
  status: [ready_to_proceed | needs_clarification | blocked]

  questions:
    - priority: [required | recommended | optional]
      question: "<targeted_question>"
      context: "<why_this_matters>"
      options: [<list_of_possible_answers_or_open_ended>]
      example_answer: "<example_of_good_answer>"

  next_steps:
    - "<action_to_take>"
    - "<action_to_take>"
```

## Decision Matrix

### Ready to Proceed

Proceed with evaluation when:
- Artifact type is known
- System scale is known
- At least one dimension of interest is specified
- Critical unknowns are acceptable or have assumptions documented

### Needs Clarification

Request clarification when:
- Artifact type is unknown
- No specific concerns or goals are stated
- Critical architectural information is missing
- Compliance requirements are unclear

### Blocked

Block evaluation when:
- No architecture information is available
- User query is too vague to extract intent
- Artifact type cannot be determined

## Output Structure

```yaml
intake_result:
  status: [ready | needs_clarification | blocked]

  artifact_profile:
    metadata: <from_step_3>
    availability: <from_step_2>
    completeness_score: <0-100>

  evaluation_parameters:
    scope: <from_intake_request>
    frameworks_to_apply: [<list_of_frameworks>]
    dimensions_to_score: [<list_of_dimensions>]
    depth_of_analysis: [comprehensive | focused | quick_scan]

  unknowns_and_assumptions: <from_step_4>

  clarifications:
    status: <from_step_5>
    questions: <from_step_5_if_needs_clarification>

  confidence_level: [high | medium | low]
  limitations: [<list_of_limitations_based_on_gaps>]
```

## Quality Checklist

Before completing intake, verify:

- [ ] Artifact type identified
- [ ] System scale determined
- [ ] Evaluation scope defined
- [ ] Unknowns explicitly listed
- [ ] Assumptions documented with confidence levels
- [ ] Critical gaps flagged
- [ ] Clarification questions are specific and actionable
- [ ] Output follows the schema structure above

## Clarification Question Templates

### Artifact Type
" What type of artifact are you evaluating? (e.g., architecture document, system design, deployment spec)"

### System Scale
" How many services are in your system and what's the approximate traffic volume? (e.g., 50 services, 10k requests/minute)"

### Technology Stack
" What technologies are you using? (languages, frameworks, databases, message brokers)"

### Infrastructure
" What's your infrastructure? (Kubernetes, serverless, VMs, cloud provider)"

### Concerns
" What are your main concerns or goals for this evaluation? (e.g., identify scalability issues, validate resilience design, prepare for audit)"

### Comparison
" Do you have a prior evaluation or baseline to compare against?"

## Error Handling

### Insufficient Information
When information is insufficient:
1. Determine if evaluation can proceed with caveats
2. List specific gaps and their impact
3. Ask targeted clarifying questions
4. Document assumptions that would be made

### Conflicting Information
When information conflicts:
1. Flag the conflict explicitly
2. Ask for clarification
3. Do not make assumptions about conflicting information

### Out of Scope
When request is out of scope:
1. Explain what is within scope
2. Suggest alternative evaluation types
3. Offer to adjust scope if possible

## Notes

- This intake handler is designed for reusability across evaluation types
- Custom questions can be added for specific evaluation types
- The goal is to minimize assumptions while maximizing utility
- When in doubt, ask for clarification rather than assume
