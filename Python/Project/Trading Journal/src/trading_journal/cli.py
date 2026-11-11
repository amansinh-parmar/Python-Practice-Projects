"""Command-line interface: orchestrates import -> analyze -> report."""

from __future__ import annotations

import argparse
import math
import sys
from typing import Sequence

from . import __version__
from .importer import ImportValidationError, load_trades
from .metrics import compute_metrics
from .reporter import format_report, write_json

EXIT_OK = 0
EXIT_DATA_ERROR = 1  # argparse itself exits with 2 on bad usage


def _non_negative_float(text: str) -> float:
    try:
        value = float(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{text!r} is not a number") from None
    if not math.isfinite(value) or value < 0:
        raise argparse.ArgumentTypeError("must be a non-negative number")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_journal",
        description="Analyze a CSV of completed trades.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="command")

    analyze = sub.add_parser(
        "analyze", help="print a performance report for a trades CSV file"
    )
    analyze.add_argument("csv_file", help="path to the trades CSV")
    analyze.add_argument(
        "-o", "--output", metavar="PATH", help="also write a JSON summary to PATH"
    )
    analyze.add_argument(
        "--initial-balance",
        type=_non_negative_float,
        default=0.0,
        metavar="AMOUNT",
        help="starting account balance; enables drawdown %% (default: 0, "
        "i.e. drawdown on the cumulative P/L curve)",
    )
    analyze.add_argument(
        "-q", "--quiet", action="store_true", help="suppress the terminal report"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        trades = load_trades(args.csv_file)
    except FileNotFoundError:
        print(f"error: file not found: {args.csv_file}", file=sys.stderr)
        return EXIT_DATA_ERROR
    except (OSError, UnicodeDecodeError) as exc:
        print(f"error: cannot read {args.csv_file}: {exc}", file=sys.stderr)
        return EXIT_DATA_ERROR
    except ImportValidationError as exc:
        print(f"error: {args.csv_file} is not a valid trades file:", file=sys.stderr)
        for message in exc.errors:
            print(f"  - {message}", file=sys.stderr)
        return EXIT_DATA_ERROR

    metrics = compute_metrics(trades, initial_balance=args.initial_balance)

    if not args.quiet:
        print(format_report(metrics))

    if args.output:
        try:
            path = write_json(metrics, args.output)
        except OSError as exc:
            print(f"error: cannot write {args.output}: {exc}", file=sys.stderr)
            return EXIT_DATA_ERROR
        print(f"JSON summary written to {path}")

    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
