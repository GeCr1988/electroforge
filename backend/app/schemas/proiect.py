from pydantic import BaseModel, ConfigDict

from app.models.enums import TipCladire


class ProiectCreate(BaseModel):
    nume: str
    beneficiar: str
    tip_cladire: TipCladire
    adresa: str | None = None
    tensiune_alimentare: str = "230/400V"
    impedanta_retea_amonte_ohm: float | None = None


class ProiectUpdate(BaseModel):
    nume: str | None = None
    beneficiar: str | None = None
    tip_cladire: TipCladire | None = None
    adresa: str | None = None
    tensiune_alimentare: str | None = None
    impedanta_retea_amonte_ohm: float | None = None


class ProiectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nume: str
    beneficiar: str
    tip_cladire: TipCladire
    adresa: str | None
    tensiune_alimentare: str
    impedanta_retea_amonte_ohm: float | None
    owner_id: int
