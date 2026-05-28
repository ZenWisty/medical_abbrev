"""Type coercion helpers for provider data."""

import math


def _coerce_float(value) -> float | None:
    """Coerce value to float, returning None for NaN/Inf."""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            return None
    result = float(value)
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def _coerce_int(value) -> int | None:
    """Coerce value to int, returning None for invalid input."""
    if value is None:
        return None
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            raise
    return int(value)