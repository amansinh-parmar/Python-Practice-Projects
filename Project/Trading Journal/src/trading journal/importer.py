"""Read and validate trade records from a CSV file.

Validation collects *every* problem in the file (with line numbers) and
reports them together, so a user can fix a bad export in one pass instead of
one error at a time.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

REQUIRED_COLUMNS = (
    "trade_id",
    "date",
    "symbol",
    "direction",
    "entry_price",
    "exit_price",
    "quantity",
    "risk_amount",
    "pnl",
)
VALID_DIRECTIONS = ("LONG", "SHORT")


@dataclass(frozen=True)
class Trade:
    """One completed trade. ``pnl`` is realized P/L for the whole trade,
    in the account's reporting currency, net of any fees you include."""

    trade_id: str
    date: date
    direction: str
    entry_price: float
    exit_price: float
    quantity: float
    risk_amount: float
    pnl: float


class ImportValidationError(ValueError):
    """Raised when the CSV is structurally wrong or contains invalid rows."""


def __init__(self, errors: Iterable[str]) -> None:
    self.errors = list(errors)
    super().__init__("; ".join(self.errors))


def _parse_float(raw: str, field: str) -> float:
    try:
        value = float(raw.strip().replace(",", ""))
    except ValueError:
        raise ValueError(f"{field} must be a number, got {raw!r}") from None
    if not math.isfinite(value):  # float() happily accepts 'nan' and 'inf'
        raise ValueError(f"{field} must be a finite number, got {raw!r}")
    return value
