import { getDispatcherContext } from "../actions";
import { UserButton } from "@clerk/nextjs";
import DashboardClient from "./dashboard-client";
import Link from "next/link";

export const dynamic = "force-dynamic";

export default async function DashboardPage() {
  const context = await getDispatcherContext();

  if (!context.authenticated) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 p-6 text-center">
        <div className="space-y-4">
          <p className="text-slate-400">Redirecting to sign-in...</p>
        </div>
      </div>
    );
  }

  if (!context.authorized) {
    if ("serviceUnavailable" in context && context.serviceUnavailable) {
      return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-radial from-slate-900 to-slate-950 p-6 text-center">
          <div className="w-full max-w-md rounded-2xl border border-amber-500/20 bg-amber-950/10 p-8 backdrop-blur-md shadow-2xl">
            <h1 className="text-2xl font-bold text-slate-100 mb-2">Dashboard Unavailable</h1>
            <p className="text-slate-400 text-sm mb-6 leading-relaxed">
              We couldn&apos;t load your dashboard data right now. Please try again shortly.
            </p>
            <Link
              href="/"
              className="text-xs text-slate-500 hover:text-slate-400 underline transition-colors"
            >
              Back to Home
            </Link>
          </div>
        </div>
      );
    }

    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-radial from-slate-900 to-slate-950 p-6 text-center">
        <div className="w-full max-w-md rounded-2xl border border-rose-500/20 bg-rose-950/10 p-8 backdrop-blur-md shadow-2xl">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-rose-500/10 text-rose-500 mb-6">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth={1.5}
              stroke="currentColor"
              className="h-8 w-8"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z"
              />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-slate-100 mb-2">Access Denied</h1>
          <p className="text-slate-400 text-sm mb-6 leading-relaxed">
            The email <span className="font-mono text-rose-400 bg-rose-500/10 px-1.5 py-0.5 rounded">{context.email || "on your account"}</span> is not linked to any active vendor company in our system.
          </p>
          <div className="flex flex-col gap-3">
            <div className="flex justify-center bg-slate-900 border border-slate-800 rounded-xl p-3">
              <UserButton showName />
            </div>
            <Link
              href="/"
              className="mt-4 text-xs text-slate-500 hover:text-slate-400 underline transition-colors"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Find the primary company name to display in headers
  const primaryCompany = context.companies && context.companies.length > 0
    ? context.companies[0].vendor.company_name
    : "Vendor Company";

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      {/* Header bar */}
      <header className="sticky top-0 z-10 border-b border-slate-900 bg-slate-950/80 backdrop-blur-md px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-teal-500/10 text-teal-400 font-bold">
            WL
          </div>
          <div>
            <h1 className="font-bold text-sm leading-tight bg-gradient-to-r from-teal-400 to-blue-500 bg-clip-text text-transparent">
              {primaryCompany}
            </h1>
            <p className="text-[10px] text-slate-500">Vendor Portal</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <UserButton
            appearance={{
              elements: {
                userButtonAvatarBox: "h-8 w-8 ring-2 ring-teal-500/20",
              },
            }}
          />
        </div>
      </header>

      {/* Main dashboard client area */}
      <main className="flex-1 w-full max-w-lg mx-auto p-4 space-y-6">
        <DashboardClient
          initialCompanies={context.companies || []}
          initialDeliveries={context.deliveries || []}
        />
      </main>
    </div>
  );
}
