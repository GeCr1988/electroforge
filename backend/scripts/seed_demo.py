"""Populează un proiect demo complet (tablou + circuite + receptori + catalog)
pentru dezvoltare/testare manuală rapidă, fără să completezi totul din UI.

Rulare (din directorul backend/, cu DATABASE_URL setat spre o bază pornită):
    python -m scripts.seed_demo

Nu rulează motorul de calcul — după seed, loghează-te cu contul demo și apasă
"Calculează" pe fiecare circuit din UI (evită duplicarea logicii din
app/api/calcule.py aici).
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.auth.security import hash_password
from app.db.session import Base, SessionLocal, engine
from app.models.componenta_catalog import ComponentaCatalog
from app.models.circuit import Circuit
from app.models.proiect import Proiect
from app.models.receptor import Receptor
from app.models.tablou import TabloElectric
from app.models.user import User

DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo12345"

CATALOG_EXEMPLU_PATH = Path(__file__).resolve().parent.parent / "app" / "standards" / "catalog_exemplu.json"


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == DEMO_EMAIL).first()
        if user is None:
            user = User(email=DEMO_EMAIL, password_hash=hash_password(DEMO_PASSWORD), rol="proiectant")
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Creat user demo: {DEMO_EMAIL} / {DEMO_PASSWORD}")
        else:
            print(f"User demo există deja: {DEMO_EMAIL}")

        proiect = db.query(Proiect).filter(Proiect.owner_id == user.id, Proiect.nume == "Casa Demo").first()
        if proiect is None:
            proiect = Proiect(
                nume="Casa Demo",
                beneficiar="Ion Popescu",
                tip_cladire="rezidential",
                adresa="Str. Exemplu 1",
                tensiune_alimentare="230/400V",
                impedanta_retea_amonte_ohm=0.1,
                owner_id=user.id,
            )
            db.add(proiect)
            db.commit()
            db.refresh(proiect)

            tablou = TabloElectric(nume="TE", proiect_id=proiect.id)
            db.add(tablou)
            db.commit()
            db.refresh(tablou)

            circuit_iluminat = Circuit(
                tablou_id=tablou.id,
                nume="C1 iluminat living",
                tip="monofazat",
                mod_pozare="B1",
                lungime_cablu_m=15,
            )
            circuit_prize = Circuit(
                tablou_id=tablou.id,
                nume="C2 prize living",
                tip="monofazat",
                mod_pozare="B1",
                lungime_cablu_m=12,
            )
            db.add_all([circuit_iluminat, circuit_prize])
            db.commit()
            db.refresh(circuit_iluminat)
            db.refresh(circuit_prize)

            db.add_all(
                [
                    Receptor(
                        circuit_id=circuit_iluminat.id,
                        nume="Corp iluminat living",
                        tip="iluminat",
                        putere_nominala_w=100,
                        cos_phi=1.0,
                        ku=1.0,
                        ks=1.0,
                    ),
                    Receptor(
                        circuit_id=circuit_prize.id,
                        nume="Priză dublă living",
                        tip="priza",
                        putere_nominala_w=2000,
                        cos_phi=0.9,
                        ku=0.2,
                        ks=1.0,
                    ),
                ]
            )
            db.commit()
            print(f"Creat proiect demo 'Casa Demo' (id={proiect.id}) cu tablou TE și 2 circuite.")
        else:
            print("Proiectul demo 'Casa Demo' există deja.")

        if db.query(ComponentaCatalog).filter(ComponentaCatalog.owner_id == user.id).count() == 0:
            with open(CATALOG_EXEMPLU_PATH, encoding="utf-8") as f:
                catalog_json = json.load(f)
            for item in catalog_json["componente"]:
                db.add(
                    ComponentaCatalog(
                        owner_id=user.id,
                        categorie=item["categorie"],
                        nume=item["nume"],
                        producator=item.get("producator"),
                        cod_produs=item.get("cod_produs"),
                        specificatii=item.get("specificatii", {}),
                        pret_estimativ=item.get("pret_estimativ"),
                        unitate_masura=item.get("unitate_masura", "buc"),
                        simbol_ref=item.get("simbol_ref"),
                    )
                )
            db.commit()
            print(f"Populat catalog demo din {CATALOG_EXEMPLU_PATH.name}.")
        else:
            print("Catalogul demo există deja.")

        print("\nGata. Loghează-te cu:")
        print(f"  email: {DEMO_EMAIL}")
        print(f"  parolă: {DEMO_PASSWORD}")
        print("Apoi deschide proiectul 'Casa Demo' și apasă Calculează pe fiecare circuit.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
