from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.ownership import get_proiect_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.proiect import Proiect
from app.models.user import User
from app.schemas.proiect import ProiectCreate, ProiectOut, ProiectUpdate

router = APIRouter(prefix="/proiecte", tags=["proiecte"])


@router.post("", response_model=ProiectOut, status_code=status.HTTP_201_CREATED)
def creeaza_proiect(
    payload: ProiectCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    proiect = Proiect(**payload.model_dump(), owner_id=user.id)
    db.add(proiect)
    db.commit()
    db.refresh(proiect)
    return proiect


@router.get("", response_model=list[ProiectOut])
def listeaza_proiecte(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Proiect).filter(Proiect.owner_id == user.id).all()


@router.get("/{proiect_id}", response_model=ProiectOut)
def obtine_proiect(proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_proiect_or_404(db, proiect_id, user)


@router.patch("/{proiect_id}", response_model=ProiectOut)
def actualizeaza_proiect(
    proiect_id: int,
    payload: ProiectUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    proiect = get_proiect_or_404(db, proiect_id, user)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(proiect, key, value)
    db.commit()
    db.refresh(proiect)
    return proiect


@router.delete("/{proiect_id}", status_code=status.HTTP_204_NO_CONTENT)
def sterge_proiect(proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    proiect = get_proiect_or_404(db, proiect_id, user)
    db.delete(proiect)
    db.commit()
