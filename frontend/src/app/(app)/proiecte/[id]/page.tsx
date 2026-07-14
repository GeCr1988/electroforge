"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, Proiect, Tablou } from "@/lib/api";

export default function ProiectDetailPage() {
  const params = useParams<{ id: string }>();
  const proiectId = Number(params.id);

  const [proiect, setProiect] = useState<Proiect | null>(null);
  const [tablouri, setTablouri] = useState<Tablou[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nume, setNume] = useState("");
  const [creating, setCreating] = useState(false);

  function incarca() {
    Promise.all([api.obtineProiect(proiectId), api.listaTablouri(proiectId)])
      .then(([p, t]) => {
        setProiect(p);
        setTablouri(t);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }

  useEffect(incarca, [proiectId]);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      await api.creeazaTablou(proiectId, nume);
      setNume("");
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la creare");
    } finally {
      setCreating(false);
    }
  }

  if (loading) return <p className="text-zinc-500">Se încarcă...</p>;

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <Link href="/proiecte" className="text-sm text-zinc-500 hover:underline">
          ← Toate proiectele
        </Link>
        {proiect && (
          <>
            <h1 className="mt-1 text-xl font-semibold">{proiect.nume}</h1>
            <p className="text-sm text-zinc-500">
              {proiect.beneficiar} · {proiect.tip_cladire} · {proiect.tensiune_alimentare}
              {proiect.adresa ? ` · ${proiect.adresa}` : ""}
            </p>
          </>
        )}
      </div>

      <form onSubmit={handleCreate} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-medium">Tablou electric nou</h2>
        <div className="flex flex-col gap-3 sm:flex-row">
          <input
            required
            placeholder="Nume tablou (ex: TE, TD1)"
            value={nume}
            onChange={(e) => setNume(e.target.value)}
            className="flex-1 rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <button
            type="submit"
            disabled={creating}
            className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
          >
            {creating ? "Se creează..." : "Adaugă tablou"}
          </button>
        </div>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {tablouri.length === 0 ? (
        <p className="text-zinc-500">Niciun tablou încă.</p>
      ) : (
        <ul className="divide-y divide-zinc-200 rounded-lg border border-zinc-200 dark:divide-zinc-800 dark:border-zinc-800">
          {tablouri.map((t) => (
            <li key={t.id}>
              <Link
                href={`/tablouri/${t.id}`}
                className="flex flex-col gap-1 px-4 py-3 hover:bg-zinc-50 sm:flex-row sm:items-center sm:justify-between dark:hover:bg-zinc-900"
              >
                <span className="font-medium">{t.nume}</span>
                <span className="text-sm text-zinc-500">
                  Pi: {t.putere_instalata != null ? `${t.putere_instalata.toFixed(0)} W` : "—"} · Pc:{" "}
                  {t.putere_calcul != null ? `${t.putere_calcul.toFixed(0)} W` : "—"}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
