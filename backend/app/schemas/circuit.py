from pydantic import BaseModel, ConfigDict

from app.models.enums import TipCircuit


class CircuitCreate(BaseModel):
    nume: str
    tip: TipCircuit
    mod_pozare: str = "B1"
    lungime_cablu_m: float


class CircuitUpdate(BaseModel):
    nume: str | None = None
    tip: TipCircuit | None = None
    mod_pozare: str | None = None
    lungime_cablu_m: float | None = None
    protectie_selectata_id: int | None = None
    cablu_selectat_id: int | None = None


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
    protectie_selectata_id: int | None
    protectie_auto: bool
    cablu_selectat_id: int | None
    cablu_auto: bool
