from fastapi import HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User
from app.models.account import Account
from app.repositories.user_repository import UserRepository
from app.repositories.account_repository import AccountRepository
from app.services.account_service import generate_account_number


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        account_repo: AccountRepository,
    ):
        self.user_repo = user_repo
        self.account_repo = account_repo

    async def register(self, full_name: str, email: str, password: str):
        existing_user = await self.user_repo.get_by_email(email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
        )

        self.user_repo.add(user)

        # Needed so user.id exists before creating account
        await self.user_repo.db.flush()

        account = Account(
            user_id=user.id,
            account_number=generate_account_number(),
        )

        self.account_repo.add(account)

        return user

    async def login(self, email: str, password: str):
        user = await self.user_repo.get_by_email(email)

        if user is None or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        return create_access_token(subject=str(user.id))

    async def get_user_by_id(self, user_id):
        return await self.user_repo.get_by_id(user_id)