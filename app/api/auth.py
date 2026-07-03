from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.repositories.account_repository import AccountRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from app.services.auth_service import AuthService

from app.db.dependencies import get_uow
from app.db.unit_of_work import UnitOfWork


router = APIRouter(prefix="/auth", tags=["Auth"])
bearer_scheme = HTTPBearer()


def get_auth_service(
    uow: UnitOfWork = Depends(get_uow),
) -> AuthService:
    return AuthService(uow)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    data: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.register(
        full_name=data.full_name,
        email=data.email,
        password=data.password,
    )

    await service.uow.commit()
    await service.uow.refresh(user)

    return user


@router.post("/login", response_model=TokenResponse)
async def login_user(
    data: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):
    token = await service.login(
        email=data.email,
        password=data.password,
    )

    return TokenResponse(access_token=token)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user