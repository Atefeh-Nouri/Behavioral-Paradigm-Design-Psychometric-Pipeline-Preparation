# Literature Synthesis Matrix A: Paradigms & Psychometrics (Deliverable D8)

## 1. Paradigm Family Synthesis Matrix

| Paradigm | Canonical Reference | Standard Timing Architecture | Trial Count & Load Design | Test-Retest Reliability ($r_{tt}$ / ICC) | Cognitive Load / Construct Sensitivity | Documented Methodological Pitfalls & Confounds |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Standard CPT (Conners / X-Type)** | Rosvold et al. (1956); Conners (2000) | Stimulus: 100–250 ms;<br>ISI: 1000–2000 ms (often variable/jittered);<br>Response window: ~1000 ms. | 360–400 trials;<br>Target ratio: 80% to 90% Go (or inverse in Not-X: 90% Go, 10% No-Go). | $r_{tt} \approx .65\text{--}.85$ for mean RT;<br>$r_{tt} \approx .40\text{--}.65$ for commission errors [verify]. | High sensitivity to sustained tonic alertness and motor withholding; low working memory demand (zero updating). | Ceiling effects in healthy adults; fails to distinguish motor speed from attentional lapses; susceptible to speed-accuracy trade-offs (SATO). |
| **AX-CPT** | Servan-Schreiber et al. (1996); Braver et al. (2001, 2005) | Cue: 300–500 ms;<br>Delay/CPI: Short (1000 ms) vs. Long (4000–5000 ms);<br>Probe: 300–500 ms;<br>ITI: 1000–2000 ms. | 200–400 trials total;<br>Typical cell split: 70% AX (target), 10% AY, 10% BX, 10% BY. | $r_{tt} \approx .70\text{--}.80$ for mean RT / $d'_{\text{context}}$;<br>$r_{tt} \approx .50\text{--}.70$ for error indices [verify]. | High sensitivity to proactive vs. reactive control dynamics; delay manipulation directly tests context maintenance in prefrontal cortex. | Low trial counts in minority cells (e.g., 20 AY/BX trials per block) induce high sampling variance; extreme cell error rates (0% or 100%) distort linear statistics. |
| **CPT-IP (Identical Pairs)** | Cornblatt et al. (1988, 1989) | Stimulus: 50 ms (flashed);<br>ISI: 1000 ms fixed;<br>Rapid presentation stream. | 300–600 trials;<br>Target: consecutive identical stimuli (~20% occurrence). | $r_{tt} \approx .60\text{--}.75$ for $d'$ across clinical and healthy cohorts [verify]. | Loads heavily on early visual sensory buffer and active short-term phonological/visual matching; eliminates explicit cue–probe cueing. | High perceptual/visual encoding confound; stimulus discrimination difficulty can mask executive attention deficits; high floor effects if stimulus duration $<50\,\text{ms}$. |
| **$N$-Back (Continuous Updating)** | Kirchner (1958); Owen et al. (2005); Kane et al. (2007) | Stimulus: 500 ms;<br>ISI: 1500–2000 ms;<br>Response window: matched to ISI. | 100–200 trials per load level (e.g., 1-Back, 2-Back, 3-Back);<br>Target ratio: 20% to 33%. | $r_{tt} \approx .50\text{--}.75$ for $d'$;<br>Poor correlation ($r \approx .20\text{--}.30$) with complex WM span measures (*Kane et al., 2007*). | High sensitivity to active memory updating, item replacement, and continuous interference resolution. | Strategy shifts: participants often revert to passive familiarity matching rather than active content updating; high rate of unmodeled false alarms to lure items (e.g., $(N-1)$ or $(N+1)$ matches). |

---

## 2. RT Distribution & Psychometric Scoring Methodology

### 2.1 Ex-Gaussian Modeling
Human response latencies exhibit skewness and elongated tails reflecting attentional lapses (*Matzke & Wagenmakers, 2009*). The distribution is modeled as a convolution of Gaussian and Exponential distributions:

$$f(t; \mu, \sigma, \tau) = \frac{1}{\tau\sqrt{2\pi}} \exp\left(\frac{\mu - t}{\tau} + \frac{\sigma^2}{2\tau^2}\right) \Phi\left(\frac{t - \mu}{\sigma} - \frac{\sigma}{\tau}\right)$$

$$\mathbb{E}[T] = \mu + \tau, \quad \operatorname{Var}(T) = \sigma^2 + \tau^2$$

- $\mu$: Central tendency of normal component (sensorimotor speed).
- $\sigma$: Spread of normal component.
- $\tau$: Mean and standard deviation of exponential tail (attentional lapses).
- *Sample Size Rule*: Requires $\ge 100$ valid responses per condition cell for stable Maximum Likelihood Estimation (MLE) (*Whelan, 2008*).

### 2.2 Signal Detection Theory (SDT) with Hautus (1995) Log-Linear Correction
To prevent infinite $Z$-scores when hit or false alarm rates reach 0 or 1:

$$H_{\text{adj}} = \frac{N_{\text{Hits}} + 0.5}{N_{\text{Signal Trials}} + 1.0}, \quad FA_{\text{adj}} = \frac{N_{\text{False Alarms}} + 0.5}{N_{\text{Noise Trials}} + 1.0}$$

$$d' = \Phi^{-1}(H_{\text{adj}}) - \Phi^{-1}(FA_{\text{adj}})$$

$$c = -\frac{1}{2} \left[ \Phi^{-1}(H_{\text{adj}}) + \Phi^{-1}(FA_{\text{adj}}) \right]$$

---

## 3. Reusable Paradigm Design Recommendations

1. **Enforce Target Prepotency ($\ge 70\%$)**: Necessary to measure proactive inhibition and context gating.
2. **Parametric Cue-Probe Interval (CPI)**: Include both short ($1200\,\text{ms}$) and long ($4000\,\text{ms}$) delays to isolate context maintenance in DLPFC.
3. **Censor Latencies $<150\,\text{ms}$**: Anticipatory motor entrainment must be isolated from cognitive decisions.
4. **Mandate Minimum 100 Trials Per Primary Cell**: Ensures stable estimation of Ex-Gaussian $\tau$ and DDM parameters.
5. **Universal Hautus (1995) Adjustment**: Apply $+0.5 / +1.0$ correction across all SDT cells.
6. **Deploy Uniform Jittered ITIs (1000–1400 ms)**: Prevents rhythmic motor entrainment.
7. **Baseline Motor Calibration**: Dedicated SRT block to isolate non-decision time ($t_0$).
8. **Structured Rest Pauses Every 8–10 Minutes**: Minimizes non-target ocular and muscular fatigue.
9. **Visual Separation of Distractors**: Exclude distractor letters visually or phonologically identical to targets.
10. **Post-Error Tracking**: Flag trials following errors to calculate Post-Error Slowing ($PES$).