"""Tests for the Trading Journal command-line interface."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from trading_journal.cli import main

SRC = Path(__file__).resolve().parents[1] / "src"


def test_analyze_prints_report(sample_csv, capsys):
    """Analyze should print the performance report."""
    result = main(["analyze", str(sample_csv)])

    captured = capsys.readouterr()

    assert result == 0
    assert "TRADING JOURNAL — PERFORMANCE REPORT" in captured.out
    assert "Trades analyzed:" in captured.out
    assert "Win rate:" in captured.out
    assert "60.00%" in captured.out
    assert captured.err == ""


def test_analyze_writes_json(sample_csv, tmp_path, capsys):
    """Analyze should write a valid JSON summary."""
    target = tmp_path / "reports" / "summary.json"

    result = main(
        [
            "analyze",
            str(sample_csv),
            "--output",
            str(target),
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert target.is_file()

    data = json.loads(target.read_text(encoding="utf-8"))

    assert data["total_trades"] == 5
    assert data["net_pnl"] == 100.0
    assert "written to" in captured.out.lower()
    assert captured.err == ""


def test_quiet_suppresses_report(sample_csv, capsys):
    """Quiet mode should suppress terminal report output."""
    result = main(["analyze", str(sample_csv), "--quiet"])

    captured = capsys.readouterr()

    assert result == 0
    assert captured.out == ""
    assert captured.err == ""


def test_initial_balance_enables_drawdown_percent(sample_csv, tmp_path):
    """An initial balance should enable drawdown percentage."""
    target = tmp_path / "summary.json"

    result = main(
        [
            "analyze",
            str(sample_csv),
            "--quiet",
            "--output",
            str(target),
            "--initial-balance",
            "1000",
        ]
    )

    assert result == 0

    data = json.loads(target.read_text(encoding="utf-8"))

    assert data["initial_balance"] == 1000.0
    assert data["max_drawdown_pct"] is not None


def test_missing_file_returns_error(tmp_path, capsys):
    """A nonexistent CSV file should produce a clear error."""
    missing = tmp_path / "missing.csv"

    result = main(["analyze", str(missing)])

    captured = capsys.readouterr()

    assert result == 1
    assert "file not found" in captured.err.lower()


def test_invalid_data_lists_every_problem(write_csv, capsys):
    """All invalid rows should be reported in one invocation."""
    path = write_csv(
        "trade_id,date,symbol,direction,entry_price,exit_price,"
        "quantity,risk_amount,pnl\n"
        "T1,nope,AAPL,LONG,1,2,1,1,1\n"
        "T2,2026-01-01,AAPL,LONG,1,2,0,1,1\n"
    )

    result = main(["analyze", str(path)])

    captured = capsys.readouterr()

    assert result == 1
    assert "line 2" in captured.err
    assert "line 3" in captured.err


def test_negative_balance_rejected_by_argparse(sample_csv, capsys):
    """A negative initial balance should be rejected."""
    with pytest.raises(SystemExit) as exc_info:
        main(
            [
                "analyze",
                str(sample_csv),
                "--initial-balance",
                "-5",
            ]
        )

    assert exc_info.value.code == 2


def test_python_dash_m_entry_point(sample_csv):
    """The package should run through python -m."""
    env = os.environ.copy()
    existing_path = env.get("PYTHONPATH")

    env["PYTHONPATH"] = (
        str(SRC) if not existing_path else str(SRC) + os.pathsep + existing_path
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "trading_journal",
            "analyze",
            str(sample_csv),
        ],
        capture_output=True,
        text=True,
        env=env,
        check=False,
        timeout=30,
    )

    assert result.returncode == 0, (
        f"CLI failed.\nstdout:\n{result.stdout}\n" f"stderr:\n{result.stderr}"
    )
    assert "Trades analyzed:" in result.stdout


def test_help_exits_zero(capsys):
    """The help option should exit successfully."""
    with pytest.raises(SystemExit) as exc_info:
        main(["--help"])

    captured = capsys.readouterr()

    assert exc_info.value.code == 0
    assert "analyze" in captured.out
