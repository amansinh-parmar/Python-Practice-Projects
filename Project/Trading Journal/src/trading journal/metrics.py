"""Pure performance calculations. No I/O, no formatting.

Conventions (also stated in the report):
* A trade with pnl == 0 is breakeven: neither a win nor a loss.
* Average risk/reward = mean(|pnl| / risk_amount) over trades with risk > 0.
* Average R-multiple = mean(pnl / risk_amount): the signed version, i.e.
  expectancy per trade measured in units of risk.
* Profit factor = gross profit / gross loss; None when there are no losses.
* Drawdown is measured on the cumulative realized-P/L curve, trades ordered
  by date (file order breaks ties), starting from ``initial_balance``
  (default 0). Drawdown % is only reported when a positive starting balance
  is supplied, because a percentage of a zero-based P/L curve is meaningless.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, Sequence

from .importer import Trade


@dataclass(frozen=True)
class SymbolStats:
    trades: int
    net_pnl: float
    win_rate_pct: float


@dataclass(frozen=True)
class Metrics:
    total_trades: int
    winning_trades: int
    losing_trades: int
    breakeven_trades: int
    win_rate_pct: float
    gross_profit: float
    gross_loss: float  # reported as a positive number
    net_pnl: float
    profit_factor: float | None
    average_win: float | None
    average_loss: float | None  # reported as a positive number
    average_risk_reward: float | None
    average_r_multiple: float | None
    largest_win: float | None
    largest_loss: float | None  # reported as a positive number
    max_consecutive_losses: int
    max_drawdown: float
    max_drawdown_pct: float | None
    initial_balance: float
    by_symbol: dict[str, SymbolStats] = field(default_factory=dict)


def _mean(values: Sequence[float]) -> float | None:
    return math.fsum(values) / len(values) if values else None


def max_drawdown(
    pnls: Sequence[float], initial_balance: float = 0.0
) -> tuple[float, float | None]:
    """Largest peak-to-trough decline of the cumulative equity curve.

    Returns (absolute drawdown, drawdown as % of the peak or None when the
    peak was never positive).
    """
    equity = peak = initial_balance
    worst = 0.0
    worst_pct: float | None = None
    for pnl in pnls:
        equity += pnl
        peak = max(peak, equity)
        drawdown = peak - equity
        worst = max(worst, drawdown)
        if peak > 0:
            pct = drawdown / peak * 100
            if worst_pct is None or pct > worst_pct:
                worst_pct = pct
    return worst, worst_pct


def max_consecutive(pnls: Sequence[float], predicate: Callable[[float], bool]) -> int:
    best = run = 0
    for pnl in pnls:
        run = run + 1 if predicate(pnl) else 0
        best = max(best, run)
    return best


def compute_metrics(trades: Sequence[Trade], initial_balance: float = 0.0) -> Metrics:
    if initial_balance < 0 or not math.isfinite(initial_balance):
        raise ValueError("initial_balance must be a non-negative finite number")

    # sorted() is stable, so trades on the same day keep their file order.
    ordered = sorted(trades, key=lambda t: t.date)
    pnls = [t.pnl for t in ordered]

    wins = [p for p in pnls if p > 0]
    losses = [p for p in pnls if p < 0]
    breakeven = len(pnls) - len(wins) - len(losses)

    gross_profit = math.fsum(wins)
    gross_loss = abs(math.fsum(losses))
    total = len(pnls)

    # Only trades with a usuable risk figure contribute to risk-based ratio.
    risked = [t for t in ordered if t.risk_amount > 0 and math.isfinite(t.risk_amount)]
    risk_reward = _mean([abs(t.pnl) / t.risk_amount for t in risked])
    r_multiple = _mean([t.pnl / t.risk_amount for t in risked])

    drawdown, drawdown_pct = max_drawdown(pnls, initial_balance)
    if initial_balance <= 0:
        drawdown_pct = None

    by_symbol: dict[str, SymbolStats] = {}
    for symbol in sorted({t.symbol for t in ordered}):
        sym_pnls = [t.pnl for t in ordered if t.symbol == symbol]
        by_symbol[symbol] = SymbolStats(
            trades=len(sym_pnls),
            net_pnl=math.fsum(sym_pnls),
            win_rate_pct=sum(1 for p in sym_pnls if p > 0) / len(sym_pnls) * 100,
        )

    return Metrics(
        total_trades=total,
        winning_trades=len(wins),
        losing_trades=len(losses),
        breakeven_trades=breakeven,
        win_rate_pct=(len(wins) / total * 100) if total else 0.0,
        gross_profit=gross_profit,
        gross_loss=gross_loss,
        net_pnl=math.fsum(pnls),
        profit_factor=(gross_profit / gross_loss) if gross_loss > 0 else None,
        average_win=_mean(wins),
        average_loss=_mean([abs(p) for p in losses]),
        average_risk_reward=risk_reward,
        average_r_multiple=r_multiple,
        largest_win=max(wins) if wins else None,
        largest_loss=abs(min(losses)) if losses else None,
        max_consecutive_losses=max_consecutive(pnls, lambda p: p < 0),
        max_drawdown=drawdown,
        max_drawdown_pct=drawdown_pct,
        initial_balance=float(initial_balance),
        by_symbol=by_symbol,
    )
