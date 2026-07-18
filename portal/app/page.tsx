import Link from "next/link";
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export const dynamic = "force-dynamic";

export default async function Home() {
  const { userId } = await auth();

  if (userId) {
    redirect("/dashboard");
  }

  return (
    <div className="flex flex-col flex-1 items-center justify-center bg-radial from-slate-900 via-slate-950 to-black px-6 py-24 text-center">
      <main className="max-w-2xl space-y-8">
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full border border-teal-500/30 bg-teal-500/10 px-4 py-1.5 text-xs font-semibold text-teal-400 backdrop-blur-md">
            ✨ Mobile-First Vendor Access
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl bg-gradient-to-r from-teal-300 via-emerald-400 to-blue-500 bg-clip-text text-transparent py-2">
            We Lift Dispatcher Portal
          </h1>
          <p className="text-base sm:text-lg text-slate-400 max-w-md mx-auto leading-relaxed">
            Securely issue daily gate codes to technicians. Verify community authorizations and track deliveries in real time.
          </p>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/dashboard"
            className="w-full sm:w-auto px-8 py-4 rounded-xl font-bold bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-slate-950 transition-all duration-300 transform hover:scale-[1.02] shadow-lg shadow-teal-500/25 text-center"
          >
            Access Dispatcher Dashboard
          </Link>
        </div>

        <div className="pt-12 grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-xl mx-auto">
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 backdrop-blur-sm text-left">
            <h3 className="font-semibold text-teal-400 mb-2">⚡️ Fast Minting</h3>
            <p className="text-xs text-slate-400 leading-normal">
              Generates secure 6-digit gate codes instantly.
            </p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 backdrop-blur-sm text-left">
            <h3 className="font-semibold text-teal-400 mb-2">📱 Direct SMS</h3>
            <p className="text-xs text-slate-400 leading-normal">
              Sends code and instructions directly to the tech.
            </p>
          </div>
          <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 backdrop-blur-sm text-left">
            <h3 className="font-semibold text-teal-400 mb-2">🔒 Audit logs</h3>
            <p className="text-xs text-slate-400 leading-normal">
              Keeps a secure feed of code delivery history.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
