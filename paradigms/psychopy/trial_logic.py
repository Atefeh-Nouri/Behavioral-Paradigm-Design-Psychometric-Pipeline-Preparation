
"""Python AX-CPT trial sequence generation logic.

This module intentionally avoids importing PsychoPy, visual, core, keyboard,
or any hardware/GUI dependency. It can therefore be imported by unit tests and
GitHub Actions CI without installing PsychoPy/PsychToolbox.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, Sequence, Tuple

BlockCondition = Literal["SHORT_DELAY", "LONG_DELAY"]
TrialType = Literal["AX", "AY", "BX", "BY"]


@dataclass(frozen=True)
class TrialDefinition:
    """Immutable definition of one AX-CPT trial."""

    trial_type: TrialType
    cue_stimulus: str
    probe_stimulus: str
    required_key: str
    cpi_nominal_ms: float
    block_condition: BlockCondition


class TrialSequenceGenerator:
    """
    Generates AX-CPT trial blocks without any PsychoPy dependency.

    The generator satisfies:
      - exact block distribution counts
      - max consecutive AX/target runs
      - max consecutive non-target runs
      - no consecutive identical distractors under canonical A/B/X/Y stimuli
      - deterministic output for a fixed seed
    """

    def __init__(self, config: Dict[str, Any], seed: Optional[int] = None) -> None:
        self.config = config

        if seed is None:
            seed = int(config.get("design", {}).get("random_seed", 2026))

        self.rng = random.Random(seed)

    def _block_distribution(self) -> Dict[str, int]:
        dist = self.config.get("design", {}).get("block_distribution", {})
        return {
            "ax_count": int(dist.get("ax_count", 70)),
            "ay_count": int(dist.get("ay_count", 10)),
            "bx_count": int(dist.get("bx_count", 10)),
            "by_count": int(dist.get("by_count", 10)),
        }

    def _run_rules(self) -> Dict[str, Any]:
        rules = self.config.get("design", {}).get("run_rules", {})
        return {
            "max_consecutive_targets": int(
                rules.get("max_consecutive_targets", 4)
            ),
            "max_consecutive_nontargets": int(
                rules.get("max_consecutive_nontargets", 2)
            ),
            "no_consecutive_identical_distractors": bool(
                rules.get("no_consecutive_identical_distractors", True)
            ),
        }

    def _nominal_cpi_ms(self, condition: BlockCondition) -> float:
        delays = self.config.get("timing", {}).get("delays", {})

        if condition == "SHORT_DELAY":
            return float(delays.get("short_delay_ms", 1500))

        return float(delays.get("long_delay_ms", 5000))

    def _response_keys(self) -> Tuple[str, str]:
        hardware = self.config.get("hardware", {})
        return (
            str(hardware.get("target_key", "f")),
            str(hardware.get("non_target_key", "j")),
        )

    def _stimulus_map(self) -> Dict[TrialType, Tuple[str, str]]:
        stimuli = self.config.get("stimuli", {})

        def _pick(key: str, default: str) -> str:
            value = stimuli.get(key, default)

            if isinstance(value, (list, tuple)):
                return str(value[0]) if value else default

            return str(value)

        target_cue = _pick("target_cue", "A")
        target_probe = _pick("target_probe", "X")
        distractor_cue = _pick("distractor_cue", "B")
        distractor_probe = _pick("distractor_probe", "Y")

        return {
            "AX": (target_cue, target_probe),
            "AY": (target_cue, distractor_probe),
            "BX": (distractor_cue, target_probe),
            "BY": (distractor_cue, distractor_probe),
        }

    def _sample_stimuli(self, trial_type: TrialType) -> Tuple[str, str]:
        try:
            return self._stimulus_map()[trial_type]
        except KeyError as exc:
            raise ValueError(f"Unknown trial type: {trial_type}") from exc

    def _distribute_total(
        self,
        total: int,
        parts: int,
        min_each: int,
        max_each: int,
    ) -> Optional[List[int]]:
        """
        Distribute `total` into `parts` integer bins, each between
        `min_each` and `max_each`, using the instance RNG.
        """

        if parts == 0:
            return [] if total == 0 else None

        if min_each < 0 or max_each < min_each:
            return None

        if total < parts * min_each or total > parts * max_each:
            return None

        values = [min_each] * parts
        remaining = total - parts * min_each
        slot_capacity = max_each - min_each

        if remaining == 0:
            return values

        if slot_capacity == 0:
            return None

        order = list(range(parts))
        self.rng.shuffle(order)

        for idx in order:
            if remaining <= 0:
                break

            add = min(slot_capacity, remaining)
            values[idx] += add
            remaining -= add

        if remaining != 0:
            return None

        return values

    def _assign_non_target_types(
        self,
        non_bins: List[int],
        ay_count: int,
        bx_count: int,
        by_count: int,
        rules: Dict[str, Any],
    ) -> Optional[List[List[TrialType]]]:
        """
        Assign AY/BX/BY trial types into non-target gaps.

        For the canonical AX-CPT stimulus mapping:
          - AX = A/X target
          - AY = A/Y non-target
          - BX = B/X non-target
          - BY = B/Y non-target

        Under `no_consecutive_identical_distractors`:
          - adjacent BX/BY are invalid because both use distractor cue B
          - adjacent AY/BY are invalid because both use distractor probe Y
          - BY cannot be adjacent to any other non-target type

        Therefore, for max non-target run length = 2:
          - BY must occupy singleton non-target gaps
          - double non-target gaps must be AY-BX or BX-AY
        """

        gaps = len(non_bins)
        non_count = ay_count + bx_count + by_count

        if gaps == 0:
            return [] if non_count == 0 else None

        if sum(non_bins) != non_count:
            return None

        max_non = int(rules["max_consecutive_nontargets"])
        no_distractor_repeat = bool(
            rules["no_consecutive_identical_distractors"]
        )

        # Generic fallback for non-canonical configurations.
        # The outer validator will reject invalid blocks and the generator
        # will retry.
        if (not no_distractor_repeat) or max_non != 2:
            pool: List[TrialType] = (
                ["AY"] * ay_count
                + ["BX"] * bx_count
                + ["BY"] * by_count
            )
            self.rng.shuffle(pool)

            assignments: List[List[TrialType]] = []
            cursor = 0

            for length in non_bins:
                assignments.append(pool[cursor:cursor + length])
                cursor += length

            return assignments

        singles = [
            idx for idx, length in enumerate(non_bins) if length == 1
        ]
        doubles = [
            idx for idx, length in enumerate(non_bins) if length == 2
        ]

        if len(singles) + len(doubles) != gaps:
            return None

        if len(singles) < by_count:
            return None

        if len(doubles) > min(ay_count, bx_count):
            return None

        assignments = [[] for _ in range(gaps)]

        by_slots = self.rng.sample(singles, by_count) if by_count > 0 else []
        by_slot_set = set(by_slots)

        for idx in by_slots:
            assignments[idx] = ["BY"]

        ay_remaining = ay_count
        bx_remaining = bx_count

        for idx in doubles:
            if self.rng.random() < 0.5:
                assignments[idx] = ["AY", "BX"]
            else:
                assignments[idx] = ["BX", "AY"]

            ay_remaining -= 1
            bx_remaining -= 1

        if ay_remaining < 0 or bx_remaining < 0:
            return None

        remaining_singles = [
            idx for idx in singles if idx not in by_slot_set
        ]

        if ay_remaining + bx_remaining != len(remaining_singles):
            return None

        ay_slots = (
            self.rng.sample(remaining_singles, ay_remaining)
            if ay_remaining > 0
            else []
        )
        ay_slot_set = set(ay_slots)

        for idx in remaining_singles:
            assignments[idx] = ["AY"] if idx in ay_slot_set else ["BX"]

        for assignment in assignments:
            if not assignment:
                return None

            if len(assignment) not in (1, 2):
                return None

        return assignments

    def _rejection_type_sequence(self) -> Optional[List[TrialType]]:
        """
        Fallback bounded rejection sampler over trial-type labels only.

        This does not build TrialDefinition objects yet, so it is cheap.
        """

        dist = self._block_distribution()

        pool: List[TrialType] = (
            ["AX"] * dist["ax_count"]
            + ["AY"] * dist["ay_count"]
            + ["BX"] * dist["bx_count"]
            + ["BY"] * dist["by_count"]
        )

        for _ in range(1000):
            self.rng.shuffle(pool)

            if self._satisfies_type_run_rules(pool):
                return pool[:]

        return None

    def _satisfies_type_run_rules(
        self,
        types: Sequence[TrialType],
    ) -> bool:
        """
        Validate a trial-type sequence before stimulus materialization.

        For canonical A/B/X/Y stimuli:
          - BX/BY adjacent repeats distractor cue B
          - AY/BY adjacent repeats distractor probe Y
        """

        rules = self._run_rules()
        max_target = int(rules["max_consecutive_targets"])
        max_non = int(rules["max_consecutive_nontargets"])
        no_distractor_repeat = bool(
            rules["no_consecutive_identical_distractors"]
        )

        run_target = 0
        run_non = 0

        for idx, trial_type in enumerate(types):
            if trial_type == "AX":
                run_target += 1
                run_non = 0

                if run_target > max_target:
                    return False
            else:
                run_non += 1
                run_target = 0

                if run_non > max_non:
                    return False

            if no_distractor_repeat and idx > 0:
                prev_type = types[idx - 1]

                if (
                    trial_type in ("BX", "BY")
                    and prev_type in ("BX", "BY")
                ):
                    return False

                if (
                    trial_type in ("AY", "BY")
                    and prev_type in ("AY", "BY")
                ):
                    return False

        return True

    def _construct_type_sequence(self) -> Optional[List[TrialType]]:
        """
        Deterministically construct a valid trial-type skeleton.

        Strategy:
          1. Split AX trials into bins of length <= max_consecutive_targets.
          2. Place non-target trials into gaps between AX bins.
          3. Respect max_consecutive_nontargets.
          4. Assign AY/BX/BY into non-target gaps while respecting
             no-consecutive-identical-distractor constraints.
        """

        dist = self._block_distribution()
        ax_count = dist["ax_count"]
        ay_count = dist["ay_count"]
        bx_count = dist["bx_count"]
        by_count = dist["by_count"]
        non_count = ay_count + bx_count + by_count

        rules = self._run_rules()
        max_target = int(rules["max_consecutive_targets"])
        max_non = int(rules["max_consecutive_nontargets"])

        if ax_count == 0 and non_count == 0:
            return []

        if non_count == 0:
            if ax_count <= max_target:
                return ["AX"] * ax_count

            return self._rejection_type_sequence()

        if ax_count == 0:
            if non_count <= max_non:
                assignments = self._assign_non_target_types(
                    [non_count],
                    ay_count,
                    bx_count,
                    by_count,
                    rules,
                )

                if assignments is not None and len(assignments) == 1:
                    return assignments[0]

            return self._rejection_type_sequence()

        if max_target <= 0 or max_non <= 0:
            return self._rejection_type_sequence()

        # Number of AX bins must be large enough to:
        #   - keep AX runs <= max_target
        #   - provide enough non-target gaps to keep non runs <= max_non
        min_bins = max(1, math.ceil(ax_count / max_target))
        min_bins = max(min_bins, math.ceil(non_count / max_non) + 1)

        # Each gap needs at least one non-target trial, so gaps <= non_count.
        # Therefore bins <= non_count + 1.
        max_bins = min(ax_count, non_count + 1)

        lower_bins = min_bins
        upper_bins = max_bins

        # Extra feasibility constraints for canonical distractor-repeat rule
        # when max non-target run length is exactly 2.
        if (
            bool(rules["no_consecutive_identical_distractors"])
            and max_non == 2
            and by_count > 0
        ):
            # BY cannot be adjacent to another non-target.
            # Therefore BY needs singleton non-target gaps.
            #
            # If g = number of non-target gaps:
            #   double gaps = non_count - g
            #   singleton gaps = 2g - non_count
            #
            # Need singleton gaps >= by_count:
            #   2g - non_count >= by_count
            #   g >= ceil((non_count + by_count) / 2)
            min_gaps_for_by = math.ceil((non_count + by_count) / 2)

            # Double gaps must be AY-BX or BX-AY.
            # Therefore number of double gaps cannot exceed min(AY, BX).
            #
            # double gaps = non_count - g <= min(AY, BX)
            # g >= non_count - min(AY, BX)
            min_gaps_for_double_pairs = non_count - min(ay_count, bx_count)

            min_gaps = max(min_gaps_for_by, min_gaps_for_double_pairs)
            lower_bins = max(lower_bins, min_gaps + 1)

        if lower_bins > upper_bins:
            return self._rejection_type_sequence()

        bins = self.rng.randint(lower_bins, upper_bins)
        gaps = bins - 1

        ax_bins = self._distribute_total(
            total=ax_count,
            parts=bins,
            min_each=1,
            max_each=max_target,
        )

        if ax_bins is None:
            return self._rejection_type_sequence()

        non_bins = self._distribute_total(
            total=non_count,
            parts=gaps,
            min_each=1,
            max_each=max_non,
        )

        if non_bins is None:
            return self._rejection_type_sequence()

        assignments = self._assign_non_target_types(
            non_bins=non_bins,
            ay_count=ay_count,
            bx_count=bx_count,
            by_count=by_count,
            rules=rules,
        )

        if assignments is None:
            return self._rejection_type_sequence()

        types: List[TrialType] = []

        for bin_idx, ax_len in enumerate(ax_bins):
            types.extend(["AX"] * ax_len)

            if bin_idx < gaps:
                types.extend(assignments[bin_idx])

        if len(types) != ax_count + non_count:
            return self._rejection_type_sequence()

        return types

    def _satisfies_run_rules(self, block: List[TrialDefinition]) -> bool:
        """
        Final validation on materialized TrialDefinition objects.

        This checks actual cue/probe strings, not only trial-type labels.
        """

        rules = self._run_rules()
        max_target = int(rules["max_consecutive_targets"])
        max_non = int(rules["max_consecutive_nontargets"])
        no_distractor_repeat = bool(
            rules["no_consecutive_identical_distractors"]
        )

        run_target = 0
        run_non = 0

        for idx, trial in enumerate(block):
            if trial.trial_type == "AX":
                run_target += 1
                run_non = 0

                if run_target > max_target:
                    return False
            else:
                run_non += 1
                run_target = 0

                if run_non > max_non:
                    return False

            if no_distractor_repeat and idx > 0:
                prev = block[idx - 1]

                if (
                    trial.trial_type in ("BX", "BY")
                    and prev.trial_type in ("BX", "BY")
                    and trial.cue_stimulus == prev.cue_stimulus
                ):
                    return False

                if (
                    trial.trial_type in ("AY", "BY")
                    and prev.trial_type in ("AY", "BY")
                    and trial.probe_stimulus == prev.probe_stimulus
                ):
                    return False

        return True

    def generate_block(
        self,
        condition: BlockCondition,
    ) -> List[TrialDefinition]:
        """
        Generate one validated 100-trial AX-CPT block.

        This method is pure Python and CI-safe.
        """

        target_key, non_target_key = self._response_keys()
        cpi_nominal_ms = self._nominal_cpi_ms(condition)

        max_attempts = int(
            self.config.get("design", {}).get(
                "max_generation_attempts",
                5000,
            )
        )

        for _ in range(max_attempts):
            types = self._construct_type_sequence()

            if types is None:
                continue

            if not self._satisfies_type_run_rules(types):
                continue

            candidate_block: List[TrialDefinition] = []

            for trial_type in types:
                cue, probe = self._sample_stimuli(trial_type)

                required_key = (
                    target_key if trial_type == "AX" else non_target_key
                )

                candidate_block.append(
                    TrialDefinition(
                        trial_type=trial_type,
                        cue_stimulus=cue,
                        probe_stimulus=probe,
                        required_key=required_key,
                        cpi_nominal_ms=cpi_nominal_ms,
                        block_condition=condition,
                    )
                )

            if self._satisfies_run_rules(candidate_block):
                return candidate_block

        raise RuntimeError(
            "Failed to generate valid block satisfying run-rules within "
            f"{max_attempts} iterations."
        )


__all__ = [
    "BlockCondition",
    "TrialType",
    "TrialDefinition",
    "TrialSequenceGenerator",
]