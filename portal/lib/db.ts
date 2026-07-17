// Uses Node.js built-in sqlite module (available in Node >= 22.5, stable in Node 24+)
// No npm install needed — works with Node 26 out of the box.
import { DatabaseSync } from "node:sqlite";
import path from "path";

const DB_PATH = path.resolve(process.cwd(), "../data/welift.db");

let _db: DatabaseSync | null = null;

export function getDb(): DatabaseSync {
  if (!_db) {
    _db = new DatabaseSync(DB_PATH);
    _db.exec("PRAGMA journal_mode = WAL;");
  }
  return _db;
}

// ── Types ─────────────────────────────────────────────────────────────────────
export interface VendorRow {
  id: number;
  community_name: string;
  company_name: string;
  access_contact_type: string | null;
  access_phone: string | null;
  invite_email: string | null;
  window: string;
  notes: string | null;
  active: number; // 0 or 1
}

export interface CommunityRow {
  id: number;
  name: string;
  timezone: string;
}

export interface CredentialRow {
  id: string;
  community: string;
  company_name: string;
  company_key: string | null;
  last4: string;
  code_hash: string;
  status: string;
  created_at: string;
  valid_until: string;
  created_by: string;
}

export interface DeliveryRow {
  id: string;
  credential_id: string;
  community: string;
  company_name: string;
  to_masked: string;
  channel: string;
  status: string;
  actor: string;
  ts: string;
  last4: string;
  window_override: number;
}

// ── Vendor Companies ──────────────────────────────────────────────────────────
export function getActiveVendors(): VendorRow[] {
  const stmt = getDb().prepare("SELECT * FROM vendor_companies WHERE active = 1");
  const rows = stmt.all() as VendorRow[];
  return JSON.parse(JSON.stringify(rows));
}

// ── Communities ───────────────────────────────────────────────────────────────
export function getCommunity(name: string): CommunityRow | null {
  const stmt = getDb().prepare("SELECT * FROM communities WHERE name = ?");
  const row = stmt.get(name);
  return row ? JSON.parse(JSON.stringify(row)) : null;
}

// ── Credentials ───────────────────────────────────────────────────────────────
export function rotateActiveCredentials(community: string, companyKey: string): void {
  getDb()
    .prepare(
      "UPDATE credentials SET status = 'rotated' WHERE status = 'active' AND community = ? AND company_key = ?"
    )
    .run(community, companyKey);
}

export function insertCredential(cred: CredentialRow): void {
  getDb()
    .prepare(
      `INSERT INTO credentials (id, community, company_name, company_key, last4, code_hash, status, created_at, valid_until, created_by)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .run(
      cred.id, cred.community, cred.company_name, cred.company_key,
      cred.last4, cred.code_hash, cred.status, cred.created_at,
      cred.valid_until, cred.created_by
    );
}

// ── Deliveries ────────────────────────────────────────────────────────────────
export function insertDelivery(delivery: DeliveryRow): void {
  getDb()
    .prepare(
      `INSERT INTO deliveries (id, credential_id, community, company_name, to_masked, channel, status, actor, ts, last4, window_override)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
    )
    .run(
      delivery.id, delivery.credential_id, delivery.community, delivery.company_name,
      delivery.to_masked, delivery.channel, delivery.status, delivery.actor,
      delivery.ts, delivery.last4, delivery.window_override
    );
}

export function getRecentDeliveries(companyNames: string[], limit = 20): DeliveryRow[] {
  if (companyNames.length === 0) return [];
  const placeholders = companyNames.map(() => "?").join(", ");
  const stmt = getDb().prepare(
    `SELECT id, credential_id, community, company_name, to_masked, channel, status, actor, ts, last4, window_override
     FROM deliveries
     WHERE company_name IN (${placeholders})
     ORDER BY ts DESC
     LIMIT ${limit}`
  );
  const rows = stmt.all(...companyNames);
  return JSON.parse(JSON.stringify(rows));
}
