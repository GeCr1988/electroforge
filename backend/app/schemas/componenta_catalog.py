from pydantic import BaseModel, ConfigDict

from app.models.enums import CategorieComponenta


class ComponentaCatalogCreate(BaseModel):
    categorie: CategorieComponenta
    nume: str
    producator: str | None = None
    cod_produs: str | None = None
    specificatii: dict = {}
    pret_estimativ: float | None = None
    unitate_masura: str = "buc"
    simbol_ref: str | None = None


class ComponentaCatalogUpdate(BaseModel):
    categorie: CategorieComponenta | None = None
    nume: str | None = None
    producator: str | None = None
    cod_produs: str | None = None
    specificatii: dict | None = None
    pret_estimativ: float | None = None
    unitate_masura: str | None = None
    simbol_ref: str | None = None


class ComponentaCatalogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    categorie: CategorieComponenta
    nume: str
    producator: str | None
    cod_produs: str | None
    specificatii: dict
    pret_estimativ: float | None
    unitate_masura: str
    simbol_ref: str | None
