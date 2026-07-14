from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.ownership import NOT_FOUND, get_circuit_or_404, get_receptor_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.receptor import Receptor
from app.models.user import User
from app.schemas.receptor import ReceptorCreate, ReceptorOut, ReceptorUpdate

router = APIRouter(tags=["receptori"])


@router.post("/circuite/{circuit_id}/receptori", response_model=ReceptorOut, status_code=status.HTTP_201_CREATED)
def creeaza_receptor(
    circuit_id: int,
    payload: ReceptorCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    circuit = get_circuit_or_404(db, circuit_id, user)
    receptor = Receptor(circuit_id=circuit.id, **payload.model_dump())
    db.add(receptor)
    db.commit()
    db.refresh(receptor)
    return receptor


@router.get("/circuite/{circuit_id}/receptori", response_model=list[ReceptorOut])
def listeaza_receptori(
    circuit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    circuit = get_circuit_or_404(db, circuit_id, user)
    return db.query(Receptor).filter(Receptor.circuit_id == circuit.id).all()


@router.patch("/circuite/{circuit_id}/receptori/{receptor_id}", response_model=ReceptorOut)
def actualizeaza_receptor(
    circuit_id: int,
    receptor_id: int,
    payload: ReceptorUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    receptor = get_receptor_or_404(db, receptor_id, user)
    if receptor.circuit_id != circuit_id:
        raise NOT_FOUND
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(receptor, key, value)
    db.commit()
    db.refresh(receptor)
    return receptor


@router.delete("/circuite/{circuit_id}/receptori/{receptor_id}", status_code=status.HTTP_204_NO_CONTENT)
def sterge_receptor(
    circuit_id: int,
    receptor_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    receptor = get_receptor_or_404(db, receptor_id, user)
    if receptor.circuit_id != circuit_id:
        raise NOT_FOUND
    db.delete(receptor)
    db.commit()
