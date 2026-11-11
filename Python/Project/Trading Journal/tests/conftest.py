import pytest

HEADER = "trade_id,date,symbol,direction,entry_price,exit_price,quantity,risk_amount,pnl\n"

SAMPLE_ROWS = (
    "T001,2026-01-05,AAPL,LONG,100,110,10,50,100\n"
    "T002,2026-01-06,MSFT,LONG,200,190,5,40,-50\n"
    "T003,2026-01-07,TSLA,SHORT,250,230,2,30,40\n"
    "T004,2026-01-08,NVDA,LONG,120,126,5,30,30\n"
    "T005,2026-01-09,AAPL,SHORT,115,120,4,20,-20\n"
)


@pytest.fixture
def write_csv(tmp_path):
    """Return a function that writes CSV text to a temp file and returns its path."""

    def _write(text: str, name: str = "trades.csv"):
        path = tmp_path / name
        path.write_text(text, encoding="utf-8")
        return path

    return _write


@pytest.fixture
def sample_csv(write_csv):
    return write_csv(HEADER + SAMPLE_ROWS)
