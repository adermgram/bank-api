from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.schemas.transaction import (
    DepositRequest,
    WithdrawRequest,
    TransactionResponse,
    TransferRequest
)
from app.services.transaction_service import TransactionService


router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


def get_transaction_service(
    db: AsyncSession = Depends(get_db),
) -> TransactionService:
    account_repo = AccountRepository(db)
    transaction_repo = TransactionRepository(db)

    return TransactionService(
        account_repo=account_repo,
        transaction_repo=transaction_repo,
    )


@router.post(
    "/deposit",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def deposit(
    data: DepositRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = await service.deposit(
        user_id=current_user.id,
        amount=data.amount,
    )

    await db.commit()
    await db.refresh(transaction)

    return transaction


@router.post(
    "/withdraw",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def withdraw(
    data: WithdrawRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = await service.withdraw(
        user_id=current_user.id,
        amount=data.amount,
    )

    await db.commit()
    await db.refresh(transaction)

    return transaction


@router.get(
    "/me",
    response_model=list[TransactionResponse],
)
async def get_my_transactions(
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    return await service.get_user_transactions(current_user.id)


@router.post(
    "/transfer",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def transfer(
    data: TransferRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = await service.transfer(
        user_id=current_user.id,
        to_account_number=data.to_account_number,
        amount=data.amount,
        description=data.description,
    )

    await db.commit()
    await db.refresh(transaction)

    return transaction