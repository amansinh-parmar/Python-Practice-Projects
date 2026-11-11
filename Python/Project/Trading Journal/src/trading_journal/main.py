
from pathlib import Path
import sys
import subprocess

from trading_journal.importer import ImportValidationError, load_trades
from trading_journal.reporter import format_report


def display_menu() -> None:
    """Display the main Trading Journal menu."""
    print("\n" + "=" * 45)
    print("          TRADING JOURNAL CLI")
    print("=" * 45)
    print("1. Import trades from a file")
    print("2. View trading metrics")
    print("3. Generate trading report")
    print("4. Run project tests")
    print("5. Exit")
    print("=" * 45)


def get_file_path() -> Path | None:
    """Ask for a CSV file path and validate it."""
    file_path = input("Enter the path to your trade CSV file: ").strip()
    path = Path(file_path.strip('"'))

    if not path.exists():
        print(f"Error: File not found: {path}")
        return None

    if not path.is_file():
        print("Error: Please provide a file path.")
        return None

    return path


def import_trades() -> None:
    """Load and validate trades from a CSV file."""
    path = get_file_path()
    if path is None:
        return

    try:
        trades = load_trades(path)
        print(f"Successfully imported {len(trades)} trades.")
    except (ImportValidationError, OSError) as exc:
        print(f"Import failed: {exc}")


def calculate_metrics(trades):
    """Calculate metrics using the project's metrics module."""
    from trading_journal import metrics

    # Adjust this call to the actual public function in metrics.py.
    for name in ("calculate_metrics", "compute_metrics", "summarize_trades"):
        function = getattr(metrics, name, None)
        if callable(function):
            return function(trades)

    raise AttributeError(
        "No supported metrics function found in metrics.py. "
        "Check its public function names."
    )


def view_metrics() -> None:
    """Display trading metrics."""
    path = get_file_path()
    if path is None:
        return

    try:
        trades = load_trades(path)
        result = calculate_metrics(trades)
        print("\nTrading Metrics")
        print("-" * 30)
        print(result)
    except (ImportValidationError, OSError, ImportError, AttributeError, TypeError) as exc:
        print(f"Could not calculate metrics: {exc}")


def generate_report() -> None:
    """Generate a trading report from a CSV file."""
    path = get_file_path()
    if path is None:
        return

    try:
        trades = load_trades(path)
        metrics_result = calculate_metrics(trades)
        print("\nTrading Report")
        print("-" * 30)
        print(format_report(metrics_result))
    except (ImportValidationError, OSError, ImportError, AttributeError, TypeError) as exc:
        print(f"Could not generate report: {exc}")


def run_tests() -> None:
    """Run the project's pytest test suite from the project root."""
    project_root = Path(__file__).resolve().parent

    # Support running main.py from the project root or src directory.
    if not (project_root / "tests").exists():
        project_root = project_root.parent

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "tests"],
            cwd=project_root,
            check=False,
        )
        if result.returncode == 0:
            print("\nAll tests passed.")
        else:
            print(f"\nTests failed with exit code: {result.returncode}")
    except OSError as exc:
        print(f"Could not run tests: {exc}")


def main() -> None:
    """Run the Trading Journal menu."""
    actions = {
        "1": import_trades,
        "2": view_metrics,
        "3": generate_report,
        "4": run_tests,
    }

    while True:
        display_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "5":
            print("Thank you for using Trading Journal. Goodbye!")
            return

        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number from 1 to 5.")
            continue

        action()


if __name__ == "__main__":
    main()
