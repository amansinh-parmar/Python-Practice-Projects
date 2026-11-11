"""Read and validate trade records from a CSV file."""

from __future__ import annotations

import csv
import math
import re
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

VALID_DIRECTION = ("LONG", "SHORT")

# Accept integers, decimals, scientific notation, and correctly grouped
# thousands separators, without accepting malformed comma grouping.
_NUMBER_PATTERN = re.compile(
    r"[+-]?" r"(?:" r"\d{1,3}(?:,\d{3})+|\d+" r")(?:\.\d*)?" r"(?:[eE][+-]?\d+)?"
)


@dataclass(frozen=True)
class Trade:
    """One completed trade."""

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
    """Raised when a CSV file contains invalid trade data."""

    def __init__(self, errors: Iterable[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def _parse_float(raw: str, field: str) -> float:
    """Convert a CSV value to a finite float."""
    if not isinstance(raw, str):
        raise ValueError(f"{field} must be a number, got {raw!r}")

    value_text = raw.strip()

    if not value_text or not _NUMBER_PATTERN.fullmatch(value_text):
        raise ValueError(f"{field} must be a number, got {raw!r}")

    try:
        value = float(value_text.replace(",", ""))
    except (ValueError, OverflowError):
        raise ValueError(f"{field} must be a number, got {raw!r}") from None

    if not math.isfinite(value):
        raise ValueError(f"{field} must be a finite number, got {raw!r}")

    return value


def _parse_row(row: dict[str, str | None]) -> Trade:
    """Validate and convert one CSV row."""
    values = {key: (row.get(key) or "").strip() for key in REQUIRED_COLUMNS}

    # Required text fields.
    for field in ("trade_id", "symbol"):
        if not values[field]:
            raise ValueError(f"{field} is required")

    # Date validation: require the exact YYYY-MM-DD format.
    raw_date = values["date"]

    try:
        trade_date = date.fromisoformat(raw_date)
    except ValueError:
        raise ValueError(f"date must be YYYY-MM-DD, got {raw_date!r}") from None

    if trade_date.isoformat() != raw_date:
        raise ValueError(f"date must be YYYY-MM-DD, got {raw_date!r}")

    # Direction validation.
    direction = values["direction"].upper()

    if direction not in VALID_DIRECTION:
        raise ValueError(
            "direction must be LONG or SHORT, " f"got {values['direction']!r}"
        )

    # Numeric fields.
    entry = _parse_float(values["entry_price"], "entry_price")
    exit_price = _parse_float(values["exit_price"], "exit_price")
    quantity = _parse_float(values["quantity"], "quantity")
    risk = _parse_float(values["risk_amount"], "risk_amount")
    pnl = _parse_float(values["pnl"], "pnl")

    # Positive-value validation.
    if entry <= 0:
        raise ValueError("entry_price must be positive")

    if exit_price <= 0:
        raise ValueError("exit_price must be positive")

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
        exit_price=exit_price,
        quantity=quantity,
        risk_amount=risk,
        pnl=pnl,
    )


def parse_trades(lines: Iterable[str]) -> list[Trade]:
    """Parse CSV lines, collecting validation errors across all rows."""
    reader = csv.DictReader(lines, skipinitialspace=True)

    # An entirely empty file has no header.
    if reader.fieldnames is None:
        raise ImportValidationError(["file is empty"])

    # Normalize headers, including a possible UTF-8 BOM.
    normalized_headers = [
        (name or "").lstrip("\ufeff").strip().lower() for name in reader.fieldnames
    ]

    # Reject blank and duplicate column names.
    if any(not name for name in normalized_headers):
        raise ImportValidationError(["header contains an empty column name"])

    if len(normalized_headers) != len(set(normalized_headers)):
        raise ImportValidationError(["duplicate column names in header"])

    reader.fieldnames = normalized_headers

    # Check for missing required columns.
    missing = [
        column for column in REQUIRED_COLUMNS if column not in normalized_headers
    ]

    if missing:
        raise ImportValidationError(
            [f"missing required column(s): {', '.join(missing)}"]
        )

    trades: list[Trade] = []
    errors: list[str] = []
    seen_ids: dict[str, int] = {}

    try:
        for row in reader:
            line_number = reader.line_num

            # Ignore completely blank lines.
            if not any(
                isinstance(value, str) and value.strip() for value in row.values()
            ):
                continue

            # DictReader uses None for extra unnamed fields and for
            # missing values in rows with too few columns.
            if None in row or any(value is None for value in row.values()):
                errors.append(f"line {line_number}: incorrect number of columns")
                continue

            try:
                trade = _parse_row(row)
            except ValueError as exc:
                errors.append(f"line {line_number}: {exc}")
                continue

            # Trade IDs are case-sensitive, preserving the original
            # behavior: T001 and t001 are different IDs.
            if trade.trade_id in seen_ids:
                errors.append(
                    f"line {line_number}: duplicate trade_id "
                    f"{trade.trade_id!r} "
                    f"(first seen on line {seen_ids[trade.trade_id]})"
                )
                continue

            seen_ids[trade.trade_id] = line_number
            trades.append(trade)

    except csv.Error as exc:
        errors.append(f"line {reader.line_num}: invalid CSV data: {exc}")

    # Report all row errors together.
    if errors:
        raise ImportValidationError(errors)

    if not trades:
        raise ImportValidationError(["file contains no trades"])

    return trades


def load_trades(path: str | Path) -> list[Trade]:
    """Load and validate trades from a CSV file."""
    with open(
        path,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as handle:
        return parse_trades(handle)
