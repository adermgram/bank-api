import uuid
from datetime import datetime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import DateTime

from decimal import Decimal

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.enums.account import AccountStatus, AccountType

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    account_number: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=0
    )

    account_type: Mapped[AccountType] = mapped_column(
        SqlEnum(AccountType, name="account_type_enum"),
        default=AccountType.SAVINGS,
        nullable=False,
    )

    status: Mapped[AccountStatus] = mapped_column(
        SqlEnum(AccountStatus, name="account_status_enum"),
        default=AccountStatus.ACTIVE,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship("User")