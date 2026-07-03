from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.db.unit_of_work import UnitOfWork


def get_uow(
    db: AsyncSession = Depends(get_db),
) -> UnitOfWork:
    return UnitOfWork(db)