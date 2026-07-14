from pydantic import BaseModel, ConfigDict

from app.models.enums import TipReceptor


class ReceptorCreate(BaseModel):
    nume: str
    tip: TipReceptor
    putere_nominala_w: float
    cos_phi: float = 1.0
    ku: float = 1.0
    ks: float = 1.0


class ReceptorUpdate(BaseModel):
    nume: str | None = None
    tip: TipReceptor | None = None
    putere_nominala_w: float | None = None
    cos_phi: float | None = None
    ku: float | None = None
    ks: float | None = None
    componenta_id: int | None = None
    cantitate: float | None = None


class ReceptorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    circuit_id: int
    nume: str
    tip: TipReceptor
    putere_nominala_w: float
    cos_phi: float
    ku: float
    ks: float
    componenta_id: int | None
    cantitate: float
