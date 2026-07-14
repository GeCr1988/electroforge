from pydantic import BaseModel, ConfigDict

from app.models.enums import StatusConformitate


class CalculRezultatOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    circuit_id: int
    tip_calcul: str
    valoare: float
    unitate: str
    standard_referinta: str
    status_conformitate: StatusConformitate
