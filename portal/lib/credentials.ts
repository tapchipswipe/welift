import crypto from "crypto";
import twilio from "twilio";
import prisma from "./prisma";

const WINDOW_REGEX = /^([A-Za-z,\-\s]+)\s+(\d{1,2}:\d{2})\s*-\s*(\d{1,2}:\d{2})$/;

const DAY_ALIASES: Record<string, number> = {
  mon: 0, monday: 0,
  tue: 1, tues: 1, tuesday: 1,
  wed: 2, wednesday: 2,
  thu: 3, thur: 3, thurs: 3, thursday: 3,
  fri: 4, friday: 4,
  sat: 5, saturday: 5,
  sun: 6, sunday: 6,
};

export function normalizeCompany(name: string): string {
  return (name || "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

export function hashCode(code: string): string {
  return crypto.createHash("sha256").update(code, "utf-8").digest("hex");
}

export function maskPhone(phone: string): string {
  const digits = (phone || "").replace(/\D/g, "");
  if (digits.length < 4) {
    return "····";
  }
  return `···${digits.slice(-4)}`;
}

export function ensureE164(phone: string): string {
  const raw = (phone || "").trim();
  const digits = raw.replace(/\D/g, "");
  if (digits.length === 10) {
    return "+1" + digits;
  }
  if (digits.length === 11 && digits.startsWith("1")) {
    return "+" + digits;
  }
  if (raw.startsWith("+")) {
    return raw;
  }
  throw new Error("Phone must be E.164 or 10-digit US number");
}

export function parseDays(daysPart: string): Set<number> {
  const normalized = daysPart.trim().toLowerCase().replace(/\s+/g, "");
  const allDays = new Set([0, 1, 2, 3, 4, 5, 6]);
  if (!normalized || ["daily", "everyday", "as-needed", "asneeded", "any"].includes(normalized)) {
    return allDays;
  }
  const out = new Set<number>();
  const chunks = normalized.split(",");
  for (const chunk of chunks) {
    if (chunk.includes("-") && !chunk.startsWith("-")) {
      const parts = chunk.split("-", 2);
      const a = parts[0];
      const b = parts[1];
      if (a in DAY_ALIASES && b in DAY_ALIASES) {
        const start = DAY_ALIASES[a];
        const end = DAY_ALIASES[b];
        if (start <= end) {
          for (let i = start; i <= end; i++) out.add(i);
        } else {
          for (let i = start; i <= 6; i++) out.add(i);
          for (let i = 0; i <= end; i++) out.add(i);
        }
        continue;
      }
    }
    if (chunk in DAY_ALIASES) {
      out.add(DAY_ALIASES[chunk]);
    }
  }
  return out.size > 0 ? out : allDays;
}

export function getLocalTimeInfo(date: Date, timeZone: string) {
  const options: Intl.DateTimeFormatOptions = {
    timeZone,
    year: "numeric",
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
    second: "numeric",
    weekday: "short",
    hour12: false,
  };
  const formatter = new Intl.DateTimeFormat("en-US", options);
  const parts = formatter.formatToParts(date);
  
  let year = 2026, month = 1, day = 1, hour = 0, minute = 0, second = 0, weekdayStr = "Mon";
  for (const part of parts) {
    if (part.type === "year") year = parseInt(part.value, 10);
    if (part.type === "month") month = parseInt(part.value, 10);
    if (part.type === "day") day = parseInt(part.value, 10);
    if (part.type === "hour") hour = parseInt(part.value, 10);
    if (part.type === "minute") minute = parseInt(part.value, 10);
    if (part.type === "second") second = parseInt(part.value, 10);
    if (part.type === "weekday") weekdayStr = part.value;
  }
  
  const cleanWeekday = weekdayStr.toLowerCase().replace(/\./g, "").slice(0, 3);
  const weekdayMap: Record<string, number> = {
    mon: 0, tue: 1, wed: 2, thu: 3, fri: 4, sat: 5, sun: 6
  };
  const weekday = weekdayMap[cleanWeekday] ?? 0;
  
  return { year, month, day, hour, minute, second, weekday };
}

export function localDateTimeToUTC(
  year: number,
  month: number,
  day: number,
  hour: number,
  minute: number,
  second: number,
  timeZone: string
): Date {
  let date = new Date(Date.UTC(year, month - 1, day, hour, minute, second));
  for (let i = 0; i < 5; i++) {
    const info = getLocalTimeInfo(date, timeZone);
    const diffMs = 
      Date.UTC(info.year, info.month - 1, info.day, info.hour, info.minute, info.second) -
      Date.UTC(year, month - 1, day, hour, minute, second);
    if (diffMs === 0) break;
    date = new Date(date.getTime() - diffMs);
  }
  return date;
}

export function getEndOfLocalDay(tzName: string = "America/New_York"): Date {
  const local = getLocalTimeInfo(new Date(), tzName);
  return localDateTimeToUTC(local.year, local.month, local.day, 23, 59, 59, tzName);
}

export function getWindowEndToday(vendor: any, tzName: string): Date {
  if (!vendor) {
    return getEndOfLocalDay(tzName);
  }
  const windowStr = (vendor.window || "").trim();
  const match = windowStr.match(WINDOW_REGEX);
  if (!match) {
    return getEndOfLocalDay(tzName);
  }
  try {
    const endPart = match[3];
    const [eh, em] = endPart.split(":").map(Number);
    const local = getLocalTimeInfo(new Date(), tzName);
    
    let endLocal = localDateTimeToUTC(local.year, local.month, local.day, eh, em, 0, tzName);
    const now = new Date();
    if (endLocal.getTime() < now.getTime()) {
      endLocal = new Date(endLocal.getTime() + 24 * 60 * 60 * 1000);
    }
    return endLocal;
  } catch (error) {
    return getEndOfLocalDay(tzName);
  }
}

export function vendorWindowAllows(
  vendor: any,
  when: Date = new Date(),
  tzName: string = "America/New_York"
): { ok: boolean; reason: string; window?: string; local?: string } {
  if (!vendor) {
    return { ok: true, reason: "unknown_vendor_no_window" };
  }
  const windowStr = (vendor.window || "").trim();
  if (!windowStr || ["as-needed", "as needed", "any", "always"].includes(windowStr.toLowerCase())) {
    return { ok: true, reason: "as_needed" };
  }

  const match = windowStr.match(WINDOW_REGEX);
  if (!match) {
    return { ok: true, reason: "unparsed_window", window: windowStr };
  }

  const daysPart = match[1];
  const startPart = match[2];
  const endPart = match[3];

  const local = getLocalTimeInfo(when, tzName);
  const days = parseDays(daysPart);

  if (!days.has(local.weekday)) {
    return {
      ok: false,
      reason: "outside_days",
      window: windowStr,
      local: when.toISOString(),
    };
  }

  const [sh, sm] = startPart.split(":").map(Number);
  const [eh, em] = endPart.split(":").map(Number);
  
  const minutes = local.hour * 60 + local.minute;
  const startM = sh * 60 + sm;
  const endM = eh * 60 + em;

  let inHours = false;
  if (startM <= endM) {
    inHours = minutes >= startM && minutes <= endM;
  } else {
    inHours = minutes >= startM || minutes <= endM;
  }

  if (!inHours) {
    return {
      ok: false,
      reason: "outside_hours",
      window: windowStr,
      local: when.toISOString(),
    };
  }

  return { ok: true, reason: "in_window", window: windowStr };
}

export async function findVendor(companyName: string, includeInactive = false) {
  const normName = normalizeCompany(companyName);
  if (!normName) return null;
  const vendors = await prisma.vendorCompany.findMany();
  for (const v of vendors) {
    const cn = normalizeCompany(v.company_name);
    if (cn === normName || normName.includes(cn) || cn.includes(normName)) {
      if (!includeInactive && !v.active) {
        return null;
      }
      return v;
    }
  }
  return null;
}

export async function mintCredential({
  community,
  companyName,
  hoursValid,
  actor = "system",
}: {
  community: string;
  companyName: string;
  hoursValid?: number;
  actor?: string;
}) {
  const cleanCommunity = (community || "The Inlets").trim();
  const cleanCompanyName = (companyName || "").trim();
  if (!cleanCompanyName) {
    throw new Error("company_name required");
  }

  const vendor = await findVendor(cleanCompanyName);
  const displayCompany = vendor ? vendor.company_name : cleanCompanyName;

  const comm = await prisma.community.findUnique({
    where: { name: cleanCommunity },
  });
  const tz = comm ? comm.timezone : "America/New_York";

  const rand = crypto.randomInt(0, 1000000);
  const code = rand.toString().padStart(6, "0");

  const now = new Date();
  let expires: Date;
  if (hoursValid !== undefined && hoursValid !== null) {
    expires = new Date(now.getTime() + hoursValid * 60 * 60 * 1000);
  } else {
    expires = getWindowEndToday(vendor, tz);
  }

  const norm = normalizeCompany(displayCompany);

  // Rotate existing active credentials
  await prisma.credential.updateMany({
    where: {
      status: "active",
      community: cleanCommunity,
      company_key: norm,
    },
    data: {
      status: "rotated",
    },
  });

  const credId = crypto.randomBytes(8).toString("hex");
  const newCred = await prisma.credential.create({
    data: {
      id: credId,
      community: cleanCommunity,
      company_name: displayCompany,
      company_key: norm,
      code_hash: hashCode(code),
      last4: code.slice(-4),
      status: "active",
      created_at: now,
      valid_until: expires,
      created_by: actor,
    },
  });

  return {
    id: credId,
    community: cleanCommunity,
    company_name: displayCompany,
    company_key: norm,
    last4: code.slice(-4),
    status: "active",
    created_at: now.toISOString(),
    valid_until: expires.toISOString(),
    created_by: actor,
    code,
  };
}

export async function sendSms(toPhone: string, body: string): Promise<any> {
  const to = ensureE164(toPhone);
  const accountSid = process.env.TWILIO_ACCOUNT_SID || "";
  const authToken = process.env.TWILIO_AUTH_TOKEN || "";
  const fromNumber = process.env.TWILIO_FROM_NUMBER || "";
  const isConfigured = 
    accountSid && 
    authToken && 
    fromNumber && 
    !accountSid.includes("xxxxxxxx") &&
    !accountSid.includes("mock");

  if (isConfigured) {
    try {
      const client = twilio(accountSid, authToken);
      const msg = await client.messages.create({
        body,
        from: fromNumber,
        to,
      });
      return {
        channel: "twilio",
        status: "sent",
        sid: msg.sid,
        to,
        to_masked: maskPhone(to),
      };
    } catch (error: any) {
      console.error("Twilio send failed:", error);
      return {
        channel: "twilio",
        status: "error",
        error: error.message || String(error),
        to,
        to_masked: maskPhone(to),
      };
    }
  } else {
    console.log(`SMS (log-only) → ${maskPhone(to)} | ${body.replace(/\n/g, " | ")}`);
    return {
      channel: "log",
      status: "logged",
      to,
      to_masked: maskPhone(to),
      body,
    };
  }
}

export async function sendCode({
  community,
  companyName,
  phone,
  actor = "access_ui",
  overrideWindow = false,
}: {
  community: string;
  companyName: string;
  phone?: string;
  actor?: string;
  overrideWindow?: boolean;
}) {
  const cleanCommunity = (community || "The Inlets").trim();
  const cleanCompanyName = (companyName || "").trim();

  const vendor = await findVendor(cleanCompanyName);
  if (vendor && vendor.active === false) {
    throw new Error("Vendor is deactivated — reactivate before sending a code");
  }

  const windowCheck = vendorWindowAllows(vendor);
  if (!windowCheck.ok && !overrideWindow) {
    throw new Error(
      `Outside authorized window (${windowCheck.window}). Pass override_window=true for CAM emergency send.`
    );
  }

  const toRaw = (phone || "").trim() || (vendor ? vendor.access_phone : "") || "";
  const to = ensureE164(toRaw);

  const minted = await mintCredential({
    community: cleanCommunity,
    companyName: cleanCompanyName,
    actor,
  });

  const code = minted.code;
  const untilUtc = minted.valid_until;
  const contact = vendor ? vendor.access_contact_type : "access";

  const body = 
    `${cleanCommunity} — ${minted.company_name} vendor access\n` +
    `Keypad code: ${code}\n` +
    `Valid until (UTC): ${untilUtc}\n` +
    `If keypad fails: Call Attendant, say company + this PIN.\n` +
    `(Sent to ${contact} contact)`;

  const sms = await sendSms(to, body);

  const deliveryId = crypto.randomBytes(6).toString("hex");
  await prisma.delivery.create({
    data: {
      id: deliveryId,
      credential_id: minted.id,
      community: cleanCommunity,
      company_name: minted.company_name,
      to_masked: sms.to_masked,
      channel: sms.channel,
      status: sms.status,
      actor,
      ts: new Date(),
      last4: minted.last4,
      window_override: overrideWindow,
    },
  });

  return {
    ok: ["sent", "logged"].includes(sms.status),
    community: cleanCommunity,
    company_name: minted.company_name,
    last4: minted.last4,
    valid_until: minted.valid_until,
    credential_id: minted.id,
    sms,
    code,
  };
}
