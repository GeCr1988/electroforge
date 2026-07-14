"use client";

import AppChrome from "@/components/AppChrome";
import { useRequireAuth } from "@/lib/useAuth";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const { ready } = useRequireAuth();

  if (!ready) {
    return (
      <div className="flex min-h-screen items-center justify-center text-zinc-500">
        Se încarcă...
      </div>
    );
  }

  return <AppChrome>{children}</AppChrome>;
}
