"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, CalculRezultat, Circuit, ComponentaCatalog, Receptor, TipCircuit, TipReceptor } from "@/lib/api";

const STATUS_STYLES: Record<string, string> = {
  conform: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  neconform: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
};

export default function CircuitDetailPage() {
  const params = useParams<{ circuitId: string }>();
  const router = useRouter();
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

  const [editingCircuit, setEditingCircuit] = useState(false);
  const [editNume, setEditNume] = useState("");
  const [editTip, setEditTip] = useState<TipCircuit>("monofazat");
  const [editModPozare, setEditModPozare] = useState("");
  const [editLungime, setEditLungime] = useState("");
  const [savingCircuit, setSavingCircuit] = useState(false);

  const [editingReceptorId, setEditingReceptorId] = useState<number | null>(null);
  const [editRNume, setEditRNume] = useState("");
  const [editRTip, setEditRTip] = useState<TipReceptor>("iluminat");
  const [editRPutere, setEditRPutere] = useState("");
  const [editRCosPhi, setEditRCosPhi] = useState("");
  const [editRKu, setEditRKu] = useState("");
  const [editRKs, setEditRKs] = useState("");
  const [savingReceptor, setSavingReceptor] = useState(false);

  const [protectiiCatalog, setProtectiiCatalog] = useState<ComponentaCatalog[]>([]);
  const [cabluriCatalog, setCabluriCatalog] = useState<ComponentaCatalog[]>([]);

  function incarca() {
    Promise.all([api.obtineCircuit(circuitId), api.listaReceptori(circuitId), api.obtineRezultate(circuitId)])
      .then(([c, r, rez]) => {
        setCircuit(c);
        setReceptori(r);
        setRezultate(rez);
        setEditNume(c.nume);
        setEditTip(c.tip);
        setEditModPozare(c.mod_pozare);
        setEditLungime(String(c.lungime_cablu_m));
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }

  useEffect(incarca, [circuitId]);

  useEffect(() => {
    api.listaCatalog("protectie").then(setProtectiiCatalog).catch(() => setProtectiiCatalog([]));
    api.listaCatalog("cablu").then(setCabluriCatalog).catch(() => setCabluriCatalog([]));
  }, []);

  async function handleSelectProtectie(componentaId: number) {
    try {
      const c = await api.actualizeazaCircuit(circuitId, { protectie_selectata_id: componentaId });
      setCircuit(c);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la selectare protecție");
    }
  }

  async function handleSelectCablu(componentaId: number) {
    try {
      const c = await api.actualizeazaCircuit(circuitId, { cablu_selectat_id: componentaId });
      setCircuit(c);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la selectare cablu");
    }
  }

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

  async function handleSaveCircuit(e: React.FormEvent) {
    e.preventDefault();
    setSavingCircuit(true);
    setError(null);
    try {
      await api.actualizeazaCircuit(circuitId, {
        nume: editNume,
        tip: editTip,
        mod_pozare: editModPozare,
        lungime_cablu_m: Number(editLungime),
      });
      setEditingCircuit(false);
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la salvare");
    } finally {
      setSavingCircuit(false);
    }
  }

  async function handleDeleteCircuit() {
    if (!circuit) return;
    if (!window.confirm("Ștergi acest circuit? Toți receptorii lui se șterg definitiv.")) return;
    try {
      await api.stergeCircuit(circuitId);
      router.push(`/tablouri/${circuit.tablou_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
    }
  }

  function startEditReceptor(r: Receptor) {
    setEditingReceptorId(r.id);
    setEditRNume(r.nume);
    setEditRTip(r.tip);
    setEditRPutere(String(r.putere_nominala_w));
    setEditRCosPhi(String(r.cos_phi));
    setEditRKu(String(r.ku));
    setEditRKs(String(r.ks));
  }

  async function handleSaveReceptor(receptorId: number) {
    setSavingReceptor(true);
    setError(null);
    try {
      await api.actualizeazaReceptor(circuitId, receptorId, {
        nume: editRNume,
        tip: editRTip,
        putere_nominala_w: Number(editRPutere),
        cos_phi: Number(editRCosPhi),
        ku: Number(editRKu),
        ks: Number(editRKs),
      });
      setEditingReceptorId(null);
      const updated = await api.listaReceptori(circuitId);
      setReceptori(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la salvare");
    } finally {
      setSavingReceptor(false);
    }
  }

  async function handleDeleteReceptor(receptorId: number) {
    if (!window.confirm("Ștergi acest receptor?")) return;
    try {
      await api.stergeReceptor(circuitId, receptorId);
      const updated = await api.listaReceptori(circuitId);
      setReceptori(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
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
        {circuit && !editingCircuit && (
          <div className="mt-1 flex items-center justify-between gap-2">
            <div>
              <h1 className="text-xl font-semibold">{circuit.nume}</h1>
              <p className="text-sm text-zinc-500">
                {circuit.tip} · {circuit.mod_pozare} · {circuit.lungime_cablu_m}m
              </p>
            </div>
            <div className="flex shrink-0 gap-2">
              <button
                onClick={() => setEditingCircuit(true)}
                className="rounded-md border border-zinc-300 px-3 py-1.5 text-sm hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
              >
                Editează
              </button>
              <button
                onClick={handleDeleteCircuit}
                className="rounded-md px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
              >
                Șterge circuit
              </button>
            </div>
          </div>
        )}
      </div>

      {editingCircuit && (
        <form onSubmit={handleSaveCircuit} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <h2 className="font-medium">Editează circuit</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <input
              required
              value={editNume}
              onChange={(e) => setEditNume(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
            <select
              value={editTip}
              onChange={(e) => setEditTip(e.target.value as TipCircuit)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            >
              <option value="monofazat">Monofazat</option>
              <option value="trifazat">Trifazat</option>
            </select>
            <input
              required
              value={editModPozare}
              onChange={(e) => setEditModPozare(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
            <input
              required
              type="number"
              min={0}
              step="0.1"
              value={editLungime}
              onChange={(e) => setEditLungime(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
          </div>
          <div className="flex gap-2">
            <button
              type="submit"
              disabled={savingCircuit}
              className="rounded-md bg-zinc-900 px-4 py-2 text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
            >
              {savingCircuit ? "Se salvează..." : "Salvează"}
            </button>
            <button
              type="button"
              onClick={() => setEditingCircuit(false)}
              className="rounded-md border border-zinc-300 px-4 py-2 hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
            >
              Anulează
            </button>
          </div>
        </form>
      )}

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
            <table className="w-full min-w-[600px] text-left text-sm">
              <thead className="bg-zinc-50 dark:bg-zinc-900">
                <tr>
                  <th className="px-3 py-2">Nume</th>
                  <th className="px-3 py-2">Tip</th>
                  <th className="px-3 py-2">P (W)</th>
                  <th className="px-3 py-2">cos φ</th>
                  <th className="px-3 py-2">Ku</th>
                  <th className="px-3 py-2">Ks</th>
                  <th className="px-3 py-2"></th>
                </tr>
              </thead>
              <tbody>
                {receptori.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-3 py-3 text-zinc-500">
                      Niciun receptor încă.
                    </td>
                  </tr>
                ) : (
                  receptori.map((r) =>
                    editingReceptorId === r.id ? (
                      <tr key={r.id} className="border-t border-zinc-200 dark:border-zinc-800">
                        <td className="px-2 py-2">
                          <input
                            value={editRNume}
                            onChange={(e) => setEditRNume(e.target.value)}
                            className="w-full rounded-md border border-zinc-300 px-2 py-1 dark:border-zinc-700 dark:bg-zinc-900"
                          />
                        </td>
                        <td className="px-2 py-2">
                          <select
                            value={editRTip}
                            onChange={(e) => setEditRTip(e.target.value as TipReceptor)}
                            className="w-full rounded-md border border-zinc-300 px-2 py-1 dark:border-zinc-700 dark:bg-zinc-900"
                          >
                            <option value="iluminat">Iluminat</option>
                            <option value="priza">Priză</option>
                            <option value="motor">Motor</option>
                            <option value="forta">Forță</option>
                          </select>
                        </td>
                        <td className="px-2 py-2">
                          <input
                            type="number"
                            value={editRPutere}
                            onChange={(e) => setEditRPutere(e.target.value)}
                            className="w-20 rounded-md border border-zinc-300 px-2 py-1 dark:border-zinc-700 dark:bg-zinc-900"
                          />
                        </td>
                        <td className="px-2 py-2">
                          <input
                            type="number"
                            step="0.01"
                            value={editRCosPhi}
                            onChange={(e) => setEditRCosPhi(e.target.value)}
                            className="w-16 rounded-md border border-zinc-300 px-2 py-1 dark:border-zinc-700 dark:bg-zinc-900"
                          />
                        </td>
                        <td className="px-2 py-2">
                          <input
                            type="number"
                            step="0.01"
                            value={editRKu}
                            onChange={(e) => setEditRKu(e.target.value)}
                            className="w-16 rounded-md border border-zinc-300 px-2 py-1 dark:border-zinc-700 dark:bg-zinc-900"
                          />
                        </td>
                        <td className="px-2 py-2">
                          <input
                            type="number"
                            step="0.01"
                            value={editRKs}
                            onChange={(e) => setEditRKs(e.target.value)}
                            className="w-16 rounded-md border border-zinc-300 px-2 py-1 dark:border-zinc-700 dark:bg-zinc-900"
                          />
                        </td>
                        <td className="whitespace-nowrap px-2 py-2">
                          <button
                            onClick={() => handleSaveReceptor(r.id)}
                            disabled={savingReceptor}
                            className="rounded-md bg-zinc-900 px-2 py-1 text-xs text-white hover:bg-zinc-700 disabled:opacity-50 dark:bg-zinc-100 dark:text-zinc-900"
                          >
                            Salvează
                          </button>
                          <button
                            onClick={() => setEditingReceptorId(null)}
                            className="ml-1 rounded-md border border-zinc-300 px-2 py-1 text-xs hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
                          >
                            Anulează
                          </button>
                        </td>
                      </tr>
                    ) : (
                      <tr key={r.id} className="border-t border-zinc-200 dark:border-zinc-800">
                        <td className="px-3 py-2">{r.nume}</td>
                        <td className="px-3 py-2">{r.tip}</td>
                        <td className="px-3 py-2">{r.putere_nominala_w}</td>
                        <td className="px-3 py-2">{r.cos_phi}</td>
                        <td className="px-3 py-2">{r.ku}</td>
                        <td className="px-3 py-2">{r.ks}</td>
                        <td className="whitespace-nowrap px-3 py-2">
                          <button
                            onClick={() => startEditReceptor(r)}
                            className="text-xs text-zinc-500 hover:underline"
                          >
                            Editează
                          </button>
                          <button
                            onClick={() => handleDeleteReceptor(r.id)}
                            className="ml-2 text-xs text-red-600 hover:underline"
                          >
                            Șterge
                          </button>
                        </td>
                      </tr>
                    )
                  )
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

          {circuit && (
            <div className="grid gap-4 rounded-lg border border-zinc-200 p-4 sm:grid-cols-2 dark:border-zinc-800">
              <div>
                <h3 className="mb-1 font-medium">Protecție</h3>
                <p className="mb-2 text-xs text-zinc-500">
                  {circuit.protectie_auto ? "sugerată automat la calcul" : "aleasă manual"}
                </p>
                <select
                  value={circuit.protectie_selectata_id ?? ""}
                  onChange={(e) => e.target.value && handleSelectProtectie(Number(e.target.value))}
                  className="w-full rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
                >
                  <option value="">— alege din catalog —</option>
                  {protectiiCatalog.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.nume}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <h3 className="mb-1 font-medium">Cablu</h3>
                <p className="mb-2 text-xs text-zinc-500">
                  {circuit.cablu_auto ? "sugerat automat la calcul" : "ales manual"}
                </p>
                <select
                  value={circuit.cablu_selectat_id ?? ""}
                  onChange={(e) => e.target.value && handleSelectCablu(Number(e.target.value))}
                  className="w-full rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
                >
                  <option value="">— alege din catalog —</option>
                  {cabluriCatalog.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.nume}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
