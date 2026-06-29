import random

from fastapi import HTTPException

from app.repositories.account_repository import AccountRepository


def generate_account_number() -> str:
    return str(random.randint(1000000000, 9999999999))


class AccountService:
    def __init__(self, account_repo: AccountRepository):
        self.account_repo = account_repo

    async def get_my_account(self, user_id):
        account = await self.account_repo.get_by_user_id(user_id)

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found",
            )

        return account

    async def get_account_by_number(self, account_number: str):
        account = await self.account_repo.get_by_account_number(account_number)

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found",
            )

        return account