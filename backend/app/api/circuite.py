from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.ownership import get_circuit_or_404, get_tablou_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.circuit import Circuit
from app.models.user import User
from app.schemas.circuit import CircuitCreate, CircuitOut

router = APIRouter(tags=["circuite"])


@router.post("/tablouri/{tablou_id}/circuite", response_model=CircuitOut, status_code=status.HTTP_201_CREATED)
def creeaza_circuit(
    tablou_id: int,
    payload: CircuitCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    tablou = get_tablou_or_404(db, tablou_id, user)
    circuit = Circuit(tablou_id=tablou.id, **payload.model_dump())
    db.add(circuit)
    db.commit()
    db.refresh(circuit)
    return circuit


@router.get("/tablouri/{tablou_id}/circuite", response_model=list[CircuitOut])
def listeaza_circuite(
    tablou_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    tablou = get_tablou_or_404(db, tablou_id, user)
    return db.query(Circuit).filter(Circuit.tablou_id == tablou.id).all()


@router.get("/circuite/{circuit_id}", response_model=CircuitOut)
def obtine_circuit(circuit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_circuit_or_404(db, circuit_id, user)
