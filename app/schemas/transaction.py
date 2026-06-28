from decimal import Decimal
from uuid import UUID
from pydantic import BaseModel
from pydantic import Field
from datetime import datetime


class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class WithdrawRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class TransactionResponse(BaseModel):
    id: UUID
    transaction_type: str
    amount: Decimal
    balance_before: Decimal
    balance_after: Decimal
    reference: str
    description: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }