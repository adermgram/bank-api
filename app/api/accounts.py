from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.account import Account
from app.models.user import User

from app.api.auth import get_current_user

from app.schemas.account import AccountResponse


router = APIRouter(
    prefix="/accounts",
    tags=["Accounts"]
)


@router.get(
    "/me",
    response_model=AccountResponse
)
async def get_my_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Account).where(
            Account.user_id == current_user.id
        )
    )

    account = result.scalar_one()

    return account