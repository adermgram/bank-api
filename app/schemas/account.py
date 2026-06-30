from uuid import UUID
from decimal import Decimal

from pydantic import BaseModel

from app.enums.account import AccountStatus, AccountType


class AccountResponse(BaseModel):
    id: UUID
    account_number: str
    balance: Decimal
    account_type: AccountType
    status: AccountStatus

    model_config = {
        "from_attributes": True
    }