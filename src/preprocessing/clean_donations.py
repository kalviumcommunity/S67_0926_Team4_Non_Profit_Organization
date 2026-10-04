"""Clean and normalize donation CSV files without modifying the raw source."""
from __future__ import annotations

import argparse
import csv
import logging
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Mapping

logger = logging.getLogger(__name__)

DEFAULT_COLUMN_MAP = {
    "donation_id": "donation_id",
    "donation_date": "donation_date",
    "amount": "amount",
    "currency": "currency",
    "donor_id": "donor_id",
    "campaign": "campaign",
    "payment_method": "payment_method",
}

REQUIRED_FIELDS = ("donation_id", "donation_date", "amount")
OUTPUT_FIELDS = tuple(DEFAULT_COLUMN_MAP)


def _parse_date(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("donation_date is blank")
    # Accept ISO dates and common date-time strings; preserve date only.
    try:
        return date.fromisoformat(value[:10]).isoformat()
    except ValueError:
        pass
    for fmt in ("%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"unsupported date format: {value!r}")


def _parse_amount(value: str) -> str:
    try:
        amount = Decimal(value.strip().replace(",", ""))
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError(f"invalid amount: {value!r}") from exc
    if not amount.is_finite() or amount <= 0:
        raise ValueError(f"amount must be finite and positive: {value!r}")
    return format(amount, "f")


def clean_row(row: Mapping[str, str], column_map: Mapping[str, str] | None = None) -> dict[str, str]:
    """Return a canonical row or raise ValueError when required data is invalid."""
    mapping = dict(DEFAULT_COLUMN_MAP)
    if column_map:
        mapping.update(column_map)

    def get(field: str) -> str:
        source = mapping.get(field, field)
        value = row.get(source, "")
        return "" if value is None else str(value).strip()

    donation_id = get("donation_id")
    if not donation_id:
        raise ValueError("donation_id is blank")

    donation_date = _parse_date(get("donation_date"))
    amount = _parse_amount(get("amount"))

    currency = get("currency") or "INR"
    if len(currency) != 3 or not currency.isalpha():
        raise ValueError(f"currency must be a 3-letter code: {currency!r}")

    cleaned = {
        "donation_id": donation_id,
        "donation_date": donation_date,
        "amount": amount,
        "currency": currency.upper(),
        "donor_id": get("donor_id"),
        "campaign": get("campaign"),
        "payment_method": get("payment_method"),
    }
    return cleaned


def clean_csv(input_path: str | Path, output_path: str | Path,
              column_map: Mapping[str, str] | None = None) -> dict[str, int]:
    """Clean a CSV into canonical columns; invalid rows are skipped and counted.

    Duplicate donation IDs are skipped after the first valid occurrence.
    The input file is read-only and is never overwritten.
    """
    input_path, output_path = Path(input_path), Path(output_path)
    if input_path.resolve() == output_path.resolve():
        raise ValueError("output_path must differ from input_path")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    counts = {"total": 0, "cleaned": 0, "invalid": 0, "duplicates": 0}
    seen_ids: set[str] = set()

    with input_path.open("r", encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames:
            raise ValueError("input CSV has no header")
        mapping = dict(DEFAULT_COLUMN_MAP)
        if column_map:
            mapping.update(column_map)
        missing = [mapping[f] for f in REQUIRED_FIELDS if mapping[f] not in reader.fieldnames]
        if missing:
            raise ValueError(
                "Missing required source columns: " + ", ".join(missing) +
                ". Supply a column mapping for your CSV headers."
            )
        with output_path.open("w", encoding="utf-8", newline="") as target:
            writer = csv.DictWriter(target, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
            writer.writeheader()
            for row in reader:
                counts["total"] += 1
                try:
                    cleaned = clean_row(row, mapping)
                except (ValueError, TypeError) as exc:
                    counts["invalid"] += 1
                    logger.warning("Skipping CSV row %d: %s", reader.line_num, exc)
                    continue
                if cleaned["donation_id"] in seen_ids:
                    counts["duplicates"] += 1
                    continue
                seen_ids.add(cleaned["donation_id"])
                writer.writerow(cleaned)
                counts["cleaned"] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean donation CSV data.")
    parser.add_argument("input", help="Path to raw donation CSV")
    parser.add_argument("output", help="Path for cleaned CSV")
    parser.add_argument(
        "--map", action="append", default=[], metavar="FIELD=SOURCE_COLUMN",
        help="Map canonical field to a source CSV column; repeat as needed.",
    )
    args = parser.parse_args()
    mapping = {}
    for item in args.map:
        if "=" not in item:
            parser.error("--map must use FIELD=SOURCE_COLUMN")
        field, source = item.split("=", 1)
        if field not in DEFAULT_COLUMN_MAP or not source:
            parser.error(f"invalid mapping: {item}")
        mapping[field] = source
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    print(clean_csv(args.input, args.output, mapping or None))


if __name__ == "__main__":
    main()
