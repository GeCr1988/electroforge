from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.ownership import get_componenta_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.componenta_catalog import ComponentaCatalog
from app.models.enums import CategorieComponenta
from app.models.user import User
from app.schemas.componenta_catalog import ComponentaCatalogCreate, ComponentaCatalogOut, ComponentaCatalogUpdate

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.post("", response_model=ComponentaCatalogOut, status_code=status.HTTP_201_CREATED)
def creeaza_componenta(
    payload: ComponentaCatalogCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    componenta = ComponentaCatalog(**payload.model_dump(), owner_id=user.id)
    db.add(componenta)
    db.commit()
    db.refresh(componenta)
    return componenta


@router.get("", response_model=list[ComponentaCatalogOut])
def listeaza_catalog(
    categorie: CategorieComponenta | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    query = db.query(ComponentaCatalog).filter(ComponentaCatalog.owner_id == user.id)
    if categorie is not None:
        query = query.filter(ComponentaCatalog.categorie == categorie)
    return query.all()


@router.get("/{componenta_id}", response_model=ComponentaCatalogOut)
def obtine_componenta(
    componenta_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return get_componenta_or_404(db, componenta_id, user)


@router.patch("/{componenta_id}", response_model=ComponentaCatalogOut)
def actualizeaza_componenta(
    componenta_id: int,
    payload: ComponentaCatalogUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    componenta = get_componenta_or_404(db, componenta_id, user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(componenta, key, value)
    db.commit()
    db.refresh(componenta)
    return componenta


@router.delete("/{componenta_id}", status_code=status.HTTP_204_NO_CONTENT)
def sterge_componenta(
    componenta_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    componenta = get_componenta_or_404(db, componenta_id, user)
    db.delete(componenta)
    db.commit()
