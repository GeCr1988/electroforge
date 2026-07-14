"use client";

import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { api, BomResponse, Proiect, Tablou, TipCladire } from "@/lib/api";

export default function ProiectDetailPage() {
  const params = useParams<{ id: string }>();
  const router = useRouter();
  const proiectId = Number(params.id);

  const [proiect, setProiect] = useState<Proiect | null>(null);
  const [tablouri, setTablouri] = useState<Tablou[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [nume, setNume] = useState("");
  const [creating, setCreating] = useState(false);

  const [editing, setEditing] = useState(false);
  const [editNume, setEditNume] = useState("");
  const [editBeneficiar, setEditBeneficiar] = useState("");
  const [editTipCladire, setEditTipCladire] = useState<TipCladire>("rezidential");
  const [editAdresa, setEditAdresa] = useState("");
  const [savingEdit, setSavingEdit] = useState(false);

  const [schemaSvgUrl, setSchemaSvgUrl] = useState<string | null>(null);
  const [bom, setBom] = useState<BomResponse | null>(null);

  function incarca() {
    Promise.all([api.obtineProiect(proiectId), api.listaTablouri(proiectId)])
      .then(([p, t]) => {
        setProiect(p);
        setTablouri(t);
        setEditNume(p.nume);
        setEditBeneficiar(p.beneficiar);
        setEditTipCladire(p.tip_cladire);
        setEditAdresa(p.adresa ?? "");
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Eroare la încărcare"))
      .finally(() => setLoading(false));
  }

  useEffect(incarca, [proiectId]);

  useEffect(() => {
    let url: string | null = null;
    api
      .schemaMonofilaraBlobUrl(proiectId)
      .then((u) => {
        url = u;
        setSchemaSvgUrl(u);
      })
      .catch(() => setSchemaSvgUrl(null));
    return () => {
      if (url) URL.revokeObjectURL(url);
    };
  }, [proiectId, tablouri]);

  useEffect(() => {
    api.obtineBom(proiectId).then(setBom).catch(() => setBom(null));
  }, [proiectId, tablouri]);

  async function handleDownloadBom() {
    try {
      await api.descarcaBomCsv(proiectId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la descărcare BOM");
    }
  }

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

  async function handleSaveEdit(e: React.FormEvent) {
    e.preventDefault();
    setSavingEdit(true);
    setError(null);
    try {
      await api.actualizeazaProiect(proiectId, {
        nume: editNume,
        beneficiar: editBeneficiar,
        tip_cladire: editTipCladire,
        adresa: editAdresa || null,
      });
      setEditing(false);
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la salvare");
    } finally {
      setSavingEdit(false);
    }
  }

  async function handleDeleteProiect() {
    if (!window.confirm("Ștergi acest proiect? Toate tablourile/circuitele/receptorii lui se șterg definitiv.")) return;
    try {
      await api.stergeProiect(proiectId);
      router.push("/proiecte");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
    }
  }

  async function handleDeleteTablou(tabloulId: number) {
    if (!window.confirm("Ștergi acest tablou? Toate circuitele/receptorii lui se șterg definitiv.")) return;
    try {
      await api.stergeTablou(tabloulId);
      incarca();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la ștergere");
    }
  }

  async function handleDownloadBreviar() {
    try {
      await api.descarcaBreviarPdf(proiectId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Eroare la descărcare breviar");
    }
  }

  if (loading) return <p className="text-zinc-500">Se încarcă...</p>;

  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <div>
        <Link href="/proiecte" className="text-sm text-zinc-500 hover:underline">
          ← Toate proiectele
        </Link>
        {proiect && !editing && (
          <div className="mt-1 flex items-start justify-between gap-2">
            <div>
              <h1 className="text-xl font-semibold">{proiect.nume}</h1>
              <p className="text-sm text-zinc-500">
                {proiect.beneficiar} · {proiect.tip_cladire} · {proiect.tensiune_alimentare}
                {proiect.adresa ? ` · ${proiect.adresa}` : ""}
              </p>
            </div>
            <div className="flex shrink-0 flex-wrap justify-end gap-2">
              <button
                onClick={handleDownloadBreviar}
                className="rounded-md border border-zinc-300 px-3 py-1.5 text-sm hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
              >
                Descarcă breviar PDF
              </button>
              <button
                onClick={() => setEditing(true)}
                className="rounded-md border border-zinc-300 px-3 py-1.5 text-sm hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
              >
                Editează
              </button>
              <button
                onClick={handleDeleteProiect}
                className="rounded-md px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
              >
                Șterge proiect
              </button>
            </div>
          </div>
        )}
      </div>

      {editing && (
        <form onSubmit={handleSaveEdit} className="space-y-3 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <h2 className="font-medium">Editează proiect</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <input
              required
              placeholder="Nume proiect"
              value={editNume}
              onChange={(e) => setEditNume(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
            <input
              required
              placeholder="Beneficiar"
              value={editBeneficiar}
              onChange={(e) => setEditBeneficiar(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
            <select
              value={editTipCladire}
              onChange={(e) => setEditTipCladire(e.target.value as TipCladire)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            >
              <option value="rezidential">Rezidențial</option>
              <option value="industrial">Industrial</option>
            </select>
            <input
              placeholder="Adresă (opțional)"
              value={editAdresa}
              onChange={(e) => setEditAdresa(e.target.value)}
              className="rounded-md border border-zinc-300 px-3 py-2 dark:border-zinc-700 dark:bg-zinc-900"
            />
          </div>
          <div className="flex gap-2">
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
          </div>
        </form>
      )}

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
            <li key={t.id} className="flex items-center justify-between gap-2 px-4 py-3 hover:bg-zinc-50 dark:hover:bg-zinc-900">
              <Link href={`/tablouri/${t.id}`} className="flex flex-1 flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                <span className="font-medium">{t.nume}</span>
                <span className="text-sm text-zinc-500">
                  Pi: {t.putere_instalata != null ? `${t.putere_instalata.toFixed(0)} W` : "—"} · Pc:{" "}
                  {t.putere_calcul != null ? `${t.putere_calcul.toFixed(0)} W` : "—"}
                </span>
              </Link>
              <button
                onClick={() => handleDeleteTablou(t.id)}
                className="shrink-0 rounded-md px-2 py-1 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-red-950"
              >
                Șterge
              </button>
            </li>
          ))}
        </ul>
      )}

      {schemaSvgUrl && (
        <div className="space-y-2 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <div className="flex items-center justify-between">
            <h2 className="font-medium">Schemă monofilară</h2>
            <a
              href={schemaSvgUrl}
              download={`schema-monofilara-${proiectId}.svg`}
              className="text-sm text-zinc-500 hover:underline"
            >
              Descarcă SVG
            </a>
          </div>
          <div className="overflow-x-auto">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src={schemaSvgUrl} alt="Schemă monofilară" className="min-w-[400px]" />
          </div>
        </div>
      )}

      {bom && (
        <div className="space-y-2 rounded-lg border border-zinc-200 p-4 dark:border-zinc-800">
          <div className="flex items-center justify-between">
            <h2 className="font-medium">Listă de materiale (BOM)</h2>
            {bom.linii.length > 0 && (
              <button onClick={handleDownloadBom} className="text-sm text-zinc-500 hover:underline">
                Descarcă CSV
              </button>
            )}
          </div>
          {bom.linii.length === 0 ? (
            <p className="text-sm text-zinc-500">
              Niciun material selectat încă — alege protecții/cabluri/componente din catalog pe circuite și receptori.
            </p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full min-w-[500px] text-left text-sm">
                <thead className="bg-zinc-50 dark:bg-zinc-900">
                  <tr>
                    <th className="px-3 py-2">Denumire</th>
                    <th className="px-3 py-2">Categorie</th>
                    <th className="px-3 py-2">Cantitate</th>
                    <th className="px-3 py-2">Preț unitar</th>
                    <th className="px-3 py-2">Cost total</th>
                  </tr>
                </thead>
                <tbody>
                  {bom.linii.map((l) => (
                    <tr key={l.componenta_id} className="border-t border-zinc-200 dark:border-zinc-800">
                      <td className="px-3 py-2">{l.nume}</td>
                      <td className="px-3 py-2">{l.categorie}</td>
                      <td className="px-3 py-2">
                        {l.cantitate_totala} {l.unitate_masura}
                      </td>
                      <td className="px-3 py-2">{l.pret_estimativ != null ? l.pret_estimativ.toFixed(2) : "—"}</td>
                      <td className="px-3 py-2">{l.cost_total != null ? l.cost_total.toFixed(2) : "—"}</td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr className="border-t border-zinc-300 font-medium dark:border-zinc-700">
                    <td className="px-3 py-2" colSpan={4}>
                      Total general
                    </td>
                    <td className="px-3 py-2">{bom.cost_total_general.toFixed(2)}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
