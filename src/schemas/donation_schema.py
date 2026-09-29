"""Canonical donation record schema (Python standard library only)."""
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Optional

@dataclass(frozen=True, slots=True)
class DonationRecord:
    donation_id: str
    donation_date: date
    amount: Decimal
    currency: str = "INR"
    donor_id: Optional[str] = None
    campaign: Optional[str] = None
    payment_method: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.donation_id, str) or not self.donation_id.strip():
            raise ValueError("donation_id must be a non-empty string")
        if not isinstance(self.donation_date, date):
            raise TypeError("donation_date must be a datetime.date")
        try:
            amount = Decimal(str(self.amount))
        except (InvalidOperation, TypeError, ValueError) as exc:
            raise ValueError("amount must be a valid decimal number") from exc
        if not amount.is_finite() or amount <= 0:
            raise ValueError("amount must be finite and positive")
        if not isinstance(self.currency, str) or len(self.currency) != 3 or not self.currency.isalpha():
            raise ValueError("currency must be a 3-letter currency code")
        object.__setattr__(self, "amount", amount)
        object.__setattr__(self, "currency", self.currency.upper())
        for name in ("donor_id", "campaign", "payment_method"):
            value = getattr(self, name)
            if value is not None and (not isinstance(value, str) or not value.strip()):
                raise ValueError(f"{name} must be None or a non-empty string")
