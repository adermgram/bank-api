from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.user_repository import UserRepository

from app.repositories.idempotency_repository import IdempotencyRepository


class UnitOfWork:
    def __init__(self, db: AsyncSession):
        self.db = db

        self.users = UserRepository(db)
        self.accounts = AccountRepository(db)
        self.transactions = TransactionRepository(db)
        self.idempotency = IdempotencyRepository(db)

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

    async def refresh(self, obj):
        await self.db.refresh(obj)