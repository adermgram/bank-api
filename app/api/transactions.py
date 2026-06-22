from fastapi import APIRouter
from decimal import Decimal
from uuid import uuid4

from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.api.auth import get_current_user

from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction

from app.schemas.transaction import DepositRequest

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post("/deposit")
async def deposit(
    data: DepositRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Account).where(
            Account.user_id == current_user.id
        )
    )

    account = result.scalar_one()

    before = account.balance

    account.balance += data.amount

    tx = Transaction(
        account_id=account.id,
        transaction_type="deposit",
        amount=data.amount,
        balance_before=before,
        balance_after=account.balance,
        reference=str(uuid4()),
        description="Cash deposit"
    )

    db.add(tx)

    await db.commit()

    return {
        "message": "Deposit successful",
        "new_balance": account.balance
    }