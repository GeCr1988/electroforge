"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { api, CalculRezultat, Circuit, Receptor, TipReceptor } from "@/lib/api";

const STATUS_STYLES: Record<string, string> = {
  conform: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  neconform: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
};

export default function CircuitDetailPage() {
  const params = useParams<{ circuitId: string }>();
  const circuitId = Number(params.circuitId);

  const [circuit, setCircuit] = useState<Circuit | null>(null);
  const [receptori, setReceptori] = useState<Receptor[]>([]);
  const [rezultate, setRezultate] = useState<CalculRezultat[]>([]);
  const [loading, setLoading] = useState(true);
  const [calculating, setCalculating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [nume, setNume] = useState("");
  const [tip, setTip] = useState<TipReceptor>("iluminat");
  const [putere, setPutere] = useState("100");
  const [cosPhi, setCosPhi] = useState("1.0");
  const [ku, setKu] = useState("1.0");
  const [ks, setKs] = useState("1.0");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    Promise.all([api.obtineCircuit(circuitId), api.listaReceptori(circuitId), api.obtineRezultate(circuitId)])
      .then(([c, r, rez]) => {
        setCircuit(c);
        setReceptori(r);
        setRezultate(rez);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }, [circuitId]);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setCreating(true);
    setError(null);
    try {
      await api.creeazaReceptor(circuitId, {
        nume,
        tip,
        putere_nominala_w: Number(putere),
        cos_phi: Number(cosPhi),
        ku: Number(ku),
        ks: Number(ks),
      });
      setNume("");
      const updated = await api.listaReceptori(circuitId);
      setReceptori(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la creare");
    } finally {
      setCreating(false);
    }
  }

  async function handleCalculeaza() {
    setCalculating(true);
    setError(null);
    try {
      const rez = await api.calculeaza(circuitId);
      setRezultate(rez);
      const c = await api.obtineCircuit(circuitId);
      setCircuit(c);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la calcul");
    } finally {
      setCalculating(false);
    }
  }

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <Link
          href={circuit ? `/tablouri/${circuit.tablou_id}` : "/proiecte"}
          className="text-sm text-zinc-500 hover:underline"
        >
          ← Înapoi la tablou
        </Link>
        <h1 className="mt-1 text-xl font-semibold">{circuit?.nume ?? `Circuit #${circuitId}`}</h1>
        {circuit && (
          <p className="text-sm text-zinc-500">
            {circuit.tip} · {circuit.mod_pozare} · {circuit.lungime_cablu_m}m
          </p>
        )}
      </div>

      <form onSubmit={handleCreate} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
        <h2 className="font-medium">Receptor nou</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <input
            required
            placeholder="Nume receptor"
            value={nume}
            onChange={(e) => setNume(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <select
            value={tip}
            onChange={(e) => setTip(e.target.value as TipReceptor)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          >
            <option value="iluminat">Iluminat</option>
            <option value="priza">Priză</option>
            <option value="motor">Motor</option>
            <option value="forta">Forță</option>
          </select>
          <input
            required
            type="number"
            min={0}
            step="1"
            placeholder="Putere nominală (W)"
            value={putere}
            onChange={(e) => setPutere(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <input
            required
            type="number"
            min={0}
            max={1}
            step="0.01"
            placeholder="cos φ"
            value={cosPhi}
            onChange={(e) => setCosPhi(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <input
            required
            type="number"
            min={0}
            max={1}
            step="0.01"
            placeholder="Ku (utilizare)"
            value={ku}
            onChange={(e) => setKu(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
          <input
            required
            type="number"
            min={0}
            max={1}
            step="0.01"
            placeholder="Ks (simultaneitate)"
            value={ks}
            onChange={(e) => setKs(e.target.value)}
            className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
          />
        </div>
        <button
          type="submit"
          disabled={creating}
          className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
        >
          {creating ? "Se creează..." : "Adaugă receptor"}
        </button>
      </form>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {loading ? (
        <p className="text-zinc-500">Se încarcă...</p>
      ) : (
        <>
          <div className="overflow-x-auto rounded-lg border border-zinc-200 dark:border-zinc-800">
            <table className="w-full min-w-[500px] text-left text-sm">
              <thead className="bg-zinc-50 dark:bg-zinc-900">
                <tr>
                  <th className="px-3 py-2">Nume</th>
                  <th className="px-3 py-2">Tip</th>
                  <th className="px-3 py-2">P (W)</th>
                  <th className="px-3 py-2">cos φ</th>
                  <th className="px-3 py-2">Ku</th>
                  <th className="px-3 py-2">Ks</th>
                </tr>
              </thead>
              <tbody>
                {receptori.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-3 py-3 text-zinc-500">
                      Niciun receptor încă.
                    </td>
                  </tr>
                ) : (
                  receptori.map((r) => (
                    <tr key={r.id} className="border-t border-zinc-200 dark:border-zinc-800">
                      <td className="px-3 py-2">{r.nume}</td>
                      <td className="px-3 py-2">{r.tip}</td>
                      <td className="px-3 py-2">{r.putere_nominala_w}</td>
                      <td className="px-3 py-2">{r.cos_phi}</td>
                      <td className="px-3 py-2">{r.ku}</td>
                      <td className="px-3 py-2">{r.ks}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          <button
            onClick={handleCalculeaza}
            disabled={calculating || receptori.length === 0}
            className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-500 disabled:opacity-50"
          >
            {calculating ? "Se calculează..." : "Calculează"}
          </button>

          {rezultate.length > 0 && (
            <div className="overflow-x-auto rounded-lg border border-zinc-200 dark:border-zinc-800">
              <table className="w-full min-w-[500px] text-left text-sm">
                <thead className="bg-zinc-50 dark:bg-zinc-900">
                  <tr>
                    <th className="px-3 py-2">Calcul</th>
                    <th className="px-3 py-2">Valoare</th>
                    <th className="px-3 py-2">Standard</th>
                    <th className="px-3 py-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {rezultate.map((r) => (
                    <tr key={r.id} className="border-t border-zinc-200 dark:border-zinc-800">
                      <td className="px-3 py-2">{r.tip_calcul}</td>
                      <td className="px-3 py-2">
                        {r.valoare.toFixed(2)} {r.unitate}
                      </td>
                      <td className="px-3 py-2 text-zinc-500">{r.standard_referinta}</td>
                      <td className="px-3 py-2">
                        <span className={`rounded-full px-2 py-0.5 text-xs ${STATUS_STYLES[r.status_conformitate]}`}>
                          {r.status_conformitate}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  );
}
