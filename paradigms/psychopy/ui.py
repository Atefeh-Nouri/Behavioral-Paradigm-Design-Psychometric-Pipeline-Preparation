"""
Interface and Practice Manager.
Executes instructions, structured rest breaks, and criterion-gated practice.
"""

from typing import List
from psychopy import visual, core

try:
    from engine import PsychopyEngine
    from trial_logic import TrialDefinition, TrialSequenceGenerator
    from trial_executor import TrialExecutor
except ImportError:
    from .engine import PsychopyEngine
    from .trial_logic import TrialDefinition, TrialSequenceGenerator
    from .trial_executor import TrialExecutor


class UIManager:
    """Manages visual presentation of task instructions and rest breaks."""
    def __init__(self, engine: PsychopyEngine, config: dict):
        self.engine = engine
        self.config = config
        text_cfg = self.config["stimuli"]
        self.msg_stim = visual.TextStim(
            self.engine.win, text="", height=0.04,
            color=text_cfg["font_color"], font=text_cfg["font"],
            wrapWidth=0.8
        )

    def display_message_and_wait(self, text: str, advance_key: str = "space") -> None:
        self.msg_stim.text = text
        self.msg_stim.draw()
        self.engine.win.flip()

        self.engine.kb.clearEvents()
        while True:
            keys = self.engine.kb.getKeys(keyList=[advance_key, "escape"], waitRelease=False)
            if keys:
                if keys[0].name == "escape":
                    raise KeyboardInterrupt("Session aborted by user.")
                break
            self.engine.win.flip()

    def run_rest_break(self, block_index: int, total_blocks: int) -> None:
        """Executes a mandatory 60s break with an active onscreen countdown."""
        min_sec = int(self.config["timing"]["break_duration_seconds"])
        break_clock = core.CountdownTimer(min_sec)

        while break_clock.getTime() > 0:
            remaining = int(break_clock.getTime())
            self.msg_stim.text = (
                f"Block {block_index} of {total_blocks} Complete.\n\n"
                f"Please rest your eyes.\n\n"
                f"Break remaining: {remaining} seconds..."
            )
            self.msg_stim.draw()
            self.engine.win.flip()

        self.display_message_and_wait(
            f"Break concluded.\n\nPress SPACE when you are ready to start Block {block_index + 1}."
        )


class PracticeManager:
    """Runs the criterion-gated practice blocks."""
    def __init__(self, engine: PsychopyEngine, executor: TrialExecutor, config: dict):
        self.engine = engine
        self.executor = executor
        self.config = config
        self.feedback_stim = visual.TextStim(
            self.engine.win, text="", height=0.06, font="Arial"
        )

    def run_practice(self) -> bool:
        generator = TrialSequenceGenerator(self.config)
        practice_cfg = self.config["calibration"]["practice"]

        for attempt in range(1, practice_cfg["max_practice_attempts"] + 1):
            trials = generator.generate_block("SHORT_DELAY")[:practice_cfg["total_trials"]]
            correct_count = 0
            ax_omissions = 0

            for i, t_def in enumerate(trials):
                result = self.executor.execute_trial(t_def, i + 1, i + 1, False)

                # Render feedback
                if result.is_correct:
                    correct_count += 1
                    self.feedback_stim.text = "CORRECT"
                    self.feedback_stim.color = [-1.0, 1.0, -1.0]  # Green
                else:
                    self.feedback_stim.text = "INCORRECT"
                    self.feedback_stim.color = [1.0, -1.0, -1.0]  # Red
                    if t_def.trial_type == "AX" and result.outcome_code == "OMISSION_ERROR":
                        ax_omissions += 1

                feed_frames = self.engine.clock_manager.ms_to_frames(practice_cfg["feedback_duration_ms"])
                self.engine.present_stimulus_frames(self.feedback_stim, feed_frames, i)

            accuracy = correct_count / len(trials)
            if accuracy >= practice_cfg["passing_accuracy_ratio"] and ax_omissions == 0:
                return True

        return False
