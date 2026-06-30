import uuid
from datetime import datetime

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Numeric
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.database import Base

from sqlalchemy import Enum as SqlEnum

from app.enums.transaction import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id")
    )

    transaction_type: Mapped[TransactionType] = mapped_column(
        SqlEnum(TransactionType, name="transaction_type_enum"),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(15, 2)
    )

    balance_before: Mapped[float] = mapped_column(
        Numeric(15, 2)
    )

    balance_after: Mapped[float] = mapped_column(
        Numeric(15, 2)
    )

    reference: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    description: Mapped[str] = mapped_column(
        String(255)
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )