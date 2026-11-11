"""Format metrics for the terminal and write the JSON summary."""

from __future__ import annotations

import json
import math
import os
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .metrics import Metrics

TITLE = "TRADING JOURNAL — PERFORMANCE REPORT"
RULE = "=" * len(TITLE)
JSON_DECIMALS = 4


def _num(value: float | None, suffix: str = "") -> str:
    """Format a number for display, using n/a for undefined values."""
    if value is None:
        return "n/a"

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return "n/a"

    if not math.isfinite(value):
        return "n/a"

    return f"{value:,.2f}{suffix}"


def format_report(m: Metrics) -> str:
    """Return a human-readable performance report."""
    rows = [
        ("Trades analyzed:", str(m.total_trades)),
        ("Winning trades:", str(m.winning_trades)),
        ("Losing trades:", str(m.losing_trades)),
        ("Breakeven trades:", str(m.breakeven_trades)),
        ("Win rate:", _num(m.win_rate_pct, "%")),
        ("Gross profit:", _num(m.gross_profit)),
        ("Gross loss:", _num(-m.gross_loss)),
        ("Net profit/loss:", _num(m.net_pnl)),
        ("Profit factor:", _num(m.profit_factor)),
        ("Average win:", _num(m.average_win)),
        ("Average loss:", _num(m.average_loss)),
        ("Largest win:", _num(m.largest_win)),
        ("Largest loss:", _num(m.largest_loss)),
        ("Average risk/reward:", _num(m.average_risk_reward)),
        ("Average R-multiple:", _num(m.average_r_multiple)),
        ("Max consecutive losses:", str(m.max_consecutive_losses)),
        ("Maximum drawdown:", _num(m.max_drawdown)),
    ]

    if m.max_drawdown_pct is not None:
        rows.append(("Maximum drawdown %:", _num(m.max_drawdown_pct, "%")))

    lines = [TITLE, RULE]
    lines.extend(f"{label:<25}{value:>12}" for label, value in rows)

    if len(m.by_symbol) > 1:
        lines.extend(
            [
                RULE,
                "By symbol:",
                f"  {'Symbol':<10}{'Trades':>7}" f"{'Net P/L':>12}{'Win rate':>10}",
            ]
        )

        for symbol, stats in m.by_symbol.items():
            lines.append(
                f"  {symbol:<10}"
                f"{stats.trades:>7}"
                f"{_num(stats.net_pnl):>12}"
                f"{_num(stats.win_rate_pct, '%'):>10}"
            )

    if m.initial_balance > 0:
        basis = f"starting balance {m.initial_balance:,.2f}"
    else:
        basis = "cumulative P/L starting at 0"

    lines.extend(
        [
            RULE,
            "Notes:",
            "  - Breakeven (P/L = 0) trades count as neither wins nor losses.",
            "  - Risk/reward = mean(|P/L| / risk); trades with no valid risk are excluded.",
            "  - R-multiple = mean(P/L / risk), i.e. expectancy per trade in units of risk.",
            "  - Profit factor is n/a when there are no losing trades.",
            f"  - Drawdown uses {basis}, trades ordered by date.",
            RULE,
            "Report generated successfully.",
        ]
    )

    return "\n".join(lines)


def _round(obj: Any) -> Any:
    """Round floats recursively and replace non-finite values with None."""
    if isinstance(obj, float):
        if not math.isfinite(obj):
            return None
        return round(obj, JSON_DECIMALS)

    if isinstance(obj, dict):
        return {key: _round(value) for key, value in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [_round(value) for value in obj]

    return obj


def to_summary_dict(m: Metrics) -> dict[str, Any]:
    """Return a JSON-ready dictionary with rounded numeric values."""
    return _round(asdict(m))


def write_json(m: Metrics, path: str | Path) -> Path:
    """Write the JSON summary, creating parent directories as needed.

    The output is written to a temporary file before replacing the target,
    preventing serialization or interrupted-write failures from truncating
    an existing report.
    """
    target = Path(path)

    # Serialize before touching the destination file.
    payload = (
        json.dumps(
            to_summary_dict(m),
            indent=2,
            allow_nan=False,
        )
        + "\n"
    )

    target.parent.mkdir(parents=True, exist_ok=True)

    temp_path: Path | None = None

    try:
        # Use the same directory so replacement occurs on the same filesystem.
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_path = Path(handle.name)
            handle.write(payload)

        os.replace(temp_path, target)
        temp_path = None

    finally:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass

    return target
