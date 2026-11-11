"""
Trading Journal & Risk Analyzer
-------------------------------
A simple command line tool that reads trades from a CSV file
and prints a performance report (and optionally saves it as JSON).

Usage:
    python journal.py sample_trades.csv
    python journal.py sample_trades.csv --balance 10000 --output summary.json
"""

import argparse
import csv
import json

REQUIRED_COLUMNS = ["date", "symbol", "side", "entry", "exit", "quantity", "stop_loss"]


# ---------------------------------------------------------------
# STEP 1: Import trades from a CSV file
# ---------------------------------------------------------------
def load_trades(path):
    """Read the CSV file and return a list of trade dictionaries."""
    trades = []

    with open(path, newline="") as file:
        reader = csv.DictReader(file)  # reads each row as a dictionary

        # 1a. Make sure the file has all the columns we need.
        columns = reader.fieldnames or []
        missing = [c for c in REQUIRED_COLUMNS if c not in columns]

        if missing:
            raise ValueError(f"CSV is missing columns: {' '.join(missing)}")

            # 1b. Go through each row (line 1 is the header, so data starts at line

        for line_number, row in enumerate(reader, start=2):
            try:
                trade = {
                    "date": row["date"].strip(),
                    "symbol": row["symbol"].strip(),
                    "side": row["side"].strip(),
                    "entry": float(row["entry"]),
                    "exit": float(row["exit"]),
                    "quantity": float(row["quantity"]),
                    "stop_loss": float(row["stop_loss"]),
                }

            except (ValueError, AttributeError):
                # A number could not be converted, so skip this row.
                print(f"Warning: Skipping line {line_number} (band number)")
                continue

            # 1c. Side must be "long" (buy) or "short" (sell).
            if trade["side"] not in ("long", "short"):
                print(f"Warning: Skipping line {line_number} (side must be long)")
                continue

            trades.append(trade)


# ---------------------------------------------------------------
# STEP 2: Calculate profit/loss and risk for ONE trade
# ---------------------------------------------------------------

                                                                                                                                                                      