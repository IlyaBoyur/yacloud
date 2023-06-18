import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import func

from db import Base


class UserFile(Base):
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, index=True, default=func.now(), nullable=False
    )
    path: Mapped[str] = mapped_column(String(1024), default="", nullable=False)
    size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_downloadable: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="files")

    def __repr__(self):
        return f"File(id={self.id}, {self.name})"
