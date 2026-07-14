from pydantic import BaseModel, ConfigDict


class TabloCreate(BaseModel):
    nume: str


class TabloOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    proiect_id: int
    nume: str
    putere_instalata: float | None
    putere_calcul: float | None
