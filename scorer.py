"""Scoring utilities for binary crossing labels and crossing locations."""

from __future__ import annotations

from collections.abc import Iterable
from math import isnan


def _is_missing(value: object) -> bool:
    if value is None:
        return True
    try:
        return isnan(value)  # type: ignore[arg-type]
    except TypeError:
        return False


def _paired_values(expected: Iterable, observed: Iterable) -> list[tuple]:
    pairs = list(zip(expected, observed))
    return [(left, right) for left, right in pairs if not _is_missing(left) and not _is_missing(right)]


def binary_agreement(expected: Iterable[bool], observed: Iterable[bool]) -> float:
    """Return the fraction of paired binary labels that agree."""
    pairs = _paired_values(expected, observed)
    if not pairs:
        return float("nan")
    return sum(bool(left) == bool(right) for left, right in pairs) / len(pairs)


def crossing_step_error(expected_steps: Iterable[int], observed_steps: Iterable[int]) -> float:
    """Return mean absolute error for paired, present crossing steps."""
    pairs = _paired_values(expected_steps, observed_steps)
    if not pairs:
        return float("nan")
    return sum(abs(float(left) - float(right)) for left, right in pairs) / len(pairs)


def within_one_step(expected_steps: Iterable[int], observed_steps: Iterable[int]) -> float:
    """Return the fraction of paired crossing steps whose error is at most one."""
    pairs = _paired_values(expected_steps, observed_steps)
    if not pairs:
        return float("nan")
    return sum(abs(float(left) - float(right)) <= 1 for left, right in pairs) / len(pairs)


def cohen_kappa_binary(expected: Iterable[bool], observed: Iterable[bool]) -> float:
    """Return Cohen's kappa for paired binary labels."""
    pairs = _paired_values(expected, observed)
    if not pairs:
        return float("nan")

    expected_bool = [bool(left) for left, _ in pairs]
    observed_bool = [bool(right) for _, right in pairs]
    observed_agreement = binary_agreement(expected_bool, observed_bool)
    expected_positive = sum(expected_bool) / len(pairs)
    observed_positive = sum(observed_bool) / len(pairs)
    chance_agreement = (
        expected_positive * observed_positive
        + (1 - expected_positive) * (1 - observed_positive)
    )
    if chance_agreement == 1:
        return 1.0 if observed_agreement == 1 else float("nan")
    return (observed_agreement - chance_agreement) / (1 - chance_agreement)
