# Integration Map — Microservices Architecture Audit

## Cluster Integration

This skill is part of the `software-devops` cluster and shares sub-skills and schemas with sibling skills.

### Shared Resources

#### Shared Sub-Skills
Located in `skills/shared/`:

1. **shared-intake-handler** (`sub-intake-handler.md`)
   - Purpose: Standardized intake and requirements gathering
   - Used by: All cluster skills
   - Input: User query, artifact availability
   - Output: Structured artifact profile, clarification questions

2. **shared-scoring-schema** (`scoring-schema-standard.md`)
   - Purpose: Standardized scoring output format
   - Used by: All evaluation skills in cluster
   - Benefits: Enables comparison across evaluations, consistent formatting

#### Shared Schema Components

**Score Output Schema**:
- Standard score bands (A: 90-100, B: 70-89, C: 50-69, D: 30-49, F: 0-29)
- Confidence levels (high, medium, low)
- Impact levels (critical, high, medium, low)
- Dimension weight guidelines per evaluation type

**Intake Schema**:
- Standard artifact metadata structure
- Common clarification question templates
- Unknown/assumption documentation format

### Cluster Skills Reference

Related skills in the `software-devops` cluster:

#### Cloud Migration Readiness Audit
- **Skill ID**: (To be assigned)
- **Purpose**: Evaluate readiness for cloud migration
- **Shared Components**: Uses shared-intake-handler, shared-scoring-schema
- **Integration Points**:
  - Can reference prior microservices audit results
  - Can use same frameworks (AWS Well-Architected)
  - Scores can be compared for migration impact analysis

#### DevOps Maturity Assessment
- **Skill ID**: (To be assigned)
- **Purpose**: Evaluate DevOps process maturity
- **Shared Components**: Uses shared-intake-handler, shared-scoring-schema
- **Integration Points**:
  - Can reference operational scores from microservices audit
  - Shared observability and deployment dimensions
  - Combined evaluation provides complete picture

#### Infrastructure Security Review
- **Skill ID**: (To be assigned)
- **Purpose**: Evaluate infrastructure security posture
- **Shared Components**: Uses shared-intake-handler
- **Integration Points**:
  - Can leverage security boundaries scores from microservices audit
  - Shared framework: security best practices
  - Combined recommendations for comprehensive security

## Reuse Matrix

### Framework Reuse

| Framework | Used By This Skill | Can Be Reused By |
|-----------|-------------------|------------------|
| AWS Well-Architected | Yes (Reliability, Performance) | Cloud Migration, Infrastructure Security |
| Google SRE | Yes (SLOs, error budgets) | DevOps Maturity |
| Twelve-Factor App | Yes (Service design) | Cloud Migration |
| OpenTelemetry | Yes (Observability) | DevOps Maturity |
| Resilience Patterns | Yes (Fault tolerance) | All skills for reliability assessment |

### Dimension Reuse

| Dimension | This Skill Name | Can Be Mapped To |
|-----------|----------------|------------------|
| Service Boundaries | service_boundaries_coupling | Cloud Migration: application_portability |
| Resilience | resilience_fault_tolerance | Cloud Migration: reliability_readiness |
| Observability | observability | DevOps Maturity: monitoring_observability |
| Deployment Safety | deployment_rollback_safety | DevOps Maturity: cicd_maturity |
| Security | security_boundaries | Infrastructure Security: security_posture |

### Sub-Skill Reuse

| Sub-Skill | Location | Used By | Can Be Reused By |
|-----------|----------|---------|------------------|
| sub-intake-handler | skills/shared/ | All cluster skills | Any evaluation skill |
| scoring-schema-standard | skills/shared/ | All evaluation skills | Any scoring-based skill |
| sub-evaluation-framework-selector | skills/ | This skill | Cloud Migration, DevOps Maturity |
| sub-scoring-engine | skills/ | This skill | All evaluation skills (with dimension customization) |
| sub-improvement-roadmap | skills/ | This skill | All evaluation skills |
| sub-resilience-probe | skills/ | This skill | Cloud Migration, Infrastructure Security |

## Integration Patterns

### Pattern 1: Sequential Evaluation

Run multiple evaluations in sequence, using results from prior evaluations:

```
User Request: "Evaluate our microservices architecture for cloud migration readiness"

Execution Flow:
1. Run microservices-architecture-audit (baseline assessment)
2. Run cloud-migration-readiness (references baseline scores)
3. Generate integrated report showing:
   - Current state (from microservices audit)
   - Migration readiness (from cloud migration audit)
   - Combined roadmap with prioritized actions
```

### Pattern 2: Focused Deep-Dive

Run a broad evaluation, then deep-dive on specific dimensions:

```
User Request: "Evaluate our architecture, then focus on security"

Execution Flow:
1. Run microservices-architecture-audit (all 8 dimensions)
2. Run infrastructure-security-review (focuses on security dimension)
3. Generate integrated report showing:
   - All dimension scores (from microservices audit)
   - Detailed security analysis (from security review)
   - Combined roadmap with security recommendations prioritized
```

### Pattern 3: Comparison Over Time

Run the same evaluation at different points in time:

```
User Request: "Re-evaluate our architecture after implementing the recommendations"

Execution Flow:
1. Load prior evaluation results (from knowledge base)
2. Run microservices-architecture-audit with baseline reference
3. Generate comparison report showing:
   - Before/after scores for all dimensions
   - Improvements achieved
   - Remaining gaps
   - Updated roadmap
```

## Data Flow

### Input Flow

```
User Query
    ↓
shared-intake-handler
    ↓
sub-evaluation-framework-selector
    ↓
sub-scoring-engine
    ↓
sub-improvement-roadmap
    ↓
sub-resilience-probe
    ↓
Synthesis (main.md)
    ↓
Final Output (formatted per shared-scoring-schema)
```

### Output Flow

```
Evaluation Result (shared-scoring-schema format)
    ↓
Stored to knowledge base (for future comparison)
    ↓
Can be referenced by:
    - Cloud migration evaluation
    - DevOps maturity evaluation
    - Infrastructure security evaluation
    - Future microservices evaluations
```

## API Integration Points

### For Other Skills to Use

#### Referencing Prior Evaluations

```yaml
baseline_reference:
  evaluation_id: "<prior_evaluation_id>"
  evaluation_type: "microservices-architecture-audit"
  timestamp: "<ISO_8601_timestamp>"
  overall_score: <0-100>
  dimension_scores:
    <dimension_name>: <score>
```

#### Sharing Framework Selection

```yaml
framework_selection:
  shared_frameworks:
    - name: "AWS Well-Architected"
      used_by: ["microservices-architecture-audit", "cloud-migration-readiness"]
      dimensions_covered: [<list>]
```

#### Combining Recommendations

```yaml
integrated_roadmap:
  from_evaluations: [<list_of_evaluation_ids>]
  combined_recommendations:
    - recommendation: "<description>"
      source_evaluation: "<evaluation_id>"
      source_dimension: "<dimension_name>"
      priority: <1-N>
      dependencies: [<list_of_other_recommendation_ids>]
```

## Quality Gates for Integration

### Before Using Shared Resources

- [ ] Verify shared schema version compatibility
- [ ] Ensure sub-skill inputs match expected format
- [ ] Validate that framework citations are current
- [ ] Check that dimension mappings are appropriate

### After Integration

- [ ] Verify output follows shared schema
- [ ] Confirm that references are correctly attributed
- [ ] Validate that combined roadmaps are coherent
- [ ] Ensure that quality gates still pass

## Future Cluster Skills

### Potential Skills That Could Integrate

1. **Cost Optimization Audit**
   - Could leverage infrastructure metadata from microservices audit
   - Could use shared scoring schema
   - Could combine recommendations for cost + performance

2. **Performance Profiling**
   - Could leverage observability scores from microservices audit
   - Could use shared intake handler
   - Could provide detailed performance recommendations

3. **Compliance Assessment**
   - Could leverage security and compliance scores from microservices audit
   - Could use shared scoring schema
   - Could provide detailed compliance recommendations

## Cluster Governance

### Schema Versioning

- Current schema version: 1.0
- Breaking changes require: major version increment
- Non-breaking additions: minor version increment
- Backward compatibility: maintained across minor versions

### Sub-Skill Updates

- Shared sub-skills updates should maintain backward compatibility
- Breaking changes require: coordination with all dependent skills
- Update process: propose, review, test, deploy

### Quality Standards

All cluster skills must:
- Use shared intake handler for artifact collection
- Output results in shared scoring schema format
- Document integration points and dependencies
- Provide examples of integration with sibling skills
- Pass integration quality gates

---

**Last Updated**: 2026-06-30
**Schema Version**: 1.0
**Cluster**: software-devops
