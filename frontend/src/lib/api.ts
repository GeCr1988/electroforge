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
  creeazaProiect: (payload: Omit<Proiect, "id" | "owner_id">) =>
    request<Proiect>("/proiecte", { method: "POST", body: JSON.stringify(payload) }),
  obtineProiect: (id: number) => request<Proiect>(`/proiecte/${id}`),

  listaTablouri: (proiectId: number) => request<Tablou[]>(`/proiecte/${proiectId}/tablouri`),
  creeazaTablou: (proiectId: number, nume: string) =>
    request<Tablou>(`/proiecte/${proiectId}/tablouri`, { method: "POST", body: JSON.stringify({ nume }) }),
  obtineTablou: (tabloulId: number) => request<Tablou>(`/tablouri/${tabloulId}`),

  listaCircuite: (tabloulId: number) => request<Circuit[]>(`/tablouri/${tabloulId}/circuite`),
  creeazaCircuit: (
    tabloulId: number,
    payload: { nume: string; tip: TipCircuit; mod_pozare: string; lungime_cablu_m: number }
  ) => request<Circuit>(`/tablouri/${tabloulId}/circuite`, { method: "POST", body: JSON.stringify(payload) }),
  obtineCircuit: (circuitId: number) => request<Circuit>(`/circuite/${circuitId}`),

  listaReceptori: (circuitId: number) => request<Receptor[]>(`/circuite/${circuitId}/receptori`),
  creeazaReceptor: (
    circuitId: number,
    payload: { nume: string; tip: TipReceptor; putere_nominala_w: number; cos_phi: number; ku: number; ks: number }
  ) => request<Receptor>(`/circuite/${circuitId}/receptori`, { method: "POST", body: JSON.stringify(payload) }),

  calculeaza: (circuitId: number) =>
    request<CalculRezultat[]>(`/circuite/${circuitId}/calculeaza`, { method: "POST" }),
  obtineRezultate: (circuitId: number) => request<CalculRezultat[]>(`/circuite/${circuitId}/rezultate`),
};
