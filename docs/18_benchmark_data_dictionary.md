# Benchmark Data Dictionary (Deliverable D5 Part 3)

| Column Name | Data Type | Physical Units | Allowable / Expected Range | Nullable | Generative Algorithm / Source Rule |
| :--- | :--- | :--- | :--- | :---: | :--- |
| `session_id` | `VARCHAR(64)` | UUIDv4 String | 36 characters | No | Generated via `uuid.UUID()` using subject seed. |
| `participant_id` | `VARCHAR(32)` | Categorical String | `SUBJ_001` to `SUBJ_050` | No | Deterministic subject sequence index. |
| `block_index` | `INT16` | Integer Index | $1, 2, 3, 4$ | No | Block counter within session. |
| `block_condition` | `VARCHAR(16)` | Categorical String | `SHORT_DELAY`, `LONG_DELAY`| No | Counterbalanced via ABBA/BAAB schedule. |
| `trial_index_global` | `INT16` | Integer Index | $1$ to $400$ | No | Incremented monotonically per trial. |
| `trial_index_block` | `INT16` | Integer Index | $1$ to $100$ | No | Incremented within each block. |
| `trial_type` | `VARCHAR(8)` | Categorical String | `AX`, `AY`, `BX`, `BY` | No | Sampled via block distribution (70/10/10/10). |
| `cue_stimulus` | `CHAR(1)` | ASCII Character | `A`, `B`, `C`, `D`, `E`, `F`, `G` | No | `A` if `AX`/`AY`; sampled from `[B-G]` if `BX`/`BY`. |
| `probe_stimulus` | `CHAR(1)` | ASCII Character | `X`, `S`, `T`, `U`, `V`, `W`, `Z` | No | `X` if `AX`/`BX`; sampled from `[S-Z]` if `AY`/`BY`. |
| `required_key` | `VARCHAR(8)` | Keyboard Key | `space`, `l` | No | `space` for `AX` trials; `l` for all other trials. |
| `cpi_nominal_ms` | `FLOAT64` | Milliseconds | $1200.0, 4000.0$ | No | Target cue-probe delay from configuration. |
| `cpi_realized_ms` | `FLOAT64` | Milliseconds | $[1195.0, 4005.0]$ | No | `cpi_nominal_ms` + $\mathcal{N}(0.0, 0.4\,\text{ms})$ timing noise. |
| `fixation_realized_ms`| `FLOAT64` | Milliseconds | $[400.0, 600.0]$ | No | Sampled from $\text{Uniform}(400.0, 600.0)\,\text{ms}$. |
| `probe_onset_timestamp`| `FLOAT64` | Monotonic Seconds | $[10.0, 2500.0]$ | No | Cumulative trial chronometry onset tracker. |
| `response_key` | `VARCHAR(8)` | Keyboard Key | `space`, `l` | **Yes** | `null` on omissions; otherwise sampled via SDT logic. |
| `response_timestamp` | `FLOAT64` | Monotonic Seconds | $>$ `probe_onset_timestamp` | **Yes** | `probe_onset_timestamp` + $(RT / 1000.0)$; `null` on omission. |
| `rt_ms` | `FLOAT64` | Milliseconds | $[50.0, 1000.0]$ | **Yes** | Convolved Ex-Gaussian draw ($\mathcal{N}(\mu, \sigma) + \text{Exp}(\tau)$); `null` on omission. |
| `is_correct` | `BOOLEAN` | Boolean | `True`, `False` | No | Evaluated as `(response_key == required_key)`. |
| `outcome_code` | `VARCHAR(16)` | Categorical String | `HIT`, `CORRECT_REJECTION`, `COMMISSION_ERROR`, `OMISSION_ERROR`, `ANTICIPATION` | No | Deterministic scoring mapping from key and latency. |
| `is_anticipation` | `BOOLEAN` | Boolean | `True`, `False` | No | `True` if response occurred with $RT < 150.0\,\text{ms}$. |
| `post_error_trial` | `BOOLEAN` | Boolean | `True`, `False` | No | `True` if trial $k-1$ was an omission or commission. |
| `frame_drop_detected` | `BOOLEAN` | Boolean | `False` (nominal) | No | Telemetry indicator for display synchronization drops. |