from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.circuit import Circuit
from app.models.proiect import Proiect
from app.models.tablou import TabloElectric
from app.models.user import User

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resursă inexistentă")


def get_proiect_or_404(db: Session, proiect_id: int, user: User) -> Proiect:
    proiect = db.query(Proiect).filter(Proiect.id == proiect_id, Proiect.owner_id == user.id).first()
    if proiect is None:
        raise NOT_FOUND
    return proiect


def get_tablou_or_404(db: Session, tablou_id: int, user: User) -> TabloElectric:
    tablou = (
        db.query(TabloElectric)
        .join(Proiect, TabloElectric.proiect_id == Proiect.id)
        .filter(TabloElectric.id == tablou_id, Proiect.owner_id == user.id)
        .first()
    )
    if tablou is None:
        raise NOT_FOUND
    return tablou


def get_circuit_or_404(db: Session, circuit_id: int, user: User) -> Circuit:
    circuit = (
        db.query(Circuit)
        .join(TabloElectric, Circuit.tablou_id == TabloElectric.id)
        .join(Proiect, TabloElectric.proiect_id == Proiect.id)
        .filter(Circuit.id == circuit_id, Proiect.owner_id == user.id)
        .first()
    )
    if circuit is None:
        raise NOT_FOUND
    return circuit
