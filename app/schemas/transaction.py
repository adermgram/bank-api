from decimal import Decimal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field

from app.enums.transaction import TransactionType


class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class WithdrawRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class TransactionResponse(BaseModel):
    id: UUID
    transaction_type: TransactionType
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    reference: str
    description: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }