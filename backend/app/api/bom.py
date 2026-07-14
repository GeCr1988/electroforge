import csv
import io

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.ownership import get_proiect_or_404
from app.auth.deps import get_current_user
from app.bom.aggregator import agrega_bom
from app.db.session import get_db
from app.models.componenta_catalog import ComponentaCatalog
from app.models.tablou import TabloElectric
from app.models.user import User
from app.schemas.bom import BomResponse

router = APIRouter(tags=["bom"])


def _colecteaza_intrari_bom(db: Session, proiect_id: int) -> list[dict]:
    intrari: list[dict] = []
    tablouri = db.query(TabloElectric).filter(TabloElectric.proiect_id == proiect_id).all()

    for tablou in tablouri:
        for circuit in tablou.circuite:
            if circuit.cablu_selectat_id is not None:
                componenta = db.get(ComponentaCatalog, circuit.cablu_selectat_id)
                if componenta is not None:
                    intrari.append(
                        {
                            "componenta_id": componenta.id,
                            "nume": componenta.nume,
                            "categorie": componenta.categorie.value,
                            "unitate_masura": componenta.unitate_masura,
                            "cantitate": circuit.lungime_cablu_m,
                            "pret_estimativ": componenta.pret_estimativ,
                        }
                    )
            if circuit.protectie_selectata_id is not None:
                componenta = db.get(ComponentaCatalog, circuit.protectie_selectata_id)
                if componenta is not None:
                    intrari.append(
                        {
                            "componenta_id": componenta.id,
                            "nume": componenta.nume,
                            "categorie": componenta.categorie.value,
                            "unitate_masura": componenta.unitate_masura,
                            "cantitate": 1,
                            "pret_estimativ": componenta.pret_estimativ,
                        }
                    )
            for receptor in circuit.receptori:
                if receptor.componenta_id is not None:
                    componenta = db.get(ComponentaCatalog, receptor.componenta_id)
                    if componenta is not None:
                        intrari.append(
                            {
                                "componenta_id": componenta.id,
                                "nume": componenta.nume,
                                "categorie": componenta.categorie.value,
                                "unitate_masura": componenta.unitate_masura,
                                "cantitate": receptor.cantitate,
                                "pret_estimativ": componenta.pret_estimativ,
                            }
                        )
    return intrari


@router.get("/proiecte/{proiect_id}/bom", response_model=BomResponse)
def obtine_bom(proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    proiect = get_proiect_or_404(db, proiect_id, user)
    intrari = _colecteaza_intrari_bom(db, proiect.id)
    linii, total = agrega_bom(intrari)
    return BomResponse(linii=linii, cost_total_general=total)


@router.get("/proiecte/{proiect_id}/bom.csv")
def obtine_bom_csv(proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    proiect = get_proiect_or_404(db, proiect_id, user)
    intrari = _colecteaza_intrari_bom(db, proiect.id)
    linii, total = agrega_bom(intrari)

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Denumire", "Categorie", "Cantitate", "Unitate", "Pret estimativ", "Cost total"])
    for linie in linii:
        writer.writerow(
            [
                linie["nume"],
                linie["categorie"],
                linie["cantitate_totala"],
                linie["unitate_masura"],
                linie["pret_estimativ"] if linie["pret_estimativ"] is not None else "",
                linie["cost_total"] if linie["cost_total"] is not None else "",
            ]
        )
    writer.writerow([])
    writer.writerow(["", "", "", "", "Total general", total])

    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="bom-proiect-{proiect_id}.csv"'},
    )
