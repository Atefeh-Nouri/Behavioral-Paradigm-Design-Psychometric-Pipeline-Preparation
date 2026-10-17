# OpenSesame Equivalent Build & Parity Guide (Deliverable D3)

## 1. Overview & Item Hierarchy
The OpenSesame implementation mirrors the PsychoPy state machine, block balancing, and 22-column logging schema using OpenSesame 4.x items and inline Python scripting:

```text
ax_cpt_opensesame (experiment)
├── init_experiment (inline_python: loads config, generates session UUID)
├── instructions_screen (sketchpad: task directions)
├── practice_loop (loop) -> practice_sequence
│   ├── prepare_practice_trial (inline_python)
│   ├── practice_stimuli (sketchpads: fixation, cue, delay, probe)
│   ├── practice_response (keyboard_response)
│   └── feedback_eval (inline_python)
├── experiment_sequence
│   └── block_loop (loop: 4 blocks, counterbalanced delays)
│       └── block_sequence
│           ├── init_block (inline_python: trial generation via run-rules)
│           ├── trial_loop (loop: 100 iterations)
│           │   └── trial_sequence
│           │       ├── trial_init (inline_python)
│           │       ├── fixation_sketchpad (sketchpad)
│           │       ├── cue_sketchpad (sketchpad)
│           │       ├── delay_sketchpad (sketchpad)
│           │       ├── probe_sketchpad (sketchpad)
│           │       ├── response_collector (keyboard_response)
│           │       ├── score_trial (inline_python: FSM scoring & schema mapping)
│           │       └── trial_logger (logger: writes 22 columns)
│           └── break_screen (sketchpad: 60s rest)
└── session_conclude (sketchpad)
```

## 2. Platform Timing Parity & Compensation

| Dimension | PsychoPy Engine (Coder) | OpenSesame (`psycho` backend) | Timing Divergence & Compensation Mechanism |
| :--- | :--- | :--- | :--- |
| **Display Rendering** | Explicit `win.flip()` frame budgets. | Canvas elements rendered during run. | **Mitigation:** Pre-render sketchpad canvases in `prepare()` phase of sequence to avoid mid-trial garbage collection drops. |
| **Display Backend** | Direct Pyglet/GLFW context. | PsychoPy backend (`psycho`). | Set OpenSesame display backend to `psycho` with V-Sync enabled. |
| **Input Polling** | Psychtoolbox low-latency hooks. | Standard `keyboard_response`. | Input latency differences are constant and captured by non-decision time ($t_0$) in DDM modeling. |
| **Output Data Schema** | Flat CSV enforced via validator. | Native OpenSesame custom logger. | Logger configured to export only the 22 `col_*` variables matching `Raw Data Schema v1.0`. |