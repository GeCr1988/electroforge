from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.ownership import get_circuit_or_404
from app.auth.deps import get_current_user
from app.calc_engine.curent import calc_curent_monofazat, calc_curent_trifazat
from app.calc_engine.putere import calc_putere_calcul, calc_putere_instalata
from app.calc_engine.sectiune_cablu import alege_sectiune_cablu
from app.db.session import get_db
from app.models.calcul_rezultat import CalculRezultat
from app.models.circuit import Circuit
from app.models.enums import StatusConformitate
from app.models.receptor import Receptor
from app.models.user import User
from app.schemas.calcul_rezultat import CalculRezultatOut

router = APIRouter(tags=["calcule"])

TENSIUNE_MONOFAZAT_V = 230
TENSIUNE_TRIFAZAT_V = 400


def _tip_utilizare(receptori: list[Receptor]) -> str:
    if receptori and all(r.tip.value == "iluminat" for r in receptori):
        return "iluminat"
    return "forta"


def _cos_phi_efectiv(receptori: list[Receptor]) -> float:
    putere_totala = sum(r.putere_nominala_w for r in receptori)
    if putere_totala == 0:
        return 1.0
    return sum(r.putere_nominala_w * r.cos_phi for r in receptori) / putere_totala


def _pi_pc_circuit(receptori: list[Receptor]) -> tuple[float, float]:
    pi = calc_putere_instalata([r.putere_nominala_w for r in receptori])
    # Ks e definit per receptor în acest MVP (nu la nivel de circuit/tablou);
    # se combină cu Ku înainte de a apela motorul (Pc = Σ p·ku·ks).
    pc = calc_putere_calcul([(r.putere_nominala_w, r.ku * r.ks) for r in receptori], ks=1.0)
    return pi, pc


@router.post("/circuite/{circuit_id}/calculeaza", response_model=list[CalculRezultatOut])
def calculeaza_circuit(circuit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    circuit = get_circuit_or_404(db, circuit_id, user)
    receptori = db.query(Receptor).filter(Receptor.circuit_id == circuit.id).all()

    pi, pc = _pi_pc_circuit(receptori)
    cos_phi_ef = _cos_phi_efectiv(receptori)
    tensiune_v = TENSIUNE_MONOFAZAT_V if circuit.tip.value == "monofazat" else TENSIUNE_TRIFAZAT_V

    if circuit.tip.value == "monofazat":
        curent_nominal = calc_curent_monofazat(pc, tensiune_v=tensiune_v, cos_phi=cos_phi_ef)
    else:
        curent_nominal = calc_curent_trifazat(pc, tensiune_v=tensiune_v, cos_phi=cos_phi_ef)

    rezultat_sectiune = alege_sectiune_cablu(
        curent_nominal_a=curent_nominal,
        mod_pozare=circuit.mod_pozare,
        tip_circuit=circuit.tip.value,
        lungime_m=circuit.lungime_cablu_m,
        tensiune_v=tensiune_v,
        tip_utilizare=_tip_utilizare(receptori),
    )

    circuit.curent_nominal_a = curent_nominal
    circuit.sectiune_mm2 = rezultat_sectiune.sectiune_mm2 if rezultat_sectiune else None

    # putere_instalata/putere_calcul la nivel de tablou = suma peste toate circuitele
    # sale (nu doar cel recalculat acum), ca să nu se piardă contribuția celorlalte.
    tablou_pi, tablou_pc = 0.0, 0.0
    for c in db.query(Circuit).filter(Circuit.tablou_id == circuit.tablou_id).all():
        receptori_c = receptori if c.id == circuit.id else db.query(Receptor).filter(Receptor.circuit_id == c.id).all()
        pi_c, pc_c = _pi_pc_circuit(receptori_c)
        tablou_pi += pi_c
        tablou_pc += pc_c
    circuit.tablou.putere_instalata = tablou_pi
    circuit.tablou.putere_calcul = tablou_pc

    # recalculare curată: rezultatele anterioare ale acestui circuit se înlocuiesc
    db.query(CalculRezultat).filter(CalculRezultat.circuit_id == circuit.id).delete()

    rezultate = [
        CalculRezultat(
            circuit_id=circuit.id,
            tip_calcul="curent_nominal",
            valoare=curent_nominal,
            unitate="A",
            standard_referinta="I7-2011 / HD 60364",
            status_conformitate=StatusConformitate.conform,
        )
    ]

    if rezultat_sectiune is not None:
        rezultate.append(
            CalculRezultat(
                circuit_id=circuit.id,
                tip_calcul="sectiune_cablu",
                valoare=rezultat_sectiune.sectiune_mm2,
                unitate="mm2",
                standard_referinta="HD 60364-5-52",
                status_conformitate=(
                    StatusConformitate.conform
                    if rezultat_sectiune.conform_curent
                    else StatusConformitate.neconform
                ),
            )
        )
        rezultate.append(
            CalculRezultat(
                circuit_id=circuit.id,
                tip_calcul="cadere_tensiune",
                valoare=rezultat_sectiune.cadere_tensiune_procent,
                unitate="%",
                standard_referinta="I7-2011 art. 6",
                status_conformitate=(
                    StatusConformitate.conform
                    if rezultat_sectiune.conform_cadere_tensiune
                    else StatusConformitate.neconform
                ),
            )
        )
    else:
        rezultate.append(
            CalculRezultat(
                circuit_id=circuit.id,
                tip_calcul="sectiune_cablu",
                valoare=0,
                unitate="mm2",
                standard_referinta="HD 60364-5-52",
                status_conformitate=StatusConformitate.neconform,
            )
        )

    db.add_all(rezultate)
    db.commit()
    for r in rezultate:
        db.refresh(r)
    return rezultate


@router.get("/circuite/{circuit_id}/rezultate", response_model=list[CalculRezultatOut])
def obtine_rezultate(circuit_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    circuit = get_circuit_or_404(db, circuit_id, user)
    return db.query(CalculRezultat).filter(CalculRezultat.circuit_id == circuit.id).all()
