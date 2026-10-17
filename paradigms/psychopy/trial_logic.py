"""
Trial Sequence Engine.
Generates fully counterbalanced blocks adhering to strict behavioral run-rules.
"""

from dataclasses import dataclass
import random
from typing import List, Literal, Optional, Tuple

TrialType = Literal["AX", "AY", "BX", "BY"]
BlockCondition = Literal["SHORT_DELAY", "LONG_DELAY"]


@dataclass(frozen=True)
class TrialDefinition:
    """Immutable specification for a single trial."""
    trial_type: TrialType
    cue_stimulus: str
    probe_stimulus: str
    required_key: str
    cpi_nominal_ms: float
    block_condition: BlockCondition


class TrialSequenceGenerator:
    """
    Constructs pseudorandomized blocks complying with PSD run-rules:
    1. Maximum 4 consecutive target (AX) trials.
    2. Maximum 2 consecutive non-target (AY, BX, BY) trials.
    3. Zero consecutive identical distractor characters.
    """
    def __init__(self, config: dict, seed: Optional[int] = None):
        self.config = config
        self.rng = random.Random(seed)

    def _sample_stimuli(self, trial_type: TrialType) -> Tuple[str, str]:
        cues_inv = self.config["stimuli"]["cue_invalid_set"]
        probes_inv = self.config["stimuli"]["probe_invalid_set"]

        if trial_type == "AX":
            return self.config["stimuli"]["cue_valid"], self.config["stimuli"]["probe_valid"]
        elif trial_type == "AY":
            return self.config["stimuli"]["cue_valid"], self.rng.choice(probes_inv)
        elif trial_type == "BX":
            return self.rng.choice(cues_inv), self.config["stimuli"]["probe_valid"]
        elif trial_type == "BY":
            return self.rng.choice(cues_inv), self.rng.choice(probes_inv)
        raise ValueError(f"Unknown trial type: {trial_type}")

    def _satisfies_run_rules(self, sequence: List[TrialDefinition]) -> bool:
        consecutive_ax = 0
        consecutive_nontarget = 0

        for i in range(len(sequence)):
            curr = sequence[i]

            # Rule 1 & 2: Tracking runs
            if curr.trial_type == "AX":
                consecutive_ax += 1
                consecutive_nontarget = 0
            else:
                consecutive_nontarget += 1
                consecutive_ax = 0

            if consecutive_ax > self.config["design"]["run_rules"]["max_consecutive_targets"]:
                return False
            if consecutive_nontarget > self.config["design"]["run_rules"]["max_consecutive_nontargets"]:
                return False

            # Rule 3: No identical consecutive distractor characters
            if i > 0 and self.config["design"]["run_rules"]["no_consecutive_identical_distractors"]:
                prev = sequence[i - 1]
                if curr.trial_type in ["BX", "BY"] and prev.trial_type in ["BX", "BY"]:
                    if curr.cue_stimulus == prev.cue_stimulus:
                        return False
                if curr.trial_type in ["AY", "BY"] and prev.trial_type in ["AY", "BY"]:
                    if curr.probe_stimulus == prev.probe_stimulus:
                        return False

        return True

    def generate_block(self, condition: BlockCondition) -> List[TrialDefinition]:
        """Generates a validated 100-trial block satisfying run-rules deterministically."""
        dist = self.config["design"]["block_distribution"]
        nominal_cpi = (
            self.config["timing"]["delays"]["short_delay_ms"]
            if condition == "SHORT_DELAY"
            else self.config["timing"]["delays"]["long_delay_ms"]
        )
        target_key = self.config["hardware"]["target_key"]
        nontarget_key = self.config["hardware"]["non_target_key"]

        max_attempts = 5000
        for _ in range(max_attempts):
            # 1. Split 70 AX trials into random chunks of length 1 to 4
            ax_remaining = dist["ax_count"]
            ax_bins = []
            while ax_remaining > 0:
                chunk = min(self.rng.choice([2, 3, 4, 4]), ax_remaining)
                ax_bins.append(chunk)
                ax_remaining -= chunk

            k = len(ax_bins)
            # Non-target trials must be placed in gaps so that AX clusters do not exceed 4
            non_count = dist["ay_count"] + dist["bx_count"] + dist["by_count"]
            non_bins = [0] * (k - 1)
            
            # Fill the gaps (at least 1 non-target trial to separate AX clusters)
            for j in range(k - 1):
                non_bins[j] = 1
            rem_non = non_count - (k - 1)
            
            # Add second non-target trial to gaps respecting the max 2 non-targets constraint
            slots = list(range(k - 1))
            self.rng.shuffle(slots)
            for s in slots:
                if rem_non <= 0:
                    break
                non_bins[s] += 1
                rem_non -= 1

            if rem_non > 0:
                continue

            # Layout based on type string
            types_sequence = []
            for j in range(k):
                types_sequence.extend(["AX"] * ax_bins[j])
                if j < k - 1:
                    types_sequence.extend(["NON"] * non_bins[j])

            # Assign non-target types (AY, BX, BY)
            non_types = (
                ["AY"] * dist["ay_count"] +
                ["BX"] * dist["bx_count"] +
                ["BY"] * dist["by_count"]
            )
            self.rng.shuffle(non_types)

            full_types = []
            for item in types_sequence:
                if item == "AX":
                    full_types.append("AX")
                else:
                    full_types.append(non_types.pop())

            # Final construction of trials considering no-consecutive-distractor rules
            candidate_block: List[TrialDefinition] = []
            valid_assignment = True
            for i, t_type in enumerate(full_types):
                sample_found = False
                for _ in range(25):
                    cue, probe = self._sample_stimuli(t_type)
                    if i > 0 and self.config["design"]["run_rules"]["no_consecutive_identical_distractors"]:
                        prev = candidate_block[i - 1]
                        if t_type in ["BX", "BY"] and prev.trial_type in ["BX", "BY"] and cue == prev.cue_stimulus:
                            continue
                        if t_type in ["AY", "BY"] and prev.trial_type in ["AY", "BY"] and probe == prev.probe_stimulus:
                            continue
                    sample_found = True
                    break

                if not sample_found:
                    valid_assignment = False
                    break

                req_key = target_key if t_type == "AX" else nontarget_key
                candidate_block.append(
                    TrialDefinition(
                        trial_type=t_type,
                        cue_stimulus=cue,
                        probe_stimulus=probe,
                        required_key=req_key,
                        cpi_nominal_ms=nominal_cpi,
                        block_condition=condition
                    )
                )

            if valid_assignment and self._satisfies_run_rules(candidate_block):
                return candidate_block

        raise RuntimeError(f"Failed to generate valid block satisfying run-rules within {max_attempts} iterations.")
