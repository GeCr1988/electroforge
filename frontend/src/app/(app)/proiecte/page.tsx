"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { api, Proiect, TipCladire } from "@/lib/api";

export default function ProiecteListPage() {
  const [proiecte, setProiecte] = useState<Proiect[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [nume, setNume] = useState("");
  const [beneficiar, setBeneficiar] = useState("");
  const [tipCladire, setTipCladire] = useState<TipCladire>("rezidential");
  const [adresa, setAdresa] = useState("");
  const [creating, setCreating] = useState(false);

  function incarcaProiecte() {
    api
      .listaProiecte()
      .then(setProiecte)
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }

  useEffect(incarcaProiecte, []);

  async function handleDelete(id: number) {
    if (!window.confirm("Ștergi acest proiect? Toate tablourile/circuitele/receptorii lui se șterg definitiv.")) return;
    try {
      await api.stergeProiect(id);
      incarcaProiecte();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      await api.creeazaProiect({
        nume,
        beneficiar,
        tip_cladire: tipCladire,
        adresa: adresa || null,
        tensiune_alimentare: "230/400V",
      });
      setNume("");
      setBeneficiar("");
      setAdresa("");
      incarcaProiecte();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la creare");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <h1 className="text-xl font-semibold">Proiectele mele</h1>

      <form onSubmit={handleCreate} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-medium">Proiect nou</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            required
            placeholder="Nume proiect"
            value={nume}
            onChange={(e) => setNume(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <input
            required
            placeholder="Beneficiar"
            value={beneficiar}
            onChange={(e) => setBeneficiar(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <select
            value={tipCladire}
            onChange={(e) => setTipCladire(e.target.value as TipCladire)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          >
            <option value="rezidential">Rezidențial</option>
            <option value="industrial">Industrial</option>
          </select>
          <input
            placeholder="Adresă (opțional)"
            value={adresa}
            onChange={(e) => setAdresa(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
        </div>
        <button
          type="submit"
          disabled={creating}
          className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          {creating ? "Se creează..." : "Creează proiect"}
        </button>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {loading ? (
        <p className="text-zinc-500">Se încarcă...</p>
      ) : proiecte.length === 0 ? (
        <p className="text-zinc-500">Niciun proiect încă.</p>
      ) : (
        <ul className="divide-y divide-zinc-200 rounded-lg border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-800">
          {proiecte.map((p) => (
            <li key={p.id} className="flex items-center justify-between gap-2 px-4 py-3 hover:bg-zinc-50 dark:hover:bg-zinc-900">
              <Link href={`/proiecte/${p.id}`} className="flex flex-1 flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <span className="font-medium">{p.nume}</span>
                <span className="text-sm text-zinc-500">
                  {p.beneficiar} · {p.tip_cladire}
                </span>
              </Link>
              <button
                onClick={() => handleDelete(p.id)}
                className="shrink-0 rounded-md px-2 py-1 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
              >
                Șterge
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
