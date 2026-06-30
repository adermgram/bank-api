from uuid import uuid4

from fastapi import HTTPException

from app.models.transaction import Transaction
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.enums.transaction import TransactionType


class TransactionService:
    def __init__(
        self,
        account_repo: AccountRepository,
        transaction_repo: TransactionRepository,
    ):
        self.account_repo = account_repo
        self.transaction_repo = transaction_repo

    async def deposit(self, user_id, amount):
        account = await self.account_repo.get_by_user_id(user_id)

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        before = account.balance
        after = before + amount

        account.balance = after

        transaction = Transaction(
            account_id=account.id,
            transaction_type=TransactionType.DEPOSIT,
            amount=amount,
            balance_before=before,
            balance_after=after,
            reference=str(uuid4()),
            description="Cash deposit",
        )

        self.transaction_repo.add(transaction)

        return transaction

    async def withdraw(self, user_id, amount):
        account = await self.account_repo.get_by_user_id(user_id)

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        if account.balance < amount:
            raise HTTPException(
                status_code=400,
                detail="Insufficient funds"
            )

        before = account.balance
        after = before - amount

        account.balance = after

        transaction = Transaction(
            account_id=account.id,
            transaction_type=TransactionType.WITHDRAWAL,
            amount=amount,
            balance_before=before,
            balance_after=after,
            reference=str(uuid4()),
            description="Cash withdrawal",
        )

        self.transaction_repo.add(transaction)

        return transaction

    async def get_user_transactions(self, user_id):
        account = await self.account_repo.get_by_user_id(user_id)

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Account not found"
            )

        return await self.transaction_repo.get_by_account_id(account.id)