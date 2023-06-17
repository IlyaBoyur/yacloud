from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import func

from db import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    created_at: Mapped[datetime] = mapped_column(
        DateTime, index=True, default=func.now(), nullable=False
    )

    files: Mapped[list["UserFile"]] = relationship(
        back_populates="user", cascade="all, delete"
    )

    def __repr__(self):
        return f"User(id={self.id}, {self.email})"
