"use client";

import { useEffect, useState } from "react";
import { api, CategorieComponenta, ComponentaCatalog } from "@/lib/api";

const CATEGORII: CategorieComponenta[] = [
  "protectie",
  "cablu",
  "corp_iluminat",
  "priza",
  "intrerupator",
  "tablou",
  "doza",
  "altele",
];

export default function CatalogPage() {
  const [componente, setComponente] = useState<ComponentaCatalog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [categorie, setCategorie] = useState<CategorieComponenta>("protectie");
  const [nume, setNume] = useState("");
  const [pret, setPret] = useState("");
  const [inA, setInA] = useState("");
  const [icuKa, setIcuKa] = useState("");
  const [sectiuneMm2, setSectiuneMm2] = useState("");
  const [creating, setCreating] = useState(false);

  function incarca() {
    api
      .listaCatalog()
      .then(setComponente)
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }

  useEffect(incarca, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      const specificatii: Record<string, unknown> = {};
      if (categorie === "protectie") {
        if (inA) specificatii.in_a = Number(inA);
        if (icuKa) specificatii.icu_ka = Number(icuKa);
      } else if (categorie === "cablu") {
        if (sectiuneMm2) specificatii.sectiune_mm2 = Number(sectiuneMm2);
      }
      await api.creeazaComponenta({
        categorie,
        nume,
        pret_estimativ: pret ? Number(pret) : null,
        specificatii,
      });
      setNume("");
      setPret("");
      setInA("");
      setIcuKa("");
      setSectiuneMm2("");
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la creare");
    } finally {
      setCreating(false);
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm("Ștergi această componentă din catalog?")) return;
    try {
      await api.stergeComponenta(id);
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <h1 className="text-xl font-semibold">Catalog de componente</h1>
        <p className="text-sm text-zinc-500">
          Componente proprii (protecții, cabluri, corpuri iluminat, prize...) folosite pentru
          sugestii automate de selectivitate și pentru lista de materiale (BOM).
        </p>
      </div>

      <form onSubmit={handleCreate} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-medium">Componentă nouă</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <select
            value={categorie}
            onChange={(e) => setCategorie(e.target.value as CategorieComponenta)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          >
            {CATEGORII.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          <input
            required
            placeholder="Nume (ex: Disjunctor C16)"
            value={nume}
            onChange={(e) => setNume(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <input
            type="number"
            step="0.01"
            placeholder="Preț estimativ (opțional)"
            value={pret}
            onChange={(e) => setPret(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          {categorie === "protectie" && (
            <>
              <input
                type="number"
                placeholder="In (A)"
                value={inA}
                onChange={(e) => setInA(e.target.value)}
                className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
              />
              <input
                type="number"
                placeholder="Icu (kA)"
                value={icuKa}
                onChange={(e) => setIcuKa(e.target.value)}
                className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
              />
            </>
          )}
          {categorie === "cablu" && (
            <input
              type="number"
              step="0.1"
              placeholder="Secțiune (mm²)"
              value={sectiuneMm2}
              onChange={(e) => setSectiuneMm2(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
          )}
        </div>
        <button
          type="submit"
          disabled={creating}
          className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          {creating ? "Se creează..." : "Adaugă componentă"}
        </button>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {loading ? (
        <p className="text-zinc-500">Se încarcă...</p>
      ) : componente.length === 0 ? (
        <p className="text-zinc-500">Nicio componentă încă.</p>
      ) : (
        <div className="overflow-x-auto rounded-lg border border-zinc-200 dark:border-zinc-800">
          <table className="w-full min-w-[500px] text-left text-sm">
            <thead className="bg-zinc-50 dark:bg-zinc-900">
              <tr>
                <th className="px-3 py-2">Nume</th>
                <th className="px-3 py-2">Categorie</th>
                <th className="px-3 py-2">Specificații</th>
                <th className="px-3 py-2">Preț</th>
                <th className="px-3 py-2"></th>
              </tr>
            </thead>
            <tbody>
              {componente.map((c) => (
                <tr key={c.id} className="border-t border-zinc-200 dark:border-zinc-800">
                  <td className="px-3 py-2">{c.nume}</td>
                  <td className="px-3 py-2">{c.categorie}</td>
                  <td className="px-3 py-2 text-zinc-500">
                    {Object.entries(c.specificatii)
                      .map(([k, v]) => `${k}=${v}`)
                      .join(", ") || "—"}
                  </td>
                  <td className="px-3 py-2">{c.pret_estimativ != null ? c.pret_estimativ.toFixed(2) : "—"}</td>
                  <td className="px-3 py-2">
                    <button onClick={() => handleDelete(c.id)} className="text-xs text-red-600 hover:underline">
                      Șterge
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
