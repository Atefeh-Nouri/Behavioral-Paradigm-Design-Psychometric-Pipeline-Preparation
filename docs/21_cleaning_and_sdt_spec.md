# Psychometric Cleaning & SDT Metric Specification (Day 21)

## 1. Non-Destructive Cleaning Engine

### 1.1 Absolute Cutoffs
- Min RT: $150.0\,\text{ms}$ (anticipation boundary).
- Max RT: $2000.0\,\text{ms}$ (extreme slow outlier).

### 1.2 Median Absolute Deviation (MAD) Filtering
Computed within-subject exclusively on correct $AX$ trials:
$$\text{MAD} = 1.4826022185056 \times \operatorname{median}\left(\left|RT - \operatorname{median}(RT)\right|\right)$$
$$\text{Lower Bound} = \max\left(150.0, \operatorname{median}(RT) - 3.0 \times \text{MAD}\right)$$
$$\text{Upper Bound} = \min\left(2000.0, \operatorname{median}(RT) + 3.0 \times \text{MAD}\right)$$

---

## 2. Signal Detection Theory (Hautus, 1995)

$$H_{\text{adj}} = \frac{N_{\text{Hits}} + 0.5}{N_{\text{Signal Trials}} + 1.0}, \quad FA_{\text{adj}} = \frac{N_{\text{False Alarms}} + 0.5}{N_{\text{Noise Trials}} + 1.0}$$
$$d' = \Phi^{-1}(H_{\text{adj}}) - \Phi^{-1}(FA_{\text{adj}})$$
$$c = -0.5 \left[ \Phi^{-1}(H_{\text{adj}}) + \Phi^{-1}(FA_{\text{adj}}) \right]$$
$$\beta = \exp(d' \cdot c)$$

- **Global Discriminability ($d'_{\text{global}}$)**: Signal = $AX$ Target; Noise = $AY + BX + BY$.
- **Context Discriminability ($d'_{\text{context}}$)**: Signal = $AX$ Target; Noise = $BX$ Context Lure.
- **Proactive Behavioral Index ($PBI$)**:
  $$PBI = \frac{\text{AY Error Rate} - \text{BX Error Rate}}{\text{AY Error Rate} + \text{BX Error Rate}}$$