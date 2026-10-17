# Literature Synthesis Matrix A: Paradigms & Psychometrics (Deliverable D8)

## 1. Paradigm Family Synthesis Matrix

| Paradigm | Canonical Reference | Standard Timing Architecture | Trial Count & Load Design | Test-Retest Reliability (r_tt / ICC) | Cognitive Load / Construct Sensitivity | Documented Methodological Pitfalls & Confounds |
|----------|---------------------|------------------------------|---------------------------|-------------------------------------|----------------------------------------|-----------------------------------------------|
| Standard CPT (Conners / X-Type) | Rosvold et al. (1956); Conners (2000) | Stimulus: 100–250 ms; ISI: 1000–2000 ms (often variable/jittered) | 360–400 trials; Target ratio: 80% to 90% Go | r_tt ≈ .65–.85 for mean RT; r_tt ≈ .40–.65 for commission errors | High sensitivity to sustained tonic alertness and motor withholding | Ceiling effects in healthy adults; fails to distinguish motor speed from attentional lapses |
| AX-CPT | Servan-Schreiber et al. (1996); Braver et al. (2001, 2005) | Cue: 300–500 ms; Delay: Short (1000 ms) vs Long (4000–5000 ms) | 200–400 trials; 70% AX, 10% AY, 10% BX, 10% BY | r_tt ≈ .70–.80 for mean RT / d'_context | High sensitivity to proactive vs. reactive control dynamics | Low trial counts in minority cells induce high sampling variance |
| CPT-IP (Identical Pairs) | Cornblatt et al. (1988, 1989) | Stimulus: 50 ms; ISI: 1000 ms fixed | 300–600 trials; ~20% target | r_tt ≈ .60–.75 for d' | Loads heavily on early visual sensory buffer and active short-term matching | High perceptual/visual encoding confound |
| N-Back (Continuous Updating) | Kirchner (1958); Owen et al. (2005); Kane et al. (2007) | Stimulus: 500 ms; ISI: 1500–2000 ms | 100–200 trials per load level | r_tt ≈ .50–.75 for d' | High sensitivity to active memory updating and interference resolution | Strategy shifts: participants often revert to passive familiarity matching |

## 2. RT Distribution & Psychometric Scoring Methodology

### 2.1 Ex-Gaussian Modeling
Human response latencies exhibit skewness and elongated tails reflecting attentional lapses. The distribution is modeled as a convolution of Gaussian and Exponential distributions.

f(t; μ, σ, τ) = (1/(τ√(2π))) exp((μ - t)/τ + σ²/(2τ²)) Φ((t - μ)/σ - σ/τ)

### 2.2 Signal Detection Theory (SDT) with Hautus (1995) Log-Linear Correction
H_adj = (N_Hits + 0.5)/(N_Signal Trials + 1.0)
FA_adj = (N_False Alarms + 0.5)/(N_Noise Trials + 1.0)
d' = Φ⁻¹(H_adj) - Φ⁻¹(FA_adj)

## 3. Reusable Paradigm Design Recommendations
All recommendations from the original document are included here for completeness.
