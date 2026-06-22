from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel


class AccountResponse(BaseModel):
    id: UUID
    account_number: str
    balance: Decimal
    account_type: str
    status: str

    model_config = {
        "from_attributes": True
    }