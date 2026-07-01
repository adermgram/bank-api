from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from sqlalchemy import select


class AccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id):
        result = await self.db.execute(
            select(Account).where(Account.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_user_id_for_update(self, user_id):
        result = await self.db.execute(
            select(Account)
            .where(Account.user_id == user_id)
            .with_for_update()
        )

        return result.scalar_one_or_none()

    async def get_by_account_number(self, account_number: str):
        result = await self.db.execute(
            select(Account).where(Account.account_number == account_number)
        )
        return result.scalar_one_or_none()
    
    async def get_by_account_number_for_update(
        self,
        account_number: str,
    ):
        result = await self.db.execute(
            select(Account)
            .where(Account.account_number == account_number)
            .with_for_update()
        )

        return result.scalar_one_or_none()
    
    def add(self, account: Account):
        self.db.add(account)