# CLAUDE.md — Instrucțiuni proiect: Aplicație Proiectare Instalații Electrice

Acest fișier ghidează Claude Code în lucrul pe acest proiect. Specificațiile complete sunt în `docs/specificatii-complete.md` — citește-l înainte de a începe orice task major.

## Ce construim

Aplicație web pentru proiectarea instalațiilor electrice la case (rezidențial) și fabrici (industrial): calcule electrice, generare scheme, BOM (listă materiale) și verificare conformitate cu standardele I7-2011, PE 107, SR EN/HD 60364, SR EN 61439, SR EN 62305, SR EN 12464-1.

## Stack tehnic (decizii fixate)

- **Frontend**: React + Next.js
- **Backend**: Python + FastAPI (motorul de calcul beneficiază de ecosistemul Python)
- **Bază de date**: PostgreSQL
- **Generare PDF**: WeasyPrint
- **Generare scheme**: SVG generat programatic

Nu schimba stack-ul fără să întrebi întâi.

## Structura folderelor

```
electro-proiect/
├── docs/
│   └── specificatii-complete.md   # specificațiile complete, sursa de adevăr
├── backend/
│   ├── app/
│   │   ├── calc_engine/           # motorul de calcul — modul izolat, testabil unitar
│   │   ├── models/                # entități DB (Proiect, TabloElectric, Circuit, Receptor...)
│   │   ├── api/                   # rute FastAPI
│   │   └── standards/             # tabele normative versionate (JSON) — secțiuni cabluri, Ku/Ks, curbe protecții
│   └── tests/
├── frontend/
│   └── src/
└── README.md
```

## Reguli de lucru

1. **Motorul de calcul e sacru**: orice funcție de calcul (secțiune cablu, curent de scurtcircuit, cădere de tensiune) trebuie să aibă teste unitare cu valori de referință din I7-2011/HD 60364 înainte de a fi considerată completă.
2. **Datele normative nu se hardcodează în cod** — stau în `backend/app/standards/*.json`, versionate, ca să poată fi actualizate fără redeploy.
3. **Nu inventa formule de calcul.** Dacă o formulă normativă nu e clară, marchează cu `TODO: verifică cu I7-2011 art. X` în loc să presupui o valoare.
4. **Ordinea de dezvoltare** urmează roadmap-ul din `docs/specificatii-complete.md` secțiunea 8 (MVP → etape). Nu sări la scheme/BOM înainte ca motorul de calcul de bază (puteri, curenți, secțiuni cabluri) să fie solid.
5. **Disclaimer legal**: aplicația generează documentație, nu înlocuiește avizarea unui inginer atestat (RTE/ANRE). Orice ecran de export trebuie să includă acest disclaimer.

## Stare curentă

Proiect în fază de specificații — nu există încă cod. Primul task recomandat: scaffolding backend (FastAPI + PostgreSQL) și primul modul de calcul (puteri instalate + curenți nominali) conform secțiunii 4.3 din specificații.
