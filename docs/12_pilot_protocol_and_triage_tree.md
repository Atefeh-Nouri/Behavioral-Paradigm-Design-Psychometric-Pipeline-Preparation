# Pilot Validation Protocol & Triage Decision Tree (Deliverable D4 Part 2)

## 1. Pilot Validation Protocol (3–5 Sessions)

### 1.1 Technical Checks
1. **Frame Drop Ratio**: $<0.1\%$ across 400 trials ($<4$ dropped frames total).
2. **Timing Drift**: Total session duration matches nominal within 1.0 second.
3. **Schema Compliance**: Pydantic schema validation passes with zero errors.

### 1.2 Behavioral Sanity Checks
1. **AX Hit Rate**: $>85\%$ in healthy adults.
2. **AY Commission Errors**: Between $10\%$ and $30\%$ (proves target prepotency).
3. **BX Delay Effect**: Long Delay ($4000\,\text{ms}$) error rate exceeds Short Delay ($1200\,\text{ms}$) error rate.
4. **Anticipation Rate**: $<3\%$ of total trials.

---

## 2. Pilot Triage Decision Tree

```mermaid
graph TD
    A[Pilot Anomaly Detected] --> B{What is the failure nature?}
    
    B -->|Dropped Frames > 0.1%| C[Technical: OS / Graphics Issue]
    B -->|AY Error Rate == 0%| D[Behavioral: Prepotency Failure]
    B -->|High Anticipations > 5%| E[Behavioral: Motor Entrainment]
    B -->|Schema Validation Fails| F[Technical: Output Code Bug]

    C --> G[Triage: Code Change]
    G --> G1[Pre-render drawables, disable OS Compositor, update GPU drivers]

    D --> H[Triage: Config Change]
    H --> H1[Shorten Probe duration or enforce speed emphasis in instructions]

    E --> I[Triage: Config Change]
    I --> I1[Increase ITI jitter window from 400ms to 800ms]

    F --> J[Triage: Code Change]
    J --> J1[Correct logging mapping to enforce Raw Data Schema v1.0]

    B -->|BX Delay effect inverted across all pilots| K[Theoretical / Structural Failure]
    K --> L[Triage: PSD Change]
    L --> L1[Reconvene panel to reconsider delay interval or cue contrast; bump PSD to v1.1]
```