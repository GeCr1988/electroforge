# Electro-Proiect

Aplicație web pentru proiectarea instalațiilor electrice la case și fabrici — calcule, scheme, BOM și verificare conformitate cu standardele românești și europene.

- Specificații complete: [`docs/specificatii-complete.md`](docs/specificatii-complete.md)
- Instrucțiuni pentru dezvoltare cu Claude Code: [`CLAUDE.md`](CLAUDE.md)

## Status

🚧 MVP în dezvoltare activă. Fluxul de bază funcționează: autentificare, proiecte →
tablouri → circuite → receptori, calcul puteri/curenți/secțiuni/scurtcircuit,
selectivitate protecții din catalog propriu, schemă monofilară SVG, BOM și
export PDF al breviarului de calcul.

## Stack

React/Next.js (frontend) · Python/FastAPI (backend) · PostgreSQL · WeasyPrint (PDF) · SVG generat programatic. Detalii complete în [`CLAUDE.md`](CLAUDE.md).

## Pornire rapidă (Docker)

```bash
cp .env.example .env
docker compose up
```

- Frontend: http://localhost:3000
- Backend (Swagger UI): http://localhost:8000/docs
- La primul `docker compose up`, backend-ul rulează automat migrațiile Alembic
  (`alembic upgrade head`) înainte de a porni serverul.

Creează-ți un cont din pagina de înregistrare (`/register`) și ești gata de lucru.

## Dezvoltare locală (fără Docker, doar backend)

```bash
cd backend
python -m venv .venv && .venv/Scripts/activate  # sau source .venv/bin/activate pe Linux/Mac
pip install -r requirements.txt

# migrații (necesită un Postgres accesibil la DATABASE_URL din .env)
alembic upgrade head

# rulează serverul
uvicorn app.main:app --reload
```

## Teste

Testele backend (motor de calcul + API) rulează cu SQLite in-memory — nu au
nevoie de Docker/Postgres pornit:

```bash
cd backend
python -m pytest
```

Testul breviarului PDF are nevoie de bibliotecile native ale WeasyPrint
(Pango/GTK) — pe Windows fără ele instalate, testul se sare automat (`skipped`),
nu eșuează; rulează normal în Docker și în CI (GitHub Actions), unde sunt instalate.

Verificări frontend:

```bash
cd frontend
npx tsc --noEmit   # type-check
npx eslint src     # lint
npm run build      # build de producție
```

## Migrații noi (Alembic)

După ce modifici un model SQLAlchemy din `backend/app/models/`:

```bash
cd backend
DATABASE_URL="postgresql+psycopg2://electro:electro_dev_password@localhost:5432/electro_proiect" \
  python -m alembic revision --autogenerate -m "descriere schimbare"
```

Verifică fișierul generat în `backend/alembic/versions/` — autogenerate nu
adaugă `server_default` pentru coloane noi NOT NULL pe tabele cu date
existente, trebuie adăugat manual dacă e cazul.

## Date demo

Pentru un proiect exemplu complet (tablou, circuite, receptori, catalog,
selecții), vezi [`backend/scripts/seed_demo.py`](backend/scripts/seed_demo.py).

## CI

GitHub Actions (`.github/workflows/ci.yml`) rulează la fiecare push/PR: teste
backend (pytest) și verificări frontend (type-check, lint, build).

## Disclaimer

Aplicația generează documentație tehnică orientativă și nu înlocuiește
avizarea unui inginer atestat (RTE / proiectant autorizat ANRE). Datele
normative din `backend/app/standards/*.json` marcate `_todo` trebuie
verificate cu textul oficial I7-2011/HD 60364 înainte de folosire în proiecte
reale.
