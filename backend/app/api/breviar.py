from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.bom import _colecteaza_intrari_bom
from app.api.ownership import get_proiect_or_404
from app.auth.deps import get_current_user
from app.bom.aggregator import agrega_bom
from app.db.session import get_db
from app.models.calcul_rezultat import CalculRezultat
from app.models.componenta_catalog import ComponentaCatalog
from app.models.tablou import TabloElectric
from app.models.user import User
from app.reports.breviar import genereaza_html_breviar, genereaza_pdf_breviar
from app.schema_engine.monofilara import genereaza_schema_monofilara

router = APIRouter(tags=["breviar"])


def _construieste_context_breviar(db: Session, proiect) -> tuple[dict, list[dict], str, list[dict], float]:
    proiect_dict = {
        "nume": proiect.nume,
        "beneficiar": proiect.beneficiar,
        "tip_cladire": proiect.tip_cladire.value,
        "tensiune_alimentare": proiect.tensiune_alimentare,
        "adresa": proiect.adresa,
    }

    tablouri_orm = db.query(TabloElectric).filter(TabloElectric.proiect_id == proiect.id).all()
    tablouri: list[dict] = []
    schema_tablouri: list[dict] = []

    for tablou in tablouri_orm:
        circuite = []
        schema_circuite = []
        for circuit in tablou.circuite:
            protectie_nume = None
            if circuit.protectie_selectata_id is not None:
                protectie = db.get(ComponentaCatalog, circuit.protectie_selectata_id)
                protectie_nume = protectie.nume if protectie else None

            rezultate = (
                db.query(CalculRezultat).filter(CalculRezultat.circuit_id == circuit.id).all()
            )
            circuite.append(
                {
                    "nume": circuit.nume,
                    "tip": circuit.tip.value,
                    "mod_pozare": circuit.mod_pozare,
                    "lungime_cablu_m": circuit.lungime_cablu_m,
                    "receptori": [
                        {
                            "nume": r.nume,
                            "tip": r.tip.value,
                            "putere_nominala_w": r.putere_nominala_w,
                            "cos_phi": r.cos_phi,
                            "ku": r.ku,
                            "ks": r.ks,
                        }
                        for r in circuit.receptori
                    ],
                    "rezultate": [
                        {
                            "tip_calcul": rez.tip_calcul,
                            "valoare": rez.valoare,
                            "unitate": rez.unitate,
                            "standard_referinta": rez.standard_referinta,
                            "status_conformitate": rez.status_conformitate.value,
                        }
                        for rez in rezultate
                    ],
                }
            )
            schema_circuite.append(
                {"nume": circuit.nume, "sectiune_mm2": circuit.sectiune_mm2, "protectie_nume": protectie_nume}
            )

        tablouri.append(
            {
                "nume": tablou.nume,
                "putere_instalata": tablou.putere_instalata,
                "putere_calcul": tablou.putere_calcul,
                "circuite": circuite,
            }
        )
        schema_tablouri.append({"nume": tablou.nume, "circuite": schema_circuite})

    schema_svg = genereaza_schema_monofilara(
        nume_proiect=proiect.nume, tensiune_alimentare=proiect.tensiune_alimentare, tablouri=schema_tablouri
    )

    intrari_bom = _colecteaza_intrari_bom(db, proiect.id)
    bom_linii, bom_cost_total = agrega_bom(intrari_bom)

    return proiect_dict, tablouri, schema_svg, bom_linii, bom_cost_total


@router.get("/proiecte/{proiect_id}/breviar.pdf")
def breviar_pdf(proiect_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    proiect = get_proiect_or_404(db, proiect_id, user)
    proiect_dict, tablouri, schema_svg, bom_linii, bom_cost_total = _construieste_context_breviar(db, proiect)

    html = genereaza_html_breviar(proiect_dict, tablouri, schema_svg, bom_linii, bom_cost_total)
    pdf_bytes = genereaza_pdf_breviar(html)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="breviar-proiect-{proiect_id}.pdf"'},
    )
