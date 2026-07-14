"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, Circuit, Tablou, TipCircuit } from "@/lib/api";

export default function TabloDetailPage() {
  const params = useParams<{ tabloulId: string }>();
  const router = useRouter();
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

  const [editing, setEditing] = useState(false);
  const [editNume, setEditNume] = useState("");
  const [savingEdit, setSavingEdit] = useState(false);

  function incarca() {
    Promise.all([api.obtineTablou(tabloulId), api.listaCircuite(tabloulId)])
      .then(([t, c]) => {
        setTablou(t);
        setCircuite(c);
        setEditNume(t.nume);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }

  useEffect(incarca, [tabloulId]);

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

  async function handleSaveEdit(e: React.FormEvent) {
    e.preventDefault();
    setSavingEdit(true);
    setError(null);
    try {
      await api.actualizeazaTablou(tabloulId, editNume);
      setEditing(false);
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la salvare");
    } finally {
      setSavingEdit(false);
    }
  }

  async function handleDeleteTablou() {
    if (!tablou) return;
    if (!window.confirm("Ștergi acest tablou? Toate circuitele/receptorii lui se șterg definitiv.")) return;
    try {
      await api.stergeTablou(tabloulId);
      router.push(`/proiecte/${tablou.proiect_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
    }
  }

  async function handleDeleteCircuit(circuitId: number) {
    if (!window.confirm("Ștergi acest circuit? Toți receptorii lui se șterg definitiv.")) return;
    try {
      await api.stergeCircuit(circuitId);
      await reincarcaCircuite();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
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
        {tablou && !editing && (
          <div className="mt-1 flex items-center justify-between gap-2">
            <h1 className="text-xl font-semibold">{tablou.nume}</h1>
            <div className="flex shrink-0 gap-2">
              <button
                onClick={() => setEditing(true)}
                className="rounded-md border border-zinc-300 px-3 py-1.5 text-sm hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
              >
                Editează
              </button>
              <button
                onClick={handleDeleteTablou}
                className="rounded-md px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
              >
                Șterge tablou
              </button>
            </div>
          </div>
        )}
      </div>

      {editing && (
        <form onSubmit={handleSaveEdit} className="flex gap-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <input
            required
            value={editNume}
            onChange={(e) => setEditNume(e.target.value)}
            className="flex-1 rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <button
            type="submit"
            disabled={savingEdit}
            className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
          >
            {savingEdit ? "Se salvează..." : "Salvează"}
          </button>
          <button
            type="button"
            onClick={() => setEditing(false)}
            className="rounded-md border border-zinc-300 px-4 py-2 hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
          >
            Anulează
          </button>
        </form>
      )}

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
            <li key={c.id} className="flex items-center justify-between gap-2 px-4 py-3 hover:bg-zinc-50 dark:hover:bg-zinc-900">
              <Link href={`/circuite/${c.id}`} className="flex flex-1 flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <span className="font-medium">{c.nume}</span>
                <span className="text-sm text-zinc-500">
                  {c.tip} · {c.mod_pozare} · {c.lungime_cablu_m}m
                  {c.sectiune_mm2 != null ? ` · ${c.sectiune_mm2}mm²` : ""}
                  {c.curent_nominal_a != null ? ` · ${c.curent_nominal_a.toFixed(1)}A` : ""}
                </span>
              </Link>
              <button
                onClick={() => handleDeleteCircuit(c.id)}
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
