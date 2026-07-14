from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.ownership import get_proiect_or_404, get_tablou_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.tablou import TabloElectric
from app.models.user import User
from app.schemas.tablou import TabloCreate, TabloOut, TabloUpdate

router = APIRouter(tags=["tablouri"])


@router.post("/proiecte/{proiect_id}/tablouri", response_model=TabloOut, status_code=status.HTTP_201_CREATED)
def creeaza_tablou(
    proiect_id: int,
    payload: TabloCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    proiect = get_proiect_or_404(db, proiect_id, user)
    tablou = TabloElectric(nume=payload.nume, proiect_id=proiect.id)
    db.add(tablou)
    db.commit()
    db.refresh(tablou)
    return tablou


@router.get("/proiecte/{proiect_id}/tablouri", response_model=list[TabloOut])
def listeaza_tablouri(
    proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    proiect = get_proiect_or_404(db, proiect_id, user)
    return db.query(TabloElectric).filter(TabloElectric.proiect_id == proiect.id).all()


@router.get("/tablouri/{tablou_id}", response_model=TabloOut)
def obtine_tablou(tablou_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_tablou_or_404(db, tablou_id, user)


@router.patch("/tablouri/{tablou_id}", response_model=TabloOut)
def actualizeaza_tablou(
    tablou_id: int,
    payload: TabloUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tablou = get_tablou_or_404(db, tablou_id, user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tablou, key, value)
    db.commit()
    db.refresh(tablou)
    return tablou


@router.delete("/tablouri/{tablou_id}", status_code=status.HTTP_204_NO_CONTENT)
def sterge_tablou(tablou_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    tablou = get_tablou_or_404(db, tablou_id, user)
    db.delete(tablou)
    db.commit()
