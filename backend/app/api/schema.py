from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.ownership import get_proiect_or_404
from app.auth.deps import get_current_user
from app.db.session import get_db
from app.models.componenta_catalog import ComponentaCatalog
from app.models.tablou import TabloElectric
from app.models.user import User
from app.schema_engine.monofilara import genereaza_schema_monofilara

router = APIRouter(tags=["schema"])


@router.get("/proiecte/{proiect_id}/schema-monofilara.svg")
def schema_monofilara(proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    proiect = get_proiect_or_404(db, proiect_id, user)
    tablouri_orm = db.query(TabloElectric).filter(TabloElectric.proiect_id == proiect.id).all()

    tablouri: list[dict] = []
    for tablou in tablouri_orm:
        circuite = []
        for circuit in tablou.circuite:
            protectie_nume = None
            if circuit.protectie_selectata_id is not None:
                protectie = db.get(ComponentaCatalog, circuit.protectie_selectata_id)
                protectie_nume = protectie.nume if protectie else None
            circuite.append(
                {
                    "nume": circuit.nume,
                    "sectiune_mm2": circuit.sectiune_mm2,
                    "protectie_nume": protectie_nume,
                }
            )
        tablouri.append({"nume": tablou.nume, "circuite": circuite})

    svg = genereaza_schema_monofilara(
        nume_proiect=proiect.nume, tensiune_alimentare=proiect.tensiune_alimentare, tablouri=tablouri
    )
    return Response(content=svg, media_type="image/svg+xml")
