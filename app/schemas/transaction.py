from decimal import Decimal

from pydantic import BaseModel
from pydantic import Field


class DepositRequest(BaseModel):
    amount: Decimal = Field(gt=0)