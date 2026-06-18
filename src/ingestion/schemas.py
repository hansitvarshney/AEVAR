from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone

class RawInvoiceModel(BaseModel):
    invoice_id: str = Field(..., min_length=4)
    vendor_name: str = Field(..., min_length=2)
    amount: float = Field(..., description="Raw billing total amount")
    status: str = Field(default="PENDING")
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("amount", mode="before")
    @classmethod
    def clean_and_validate_amount(cls, value: any) -> float:
        if value is None:
            raise ValueError("Invoice amount cannot be null or empty.")
        if isinstance(value, str):
            sanitized = value.replace("$", "").replace(",", "").strip()
            try:
                value = float(sanitized)
            except ValueError:
                raise ValueError(f"Could not convert currency string '{value}' to a valid float.")
        if value <= 0:
            raise ValueError(f"Invoice amount must be positive. Got: {value}")
        return value

    @field_validator("status")
    @classmethod
    def sanitize_status(cls, value: str) -> str:
        sanitized = value.strip().upper()
        valid_statuses = {"PAID", "PENDING", "PROCESSING"}
        if not sanitized or sanitized not in valid_statuses:
            return "PENDING"
        return sanitized