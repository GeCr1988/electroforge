from pydantic import BaseModel, ConfigDict

from app.models.enums import TipCircuit


class CircuitCreate(BaseModel):
    nume: str
    tip: TipCircuit
    mod_pozare: str = "B1"
    lungime_cablu_m: float


class CircuitOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tablou_id: int
    nume: str
    tip: TipCircuit
    mod_pozare: str
    lungime_cablu_m: float
    sectiune_mm2: float | None
    curent_nominal_a: float | None
