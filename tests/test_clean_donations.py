import csv
from pathlib import Path

import pytest

from src.preprocessing.clean_donations import clean_row, clean_csv


def test_clean_row_normalizes_values():
    row = {
        "donation_id": " d-1 ", "donation_date": "09/29/2026",
        "amount": "1,250.50", "currency": "usd",
        "donor_id": "", "campaign": " Spring ", "payment_method": " card ",
    }
    result = clean_row(row)
    assert result["donation_id"] == "d-1"
    assert result["donation_date"] == "2026-09-29"
    assert result["amount"] == "1250.50"
    assert result["currency"] == "USD"
    assert result["campaign"] == "Spring"


@pytest.mark.parametrize("amount", ["0", "-3", "NaN", "Infinity", "abc", ""])
def test_rejects_invalid_amount(amount):
    row = {"donation_id": "d1", "donation_date": "2026-09-29", "amount": amount}
    with pytest.raises(ValueError):
        clean_row(row)


def test_rejects_missing_id():
    with pytest.raises(ValueError, match="donation_id"):
        clean_row({"donation_id": " ", "donation_date": "2026-09-29", "amount": "1"})


def test_clean_csv_skips_invalid_and_duplicate_rows(tmp_path: Path):
    source = tmp_path / "raw.csv"
    output = tmp_path / "processed" / "clean.csv"
    with source.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["donation_id", "donation_date", "amount", "currency"])
        writer.writeheader()
        writer.writerow({"donation_id": "d1", "donation_date": "2026-09-29", "amount": "10", "currency": "inr"})
        writer.writerow({"donation_id": "d1", "donation_date": "2026-09-29", "amount": "20", "currency": "INR"})
        writer.writerow({"donation_id": "d2", "donation_date": "bad-date", "amount": "30", "currency": "INR"})
    stats = clean_csv(source, output)
    assert stats == {"total": 3, "cleaned": 1, "invalid": 1, "duplicates": 1}
    assert source.exists()
    with output.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 1
    assert rows[0]["donation_id"] == "d1"


def test_requires_different_input_and_output(tmp_path):
    path = tmp_path / "same.csv"
    path.write_text("donation_id,donation_date,amount\nd1,2026-09-29,10\n")
    with pytest.raises(ValueError, match="differ"):
        clean_csv(path, path)


def test_supports_source_column_mapping():
    row = {"ID": "x1", "Date": "2026-09-29", "Donation": "25"}
    result = clean_row(row, {"donation_id": "ID", "donation_date": "Date", "amount": "Donation"})
    assert result["donation_id"] == "x1"
    assert result["amount"] == "25"
