"""Shared test helpers for Trading Journal."""

from collections.abc import Iterable

from trading_journal.importer import Trade, parse_trades

HEADER = (
    "trade_id,date,symbol,direction,entry_price,exit_price,"
    "quantity,risk_amount,pnl\n"
)

SAMPLE_ROWS = (
    "T001,2026-01-05,AAPL,LONG,100,110,10,50,100\n"
    "T002,2026-01-06,MSFT,LONG,200,190,5,40,-50\n"
    "T003,2026-01-07,TSLA,SHORT,300,280,2,30,40\n"
    "T004,2026-01-08,NVDA,LONG,150,160,4,20,40\n"
    "T005,2026-01-09,AMZN,SHORT,180,185,3,25,-15\n"
)

_HEADER_COLUMNS = tuple(column.strip().lower() for column in HEADER.strip().split(","))


def trades_from(
    rows: str | Iterable[str] = SAMPLE_ROWS,
) -> list[Trade]:
    """Convert CSV text or an iterable of CSV lines into trades.

    If the supplied text does not contain a header, the standard test
    header is prepended. Existing headers are recognized by their
    normalized column names.
    """
    if isinstance(rows, str):
        text = rows
    else:
        try:
            parts = list(rows)
        except TypeError:
            raise TypeError("rows must be CSV text or an iterable of strings") from None

        if not all(isinstance(part, str) for part in parts):
            raise TypeError("every item in rows must be a string")

        text = "".join(parts)

    # Remove a possible UTF-8 BOM for header detection.
    normalized_text = text.lstrip("\ufeff")
    first_line = normalized_text.splitlines()[0] if normalized_text.splitlines() else ""

    normalized_header = tuple(
        column.strip().lower().lstrip("\ufeff") for column in first_line.split(",")
    )

    # Prepend a header only when the input does not already have one.
    if normalized_header != _HEADER_COLUMNS:
        text = HEADER + text

    return parse_trades(text.splitlines(keepends=True))
