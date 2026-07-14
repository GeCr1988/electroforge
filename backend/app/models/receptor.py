from sqlalchemy import Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import TipReceptor


class Receptor(Base):
    __tablename__ = "receptori"

    id: Mapped[int] = mapped_column(primary_key=True)
    circuit_id: Mapped[int] = mapped_column(ForeignKey("circuite.id"), nullable=False)
    nume: Mapped[str] = mapped_column(String(255), nullable=False)
    tip: Mapped[TipReceptor] = mapped_column(Enum(TipReceptor, name="tip_receptor"), nullable=False)
    putere_nominala_w: Mapped[float] = mapped_column(Float, nullable=False)
    cos_phi: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    ku: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    ks: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    componenta_id: Mapped[int | None] = mapped_column(ForeignKey("componente_catalog.id"), nullable=True)
    cantitate: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)

    circuit: Mapped["Circuit"] = relationship(back_populates="receptori")
    componenta: Mapped["ComponentaCatalog | None"] = relationship()
