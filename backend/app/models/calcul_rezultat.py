from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import StatusConformitate


class CalculRezultat(Base):
    __tablename__ = "calcul_rezultate"

    id: Mapped[int] = mapped_column(primary_key=True)
    circuit_id: Mapped[int] = mapped_column(ForeignKey("circuite.id"), nullable=False)
    tip_calcul: Mapped[str] = mapped_column(String(100), nullable=False)
    valoare: Mapped[float] = mapped_column(Float, nullable=False)
    unitate: Mapped[str] = mapped_column(String(50), nullable=False, default="")
    standard_referinta: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    status_conformitate: Mapped[StatusConformitate] = mapped_column(
        Enum(StatusConformitate, name="status_conformitate"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    circuit: Mapped["Circuit"] = relationship(back_populates="rezultate")
