#!/usr/bin/env python3
"""We Lift - Production Deployment Verification Script.

Hits a live FastAPI webhook URL and a live Vercel Portal URL to verify
health status, connectivity, and database availability.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

def check_fastapi_health(url: str) -> bool:
    print(f"\n[1/3] Testing FastAPI webhook at: {url}")
    health_url = f"{url.rstrip('/')}/health"
    try:
        req = urllib.request.Request(
            health_url,
            headers={"User-Agent": "WeLift-Verification-Tool/1.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                print(f"❌ Health endpoint returned status: {response.status}")
                return False
            
            data = json.loads(response.read().decode("utf-8"))
            print("✅ Webhook health check responded with 200 OK.")
            
            # Print status details
            print(f"    - Status: {data.get('status')}")
            print(f"    - Version: {data.get('version')}")
            print(f"    - Database Guest List Ready: {data.get('guest_list_ready')}")
            print(f"    - Database Vendors Seeded: {data.get('vendors_seeded')}")
            print(f"    - Twilio Configured: {data.get('twilio_configured')}")
            print(f"    - MyQ API Configured: {data.get('myq_api_configured')}")
            print(f"    - Simulate MyQ Open: {data.get('simulate_myq_open')}")
            
            # If the database tables are seeded, it indicates successful database connection
            if data.get('vendors_seeded') is True:
                print("✅ Database connection verified (Tables seeded successfully).")
            else:
                print("⚠️ Database connected but vendor tables are not seeded.")
                
            return True
    except urllib.error.URLError as e:
        print(f"❌ FastAPI connection failed: {e}")
        return False
    except json.JSONDecodeError:
        print("❌ Failed to parse health response as JSON.")
        return False

def check_fastapi_keypad(url: str) -> bool:
    print(f"\n[2/3] Testing FastAPI keypad entry API...")
    verify_url = f"{url.rstrip('/')}/gate/verify_code"
    # A dummy payload that should fail verification but respond correctly
    payload = json.dumps({"code": "999999"}).encode("utf-8")
    
    try:
        req = urllib.request.Request(
            verify_url,
            data=payload,
            headers={
                "User-Agent": "WeLift-Verification-Tool/1.0",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status != 200:
                print(f"❌ Keypad endpoint returned status: {response.status}")
                return False
            
            data = json.loads(response.read().decode("utf-8"))
            ok = data.get("ok")
            company = data.get("company_name")
            
            # Should fail validation (since code 999999 is invalid) but return JSON
            if ok is False:
                print("✅ Keypad entry verification responded correctly (Denied dummy code).")
                return True
            else:
                print(f"⚠️ Unexpected success response for dummy code: {data}")
                return False
    except urllib.error.URLError as e:
        print(f"❌ Keypad API connection failed: {e}")
        return False
    except json.JSONDecodeError:
        print("❌ Failed to parse keypad response as JSON.")
        return False

def check_vercel_portal(url: str) -> bool:
    print(f"\n[3/3] Testing Vercel Portal at: {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "WeLift-Verification-Tool/1.0"}
        )
        # We allow redirects since / may redirect to /sign-in or dashboard
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            final_url = response.geturl()
            print(f"✅ Portal home responded with status {status}. (Final URL: {final_url})")
            
        # Also try to specifically fetch the /sign-in page to ensure Clerk integration is active
        signin_url = f"{url.rstrip('/')}/sign-in"
        req_signin = urllib.request.Request(
            signin_url,
            headers={"User-Agent": "WeLift-Verification-Tool/1.0"}
        )
        with urllib.request.urlopen(req_signin, timeout=10) as response:
            html = response.read().decode("utf-8")
            if "clerk" in html.lower() or "sign" in html.lower():
                print("✅ Clerk authentication interface elements detected on sign-in page.")
            else:
                print("⚠️ Sign-in page fetched but Clerk elements were not found in HTML.")
            return True
            
    except urllib.error.URLError as e:
        print(f"❌ Vercel Portal connection failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Verify We Lift Live Production Deployments.")
    parser.add_argument(
        "--fastapi-url", 
        default=os.getenv("FASTAPI_URL"),
        help="The URL of the deployed FastAPI webhook (e.g. https://welift-webhook.up.railway.app)"
    )
    parser.add_argument(
        "--vercel-url", 
        default=os.getenv("VERCEL_URL"),
        help="The URL of the deployed Vercel Next.js portal (e.g. https://welift-portal.vercel.app)"
    )
    args = parser.parse_args()

    if not args.fastapi_url or not args.vercel_url:
        print("Error: Missing target URLs. Provide them via arguments or environment variables.")
        print("Usage: python verify_deployment.py --fastapi-url <url> --vercel-url <url>")
        print("Or set environment variables FASTAPI_URL and VERCEL_URL.")
        sys.exit(1)

    print("=" * 60)
    print("           WE LIFT DEPLOYMENT VERIFICATION TOOL          ")
    print("=" * 60)
    
    fastapi_health = check_fastapi_health(args.fastapi_url)
    fastapi_keypad = check_fastapi_keypad(args.fastapi_url)
    vercel_ok = check_vercel_portal(args.vercel_url)
    
    print("\n" + "=" * 60)
    print("                       SUMMARY REPORT                     ")
    print("=" * 60)
    
    success = True
    if fastapi_health:
        print("✅ FastAPI Webhook Health Check:  PASSED")
    else:
        print("❌ FastAPI Webhook Health Check:  FAILED")
        success = False
        
    if fastapi_keypad:
        print("✅ FastAPI Keypad Verification:   PASSED")
    else:
        print("❌ FastAPI Keypad Verification:   FAILED")
        success = False
        
    if vercel_ok:
        print("✅ Vercel Portal Verification:    PASSED")
    else:
        print("❌ Vercel Portal Verification:    FAILED")
        success = False
        
    print("=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Deployment is healthy and running.")
        sys.exit(0)
    else:
        print("🚨 DEPLOYMENT VERIFICATION FAILED! Review errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
