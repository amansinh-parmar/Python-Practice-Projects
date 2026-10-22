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
    symbol: str
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


def _parse_row(row: dict[str, str]) -> Trade:
    """Convert one CSV row to a Trade, raising ValueError on the first problem."""
    values = {col: (row.get(col) or "").strip() for col in REQUIRED_COLUMNS}

    for col in ("trade_id", "symbol"):
        if not values[col]:
            raise ValueError(f"{col} is required")

    try:
        trade_date = date.fromisoformat(values["date"])
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got {values['date']!r}") from None

    direction = values["direction"].upper()
    if direction not in VALID_DIRECTIONS:
        raise ValueError(
            f"direction must be LONG or SHORT, got {values['direction']!r}"
        )

    entry = _parse_float(values["entry_price"], "entry_price")
    exit_ = _parse_float(values["exit_price"], "exit_price")
    quantity = _parse_float(values["quantity"], "quantity")
    risk = _parse_float(values["risk_amount"], "risk_amount")
    pnl = _parse_float(values["pnl"], "pnl")

    if entry <= 0 or exit_ <= 0:
        raise ValueError("entry_price and exit_price must be positive")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    if risk <= 0:
        raise ValueError("risk_amount must be positive")

    return Trade(
        trade_id=values["trade_id"],
        date=trade_date,
        symbol=values["symbol"].upper(),
        direction=direction,
        entry_price=entry,
        exit_price=exit_,
        quantity=quantity,
        risk_amount=risk,
        pnl=pnl,
    )


def parse_trades(lines: Iterable[str]) -> list[Trade]:
    """Parse trades from an iterable of CSV lines."""
    reader = csv.DictReader(lines)

    if reader.fieldnames is None:
        raise ImportValidationError(["file is empty"])

    # Normalise headers (trim whitespace, lowercase) so exports from
    # spreadsheets with sloppy headers still work.
    reader.fieldnames = [(name or "").strip().lower() for name in reader.fieldnames]
    missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
    if missing:
        raise ImportValidationError(
            [f"missing required column(s): {', '.join(missing)}"]
        )

    trades: list[Trade] = []
    errors: list[str] = []
    seen_ids: dict[str, int] = {}

    for row in reader:
        line = reader.line_num
        if not any((v or "").strip() for v in row.values() if isinstance(v, str)):
            continue  # skip blank lines
        try:
            trade = _parse_row(row)
        except ValueError as exc:
            errors.append(f"line {line}: {exc}")
            continue

        if trade.trade_id in seen_ids:
            errors.append(
                f"line {line}: duplicate trade_id {trade.trade_id!r} "
                f"(first seen on line {seen_ids[trade.trade_id]})"
            )
            continue
        seen_ids[trade.trade_id] = line
        trades.append(trade)

    if errors:
        raise ImportValidationError(errors)
    if not trades:
        raise ImportValidationError(["file contains no trades"])
    return trades


def load_trades(path: str | Path) -> list[Trade]:
    """Load and validate trades from a CSV file.

    Raises FileNotFoundError if the file is missing and
    ImportValidationError if its contents are invalid.
    """
    # utf-8-sig transparently strips the BOM that Excel adds to CSV exports.
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return parse_trades(handle)
