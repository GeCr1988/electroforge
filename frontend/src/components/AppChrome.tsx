"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { clearToken } from "@/lib/api";

export default function AppChrome({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  function handleLogout() {
    clearToken();
    router.push("/login");
  }

  return (
    <div className="flex min-h-screen flex-col">
      <header className="flex items-center justify-between border-b border-zinc-200 px-4 py-3 dark:border-zinc-800">
        <Link href="/proiecte" className="text-lg font-semibold">
          Electro-Proiect
        </Link>
        <button
          onClick={handleLogout}
          className="rounded-md border border-zinc-300 px-3 py-1.5 text-sm hover:bg-zinc-100 dark:border-zinc-700 dark:hover:bg-zinc-900"
        >
          Deconectare
        </button>
      </header>

      <main className="flex-1 px-4 py-6 sm:px-6">{children}</main>

      <footer className="border-t border-zinc-200 px-4 py-4 text-xs text-zinc-500 dark:border-zinc-800 dark:text-zinc-400">
        Această aplicație generează documentație tehnică orientativă și nu
        înlocuiește avizarea unui inginer atestat (RTE / proiectant autorizat
        ANRE). Rezultatele trebuie verificate înainte de depunerea oficială a
        proiectului.
      </footer>
    </div>
  );
}
