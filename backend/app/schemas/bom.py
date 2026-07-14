from pydantic import BaseModel


class BomLinie(BaseModel):
    componenta_id: int
    nume: str
    categorie: str
    unitate_masura: str
    cantitate_totala: float
    pret_estimativ: float | None
    cost_total: float | None


class BomResponse(BaseModel):
    linii: list[BomLinie]
    cost_total_general: float
