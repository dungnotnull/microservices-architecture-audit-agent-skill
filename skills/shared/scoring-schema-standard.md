---
name: shared-scoring-schema
description: Standardized scoring output schema for distributed system evaluation skills.
---

## Role
You are the **shared-scoring-schema** sub-skill, providing a standardized output format for scoring results across all cluster skills in the `software-devops` cluster. This ensures consistency and enables comparison between different evaluation types.

## Purpose

Provide a uniform schema for scoring outputs that:
- Enables comparison across different evaluation types
- Supports aggregation of scores across dimensions
- Facilitates trend analysis over time
- Enables benchmarking against industry standards

## Standard Schema Definition

### Score Output Structure

```yaml
evaluation_output:
  metadata:
    evaluation_id: "<unique_identifier>"
    evaluation_type: "<skill_name>"
    timestamp: "<ISO_8601_timestamp>"
    evaluator_version: "<version>"
    artifact_metadata:
      type: "<artifact_type>"
      scale: "<scale_category>"
      domain: "<domain>"

  scoring_framework:
    frameworks_used:
      - name: "<framework_name>"
        citation: "<url_or_reference>"
        description: "<brief_description>"
        weight: <0-1>

    dimensions_scored:
      - name: "<dimension_name>"
        weight: <0-1>
        description: "<what_this_dimension_measures>"
        framework_source: "<primary_framework>"
        scoring_criteria: "<brief_criteria_description>"

  dimension_scores:
    <dimension_name>:
      score:
        value: <0-100>
        band: [A | B | C | D | F]
        confidence: [high | medium | low]

      evidence:
        - item: "<evidence_item>"
          source: "<artifact_location_or_observation>"
          strength: [strong | moderate | weak]

      strengths:
        - "<strength_description>"

      weaknesses:
        - "<weakness_description>"

      gaps:
        - "<gap_description>"

      recommendations_count: <number>

  overall_metrics:
    total_score:
      value: <0-100>
      band: [A | B | C | D | F]
      calculation_method: "weighted_average"

    dimension_coverage:
      total_dimensions: <count>
      scored_dimensions: <count>
      coverage_percentage: <0-100>

    evidence_confidence:
      high_confidence_dimensions: <count>
      medium_confidence_dimensions: <count>
      low_confidence_dimensions: <count>

    score_distribution:
      a_band_dimensions: <count>
      b_band_dimensions: <count>
      c_band_dimensions: <count>
      d_band_dimensions: <count>
      f_band_dimensions: <count>

  ranked_weaknesses:
    - rank: <1-N>
      dimension: "<dimension_name>"
      score: <0-100>
      gap: "<specific_weakness>"
      impact: [critical | high | medium | low]
      urgency: [immediate | near_term | long_term]

  framework_alignment:
    - framework: "<framework_name>"
      alignment_score: <0-100>
      aligned_dimensions: [<list_of_dimension_names>]
      misaligned_dimensions: [<list_of_dimension_names>]
      notes: "<any_notes_on_alignment>"

  limitations:
    unknowns:
      - assumption: "<assumption_made>"
        impact: "<how_this_affects_scores>"
        recommendation: "<how_to_resolve>"

    constraints:
      - constraint: "<constraint_description>"
        effect: "<how_this_constrained_the_evaluation>"

    degraded_mode:
      active: [true | false]
      limitations: [<list_of_limitations>]
      confidence_adjustment: "<how_confidence_was_reduced>"

  sources_cited:
    frameworks: [<list_of_framework_citations>]
    external_sources: [<list_of_external_source_urls>]
    internal_knowledge: [<list_of_internal_knowledge_references>]
```

## Score Band Definitions

Standard score bands for consistent interpretation:

| Band | Range | Label | Description |
|------|-------|-------|-------------|
| A | 90-100 | Excellent | Industry-leading, best practices fully implemented |
| B | 70-89 | Good | Solid implementation, minor gaps |
| C | 50-69 | Fair | Basic implementation, significant gaps |
| D | 30-49 | Poor | Minimal implementation, critical gaps |
| F | 0-29 | Critical | No meaningful implementation, urgent action needed |

## Confidence Levels

Standard confidence levels for evidence quality:

| Level | Description | When to Use |
|-------|-------------|-------------|
| High | Strong evidence from production artifacts, configuration, or direct observation | When artifact evidence is clear and direct |
| Medium | Moderate evidence from documentation, inferred from patterns | When evidence is indirect but reasonable |
| Low | Weak evidence, assumptions, or lack of data | When making assumptions or data is missing |

## Impact Levels

Standard impact levels for prioritizing weaknesses:

| Level | Description | Urgency |
|-------|-------------|---------|
| Critical | Immediate risk to production, data loss, or security | Immediate |
| High | Significant risk, may cause incidents | Near-term |
| Medium | Moderate risk, affects non-critical paths | Short-term |
| Low | Minor risk, improvement opportunity | Long-term |

## Dimension Weighting Guidelines

Standard dimension weight ranges for different evaluation types:

### Microservices Architecture Audit
- Service Boundaries & Coupling: 0.15
- Resilience & Fault Tolerance: 0.20
- Scalability & Elasticity: 0.15
- Data Consistency Strategy: 0.12
- Observability: 0.15
- Deployment & Rollback Safety: 0.08
- Security Boundaries: 0.08
- Operational/SLO Readiness: 0.07

### Cloud Migration Readiness
- Application Portability: 0.20
- Data Migration Strategy: 0.15
- Security & Compliance: 0.20
- Cost Optimization: 0.10
- Operational Readiness: 0.15
- Performance & Scalability: 0.20

### DevOps Maturity Assessment
- CI/CD Maturity: 0.25
- Infrastructure as Code: 0.20
- Monitoring & Observability: 0.20
- Security Integration: 0.15
- Collaboration & Culture: 0.20

## Reuse Guidelines

### When to Use This Schema

Use this standardized schema when:
- Creating a new evaluation skill in the software-devops cluster
- Modifying an existing skill to use consistent output
- Comparing results across different evaluation types
- Building tooling that consumes evaluation results

### How to Adapt This Schema

1. **Define your dimensions**: Add dimension names specific to your evaluation type
2. **Set dimension weights**: Allocate weights that sum to 1.0
3. **Choose frameworks**: Select appropriate frameworks from your domain
4. **Define scoring criteria**: Specify what each score range means for each dimension
5. **Customize recommendations**: Add recommendation types specific to your evaluation

### Version Compatibility

This schema is version `1.0`. When updating:
1. Increment the version number
2. Document breaking changes
3. Provide migration guidance for existing implementations
4. Maintain backward compatibility when possible

## Integration Points

### With Main Harness
The main harness should:
1. Collect scoring output from sub-skills
2. Validate against this schema
3. Aggregate dimension scores into overall metrics
4. Present results using standardized formatting

### With Improvement Roadmap
The roadmap sub-skill should:
1. Consume ranked_weaknesses from scoring output
2. Use dimension scores to prioritize recommendations
3. Reference evidence when creating success criteria
4. Maintain traceability from weakness to recommendation

### With Resilience Probe
The resilience probe should:
1. Consume dimension scores to focus failure scenarios
2. Use confidence levels to determine depth of analysis
3. Update scoring based on findings (e.g., undiscovered SPoFs)
4. Reference evidence when challenging assumptions

## Example Output

```yaml
evaluation_output:
  metadata:
    evaluation_id: "MSAA-2026-06-30-001"
    evaluation_type: "microservices-architecture-audit"
    timestamp: "2026-06-30T12:00:00Z"
    evaluator_version: "1.0"
    artifact_metadata:
      type: "architecture_document"
      scale: "medium"
      domain: "e-commerce"

  scoring_framework:
    frameworks_used:
      - name: "AWS Well-Architected Framework"
        citation: "https://aws.amazon.com/architecture/well-architected/"
        weight: 1.0

    dimensions_scored:
      - name: "service_boundaries_coupling"
        weight: 0.15
        framework_source: "AWS Well-Architected (Reliability)"

  dimension_scores:
    service_boundaries_coupling:
      score:
        value: 65
        band: "C"
        confidence: "high"
      evidence:
        - item: "Clear service boundaries documented"
          source: "architecture_documentation"
          strength: "strong"
      strengths:
        - "Domain-driven design boundaries well-defined"
      weaknesses:
        - "Shared PostgreSQL database creates coupling"
      gaps:
        - "No event-driven communication for cross-boundary operations"
      recommendations_count: 3

  overall_metrics:
    total_score:
      value: 55
      band: "C"
      calculation_method: "weighted_average"
    dimension_coverage:
      total_dimensions: 8
      scored_dimensions: 8
      coverage_percentage: 100
    evidence_confidence:
      high_confidence_dimensions: 5
      medium_confidence_dimensions: 3
      low_confidence_dimensions: 0

  ranked_weaknesses:
    - rank: 1
      dimension: "resilience_fault_tolerance"
      score: 40
      gap: "No circuit breakers on external dependencies"
      impact: "high"
      urgency: "immediate"
```

## Quality Checklist

Before outputting scoring results, verify:

- [ ] All dimensions have numeric scores (0-100)
- [ ] All dimensions have score bands assigned
- [ ] All dimensions have evidence with sources
- [ ] Overall score calculated using weighted average
- [ ] Dimension coverage is 100%
- [ ] Ranked weaknesses include impact and urgency
- [ ] Frameworks are cited with URLs
- [ ] Confidence levels are appropriate
- [ ] Limitations and assumptions documented
- [ ] Output follows the schema structure above

## Notes

- This schema is designed for extensibility while maintaining consistency
- New dimensions can be added while preserving the overall structure
- Confidence levels should reflect the quality of available evidence
- When in doubt, choose lower confidence and explicitly state assumptions
