import prisma from "./prisma";

export interface VendorRow {
  id: number;
  community_name: string;
  company_name: string;
  access_contact_type: string;
  access_phone: string | null;
  invite_email: string | null;
  window: string;
  notes: string | null;
  active: boolean;
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
export async function getActiveVendors(): Promise<VendorRow[]> {
  const vendors = await prisma.vendorCompany.findMany({
    where: { active: true },
  });
  return vendors as unknown as VendorRow[];
}

// ── Communities ───────────────────────────────────────────────────────────────
export async function getCommunity(name: string): Promise<CommunityRow | null> {
  const comm = await prisma.community.findUnique({
    where: { name },
  });
  return comm as CommunityRow | null;
}

// ── Credentials ───────────────────────────────────────────────────────────────
export async function rotateActiveCredentials(community: string, companyKey: string): Promise<void> {
  await prisma.credential.updateMany({
    where: {
      status: "active",
      community,
      company_key: companyKey,
    },
    data: {
      status: "rotated",
    },
  });
}

export async function insertCredential(cred: CredentialRow): Promise<void> {
  await prisma.credential.create({
    data: {
      id: cred.id,
      community: cred.community,
      company_name: cred.company_name,
      company_key: cred.company_key,
      last4: cred.last4,
      code_hash: cred.code_hash,
      status: cred.status,
      created_at: cred.created_at,
      valid_until: cred.valid_until,
      created_by: cred.created_by,
    },
  });
}

// ── Deliveries ────────────────────────────────────────────────────────────────
export async function insertDelivery(delivery: DeliveryRow): Promise<void> {
  await prisma.delivery.create({
    data: {
      id: delivery.id,
      credential_id: delivery.credential_id,
      community: delivery.community,
      company_name: delivery.company_name,
      to_masked: delivery.to_masked,
      channel: delivery.channel,
      status: delivery.status,
      actor: delivery.actor,
      ts: delivery.ts,
      last4: delivery.last4,
      window_override: delivery.window_override,
    },
  });
}

export async function getRecentDeliveries(companyNames: string[], limit = 20): Promise<DeliveryRow[]> {
  if (companyNames.length === 0) return [];
  const deliveries = await prisma.delivery.findMany({
    where: {
      company_name: {
        in: companyNames,
      },
    },
    orderBy: {
      ts: "desc",
    },
    take: limit,
  });
  return deliveries as unknown as DeliveryRow[];
}
