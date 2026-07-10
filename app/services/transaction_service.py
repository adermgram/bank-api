from decimal import Decimal
from uuid import uuid4

from app.core.exceptions import AccountNotFoundError, InsufficientFundsError, DuplicateRequestError

from app.models.transaction import Transaction
from app.models.idempotency_key import IdempotencyKey
from app.repositories.account_repository import AccountRepository
from app.repositories.transaction_repository import TransactionRepository
from app.enums.transaction import TransactionType

from app.db.unit_of_work import UnitOfWork


class TransactionService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def deposit(self, user_id, amount):
        account = await self.uow.accounts.get_by_user_id(user_id)

        if account is None:
            raise AccountNotFoundError("Account not found")

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

        self.uow.transactions.add(transaction)

        return transaction

    async def withdraw(self, user_id, amount):
        account = await self.uow.accounts.get_by_user_id(user_id)

        if account is None:
            raise AccountNotFoundError("Account not found")

        if account.balance < amount:
            raise InsufficientFundsError("Insufficient funds")

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

        self.uow.transactions.add(transaction)

        return transaction

    async def get_user_transactions(self, user_id):
        account = await self.uow.accounts.get_by_user_id(user_id)

        if account is None:
            raise AccountNotFoundError("Account not found")

        return await self.uow.transactions.get_by_account_id(account.id)


    async def transfer(
        self,
        user_id,
        to_account_number: str,
        amount: Decimal,
        description: str,
        idempotency_key: str,
    ):
        # Check idempotency
        existing_request = await self.uow.idempotency.get(idempotency_key)

        if existing_request:
            raise DuplicateRequestError("Duplicate request")

        # Lock sender
        sender = await self.uow.accounts.get_by_user_id_for_update(user_id)

        if sender is None:
            raise AccountNotFoundError("Sender account not found")

        # Lock receiver
        receiver = await self.uow.accounts.get_by_account_number_for_update(
            to_account_number
        )

        if receiver is None:
            raise AccountNotFoundError("Receiver account not found")

        if sender.id == receiver.id:
            raise InsufficientFundsError(
                "You cannot transfer to your own account"
            )

        if sender.balance < amount:
            raise InsufficientFundsError("Insufficient funds")

        reference = f"TXN-{uuid4()}"

        sender_before = sender.balance
        receiver_before = receiver.balance

        sender.balance -= amount
        receiver.balance += amount

        sender_tx = Transaction(
            account_id=sender.id,
            transaction_type=TransactionType.TRANSFER_OUT,
            amount=amount,
            balance_before=sender_before,
            balance_after=sender.balance,
            reference=f"{reference}-OUT",
            description=description,
        )

        receiver_tx = Transaction(
            account_id=receiver.id,
            transaction_type=TransactionType.TRANSFER_IN,
            amount=amount,
            balance_before=receiver_before,
            balance_after=receiver.balance,
            reference=f"{reference}-IN",
            description=description,
        )

        self.uow.transactions.add(sender_tx)
        self.uow.transactions.add(receiver_tx)

        # Save idempotency record
        self.uow.idempotency.add(
            IdempotencyKey(
                key=idempotency_key,
                user_id=user_id,
                endpoint="/transactions/transfer",
            )
        )

        return sender_tx