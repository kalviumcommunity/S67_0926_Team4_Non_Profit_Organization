from datetime import date
from decimal import Decimal
import pytest
from src.schemas.donation_schema import DonationRecord

def sample(**kw):
    d = dict(donation_id="don-001", donation_date=date(2026, 9, 29), amount=Decimal("12.50"))
    d.update(kw)
    return d

def test_valid_record():
    assert DonationRecord(**sample()).amount == Decimal("12.50")

def test_normalizes_currency():
    assert DonationRecord(**sample(currency="usd")).currency == "USD"

@pytest.mark.parametrize("amount", [0, -1, "NaN", "Infinity", "invalid"])
def test_rejects_invalid_amount(amount):
    with pytest.raises(ValueError):
        DonationRecord(**sample(amount=amount))

def test_rejects_blank_id():
    with pytest.raises(ValueError):
        DonationRecord(**sample(donation_id=" "))
