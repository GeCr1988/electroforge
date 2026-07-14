const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Rol = "proiectant" | "verificator" | "administrator";
export type TipCladire = "rezidential" | "industrial";
export type TipCircuit = "monofazat" | "trifazat";
export type TipReceptor = "iluminat" | "priza" | "motor" | "forta";
export type StatusConformitate = "conform" | "neconform";

export interface Proiect {
  id: number;
  nume: string;
  beneficiar: string;
  tip_cladire: TipCladire;
  adresa: string | null;
  tensiune_alimentare: string;
  impedanta_retea_amonte_ohm: number | null;
  owner_id: number;
}

export interface Tablou {
  id: number;
  proiect_id: number;
  nume: string;
  putere_instalata: number | null;
  putere_calcul: number | null;
}

export interface Circuit {
  id: number;
  tablou_id: number;
  nume: string;
  tip: TipCircuit;
  mod_pozare: string;
  lungime_cablu_m: number;
  sectiune_mm2: number | null;
  curent_nominal_a: number | null;
  protectie_selectata_id: number | null;
  protectie_auto: boolean;
  cablu_selectat_id: number | null;
  cablu_auto: boolean;
}

export interface Receptor {
  id: number;
  circuit_id: number;
  nume: string;
  tip: TipReceptor;
  putere_nominala_w: number;
  cos_phi: number;
  ku: number;
  ks: number;
}

export interface CalculRezultat {
  id: number;
  circuit_id: number;
  tip_calcul: string;
  valoare: number;
  unitate: string;
  standard_referinta: string;
  status_conformitate: StatusConformitate;
}

export interface BomLinie {
  componenta_id: number;
  nume: string;
  categorie: string;
  unitate_masura: string;
  cantitate_totala: number;
  pret_estimativ: number | null;
  cost_total: number | null;
}

export interface BomResponse {
  linii: BomLinie[];
  cost_total_general: number;
}

export type CategorieComponenta =
  | "protectie"
  | "cablu"
  | "corp_iluminat"
  | "priza"
  | "intrerupator"
  | "tablou"
  | "doza"
  | "altele";

export interface ComponentaCatalog {
  id: number;
  owner_id: number;
  categorie: CategorieComponenta;
  nume: string;
  producator: string | null;
  cod_produs: string | null;
  specificatii: Record<string, unknown>;
  pret_estimativ: number | null;
  unitate_masura: string;
  simbol_ref: string | null;
}

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

export function setToken(token: string) {
  localStorage.setItem("access_token", token);
}

export function clearToken() {
  localStorage.removeItem("access_token");
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers);
  if (!(options.body instanceof URLSearchParams)) {
    headers.set("Content-Type", "application/json");
  }
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? detail;
    } catch {
      // ignore
    }
    throw new Error(detail);
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  register: (email: string, password: string, rol: Rol = "proiectant") =>
    request<{ id: number; email: string; rol: Rol }>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, rol }),
    }),

  login: async (email: string, password: string) => {
    const body = new URLSearchParams({ username: email, password });
    const data = await request<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body,
    });
    setToken(data.access_token);
    return data;
  },

  me: () => request<{ id: number; email: string; rol: Rol }>("/auth/me"),

  listaProiecte: () => request<Proiect[]>("/proiecte"),
  creeazaProiect: (payload: Partial<Omit<Proiect, "id" | "owner_id">> & { nume: string; beneficiar: string; tip_cladire: TipCladire }) =>
    request<Proiect>("/proiecte", { method: "POST", body: JSON.stringify(payload) }),
  obtineProiect: (id: number) => request<Proiect>(`/proiecte/${id}`),
  actualizeazaProiect: (id: number, payload: Partial<Omit<Proiect, "id" | "owner_id">>) =>
    request<Proiect>(`/proiecte/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  stergeProiect: (id: number) => request<void>(`/proiecte/${id}`, { method: "DELETE" }),

  listaTablouri: (proiectId: number) => request<Tablou[]>(`/proiecte/${proiectId}/tablouri`),
  creeazaTablou: (proiectId: number, nume: string) =>
    request<Tablou>(`/proiecte/${proiectId}/tablouri`, { method: "POST", body: JSON.stringify({ nume }) }),
  obtineTablou: (tabloulId: number) => request<Tablou>(`/tablouri/${tabloulId}`),
  actualizeazaTablou: (tabloulId: number, nume: string) =>
    request<Tablou>(`/tablouri/${tabloulId}`, { method: "PATCH", body: JSON.stringify({ nume }) }),
  stergeTablou: (tabloulId: number) => request<void>(`/tablouri/${tabloulId}`, { method: "DELETE" }),

  listaCircuite: (tabloulId: number) => request<Circuit[]>(`/tablouri/${tabloulId}/circuite`),
  creeazaCircuit: (
    tabloulId: number,
    payload: { nume: string; tip: TipCircuit; mod_pozare: string; lungime_cablu_m: number }
  ) => request<Circuit>(`/tablouri/${tabloulId}/circuite`, { method: "POST", body: JSON.stringify(payload) }),
  obtineCircuit: (circuitId: number) => request<Circuit>(`/circuite/${circuitId}`),
  actualizeazaCircuit: (
    circuitId: number,
    payload: Partial<{
      nume: string;
      tip: TipCircuit;
      mod_pozare: string;
      lungime_cablu_m: number;
      protectie_selectata_id: number;
      cablu_selectat_id: number;
    }>
  ) => request<Circuit>(`/circuite/${circuitId}`, { method: "PATCH", body: JSON.stringify(payload) }),
  stergeCircuit: (circuitId: number) => request<void>(`/circuite/${circuitId}`, { method: "DELETE" }),

  listaReceptori: (circuitId: number) => request<Receptor[]>(`/circuite/${circuitId}/receptori`),
  creeazaReceptor: (
    circuitId: number,
    payload: { nume: string; tip: TipReceptor; putere_nominala_w: number; cos_phi: number; ku: number; ks: number }
  ) => request<Receptor>(`/circuite/${circuitId}/receptori`, { method: "POST", body: JSON.stringify(payload) }),
  actualizeazaReceptor: (
    circuitId: number,
    receptorId: number,
    payload: Partial<{
      nume: string;
      tip: TipReceptor;
      putere_nominala_w: number;
      cos_phi: number;
      ku: number;
      ks: number;
    }>
  ) =>
    request<Receptor>(`/circuite/${circuitId}/receptori/${receptorId}`, {
      method: "PATCH",
      body: JSON.stringify(payload),
    }),
  stergeReceptor: (circuitId: number, receptorId: number) =>
    request<void>(`/circuite/${circuitId}/receptori/${receptorId}`, { method: "DELETE" }),

  calculeaza: (circuitId: number) =>
    request<CalculRezultat[]>(`/circuite/${circuitId}/calculeaza`, { method: "POST" }),
  obtineRezultate: (circuitId: number) => request<CalculRezultat[]>(`/circuite/${circuitId}/rezultate`),

  schemaMonofilaraBlobUrl: async (proiectId: number): Promise<string> => {
    const token = getToken();
    const res = await fetch(`${API_URL}/proiecte/${proiectId}/schema-monofilara.svg`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error("Nu s-a putut încărca schema monofilară");
    const blob = await res.blob();
    return URL.createObjectURL(blob);
  },

  obtineBom: (proiectId: number) => request<BomResponse>(`/proiecte/${proiectId}/bom`),

  descarcaBomCsv: async (proiectId: number): Promise<void> => {
    const token = getToken();
    const res = await fetch(`${API_URL}/proiecte/${proiectId}/bom.csv`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error("Nu s-a putut descărca BOM-ul");
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `bom-proiect-${proiectId}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  },

  listaCatalog: (categorie?: CategorieComponenta) =>
    request<ComponentaCatalog[]>(`/catalog${categorie ? `?categorie=${categorie}` : ""}`),
  creeazaComponenta: (payload: {
    categorie: CategorieComponenta;
    nume: string;
    producator?: string | null;
    cod_produs?: string | null;
    specificatii?: Record<string, unknown>;
    pret_estimativ?: number | null;
    unitate_masura?: string;
  }) => request<ComponentaCatalog>("/catalog", { method: "POST", body: JSON.stringify(payload) }),
  stergeComponenta: (id: number) => request<void>(`/catalog/${id}`, { method: "DELETE" }),

  descarcaBreviarPdf: async (proiectId: number): Promise<void> => {
    const token = getToken();
    const res = await fetch(`${API_URL}/proiecte/${proiectId}/breviar.pdf`, {
      headers: token ? { Authorization: `Bearer ${token}` } : {},
    });
    if (!res.ok) throw new Error("Nu s-a putut descărca breviarul PDF");
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `breviar-proiect-${proiectId}.pdf`;
    a.click();
    URL.revokeObjectURL(url);
  },
};
