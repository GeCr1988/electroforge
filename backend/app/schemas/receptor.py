from pydantic import BaseModel, ConfigDict

from app.models.enums import TipReceptor


class ReceptorCreate(BaseModel):
    nume: str
    tip: TipReceptor
    putere_nominala_w: float
    cos_phi: float = 1.0
    ku: float = 1.0
    ks: float = 1.0


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
