from sqlalchemy import JSON, Enum, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.enums import CategorieComponenta


class ComponentaCatalog(Base):
    __tablename__ = "componente_catalog"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    categorie: Mapped[CategorieComponenta] = mapped_column(
        Enum(CategorieComponenta, name="categorie_componenta"), nullable=False
    )
    nume: Mapped[str] = mapped_column(String(255), nullable=False)
    producator: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cod_produs: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specificatii: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    pret_estimativ: Mapped[float | None] = mapped_column(Float, nullable=True)
    unitate_masura: Mapped[str] = mapped_column(String(50), nullable=False, default="buc")
    simbol_ref: Mapped[str | None] = mapped_column(String(100), nullable=True)

    owner: Mapped["User"] = relationship()
