"use client";

import { useState } from "react";
import { sendCodeAction } from "../actions";

interface CompanyContext {
  vendor: {
    id: number;
    company_name: string;
    community_name: string;
    access_contact_type: string;
    access_phone: string | null;
    invite_email: string | null;
    window: string;
    notes: string | null;
    active: boolean;
  };
  communityName: string;
  timezone: string;
  window: string;
  isAuthorizedToday: boolean;
  reason: string;
}

interface DeliveryItem {
  id: string;
  community: string;
  companyName: string;
  toMasked: string;
  channel: string;
  status: string;
  technicianName: string;
  timestamp: string;
  last4: string;
}

interface DashboardClientProps {
  initialCompanies: CompanyContext[];
  initialDeliveries: DeliveryItem[];
}

export default function DashboardClient({
  initialCompanies,
  initialDeliveries,
}: DashboardClientProps) {
  const [companies] = useState<CompanyContext[]>(initialCompanies);
  const [deliveries, setDeliveries] = useState<DeliveryItem[]>(initialDeliveries);

  // Form states
  const [selectedCommunity, setSelectedCommunity] = useState(
    companies.length > 0 ? companies[0].communityName : ""
  );
  const [technicianName, setTechnicianName] = useState("");
  const [phone, setPhone] = useState("");
  
  // Interaction states
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [successData, setSuccessData] = useState<{
    code: string;
    last4: string;
    validUntil: string;
    smsStatus: string;
    community: string;
  } | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    setSuccessData(null);
    setIsSubmitting(true);

    try {
      const res = await sendCodeAction({
        communityName: selectedCommunity,
        technicianName,
        phone,
      });

      if (!res.success) {
        setErrorMsg(res.error || "Failed to send gate code.");
        setIsSubmitting(false);
        return;
      }

      if (res.result) {
        setSuccessData({
          code: res.result.code,
          last4: res.result.last4,
          validUntil: res.result.validUntil,
          smsStatus: res.result.smsStatus,
          community: res.result.community,
        });

        // Prepend new delivery log locally to the audit feed
        const newDelivery: DeliveryItem = {
          id: Math.random().toString(36).substring(2, 8),
          community: res.result.community,
          companyName: res.result.companyName,
          toMasked: phone.length > 4 ? `···${phone.slice(-4)}` : "····",
          channel: res.result.smsStatus === "logged" ? "log" : "twilio",
          status: res.result.smsStatus,
          technicianName,
          timestamp: new Date().toISOString(),
          last4: res.result.last4,
        };

        setDeliveries((prev) => [newDelivery, ...prev.slice(0, 19)]);
        
        // Reset form inputs except name if dispatching multiple codes
        setPhone("");
      }
    } catch (err: any) {
      setErrorMsg(err.message || "An unexpected error occurred.");
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleReset = () => {
    setSuccessData(null);
    setErrorMsg(null);
  };

  const formatTimestamp = (isoString: string) => {
    try {
      const date = new Date(isoString);
      return date.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
      }) + " • " + date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      });
    } catch (e) {
      return isoString;
    }
  };

  return (
    <div className="space-y-6">
      {/* 1. TODAY FEED */}
      <section className="space-y-3">
        <h2 className="text-xs font-semibold tracking-wider text-slate-500 uppercase">
          Today's Community Access
        </h2>
        <div className="grid gap-3">
          {companies.map((c, idx) => (
            <div
              key={idx}
              className={`rounded-xl border p-4 bg-slate-900/40 backdrop-blur-sm flex items-center justify-between transition-colors ${
                c.isAuthorizedToday
                  ? "border-teal-500/20"
                  : "border-slate-800"
              }`}
            >
              <div className="space-y-1">
                <h3 className="font-semibold text-slate-200 text-sm">
                  {c.communityName}
                </h3>
                <p className="text-xs text-slate-400">
                  Window: <span className="font-medium text-slate-300">{c.window}</span>
                </p>
              </div>
              <div>
                {c.isAuthorizedToday ? (
                  <span className="inline-flex items-center gap-1 rounded-full bg-teal-500/10 px-2.5 py-0.5 text-xs font-medium text-teal-400">
                    <span className="h-1.5 w-1.5 rounded-full bg-teal-400 animate-pulse" />
                    Authorized
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 rounded-full bg-slate-800 px-2.5 py-0.5 text-xs font-medium text-slate-400">
                    Closed Today
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 2. ASSIGN & SEND */}
      <section className="space-y-3">
        <h2 className="text-xs font-semibold tracking-wider text-slate-500 uppercase">
          Assign & Send Code
        </h2>

        {successData ? (
          /* SUCCESS VIEW */
          <div className="rounded-2xl border border-teal-500/30 bg-teal-950/10 p-6 backdrop-blur-md text-center space-y-5 animate-in fade-in-50 duration-200">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-teal-500/10 text-teal-400">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={2}
                stroke="currentColor"
                className="h-6 w-6"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M4.5 12.75l6 6 9-13.5"
                />
              </svg>
            </div>

            <div className="space-y-2">
              <h3 className="text-lg font-bold text-slate-200">
                Gate Code Dispatched!
              </h3>
              <p className="text-xs text-slate-400 px-4">
                SMS delivered to technician via{" "}
                <span className="font-mono text-teal-400 font-semibold uppercase">
                  {successData.smsStatus}
                </span>
                .
              </p>
            </div>

            <div className="py-4 bg-slate-950/60 rounded-xl border border-slate-900 max-w-xs mx-auto space-y-1">
              <div className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">
                Minted Keypad Code
              </div>
              <div className="text-4xl font-extrabold font-mono tracking-widest text-teal-400">
                {successData.code}
              </div>
            </div>

            <div className="text-xs text-slate-400 space-y-1">
              <p>
                Community: <span className="font-medium text-slate-200">{successData.community}</span>
              </p>
              <p>
                Expires: <span className="font-mono text-slate-300">{new Date(successData.validUntil).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })} (Local)</span>
              </p>
            </div>

            <button
              onClick={handleReset}
              className="w-full py-3 rounded-xl font-bold bg-slate-900 border border-slate-800 hover:bg-slate-800/80 text-slate-200 transition-colors"
            >
              Send Another Code
            </button>
          </div>
        ) : (
          /* FORM VIEW */
          <form
            onSubmit={handleSubmit}
            className="rounded-2xl border border-slate-900 bg-slate-900/20 p-5 backdrop-blur-sm space-y-4"
          >
            {errorMsg && (
              <div className="rounded-xl bg-rose-500/10 border border-rose-500/20 p-3 text-xs text-rose-400 leading-relaxed">
                {errorMsg}
              </div>
            )}

            {/* Select Community */}
            <div className="space-y-1.5">
              <label htmlFor="community" className="text-xs font-semibold text-slate-400">
                Community
              </label>
              <select
                id="community"
                value={selectedCommunity}
                onChange={(e) => setSelectedCommunity(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-3 text-sm text-slate-200 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
              >
                {companies.map((c, idx) => (
                  <option key={idx} value={c.communityName} disabled={!c.isAuthorizedToday}>
                    {c.communityName} {!c.isAuthorizedToday ? "(Unauthorized today)" : ""}
                  </option>
                ))}
              </select>
            </div>

            {/* Technician Name */}
            <div className="space-y-1.5">
              <label htmlFor="techName" className="text-xs font-semibold text-slate-400">
                Technician Name
              </label>
              <input
                id="techName"
                type="text"
                required
                value={technicianName}
                onChange={(e) => setTechnicianName(e.target.value)}
                placeholder="e.g. John Doe"
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
              />
            </div>

            {/* Technician Phone */}
            <div className="space-y-1.5">
              <label htmlFor="phone" className="text-xs font-semibold text-slate-400">
                Technician Phone
              </label>
              <input
                id="phone"
                type="tel"
                required
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="e.g. (941) 555-0199 or +19415550199"
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-3.5 py-3 text-sm text-slate-200 placeholder:text-slate-600 focus:border-teal-500 focus:outline-none focus:ring-1 focus:ring-teal-500"
              />
              <p className="text-[10px] text-slate-500">
                US 10-digit number or E.164 international format.
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isSubmitting || !selectedCommunity}
              className="w-full py-3.5 rounded-xl font-bold bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-slate-950 transition-all duration-300 disabled:opacity-50 disabled:pointer-events-none shadow-lg shadow-teal-500/10 flex items-center justify-center gap-2"
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-slate-950" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Minting & Sending Code...
                </>
              ) : (
                "Mint & Send Gate Code"
              )}
            </button>
          </form>
        )}
      </section>

      {/* 3. AUDIT FEED */}
      <section className="space-y-3">
        <h2 className="text-xs font-semibold tracking-wider text-slate-500 uppercase flex items-center justify-between">
          <span>Audit Log (Last 20)</span>
          <span className="text-[10px] text-slate-600 normal-case">Updates in real-time</span>
        </h2>

        <div className="rounded-2xl border border-slate-900 bg-slate-900/10 overflow-hidden divide-y divide-slate-900/80">
          {deliveries.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-600">
              No code delivery history for this company.
            </div>
          ) : (
            deliveries.map((item, idx) => (
              <div
                key={item.id || idx}
                className="p-4 flex items-start justify-between bg-slate-950/20 hover:bg-slate-900/10 transition-colors"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-200 text-sm">
                      {item.technicianName}
                    </span>
                    <span className="text-xs font-mono text-slate-500">
                      {item.toMasked}
                    </span>
                  </div>
                  <div className="flex items-center gap-1.5 text-xs text-slate-500">
                    <span>{item.community}</span>
                    <span>•</span>
                    <span className="font-mono bg-slate-900 text-slate-400 px-1 py-0.2 rounded text-[10px]">
                      PIN *{item.last4}
                    </span>
                  </div>
                  <p className="text-[10px] text-slate-600">
                    {formatTimestamp(item.timestamp)}
                  </p>
                </div>
                <div>
                  {item.status === "sent" ? (
                    <span className="inline-flex rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400 border border-emerald-500/15">
                      Sent
                    </span>
                  ) : item.status === "logged" ? (
                    <span className="inline-flex rounded-full bg-blue-500/10 px-2 py-0.5 text-[10px] font-medium text-blue-400 border border-blue-500/15">
                      Logged
                    </span>
                  ) : (
                    <span className="inline-flex rounded-full bg-rose-500/10 px-2 py-0.5 text-[10px] font-medium text-rose-400 border border-rose-500/15" title={item.status}>
                      Failed
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  );
}
