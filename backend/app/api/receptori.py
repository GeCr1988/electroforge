from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.ownership import get_circuit_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.receptor import Receptor
from app.models.user import User
from app.schemas.receptor import ReceptorCreate, ReceptorOut

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
