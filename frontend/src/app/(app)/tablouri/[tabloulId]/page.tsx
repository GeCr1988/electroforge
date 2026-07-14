"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, Circuit, Tablou, TipCircuit } from "@/lib/api";

export default function TabloDetailPage() {
  const params = useParams<{ tabloulId: string }>();
  const tabloulId = Number(params.tabloulId);

  const [tablou, setTablou] = useState<Tablou | null>(null);
  const [circuite, setCircuite] = useState<Circuit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [nume, setNume] = useState("");
  const [tip, setTip] = useState<TipCircuit>("monofazat");
  const [modPozare, setModPozare] = useState("B1");
  const [lungime, setLungime] = useState("10");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    Promise.all([api.obtineTablou(tabloulId), api.listaCircuite(tabloulId)])
      .then(([t, c]) => {
        setTablou(t);
        setCircuite(c);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }, [tabloulId]);

  async function reincarcaCircuite() {
    const updated = await api.listaCircuite(tabloulId);
    setCircuite(updated);
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      await api.creeazaCircuit(tabloulId, {
        nume,
        tip,
        mod_pozare: modPozare,
        lungime_cablu_m: Number(lungime),
      });
      setNume("");
      await reincarcaCircuite();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la creare");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <Link
          href={tablou ? `/proiecte/${tablou.proiect_id}` : "/proiecte"}
          className="text-sm text-zinc-500 hover:underline"
        >
          ← Înapoi la proiect
        </Link>
        <h1 className="mt-1 text-xl font-semibold">{tablou?.nume ?? `Tablou #${tabloulId}`}</h1>
      </div>

      <form onSubmit={handleCreate} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-medium">Circuit nou</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            required
            placeholder="Nume circuit (ex: C1 - iluminat living)"
            value={nume}
            onChange={(e) => setNume(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <select
            value={tip}
            onChange={(e) => setTip(e.target.value as TipCircuit)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          >
            <option value="monofazat">Monofazat</option>
            <option value="trifazat">Trifazat</option>
          </select>
          <input
            required
            placeholder="Mod de pozare (B1 sau C)"
            value={modPozare}
            onChange={(e) => setModPozare(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <input
            required
            type="number"
            min={0}
            step="0.1"
            placeholder="Lungime cablu (m)"
            value={lungime}
            onChange={(e) => setLungime(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
        </div>
        <button
          type="submit"
          disabled={creating}
          className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          {creating ? "Se creează..." : "Adaugă circuit"}
        </button>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {loading ? (
        <p className="text-zinc-500">Se încarcă...</p>
      ) : circuite.length === 0 ? (
        <p className="text-zinc-500">Niciun circuit încă.</p>
      ) : (
        <ul className="divide-y divide-zinc-200 rounded-lg border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-800">
          {circuite.map((c) => (
            <li key={c.id}>
              <Link
                href={`/circuite/${c.id}`}
                className="flex flex-col gap-1 px-4 py-3 hover:bg-zinc-50 sm:flex-row sm:items-center sm:justify-between dark:hover:bg-zinc-900"
              >
                <span className="font-medium">{c.nume}</span>
                <span className="text-sm text-zinc-500">
                  {c.tip} · {c.mod_pozare} · {c.lungime_cablu_m}m
                  {c.sectiune_mm2 != null ? ` · ${c.sectiune_mm2}mm²` : ""}
                  {c.curent_nominal_a != null ? ` · ${c.curent_nominal_a.toFixed(1)}A` : ""}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
