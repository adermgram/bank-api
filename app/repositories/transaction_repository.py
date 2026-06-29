from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def add(self, transaction: Transaction):
        self.db.add(transaction)

    async def get_by_account_id(self, account_id):
        result = await self.db.execute(
            select(Transaction)
            .where(Transaction.account_id == account_id)
            .order_by(Transaction.created_at.desc())
        )

        return result.scalars().all()