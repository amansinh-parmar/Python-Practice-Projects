import pytest

from tests.conftest import HEADER, SAMPLE_ROWS
from trading_journal.importer import ImportValidationError, load_trades, parse_trades


def lines(text):
    return text.splitlines(keepends=True)


def test_loads_sample_file(sample_csv):
    trades = load_trades(sample_csv)
    assert len(trades) == 5
    assert trades[0].trade_id == "T001"
    assert trades[0].symbol == "AAPL"
    assert trades[2].direction == "SHORT"
    assert trades[1].pnl == -50.0


def test_normalises_case_whitespace_and_bom(write_csv):
    text = (
        "\ufeff"
        + HEADER.upper().replace("LONG", "long")
        + " T1 ,2026-01-05, aapl ,long,100,110,10,50,100\n"
    )
    # write with utf-8-sig style BOM preserved in the file
    path = write_csv(text)
    (trade,) = load_trades(path)
    assert trade.trade_id == "T1"
    assert trade.symbol == "AAPL"
    assert trade.direction == "LONG"


def test_blank_lines_are_ignored():
    trades = parse_trades(lines(HEADER + SAMPLE_ROWS + "\n\n"))
    assert len(trades) == 5


def test_missing_columns_reported():
    with pytest.raises(ImportValidationError, match="missing required column"):
        parse_trades(lines("trade_id,date\nT1,2026-01-01\n"))


def test_empty_file():
    with pytest.raises(ImportValidationError, match="empty"):
        parse_trades([])


def test_header_only_file():
    with pytest.raises(ImportValidationError, match="no trades"):
        parse_trades(lines(HEADER))


def test_duplicate_trade_ids():
    text = HEADER + SAMPLE_ROWS + "T001,2026-02-01,AAPL,LONG,1,2,1,1,1\n"
    with pytest.raises(ImportValidationError) as exc:
        parse_trades(lines(text))
    assert "duplicate trade_id 'T001'" in str(exc.value)
    assert "line 7" in exc.value.errors[0]


@pytest.mark.parametrize(
    "row, message",
    [
        ("T1,01/05/2026,AAPL,LONG,100,110,10,50,100", "date must be YYYY-MM-DD"),
        ("T1,2026-02-30,AAPL,LONG,100,110,10,50,100", "date must be YYYY-MM-DD"),
        ("T1,2026-01-05,AAPL,BUY,100,110,10,50,100", "direction must be"),
        ("T1,2026-01-05,AAPL,LONG,abc,110,10,50,100", "entry_price must be a number"),
        ("T1,2026-01-05,AAPL,LONG,100,110,10,50,nan", "finite"),
        ("T1,2026-01-05,AAPL,LONG,100,110,10,50,inf", "finite"),
        ("T1,2026-01-05,AAPL,LONG,100,110,0,50,100", "quantity must be positive"),
        ("T1,2026-01-05,AAPL,LONG,100,110,-3,50,100", "quantity must be positive"),
        ("T1,2026-01-05,AAPL,LONG,100,110,10,0,100", "risk_amount must be positive"),
        ("T1,2026-01-05,AAPL,LONG,100,110,10,-5,100", "risk_amount must be positive"),
        ("T1,2026-01-05,AAPL,LONG,0,110,10,50,100", "must be positive"),
        (",2026-01-05,AAPL,LONG,100,110,10,50,100", "trade_id is required"),
        ("T1,2026-01-05,,LONG,100,110,10,50,100", "symbol is required"),
        ("T1,2026-01-05,AAPL,LONG,100,110,10,50", "pnl must be a number"),
    ],
)
def test_invalid_rows(row, message):
    with pytest.raises(ImportValidationError, match=message):
        parse_trades(lines(HEADER + row + "\n"))


def test_all_errors_reported_together_with_line_numbers():
    text = HEADER + (
        "T1,bad-date,AAPL,LONG,100,110,10,50,100\n"
        "T2,2026-01-05,AAPL,LONG,100,110,-1,50,100\n"
    )
    with pytest.raises(ImportValidationError) as exc:
        parse_trades(lines(text))
    assert len(exc.value.errors) == 2
    assert exc.value.errors[0].startswith("line 2:")
    assert exc.value.errors[1].startswith("line 3:")


def test_thousands_separator_in_quoted_number():
    row = 'T1,2026-01-05,AAPL,LONG,100,110,10,50,"1,250.50"\n'
    (trade,) = parse_trades(lines(HEADER + row))
    assert trade.pnl == 1250.50


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_trades(tmp_path / "nope.csv")
