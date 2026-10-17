"""
Application Entrypoint.
Coordinates CLI arguments, engine initialization, practice gating,
and experimental block execution.
"""

import argparse
import sys
import yaml

try:
    from config_loader import load_experiment_config
    from engine import PsychopyEngine
    from trial_logic import TrialSequenceGenerator
    from trial_executor import TrialExecutor
    from ui import UIManager, PracticeManager
    from logger import SessionDataLogger
except ImportError:
    from .config_loader import load_experiment_config
    from .engine import PsychopyEngine
    from .trial_logic import TrialSequenceGenerator
    from .trial_executor import TrialExecutor
    from .ui import UIManager, PracticeManager
    from .logger import SessionDataLogger


def parse_arguments():
    parser = argparse.ArgumentParser(description="AX-CPT Psychophysical Engine")
    parser.add_argument("--participant", required=True, type=str, help="Participant Identifier (e.g., P001)")
    parser.add_argument("--group", required=True, choices=["A", "B"], help="Counterbalancing Group (A or B)")
    parser.add_argument("--config", default="config/config.yaml", type=str, help="Path to config.yaml")
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = load_experiment_config(args.config)

    logger = SessionDataLogger(args.participant, args.group, config)
    engine = PsychopyEngine(config)

    try:
        engine.initialize_hardware()
        executor = TrialExecutor(engine, config)
        ui = UIManager(engine, config)
        practice = PracticeManager(engine, executor, config)
        sequence_gen = TrialSequenceGenerator(config)

        # Instructions
        ui.display_message_and_wait(
            "WELCOME TO THE COGNITIVE ASSESSMENT\n\n"
            "Respond to pairs of letters:\n"
            "- Press SPACE ONLY when you see an 'A' followed immediately by an 'X'.\n"
            "- For any other letter combination, press 'L'.\n\n"
            "Press SPACE to begin practice."
        )

        passed = practice.run_practice()
        if not passed:
            ui.display_message_and_wait(
                "Practice criterion not reached. Please notify the experimenter."
            )
            sys.exit(1)

        ui.display_message_and_wait(
            "Practice Complete!\n\n"
            "The main experiment will now begin.\n"
            "No feedback will be provided during the task.\n\n"
            "Press SPACE to begin Block 1."
        )

        # Execute Experimental Blocks
        group_key = f"group_{args.group.lower()}"
        block_conditions = config["design"]["counterbalancing_groups"][group_key]
        global_trial_idx = 1
        is_post_error = False

        for b_idx, condition in enumerate(block_conditions, start=1):
            block_trials = sequence_gen.generate_block(condition)

            for b_trial_idx, trial_def in enumerate(block_trials, start=1):
                result = executor.execute_trial(
                    trial_def, global_trial_idx, b_trial_idx, is_post_error
                )
                logger.log_trial(result)
                is_post_error = not result.is_correct
                global_trial_idx += 1

            if b_idx < len(block_conditions):
                ui.run_rest_break(b_idx, len(block_conditions))

        logger.save_session(engine.frame_drop_records)
        ui.display_message_and_wait("Session Complete! Thank you for your participation.")

    except KeyboardInterrupt:
        print("\nSession aborted manually.")
    finally:
        engine.close()


if __name__ == "__main__":
    main()
