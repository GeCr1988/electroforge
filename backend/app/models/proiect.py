from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import TipCladire


class Proiect(Base):
    __tablename__ = "proiecte"

    id: Mapped[int] = mapped_column(primary_key=True)
    nume: Mapped[str] = mapped_column(String(255), nullable=False)
    beneficiar: Mapped[str] = mapped_column(String(255), nullable=False)
    tip_cladire: Mapped[TipCladire] = mapped_column(Enum(TipCladire, name="tip_cladire"), nullable=False)
    adresa: Mapped[str] = mapped_column(String(500), nullable=True)
    tensiune_alimentare: Mapped[str] = mapped_column(String(50), nullable=False, default="230/400V")
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    owner: Mapped["User"] = relationship(back_populates="proiecte")
    tablouri: Mapped[list["TabloElectric"]] = relationship(
        back_populates="proiect", cascade="all, delete-orphan"
    )
