# Benchmark Analysis & Reproducibility Statement (Day 25 / Deliverables D6 & D7)

## 1. Benchmark v1.0 Cohort Psychometric Norms ($N = 49$)

```
                            COHORT PSYCHOMETRIC NORMS
┌──────────────────────────────────────────────┬───────────────────────────────┐
│ Metric Dimension                             │ Mean (SD) [95% CI]            │
├──────────────────────────────────────────────┼───────────────────────────────┤
│ Target Hit Rate (AX)                         │ 91.82% (3.41%) [90.87, 92.77] │
│ Conflict Commission Rate (AY)                │ 16.94% (4.12%) [15.79, 18.09] │
│ Context Maintenance Commission Rate (BX)     │ 14.80% (5.21%) [13.34, 16.26] │
│ Baseline Non-Target Commission Rate (BY)     │  1.42% (0.89%) [ 1.17,  1.67] │
├──────────────────────────────────────────────┼───────────────────────────────┤
│ Target Response Latency (AX M_RT)            │ 467.42 ms (35.81) [457, 477]  │
│ Intra-Individual Variability (AX ICV)        │  0.218 (0.034) [0.208, 0.228] │
│ Conflict Slowing Cost (AY Correct - AX Hit)  │ +66.21 ms (14.12) [62.3, 70.1]│
│ WM Delay Degradation Cost (BX Long - Short)  │ +17.34% (4.11%) [16.2, 18.5]  │
│ Post-Error Slowing Delta (PES)               │ +34.12 ms (11.89) [30.8, 37.4]│
│ Vigilance Decrement Slope (Blocks 1 to 4)    │ +10.82 ms/Block (3.11)        │
└──────────────────────────────────────────────┴───────────────────────────────┘
```

---

## 2. Psychometric Split-Half Reliability

Calculated across compliant participants using the Spearman-Brown prophecy formula ($r_{\text{SB}} = \frac{2 r}{1 + r}$):

| Psychometric Construct | Observed Metric | Uncorrected ($r_{\text{half}}$) | Spearman-Brown ($r_{\text{SB}}$) | Quality Tier |
| :--- | :--- | :---: | :---: | :--- |
| **Sustained Attention** | Mean RT ($\text{M}_{\text{RT}}$) | $.912$ | $\mathbf{.954}$ | **Excellent** ($> .90$) |
| **Sustained Attention** | Intra-Individual Variability ($ICV$) | $.764$ | $\mathbf{.866}$ | **Good** ($> .80$) |
| **Cognitive Control** | Conflict Slowing Cost ($\Delta RT_{AY}$) | $.642$ | $\mathbf{.782}$ | **Acceptable** ($> .75$) |
| **Working Memory** | Context Sensitivity ($d'_{\text{context}}$)| $.781$ | $\mathbf{.877}$ | **Good** ($> .80$) |
| **Executive Function** | Proactive Behavioral Index ($PBI$) | $.682$ | $\mathbf{.811}$ | **Good** ($> .80$) |

---

## 3. Formal Pipeline Freeze Declaration

```
===================================================================================================
PIPELINE FREEZE SIGN-OFF: DELIVERABLES D6 & D7
===================================================================================================
Pipeline Identifiers:
  - Deliverable D6: Python Psychometric Engine (v1.0.0-frozen)
  - Deliverable D7: R Tidyverse Psychometric Engine (v1.0.0-frozen)

Status: FROZEN & LOCKED FOR RESEARCH REPRODUCIBILITY
Contracts Verified: Cleaned Trials (Contract 1) & Subject Summaries (Contract 2).
Cross-Language Parity: Confirmed within 1e-6 tolerance.
===================================================================================================
```

---

## 4. End-to-End Methodological Reproducibility Statement

```bash
# 1. Environment Setup
git clone https://github.com/cognitive-arch-lab/ax_cpt_cognitive_lab.git
cd ax_cpt_cognitive_lab
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Rscript -e "install.packages('renv'); renv::restore()"

# 2. Benchmark Dataset Generation (Deliverable D5)
python synthetic_data/generate_benchmark.py --config config/config.yaml --seed 2026

# 3. Pipeline Execution (Deliverables D6 & D7)
python analysis_python/cpt_pipeline.py --config config/pipeline_config.yaml
Rscript analysis_r/cpt_cleaning_pipeline.R

# 4. Automated Testing & Equivalence Verification
pytest tests/ -v
python tests/verify_equivalence.py
```