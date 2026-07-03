import random

from app.core.exceptions import AccountNotFoundError

from app.repositories.account_repository import AccountRepository
from app.db.unit_of_work import UnitOfWork


def generate_account_number() -> str:
    return str(random.randint(1000000000, 9999999999))


class AccountService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def get_my_account(self, user_id):
        account = await self.uow.accounts.get_by_user_id(user_id)

        if account is None:
            raise AccountNotFoundError("Account not found")

        return account

    async def get_account_by_number(self, account_number: str):
        account = await self.uow.accounts.get_by_account_number(account_number)

        if account is None:
            raise AccountNotFoundError("Account not found")

        return account