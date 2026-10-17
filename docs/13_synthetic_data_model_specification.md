# Synthetic Data Generative Model Specification (Day 13)

## 1. Generative Architecture Overview

The synthetic behavioral data generator operationalizes a hierarchical Monte Carlo architecture linking population-level priors to trial-level Ex-Gaussian response latencies and Signal Detection Theory decision thresholds.

```
                         POPULATION HYPERPARAMETERS
                       (μ_pop, σ_pop, τ_pop, d'_pop, c_pop)
                                      │
                                      ▼
                        SUBJECT-LEVEL LATENT TRAITS (θ_i)
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
  Sensorimotor RT            Attentional Lapses             Context & Sensitivity
   (μ_i, σ_i ~ Normal)         (τ_i ~ Gamma)               (d'_i, c_i ~ Bivariate)
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                           TRIAL-LEVEL GENERATOR
        ┌───────────────────────────────────────────────────────────┐
        │ 1. Context Modulation: Condition Shifts (AY, BX, Delay)   │
        │ 2. Temporal Dynamics: Vigilance Drift β_time * TrialIndex │
        │ 3. Latency: Ex-Gaussian Convolution (Gaussian + Exp)      │
        │ 4. Decision: Signal Detection Threshold Crossing (d', c)  │
        │ 5. Artifact Filter: Anticipation (<150ms) & Lapses (>1s)  │
        └───────────────────────────────────────────────────────────┘
```

---

## 2. Mathematical Specification

### 2.1 Subject-Level Trait Sampling
For participant $i \in \{1, \dots, N\}$:
$$\mu_i \sim \mathcal{N}(\mu_{\text{pop}}, \sigma^2_{\mu,\text{pop}})$$
$$\sigma_i \sim \text{TruncatedNormal}(\sigma_{\text{pop}}, \sigma^2_{\sigma,\text{pop}}, a=10.0)$$
$$\tau_i \sim \text{Gamma}\left(\alpha = \frac{\tau_{\text{pop}}^2}{\sigma^2_{\tau,\text{pop}}}, \beta = \frac{\tau_{\text{pop}}}{\sigma^2_{\tau,\text{pop}}}\right)$$
$$\begin{bmatrix} d'_i \\ c_i \end{bmatrix} \sim \mathcal{N}\left( \begin{bmatrix} d'_{\text{pop}} \\ c_{\text{pop}} \end{bmatrix}, \begin{bmatrix} \sigma^2_{d'} & \rho_{dc}\sigma_{d'}\sigma_c \\ \rho_{dc}\sigma_{d'}\sigma_c & \sigma^2_c \end{bmatrix} \right)$$

### 2.2 Trial-Level Reaction Time Generation
For trial $k \in \{1, \dots, 400\}$, condition cell $C \in \{AX, AY, BX, BY\}$, and delay $D \in \{\text{Short}, \text{Long}\}$:
$$\mu_{ik} = \mu_i + \Delta\mu_{\text{condition}}(C) + \Delta\mu_{\text{delay}}(D, C) + \beta_{\mu} \cdot \left(\frac{k}{400}\right)$$
$$\sigma_{ik} = \sigma_i + \Delta\sigma_{\text{condition}}(C)$$
$$\tau_{ik} = \tau_i + \Delta\tau_{\text{delay}}(D, C) + \beta_{\tau} \cdot \left(\frac{k}{400}\right)$$

Reaction time is drawn via independent convolution:
$$X_{ik} \sim \mathcal{N}(\mu_{ik}, \sigma_{ik}^2), \quad Y_{ik} \sim \text{Exponential}(\tau_{ik})$$
$$T_{\text{lat}, ik} = X_{ik} + Y_{ik}$$

If trial $k-1$ resulted in an error, $\mu_{ik}$ is incremented by $\Delta\mu_{\text{PES}} = +35.0\,\text{ms}$.

### 2.3 Decision Outcome Engine (SDT Threshold Logic)
Sensory evidence $e_{ik} \sim \mathcal{N}(\delta_{ik}, 1.0)$, where:
- $AX$ (Target): $\delta_{ik} = d'_i$
- $AY$ (Valid Cue, Invalid Probe): $\delta_{ik} = 0.50 \cdot d'_i$
- $BX$ (Invalid Cue, Valid Probe):
  - Short Delay: $\delta_{ik} = 0.15 \cdot d'_i$
  - Long Delay: $\delta_{ik} = 0.15 \cdot d'_i + \Delta_{\text{decay}, i}$
- $BY$ (Baseline Control): $\delta_{ik} = 0.0$

Response selection:
$$\text{Response} = \begin{cases} \text{TARGET\_KEY ("space")}, & \text{if } e_{ik} > c_i \\ \text{NON\_TARGET\_KEY ("l")}, & \text{otherwise} \end{cases}$$

---

## 3. Artifact & Technical Anomaly Rules

1. **Anticipations ($RT < 150\,\text{ms}$)**:
   - Probability: $p_{\text{ant}} \sim \text{Beta}(1.5, 98.5)$ (mean $\approx 1.5\%$).
   - Latency: $T_{\text{ant}} \sim \text{Uniform}(50.0, 149.0)\,\text{ms}$. Key chosen at random.
2. **Attentional Lapses & Omissions**:
   - Latencies exceeding $1000\,\text{ms}$ clamp to `OMISSION_ERROR` ($RT = \text{null}$, key = null).
   - Baseline omission probability: $p_{\text{omiss}} \sim \text{Beta}(1.0, 99.0)$.
3. **Dataset-Level Structural Injections**:
   - Dropped rows: $0.5\%$ probability per trial (simulating packet drops).
   - Duplicated rows: $0.25\%$ probability per session.
   - Clock overflows: $0.25\%$ probability of logging corrupt timestamps ($RT < 0$ or $RT > 10000\,\text{ms}$).
   - Stress subject (Subject 50): Simulated near-chance discriminability ($d' = 0.20$), severe lapse tails ($\tau = 320\,\text{ms}$), and elevated omissions ($18\%$) to validate pipeline attrition rejection.

---

## 4. Population Parameter Table

| Parameter Name | Symbol | Population Mean ($\mu_{\text{pop}}$) | Between-Subject SD ($\sigma_{\text{pop}}$) | Condition / Dynamic Shift ($\Delta$) | Empirical & Theoretical Rationale |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Gaussian Central RT** | $\mu$ | $380.0\,\text{ms}$ | $35.0\,\text{ms}$ | $AY: +65.0\,\text{ms}$<br>$BX: +20.0\,\text{ms}$ | Conflict interference on $AY$ trials slows motor execution (*Braver et al., 2001*). |
| **Gaussian RT StdDev** | $\sigma$ | $42.0\,\text{ms}$ | $8.0\,\text{ms}$ | $AY: +15.0\,\text{ms}$ | Response conflict increases trial-by-trial variance. |
| **Exponential Tail** | $\tau$ | $85.0\,\text{ms}$ | $22.0\,\text{ms}$ | $BX_{\text{Long}}: +35.0\,\text{ms}$ | Context degradation across delay manifests as long-tail lapses (*Matzke & Wagenmakers, 2009*). |
| **Vigilance RT Drift** | $\beta_{\mu}$ | $+30.0\,\text{ms}$ | $10.0\,\text{ms}$ | Linear over 400 trials | Tonic alertness decrement across 30 minutes (*Parasuraman et al., 1998*). |
| **Lapse Tail Drift** | $\beta_{\tau}$ | $+25.0\,\text{ms}$ | $8.0\,\text{ms}$ | Linear over 400 trials | Mind-wandering / DMN intrusion frequency increases with time-on-task. |
| **Baseline Sensitivity** | $d'_{\text{base}}$ | $3.40$ | $0.45$ | — | High discriminability of simple suprathreshold character targets. |
| **Target Criterion** | $c$ | $1.10$ | $0.25$ | — | Conservative criterion balancing 70% target prepotency. |
| **Post-Error Slowing** | $\Delta\mu_{\text{PES}}$| $+35.0\,\text{ms}$ | $12.0\,\text{ms}$ | Trial $N+1$ after error | Adaptive motor threshold elevation (*Dutilh et al., 2012*). |