from app.core.exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.models.account import Account
from app.repositories.user_repository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.services.account_service import generate_account_number
from app.db.unit_of_work import UnitOfWork

class AuthService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def register(self, full_name: str, email: str, password: str):
        existing_user = await self.uow.users.get_by_email(email)

        if existing_user:
            raise UserAlreadyExistsError("Email already registered")

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
        )

        self.uow.users.add(user)

        # Needed so user.id exists before creating account
        await self.uow.db.flush()

        account = Account(
            user_id=user.id,
            account_number=generate_account_number(),
        )

        self.uow.accounts.add(account)

        return user

    async def login(self, email: str, password: str):
        user = await self.uow.users.get_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        return create_access_token(subject=str(user.id))

    async def get_user_by_id(self, user_id):
        return await self.uow.users.get_by_id(user_id)