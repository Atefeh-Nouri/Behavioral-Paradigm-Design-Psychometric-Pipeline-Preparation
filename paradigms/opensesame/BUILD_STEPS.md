# OpenSesame GUI Build Protocol: Dual-Delay AX-CPT (Deliverable D3)

This step-by-step build guide allows an experimenter to reconstruct the complete, millisecond-accurate Dual-Delay AX-CPT experiment in OpenSesame 4.x (using the `psycho` backend) in under 30 minutes without needing to hand-edit binary `.osexp` archives.

---

## 1. Environment & Display Backend Setup

1. Launch **OpenSesame 4.x**.
2. Create a new experiment (**Extended template** or **Default template**).
3. Click on the root item **`experiment`** in the overview tree:
   - **Backend**: Select `psycho` (forces V-Sync synchronization via PsychoPy/Pyglet).
   - **Resolution**: Set `Width = 1920`, `Height = 1080`.
   - **Foreground color**: `white` (or `#ffffff`).
   - **Background color**: `black` (or `#000000`).
4. In the main toolbar, click **File -> Save As** and save to:
   `paradigms/opensesame/ax_cpt_runner.osexp`

---

## 2. Global Sequence Architecture

Structure the overview tree to match this hierarchical layout:

```text
experiment (sequence)
├── init_experiment (inline_python)
├── instructions_screen (sketchpad)
├── practice_loop (loop)
│   └── practice_sequence (sequence)
│       ├── prepare_practice_trial (inline_python)
│       ├── practice_fixation (sketchpad)
│       ├── practice_cue (sketchpad)
│       ├── practice_delay (sketchpad)
│       ├── practice_probe (sketchpad)
│       ├── practice_keyboard (keyboard_response)
│       └── feedback_eval (inline_python)
├── post_practice_instructions (sketchpad)
├── block_loop (loop)
│   └── block_sequence (sequence)
│       ├── init_block (inline_python)
│       ├── trial_loop (loop)
│       │   └── trial_sequence (sequence)
│       │       ├── trial_init (inline_python)
│       │       ├── fixation_sketchpad (sketchpad)
│       │       ├── cue_sketchpad (sketchpad)
│       │       ├── delay_sketchpad (sketchpad)
│       │       ├── probe_sketchpad (sketchpad)
│       │       ├── response_keyboard (keyboard_response)
│       │       ├── score_trial (inline_python)
│       │       └── trial_logger (logger)
│       └── break_screen (sketchpad)
└── session_conclude (sketchpad)
```

## 3. Configuring Experiment Setup & Instructions

### Step 3.1: init_experiment (inline_python)

- Drag an `inline_python` item to the top of `experiment`.
- Rename it to `init_experiment`.
- In the **Run** tab, paste the code from:
  `paradigms/opensesame/inline_scripts/init_experiment.py`

### Step 3.2: instructions_screen (sketchpad)

- Set **Duration**: `keypress`.
- Add central text element:

```text
WELCOME TO THE COGNITIVE ASSESSMENT

Respond to pairs of letters:
- Press SPACE ONLY when you see an 'A' followed immediately by an 'X'.
- For any other letter combination, press 'L'.

Press SPACE to begin practice.
```

- Font size: `24`. Color: `white`.

## 4. Assembling the Practice Sequence

Click on `practice_loop`:

- Set **Repeat**: `1`.
- Set **Order**: `sequential`.
- Number of cycles: `20` (will be driven by inline code).

Inside `practice_sequence`:

- `prepare_practice_trial` (inline_python): Run phase samples practice trial definitions.
- `practice_fixation` (sketchpad): Duration = `500`. Text element `+` at (0, 0).
- `practice_cue` (sketchpad): Duration = `300`. Text element `[cue_char]` at (0, 0).
- `practice_delay` (sketchpad): Duration = `1200`. Text element `+` at (0, 0).
- `practice_probe` (sketchpad): Duration = `300`. Text element `[probe_char]` at (0, 0).
- `practice_keyboard` (keyboard_response):
  - Allowed responses: `space;l;escape`.
  - Timeout: `1000`.
  - Flush pending keypresses: `yes`.
- `feedback_eval` (inline_python): In the **Run** tab, paste code from:
  `paradigms/opensesame/inline_scripts/feedback_eval.py`

After `practice_loop`, insert `post_practice_instructions` (sketchpad):

- Duration: `keypress`.
- Text: `Practice complete!\n\nNo feedback will be given during the main experiment.\n\nPress SPACE to begin Block 1.`

## 5. Assembling the Experimental Loop

### Step 5.1: block_loop

- Set **Repeat**: `1`. **Order**: `sequential`. Cycles: `4` (Block 1 to 4).
- Add column `block_nr` with values `1, 2, 3, 4`.

### Step 5.2: init_block (inline_python)

Insert at the beginning of `block_sequence`. In the **Run** tab, generate 100 trials using bounded rejection sampling complying with run-rules:

```python
from paradigms.psychopy.trial_logic import TrialSequenceGenerator
seq_gen = TrialSequenceGenerator(exp.vars.config, seed=int(var.subject_nr) + var.block_nr)
exp.vars.current_block_trials = seq_gen.generate_block(exp.vars.block_conditions[var.block_nr - 1])
```

### Step 5.3: trial_loop

Inside `block_sequence`, set **Repeat**: `100`. **Order**: `sequential`.

### Step 5.4: trial_sequence Items

- `trial_init` (inline_python): Paste code from `paradigms/opensesame/inline_scripts/trial_init.py`.
- `fixation_sketchpad` (sketchpad): Duration `[fixation_duration_ms]`. Text element `+` at (0, 0).
- `cue_sketchpad` (sketchpad): Duration `300`. Text element `[cue_stimulus]` at (0, 0), font size 32.
- `delay_sketchpad` (sketchpad): Duration `[cpi_nominal_ms]`. Text element `+` at (0, 0).
- `probe_sketchpad` (sketchpad): Duration `300`. Text element `[probe_stimulus]` at (0, 0), font size 32.
- `response_keyboard` (keyboard_response):
  - Allowed responses: `space;l;escape`.
  - Timeout: `1000`.
  - Event timestamping: `Psychtoolbox low-latency`.
- `score_trial` (inline_python): Paste code from `paradigms/opensesame/inline_scripts/score_trial.py`.
- `trial_logger` (logger): Click **Custom log items** → select only the 22 variables prefixed with `col_`:
  `col_session_id, col_participant_id, col_block_index, col_block_condition, col_trial_index_global, col_trial_index_block, col_trial_type, col_cue_stimulus, col_probe_stimulus, col_required_key, col_cpi_nominal_ms, col_cpi_realized_ms, col_fixation_realized_ms, col_probe_onset_timestamp, col_response_key, col_response_timestamp, col_rt_ms, col_is_correct, col_outcome_code, col_is_anticipation, col_post_error_trial, col_frame_drop_detected.`
- `break_screen` (sketchpad): Placed at the end of `block_sequence` (runs between blocks). Duration `60000` (or keypress after 60 s countdown). Text: `Block complete! Rest your eyes.\n\nPress SPACE to continue.`

## 6. Pre-Flight Verification Check

1. Run a test run by clicking **Run in window** (blue arrow).
2. Set Subject number = `999`.
3. Verify that:
   - Cue and Probe letters render cleanly without display tearing.
   - Omissions after 1000 ms advance without freezing.
   - The generated CSV in `data/` contains exactly 22 columns matching Raw Data Schema v1.0.
