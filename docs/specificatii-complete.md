# Specificații de Proiect — Aplicație Web pentru Proiectarea Instalațiilor Electrice

## 1. Viziune și scop

O aplicație web care permite proiectanților electricieni să genereze proiecte tehnice complete pentru instalații electrice la **case (rezidențial)** și **fabrici (industrial)**, incluzând calcule, scheme, listă de materiale (BOM) și verificare de conformitate cu normativele în vigoare (românești + europene).

Rezultatul final pentru fiecare proiect: un **pachet de documentație tehnică** (memoriu, breviar de calcul, scheme, BOM) exportabil în PDF/Word/DWG, gata de depus la verificator/ISU/distribuitor de energie.

---

## 2. Domeniu de aplicare

| Categorie | Exemple |
|---|---|
| **Rezidențial** | case unifamiliale, apartamente, blocuri de locuințe |
| **Industrial** | hale de producție, fabrici, depozite |

Diferențele majore de tratat separat în aplicație:
- Tensiuni/puteri (rezidențial: monofazat/trifazat mic; industrial: trifazat, MT/JT, motoare, variatoare)
- Grad de protecție la mediu (IP, ATEX pentru zone cu pericol de explozie)
- Cerințe de continuitate (grupuri electrogene, UPS pentru industrial)

---

## 3. Standarde de referință

### Standarde/normative românești
- **I7-2011** (actualizat) — Normativ pentru proiectarea, execuția și exploatarea instalațiilor electrice cu tensiuni până la 1000V c.a. și 1500V c.c.
- **PE 107** — Normativ pentru proiectarea și executarea rețelelor de cabluri electrice
- **NP 099** — Normativ pentru proiectarea, execuția și exploatarea instalațiilor electrice ale clădirilor
- **I 18** — Instalații de telecomunicații (dacă relevant pentru curenți slabi)
- **NTE** (Norme Tehnice Energetice) — pentru racordare la rețea

### Standarde europene / IEC (aplicabile și în România prin SR EN)
- **SR EN / HD 60364** (seria) — Instalații electrice de joasă tensiune (echivalent IEC 60364)
- **SR EN 12464-1** — Iluminat pentru locuri de muncă (calcul luminotehnic)
- **SR EN 60204-1** — Echipament electric al mașinilor industriale
- **SR EN 61439** — Ansambluri de aparataj de joasă tensiune (tablouri electrice)
- **SR EN 62305** — Protecție împotriva trăsnetului (paratrăsnet)
- **SR EN 61557** — Verificarea instalațiilor electrice (măsurători)
- **SR EN ISO/IEC 80079** — ATEX (dacă industrial cu zone explozive)

> Aplicația trebuie să permită selectarea setului de standarde per proiect, cu posibilitatea de actualizare a bazei normative fără redeployment (versionare reguli).

---

## 4. Module funcționale (arhitectură completă)

### 4.1 Managementul proiectului
- Creare proiect nou: date beneficiar, adresă, tip clădire (rezidențial/industrial), tensiune de alimentare, putere disponibilă de la furnizor
- Versionare proiect (revizii), istoric modificări
- Roluri: Proiectant, Verificator tehnic (RTE), Administrator

### 4.2 Introducere consumatori/receptori
- Listă receptori electrici (nume, putere nominală, cos φ, tip: iluminat/priză/motor/forță)
- Grupare pe circuite și tablouri electrice
- Coeficienți de utilizare (Ku) și simultaneitate (Ks) per tip receptor/circuit

### 4.3 Calcule electrice (motor de calcul — nucleul aplicației)
- **Putere instalată (Pi)** și **putere de calcul/simultaneitate (Pc)**
- **Curent nominal** pe fiecare circuit (monofazat/trifazat)
- **Dimensionare conductoare/cabluri**: secțiune minimă după curent admisibil, cădere de tensiune admisă (3% iluminat, 5% forță conform I7), mod de pozare (tabele de corecție conform HD 60364-5-52)
- **Calcul curent de scurtcircuit** (Isc) în punctele caracteristice — verificare putere de rupere a protecțiilor
- **Selectivitate protecții** (siguranțe fuzibile / disjunctoare automate / diferențiale) — curbe B/C/D, In, Icu
- **Verificare declanșare automată** în timpul admis (conform I7 - protecție la atingere indirectă)
- **Calcul priză de pământ** (rezistență de dispersie, conform PE 107)
- **Calcul paratrăsnet** (nivel de protecție, raza sferei fictive — SR EN 62305)
- **Calcul luminotehnic** (nivel iluminare Lux per încăpere, uniformitate — SR EN 12464-1)
- **Compensare factor de putere (cos φ)** pentru industrial — baterii condensatoare

### 4.4 Generare scheme electrice
- Schemă monofilară generală
- Schemă tablou electric (TE, TD) cu poziții modulare
- Schemă de amplasare corpuri de iluminat/prize/întrerupătoare (plan clădire)
- Export DWG/DXF (integrare cu CAD) sau SVG editabil în aplicație

### 4.5 Generare BOM (listă de materiale)
- Cabluri (tip, secțiune, lungime, cantitate)
- Aparataj (disjunctoare, diferențiale, contactoare)
- Tablouri și doze
- Corpuri de iluminat, prize, întrerupătoare
- Export Excel/CSV cu prețuri estimative (opțional, integrare furnizori)

### 4.6 Generare documentație finală
- **Memoriu tehnic** (descriere soluție, date de intrare, standarde aplicate)
- **Breviar de calcul** (toate calculele, formule, rezultate)
- **Piese desenate** (schemele generate)
- **Listă de materiale**
- Export PDF/DOCX cu șablon personalizabil (antet firmă, ștampilă, semnătură electronică RTE)

### 4.7 Verificare conformitate (checklist normativ)
- Motor de reguli care validează automat: căderi de tensiune, selectivitate, distanțe de siguranță, IP-uri necesare, ATEX (dacă e cazul)
- Raport de neconformități cu trimitere la articolul din normativ încălcat

---

## 5. Arhitectură tehnică recomandată

| Componentă | Recomandare |
|---|---|
| Frontend | React/Next.js + bibliotecă pentru desen tehnic (Konva.js/Fabric.js sau integrare CAD) |
| Backend | Node.js (NestJS) sau Python (FastAPI) — motorul de calcul e mai natural în Python |
| Bază de date | PostgreSQL (relațional: proiecte, circuite, receptori, cataloage aparataj) |
| Motor de calcul | Modul separat, testabil unitar, cu tabele normative versionate (JSON/DB) |
| Generare documente | PDF: WeasyPrint/Puppeteer; DOCX: docx templating |
| Generare scheme | SVG generat programatic sau librărie de schematics electrice |
| Autentificare | OAuth2/JWT, roluri (RBAC) |
| Hosting | Cloud (AWS/Azure) cu storage pentru fișiere proiect |

---

## 6. Structura principală a bazei de date (entități cheie)

- `Proiect` (id, nume, beneficiar, tip_cladire, adresa, tensiune_alimentare, standard_set)
- `TabloElectric` (id, proiect_id, nume, putere_instalata, putere_calcul)
- `Circuit` (id, tablou_id, tip, lungime_cablu, sectiune, curent_nominal, protectie_id)
- `Receptor` (id, circuit_id, nume, putere_nominala, cos_phi, ku, ks)
- `Protectie` (id, tip, In, curba, Icu, poli)
- `CalculRezultat` (id, circuit_id, tip_calcul, valoare, standard_referinta, status_conformitate)
- `SchemaElectrica` (id, proiect_id, tip, fisier_svg/dwg)
- `MaterialBOM` (id, proiect_id, denumire, cantitate, unitate)

---

## 7. Roluri utilizatori

| Rol | Permisiuni |
|---|---|
| Proiectant | Creează/editează proiecte, rulează calcule, generează documente |
| Verificator (RTE) | Revizuiește, aprobă/respinge, adaugă observații |
| Administrator | Gestionează utilizatori, cataloage de aparataj, actualizează normative |

---

## 8. Roadmap sugerat (etape MVP → soluție completă)

1. **MVP**: Introducere receptori + calcul puteri/curenți + dimensionare cabluri (rezidențial simplu)
2. **Etapa 2**: Calcul scurtcircuit + selectivitate protecții + generare breviar de calcul PDF
3. **Etapa 3**: Scheme electrice (monofilară + tablou) + BOM automat
4. **Etapa 4**: Modul industrial (motoare, ATEX, compensare cos φ) + calcul luminotehnic
5. **Etapa 5**: Motor de verificare conformitate + export DWG + roluri/aprobări multi-user

---

## 9. Aspecte legale/de conformitate de reținut

- Proiectele reale trebuie semnate de un **inginer atestat (RTE - Responsabil Tehnic cu Execuția / proiectant autorizat ANRE)** — aplicația generează documentația, dar nu înlocuiește avizarea legală.
- Pentru racordare la rețea, proiectul trebuie să respecte și **cerințele distribuitorului local de energie** (poate varia).
- Recomandat: aplicația să includă un disclaimer și un flux de aprobare umană înainte de depunerea oficială.

---

## 10. Următorii pași concreți

- [ ] Alege stack tehnic definitiv (backend + motor de calcul)
- [ ] Definește tabelele normative de bază (secțiuni cabluri, curenți admisibili, coeficienți Ku/Ks) ca date structurate
- [ ] Construiește motorul de calcul ca modul independent, testat cu cazuri din I7-2011
- [ ] Proiectează UI pentru introducerea receptorilor și vizualizarea rezultatelor
- [ ] Prototip generare PDF breviar de calcul
