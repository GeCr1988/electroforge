from sqlalchemy import Boolean, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import TipCircuit


class Circuit(Base):
    __tablename__ = "circuite"

    id: Mapped[int] = mapped_column(primary_key=True)
    tablou_id: Mapped[int] = mapped_column(ForeignKey("tablouri_electrice.id"), nullable=False)
    nume: Mapped[str] = mapped_column(String(255), nullable=False)
    tip: Mapped[TipCircuit] = mapped_column(Enum(TipCircuit, name="tip_circuit"), nullable=False)
    mod_pozare: Mapped[str] = mapped_column(String(100), nullable=False, default="B1")
    lungime_cablu_m: Mapped[float] = mapped_column(Float, nullable=False)
    sectiune_mm2: Mapped[float | None] = mapped_column(Float, nullable=True)
    curent_nominal_a: Mapped[float | None] = mapped_column(Float, nullable=True)

    protectie_selectata_id: Mapped[int | None] = mapped_column(
        ForeignKey("componente_catalog.id"), nullable=True
    )
    protectie_auto: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    cablu_selectat_id: Mapped[int | None] = mapped_column(ForeignKey("componente_catalog.id"), nullable=True)
    cablu_auto: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    tablou: Mapped["TabloElectric"] = relationship(back_populates="circuite")
    receptori: Mapped[list["Receptor"]] = relationship(back_populates="circuit", cascade="all, delete-orphan")
    rezultate: Mapped[list["CalculRezultat"]] = relationship(
        back_populates="circuit", cascade="all, delete-orphan"
    )
    protectie_selectata: Mapped["ComponentaCatalog | None"] = relationship(foreign_keys=[protectie_selectata_id])
    cablu_selectat: Mapped["ComponentaCatalog | None"] = relationship(foreign_keys=[cablu_selectat_id])
