# Experimental Design Specification (PSD v0.9 Section)

## 1. Candidate Design Evaluation & Decision Record

| Dimension | Candidate 1: Classic AX-CPT (Single Delay) | Candidate 2: Continuous 2-Back CPT | Candidate 3: Dual-Delay AX-CPT (Selected) |
| :--- | :--- | :--- | :--- |
| **Sustained Attention** | Moderate. Fixed delay reduces vigilance demand. | High. Continuous stream forces vigilance. | **High.** 400 trials over 31 min allows tracking of $\tau$ and $ICV$ drift. |
| **Inhibitory Control** | High. Asymmetric cueing isolates inhibition on $AY$. | Low. Withholding lacks systematic prepotency. | **Very High.** 70% prepotency induces strong motor priming; isolates $AY$ inhibition. |
| **WM Context Maintenance** | Low. Short delay minimizes context demand. | Very High. Dynamic continuous updating. | **High.** Dual Delay (1200 ms vs 4000 ms) isolates context decay. |
| **Scoring Clarity** | Very High. Explicit $AX, AY, BX, BY$ cells. | Moderate. Lure interference confounds errors. | **Very High.** Explicit $d'_{\text{context}}$, $PBI$, and Ex-Gaussian metrics per delay. |
| **Engine Feasibility** | Simple. Feed-forward sequence. | Complex. Requires running back-buffers. | **Balanced.** Feed-forward trial sequence without runtime back-buffers. |

### Decision Record
- **Selected Paradigm**: **The Dual-Delay AX-CPT Protocol**.
- **Rationale**: Isolates response inhibition ($AY$ trials), working memory context maintenance ($BX$ trials across 1200 ms vs 4000 ms delays), and sustained attention (IIV, $\tau$, omission drift) within a single feed-forward trial design.

---

## 2. Experimental Design Specification

### 2.1 Total Trial Budget & Cell Balancing
- **Total Trials**: 400 experimental trials.
- **Factorial Structure**: $2 \text{ Delays (Short: 1200 ms, Long: 4000 ms)} \times 4 \text{ Trial Types (AX, AY, BX, BY)}$.
- **Global Distribution**:
  - $AX$ (Target): $70\%$ ($N = 280$ total; $140$ Short, $140$ Long). Key: `SPACE`.
  - $AY$ (Inhibition Lure): $10\%$ ($N = 40$ total; $20$ Short, $20$ Long). Key: `L`.
  - $BX$ (Context Lure): $10\%$ ($N = 40$ total; $20$ Short, $20$ Long). Key: `L`.
  - $BY$ (Baseline Control): $10\%$ ($N = 40$ total; $20$ Short, $20$ Long). Key: `L`.

### 2.2 Stimulus Sets
- **Context Cues**: Valid = `'A'`. Invalid = sampled from `{'B', 'C', 'D', 'E', 'F', 'G'}`.
- **Target Probes**: Valid = `'X'`. Invalid = sampled from `{'S', 'T', 'U', 'V', 'W', 'Z'}`.
- Uppercase sans-serif letters, matched for height and stroke width. Look-alike characters ($O/Q, I/L$) excluded.

### 2.3 Block Structure & Counterbalancing
- **Block Layout**: 4 blocks of 100 trials each (2 Short Delay blocks, 2 Long Delay blocks).
- **Between-Subject Counterbalancing**:
  - Group A (ABBA): Short $\to$ Long $\to$ Long $\to$ Short.
  - Group B (BAAB): Long $\to$ Short $\to$ Short $\to$ Long.

### 2.4 Randomization Constraints (Run-Rules)
1. **Max Consecutive Targets**: No more than 4 consecutive $AX$ trials.
2. **Max Consecutive Non-Targets**: No more than 2 consecutive non-target trials ($AY, BX, BY$).
3. **Distractor Non-Repetition**: No identical consecutive distractor characters.

### 2.5 Calibration & Practice Protocol
1. **Phase 0 (Motor Calibration)**: 30 trials of Simple Reaction Time (SRT) to establish baseline motor execution ($t_0$).
2. **Phase 1 (Criterion Practice)**: 20 trials with immediate feedback ("CORRECT", "INCORRECT").
   - Advancement criterion: $\ge 80\%$ accuracy and zero $AX$ omissions.
   - Max 3 attempts before flagging session as uncalibrated.

### 2.6 Session Chronometry
- Short Delay Block: $\sim 5.5\,\text{minutes}$.
- Long Delay Block: $\sim 10.1\,\text{minutes}$.
- Total Active Testing Time: $\approx 31.2\,\text{minutes}$.
- Mandatory 60-second rest break between blocks (onscreen countdown).