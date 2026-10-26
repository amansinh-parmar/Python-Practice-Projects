from datetime import date

import pytest

from trading_journal.importer import Trade
from trading_journal.metrics import compute_metrics, max_drawdown


def make_trade(i, pnl, risk=10.0, day=None, symbol="AAPL"):
    return Trade(
        trade_id=f"T{i}",
        date=day or date(2026, 1, i),
        symbol=symbol,
        direction="LONG",
        entry_price=100.0,
        exit_price=101.0,
        quantity=1.0,
        risk_amount=risk,
        pnl=float(pnl),
    )


def trades_from(pnls, **kwargs):
    return [make_trade(i + 1, p, **kwargs) for i, p in enumerate(pnls)]


def test_sample_data_results():
    # P/L values from data/sample_trades.csv
    m = compute_metrics(trades_from([100, -50, 40, 30, -20]))
    assert m.total_trades == 5
    assert m.winning_trades == 3
    assert m.losing_trades == 2
    assert m.breakeven_trades == 0
    assert m.win_rate_pct == pytest.approx(60.0)
    assert m.gross_profit == pytest.approx(170.0)
    assert m.gross_loss == pytest.approx(70.0)
    assert m.net_pnl == pytest.approx(100.0)
    assert m.profit_factor == pytest.approx(170 / 70)
    assert m.average_win == pytest.approx(170 / 3)
    assert m.average_loss == pytest.approx(35.0)
    assert m.max_drawdown == pytest.approx(50.0)
    assert m.largest_win == 100.0
    assert m.largest_loss == 50.0


def test_breakeven_is_neither_win_nor_loss():
    m = compute_metrics(trades_from([10, 0, -5]))
    assert (m.winning_trades, m.losing_trades, m.breakeven_trades) == (1, 1, 1)
    assert m.win_rate_pct == pytest.approx(100 / 3)


def test_profit_factor_none_without_losses():
    m = compute_metrics(trades_from([10, 20]))
    assert m.profit_factor is None
    assert m.average_loss is None
    assert m.largest_loss is None


def test_profit_factor_zero_without_wins():
    m = compute_metrics(trades_from([-10, -20]))
    assert m.profit_factor == 0.0
    assert m.average_win is None
    assert m.win_rate_pct == 0.0


def test_risk_reward_and_r_multiple():
    # pnl/risk: +2.0, -1.0 ; absolute: 2.0, 1.0
    m = compute_metrics(trades_from([20, -10], risk=10.0))
    assert m.average_risk_reward == pytest.approx(1.5)
    assert m.average_r_multiple == pytest.approx(0.5)


def test_risk_reward_excludes_invalid_risk():
    good = make_trade(1, 20, risk=10.0)
    bad = make_trade(2, 500, risk=0.0)  # only possible when built programmatically
    m = compute_metrics([good, bad])
    assert m.average_risk_reward == pytest.approx(2.0)
    assert m.total_trades == 2


def test_drawdown_from_zero_start():
    dd, pct = max_drawdown([100, -50, 40, 30, -20])
    assert dd == pytest.approx(50.0)


def test_drawdown_is_zero_when_equity_only_rises():
    assert max_drawdown([10, 20, 30])[0] == 0.0


def test_drawdown_starting_below_zero_peak():
    # Never above the starting equity of 0: drawdown is the deepest dip.
    assert max_drawdown([-10, -20, 5])[0] == pytest.approx(30.0)


def test_drawdown_percent_with_balance():
    m = compute_metrics(trades_from([100, -50]), initial_balance=1000.0)
    # peak 1100 -> 1050
    assert m.max_drawdown == pytest.approx(50.0)
    assert m.max_drawdown_pct == pytest.approx(50 / 1100 * 100)


def test_drawdown_percent_none_without_balance():
    assert compute_metrics(trades_from([100, -50])).max_drawdown_pct is None


def test_drawdown_uses_date_order_not_file_order():
    late_loss = make_trade(1, -50, day=date(2026, 3, 1))
    early_win = make_trade(2, 100, day=date(2026, 1, 1))
    m = compute_metrics([late_loss, early_win])  # file order: loss first
    assert m.max_drawdown == pytest.approx(50.0)  # win, then loss


def test_max_consecutive_losses():
    m = compute_metrics(trades_from([5, -1, -1, -1, 5, -1]))
    assert m.max_consecutive_losses == 3


def test_by_symbol_breakdown():
    trades = [
        make_trade(1, 10, symbol="AAPL"),
        make_trade(2, -4, symbol="AAPL"),
        make_trade(3, 7, symbol="MSFT"),
    ]
    m = compute_metrics(trades)
    assert list(m.by_symbol) == ["AAPL", "MSFT"]
    assert m.by_symbol["AAPL"].net_pnl == pytest.approx(6.0)
    assert m.by_symbol["AAPL"].win_rate_pct == pytest.approx(50.0)
    assert m.by_symbol["MSFT"].trades == 1


def test_floating_point_sums_are_exact_enough():
    m = compute_metrics(trades_from([0.1] * 10))
    assert m.net_pnl == pytest.approx(1.0, abs=1e-12)


def test_negative_initial_balance_rejected():
    with pytest.raises(ValueError):
        compute_metrics(trades_from([1]), initial_balance=-1)


def test_empty_trade_list_is_safe():
    m = compute_metrics([])
    assert m.total_trades == 0
    assert m.win_rate_pct == 0.0
    assert m.profit_factor is None
    assert m.max_drawdown == 0.0
