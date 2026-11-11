from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trading_journal.importer import ImportValidationError, load_trades
from trading_journal.reporter import format_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading-journal",
        description="Import trades and generate a trading journal report.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    import_parser = subparsers.add_parser(
        "import",
        help="Validate and import a trades CSV file.",
    )
    import_parser.add_argument("csv_file", type=Path)

    report_parser = subparsers.add_parser(
        "report",
        help="Generate a report from a trades CSV file.",
    )
    report_parser.add_argument("csv_file", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        trades = load_trades(args.csv_file)

        if args.command == "import":
            print(f"Successfully loaded {len(trades)} trades.")
            return 0

        if args.command == "report":
            print(format_report(trades))
            return 0

    except (ImportValidationError, FileNotFoundError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
