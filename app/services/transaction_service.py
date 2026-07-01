from uuid import uuid4

from app.core.exceptions import AccountNotFoundError, InsufficientFundsError

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

        self.transaction_repo.add(transaction)

        return transaction

    async def withdraw(self, user_id, amount):
        account = await self.account_repo.get_by_user_id(user_id)

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

        self.transaction_repo.add(transaction)

        return transaction

    async def get_user_transactions(self, user_id):
        account = await self.account_repo.get_by_user_id(user_id)

        if account is None:
            raise AccountNotFoundError("Account not found")

        return await self.transaction_repo.get_by_account_id(account.id)


    async def transfer(self, user_id, to_account_number: str, amount, description: str):
        sender = await self.account_repo.get_by_user_id_for_update(user_id)

        if sender is None:
            raise AccountNotFoundError("Sender account not found")

        receiver = await self.account_repo.get_by_account_number_for_update(to_account_number)

        if receiver is None:
            raise AccountNotFoundError("Receiver account not found")

        if sender.id == receiver.id:
            raise InsufficientFundsError("You cannot transfer to your own account")

        if sender.balance < amount:
            raise InsufficientFundsError("Insufficient funds")

        reference = f"TXN-{uuid4()}"

        sender_before = sender.balance
        sender_after = sender_before - amount

        receiver_before = receiver.balance
        receiver_after = receiver_before + amount

        sender.balance = sender_after
        receiver.balance = receiver_after

        sender_tx = Transaction(
            account_id=sender.id,
            transaction_type=TransactionType.TRANSFER_OUT,
            amount=amount,
            balance_before=sender_before,
            balance_after=sender_after,
            reference=f"{reference}-OUT",
            description=description,
        )

        receiver_tx = Transaction(
            account_id=receiver.id,
            transaction_type=TransactionType.TRANSFER_IN,
            amount=amount,
            balance_before=receiver_before,
            balance_after=receiver_after,
            reference=f"{reference}-IN",
            description=description,
        )

        self.transaction_repo.add(sender_tx)
        self.transaction_repo.add(receiver_tx)

        return sender_tx