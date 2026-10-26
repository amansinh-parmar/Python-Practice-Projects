import json

import pytest

from tests.test_metrics import trades_from
from trading_journal.metrics import compute_metrics
from trading_journal.reporter import format_report, to_summary_dict, write_json
from tests.conftest import HEADER, SAMPLE_ROWS
from tests.helpers import trades_from
from tests.test_metrics import trades_from


def test_report_contains_key_figures():
    text = format_report(compute_metrics(trades_from([100, -50, 40, 30, -20])))
    assert "Trades analyzed:" in text
    assert "60.00%" in text
    assert "2.43" in text
    assert "Maximum drawdown:" in text
    assert text.rstrip().endswith("Report generated successfully.")


def test_report_shows_na_for_undefined_profit_factor():
    text = format_report(compute_metrics(trades_from([10, 20])))
    line = next(l for l in text.splitlines() if l.startswith("Profit factor:"))
    assert line.rstrip().endswith("n/a")


def test_summary_dict_rounds_and_uses_none():
    summary = to_summary_dict(compute_metrics(trades_from([100, -50, 40, 30, -20])))
    assert summary["profit_factor"] == 2.4286
    assert summary["gross_loss"] == 70.0
    assert summary["max_drawdown_pct"] is None


def test_write_json_creates_parent_dirs_and_valid_json(tmp_path):
    target = tmp_path / "nested" / "dir" / "summary.json"
    write_json(compute_metrics(trades_from([10, 20])), target)
    data = json.loads(target.read_text(encoding="utf-8"))
    assert data["profit_factor"] is None  # JSON null, never Infinity/NaN
    assert data["total_trades"] == 2
    assert "Infinity" not in target.read_text()
    assert "NaN" not in target.read_text()


def test_write_json_refuses_nan(tmp_path):
    m = compute_metrics(trades_from([10, -5]))
    object.__setattr__(m, "net_pnl", float("nan"))
    with pytest.raises(ValueError):
        write_json(m, tmp_path / "bad.json")
