from pydantic import BaseModel, ConfigDict

from app.models.enums import TipCladire


class ProiectCreate(BaseModel):
    nume: str
    beneficiar: str
    tip_cladire: TipCladire
    adresa: str | None = None
    tensiune_alimentare: str = "230/400V"


class ProiectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nume: str
    beneficiar: str
    tip_cladire: TipCladire
    adresa: str | None
    tensiune_alimentare: str
    owner_id: int
