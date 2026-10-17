# Diagnostic Reasoning & CDSS Literature Synthesis (Deliverable D8-B2)

## 1. Purpose

This document synthesizes literature on human diagnostic reasoning, clinical decision support, automation bias, complacency, alert fatigue, explanation transparency, calibration, and human-AI teaming.

It connects those findings to the CDSS architecture defined in docs/27_cdss_architecture_and_contracts.md.

The purpose is to identify design requirements, failure modes, and evaluation gaps. It does not claim empirical clinical validation.

## 2. Theoretical Framework

The synthesis is organized around dual-process diagnostic reasoning:

    DIAGNOSTIC REASONING FRAMEWORK

    System 1: Fast, heuristic, pattern-based
      - vulnerable to premature closure
      - vulnerable to anchoring
      - vulnerable to automation bias
      - susceptible to alert fatigue

    System 2: Slow, analytic, probabilistic
      - calibrated via Bayesian posterior intervals
      - forces evaluation of counter-evidence
      - supports interactive what-if auditing
      - requires cognitive effort and time

The CDSS should not replace System 1 or System 2. It should make System 2 review cheaper, more transparent, and better calibrated.

## 3. Synthesis Matrix B2

| Domain / Concept | Seminal Theoretical Foundations | Core Mechanism / Failure Mode | Impact on Cognitive Assessment | Design Mitigation in This Architecture |
|---|---|---|---|---|
| Dual-process diagnostic reasoning | Croskerry; Kahneman-style framework | Fast pattern matching may override analytic checking | Premature labeling of attention, memory, or inhibition problems | Require evidence review and display alternative explanations |
| Automation bias | Parasuraman and Riley; Mosier and Skitka | Users over-trust automated output | Analyst accepts CDSS concern without inspecting data quality | Show uncertainty, data warnings, and counter-evidence |
| Complacency | Human factors literature | Under-monitoring because system appears reliable | Drift or artifact accumulation missed | Trend monitoring, audit log, reproducibility bundle |
| Alert fatigue | Clinical decision support literature | Excessive low-value warnings reduce responsiveness | Important cognitive signals ignored | Severity tiers, deduplication, minimum evidence thresholds |
| Explanation transparency | Human-AI interaction research | Opaque recommendations reduce trust calibration | Poor user calibration to system correctness | Metric-linked local explanations |
| Calibration | Decision support evaluation literature | User cannot judge when system is right or wrong | Over-reliance or under-reliance | Credible intervals and limitation statements |
| Human override | Safety-critical system design | Automation may discourage dissent | Clinician or researcher cannot correct system | Explicit override workflow and audit trail |
| Privacy by design | Data protection and research ethics | Raw behavioral data may be sensitive | Re-identification or misuse risk | Raw data ignored in Git, consent-aware pipeline design |
| Reporting standards | DECIDE-AI-style expectations | Poorly reported interventions cannot be evaluated | Reproducibility and validity unclear | Artifact registry, config hash, test logs, close-out package |

## 4. Mapping to AX-CPT CDSS

### 4.1 What the literature validates

The literature supports the need for:

- transparent data contracts
- non-destructive cleaning
- explicit uncertainty
- separation of data-quality and cognitive signals
- human-in-the-loop review
- reproducible audit trails

### 4.2 What the literature changes

It changes the design from:

    compute score -> display risk label

to:

    validate data -> compute psychometrics -> generate candidate interpretations -> show evidence and uncertainty -> require human review

### 4.3 Remaining gaps

Current gaps:

- no empirical patient or operator validation
- synthetic benchmark only
- no prospective clinical outcome linkage
- no real-time usability study
- no calibrated risk model
- no formal human-factors evaluation with target users

## 5. Anti-Fabrication Rule

This document must not claim validated clinical effectiveness.

Allowed claims:

- architectural design
- literature-informed mitigation
- synthetic pipeline validation
- reproducibility engineering

Disallowed claims:

- diagnosed cognitive disorder
- proven clinical improvement
- validated decision accuracy
- regulatory readiness

## 6. Design Requirements Derived from Literature

The CDSS must:

1. Display evidence for every candidate concern.
2. Display uncertainty for every inferred state.
3. Display alternative explanations.
4. Separate data-quality alerts from cognitive alerts.
5. Avoid binary labels without confidence context.
6. Allow human override.
7. Log all exclusions and warnings.
8. Preserve reproducibility bundles.
9. Avoid alert fatigue through severity classification.
10. Treat synthetic benchmark results as pipeline validation only.

## 7. Traceability

This deliverable should be read together with:

- docs/26_cognitive_ergonomics_matrix_b1.md
- docs/27_cdss_architecture_and_contracts.md
- docs/29_final_methodological_report.md
- docs/30_executive_summary_and_closeout.md

## 8. Exit Checklist

- Diagnostic reasoning framework synthesized.
- CDSS failure modes identified.
- Each literature finding mapped to architecture.
- Gaps explicitly listed.
- Anti-overclaiming rule enforced.
- Human-in-the-loop requirement formalized.
