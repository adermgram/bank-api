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

from fastapi import status

from app.schemas.transaction import (
    DepositRequest,
    WithdrawRequest,
    TransactionResponse
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

@router.post(
    "/deposit",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED
)
async def deposit(
    data: DepositRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )

    account = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    before = account.balance
    after = before + data.amount

    account.balance = after

    tx = Transaction(
        account_id=account.id,
        transaction_type="deposit",
        amount=data.amount,
        balance_before=before,
        balance_after=after,
        reference=str(uuid4()),
        description="Cash deposit"
    )

    db.add(tx)

    await db.commit()
    await db.refresh(tx)

    return tx



@router.post(
    "/withdraw",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED
)
async def withdraw(
    data: WithdrawRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )

    account = result.scalar_one_or_none()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    if account.balance < data.amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient funds"
        )

    before = account.balance
    after = before - data.amount

    account.balance = after

    tx = Transaction(
        account_id=account.id,
        transaction_type="withdrawal",
        amount=data.amount,
        balance_before=before,
        balance_after=after,
        reference=str(uuid4()),
        description="Cash withdrawal"
    )

    db.add(tx)

    await db.commit()
    await db.refresh(tx)

    return tx