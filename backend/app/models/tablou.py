from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TabloElectric(Base):
    __tablename__ = "tablouri_electrice"

    id: Mapped[int] = mapped_column(primary_key=True)
    proiect_id: Mapped[int] = mapped_column(ForeignKey("proiecte.id"), nullable=False)
    nume: Mapped[str] = mapped_column(String(255), nullable=False)
    putere_instalata: Mapped[float | None] = mapped_column(Float, nullable=True)
    putere_calcul: Mapped[float | None] = mapped_column(Float, nullable=True)

    proiect: Mapped["Proiect"] = relationship(back_populates="tablouri")
    circuite: Mapped[list["Circuit"]] = relationship(back_populates="tablou", cascade="all, delete-orphan")
