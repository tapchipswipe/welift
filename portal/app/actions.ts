"use server";

import { currentUser } from "@clerk/nextjs/server";
import { getActiveVendors, getCommunity, getRecentDeliveries } from "@/lib/db";
import { sendCode, vendorWindowAllows } from "@/lib/credentials";

export async function getDispatcherContext() {
  const user = await currentUser();
  if (!user) {
    return { authenticated: false, error: "Not authenticated" };
  }

  const email = user.emailAddresses[0]?.emailAddress?.toLowerCase();
  if (!email) {
    return { authenticated: true, authorized: false, error: "No email address found" };
  }

  // Find all active vendor companies matching this email
  const allActiveVendors = getActiveVendors();

  const matchingVendors = allActiveVendors.filter(
    (v) => v.invite_email?.toLowerCase() === email
  );

  if (matchingVendors.length === 0) {
    return {
      authenticated: true,
      authorized: false,
      email,
      error: `Email ${email} is not registered to any authorized vendor company.`,
    };
  }

  // We support multiple vendor records (e.g., if authorized for different communities)
  // Let's gather all vendor companies and check window authorizations
  const results = [];
  for (const vendor of matchingVendors) {
    const comm = getCommunity(vendor.community_name);
    const tz = comm?.timezone || "America/New_York";
    const windowCheck = vendorWindowAllows(vendor, new Date(), tz);
    
    results.push({
      vendor,
      communityName: vendor.community_name,
      timezone: tz,
      window: vendor.window,
      isAuthorizedToday: windowCheck.ok,
      reason: windowCheck.reason,
    });
  }

  const companyNames = matchingVendors.map((v) => v.company_name);
  const deliveries = getRecentDeliveries(companyNames);

  return {
    authenticated: true,
    authorized: true,
    email,
    companies: results,
    deliveries: deliveries.map((d) => ({
      id: d.id,
      community: d.community,
      companyName: d.company_name,
      toMasked: d.to_masked,
      channel: d.channel,
      status: d.status,
      technicianName: d.actor,
      timestamp: d.ts,
      last4: d.last4,
    })),
  };
}

export async function sendCodeAction(data: {
  communityName: string;
  technicianName: string;
  phone: string;
}) {
  try {
    const user = await currentUser();
    if (!user) {
      return { success: false, error: "Not authenticated" };
    }

    const email = user.emailAddresses[0]?.emailAddress?.toLowerCase();
    if (!email) {
      return { success: false, error: "No email address found" };
    }

    const technicianName = (data.technicianName || "").trim();
    const phone = (data.phone || "").trim();
    const communityName = (data.communityName || "").trim();

    if (!technicianName) {
      return { success: false, error: "Technician name is required" };
    }
    if (!phone) {
      return { success: false, error: "Phone number is required" };
    }
    if (!communityName) {
      return { success: false, error: "Community is required" };
    }

    // Find the vendor company matching this email and community
    const allActiveVendors = getActiveVendors();

    const vendor = allActiveVendors.find(
      (v) =>
        v.invite_email?.toLowerCase() === email &&
        v.community_name === communityName
    );

    if (!vendor) {
      return {
        success: false,
        error: `Your account is not authorized to issue codes for community "${communityName}".`,
      };
    }

    // Run the send code logic (minting + Twilio SMS + DB logging)
    const result = await sendCode({
      community: communityName,
      companyName: vendor.company_name,
      phone,
      actor: technicianName, // Log technician name as the actor
      overrideWindow: false, // Strict dispatcher window enforcement
    });

    return {
      success: true,
      result: {
        ok: result.ok,
        community: result.community,
        companyName: result.company_name,
        last4: result.last4,
        validUntil: result.valid_until,
        code: result.code,
        smsStatus: result.sms.status,
      },
    };
  } catch (error: any) {
    console.error("sendCodeAction failed:", error);
    return { success: false, error: error.message || "An unexpected error occurred" };
  }
}
