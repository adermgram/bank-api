from fastapi import APIRouter, Depends, status

from app.api.auth import get_current_user
from app.models.user import User
from app.schemas.transaction import (
    DepositRequest,
    WithdrawRequest,
    TransactionResponse,
    TransferRequest
)
from app.services.transaction_service import TransactionService
from app.db.dependencies import get_uow
from app.db.unit_of_work import UnitOfWork

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"],
)


def get_transaction_service(
    uow: UnitOfWork = Depends(get_uow),
) -> TransactionService:
    return TransactionService(uow)


@router.post(
    "/deposit",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def deposit(
    data: DepositRequest,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = await service.deposit(
        user_id=current_user.id,
        amount=data.amount,
    )

    await service.uow.commit()
    await service.uow.refresh(transaction)

    return transaction


@router.post(
    "/withdraw",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def withdraw(
    data: WithdrawRequest,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = await service.withdraw(
        user_id=current_user.id,
        amount=data.amount,
    )

    await service.uow.commit()
    await service.uow.refresh(transaction)

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
    "/withdraw",
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def withdraw(
    data: WithdrawRequest,
    current_user: User = Depends(get_current_user),
    service: TransactionService = Depends(get_transaction_service),
):
    transaction = await service.withdraw(
        user_id=current_user.id,
        amount=data.amount,
    )

    await service.uow.commit()
    await service.uow.refresh(transaction)

    return transaction