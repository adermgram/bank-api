from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.schemas.account import AccountResponse
from app.services.account_service import AccountService


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"],
)


def get_account_service(
    db: AsyncSession = Depends(get_db),
) -> AccountService:
    account_repo = AccountRepository(db)
    return AccountService(account_repo)


@router.get("/me", response_model=AccountResponse)
async def get_my_account(
    current_user: User = Depends(get_current_user),
    service: AccountService = Depends(get_account_service),
):
    return await service.get_my_account(current_user.id)


@router.get("/{account_number}", response_model=AccountResponse)
async def get_account_by_number(
    account_number: str,
    service: AccountService = Depends(get_account_service),
):
    return await service.get_account_by_number(account_number)