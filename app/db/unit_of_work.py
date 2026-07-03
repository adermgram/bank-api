from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository


class UnitOfWork:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.users = UserRepository(db)
        self.accounts = AccountRepository(db)
        self.transactions = TransactionRepository(db)

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, obj):
        await self.db.refresh(obj)