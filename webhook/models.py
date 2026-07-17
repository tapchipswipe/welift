import os
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, Any
from sqlalchemy import (
    create_engine, Column, Integer, String, Boolean, DateTime, JSON
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Database URL configuration
APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR.parent / "data"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/welift.db")

# Create sqlite database parent dir if it doesn't exist
if DATABASE_URL.startswith("sqlite:///"):
    db_path = Path(DATABASE_URL.replace("sqlite:///", ""))
    db_path.parent.mkdir(parents=True, exist_ok=True)

if DATABASE_URL in {"sqlite://", "sqlite:///:memory:"}:
    from sqlalchemy.pool import StaticPool
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
else:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite://") else {}
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 1. Community Model
class Community(Base):
    __tablename__ = "communities"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    timezone = Column(String, default="America/New_York", nullable=False)

# 2. VendorCompany Model
class VendorCompany(Base):
    __tablename__ = "vendor_companies"
    id = Column(Integer, primary_key=True, index=True)
    community_name = Column(String, nullable=False, default="The Inlets")
    company_name = Column(String, unique=True, index=True, nullable=False)
    access_contact_type = Column(String, default="dispatch")  # dispatch or owner
    access_phone = Column(String, nullable=True)
    invite_email = Column(String, nullable=True)
    window = Column(String, default="Mon-Fri 07:00-18:00")
    notes = Column(String, nullable=True)
    active = Column(Boolean, default=True, nullable=False)

# 3. GuestEntry Model
class GuestEntry(Base):
    __tablename__ = "guest_entries"
    id = Column(Integer, primary_key=True, index=True)
    community_name = Column(String, nullable=False, default="The Inlets")
    visitor_name = Column(String, index=True, nullable=False)
    company_name = Column(String, nullable=True)
    host_name = Column(String, nullable=True)
    host_address = Column(String, nullable=True)
    valid_until = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

# 4. Credential Model
class Credential(Base):
    __tablename__ = "credentials"
    id = Column(String, primary_key=True, index=True)  # UUID / minted ID string
    community = Column(String, nullable=False, default="The Inlets")
    company_name = Column(String, nullable=False)
    company_key = Column(String, nullable=True)
    last4 = Column(String, nullable=False)
    code_hash = Column(String, nullable=False)
    status = Column(String, default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime, nullable=False)
    created_by = Column(String, default="cam_desk")

# 5. Delivery Model
class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(String, primary_key=True, index=True)
    credential_id = Column(String, nullable=False)
    community = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    to_masked = Column(String, nullable=False)
    channel = Column(String, nullable=False)
    status = Column(String, nullable=False)
    actor = Column(String, nullable=False)
    ts = Column(DateTime, default=datetime.utcnow)
    last4 = Column(String, nullable=False)
    window_override = Column(Boolean, default=False, nullable=False)

# 6. AuditEvent Model
class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tool = Column(String, nullable=False)
    payload = Column(JSON, nullable=True)

# Session Dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Auto-Seeder
def init_db_and_seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if community table is empty
        if db.query(Community).count() > 0:
            return  # already seeded
            
        print("Initializing relational database and seeding from JSON files…")
        
        # 1. Seed Community & Guest List
        guest_list_path = DATA_DIR / "guest-list.json"
        if not guest_list_path.exists():
            guest_list_path = DATA_DIR / "guest-list.example.json"
            
        timezone_str = "America/New_York"
        guest_entries = []
        if guest_list_path.exists():
            try:
                with guest_list_path.open("r", encoding="utf-8") as f:
                    gl_data = json.load(f)
                    timezone_str = gl_data.get("timezone", "America/New_York")
                    guest_entries = gl_data.get("entries", [])
            except Exception as e:
                print(f"Failed to read guest list seed: {e}")
                
        inlets = Community(name="The Inlets", timezone=timezone_str)
        db.add(inlets)
        db.commit()
        
        # Seed Guest Entries
        for entry in guest_entries:
            valid_until_dt = None
            if entry.get("valid_until"):
                try:
                    valid_until_dt = datetime.fromisoformat(entry["valid_until"].replace("Z", "+00:00"))
                except ValueError:
                    pass
            db.add(GuestEntry(
                community_name="The Inlets",
                visitor_name=entry.get("visitor_name"),
                company_name=entry.get("company_name"),
                host_name=entry.get("host_name"),
                host_address=entry.get("host_address"),
                valid_until=valid_until_dt,
                notes=entry.get("notes")
            ))
            
        # 2. Seed Vendors
        vendors_path = DATA_DIR / "vendors.json"
        if not vendors_path.exists():
            vendors_path = DATA_DIR / "vendors.seed.json"
            
        vendors = []
        if vendors_path.exists():
            try:
                with vendors_path.open("r", encoding="utf-8") as f:
                    v_data = json.load(f)
                    vendors = v_data.get("vendors", []) if isinstance(v_data, dict) else v_data
            except Exception as e:
                print(f"Failed to read vendors seed: {e}")
                
        for v in vendors:
            db.add(VendorCompany(
                community_name="The Inlets",
                company_name=v.get("company_name"),
                access_contact_type=v.get("access_contact_type", "dispatch"),
                access_phone=v.get("access_phone"),
                invite_email=v.get("invite_email"),
                window=v.get("window", "Mon-Fri 07:00-18:00"),
                notes=v.get("notes"),
                active=v.get("active", True)
            ))
            
        # 3. Seed Credentials & Deliveries
        creds_path = DATA_DIR / "credentials.json"
        creds_data = {"credentials": [], "deliveries": []}
        if creds_path.exists():
            try:
                with creds_path.open("r", encoding="utf-8") as f:
                    creds_data = json.load(f)
            except Exception as e:
                print(f"Failed to read credentials store seed: {e}")
                
        for c in creds_data.get("credentials", []):
            try:
                valid_until_dt = datetime.fromisoformat(c["valid_until"].replace("Z", "+00:00"))
                created_at_dt = datetime.utcnow()
                if c.get("created_at"):
                    created_at_dt = datetime.fromisoformat(c["created_at"].replace("Z", "+00:00"))
            except Exception:
                valid_until_dt = datetime.utcnow()
                created_at_dt = datetime.utcnow()
                
            db.add(Credential(
                id=c.get("id"),
                community=c.get("community", "The Inlets"),
                company_name=c.get("company_name"),
                company_key=c.get("company_key"),
                last4=c.get("last4"),
                code_hash=c.get("code_hash"),
                status=c.get("status", "active"),
                created_at=created_at_dt,
                valid_until=valid_until_dt,
                created_by=c.get("created_by", "cam_desk")
            ))
            
        for d in creds_data.get("deliveries", []):
            try:
                ts_dt = datetime.fromisoformat(d["ts"].replace("Z", "+00:00"))
            except Exception:
                ts_dt = datetime.utcnow()
                
            db.add(Delivery(
                id=d.get("id"),
                credential_id=d.get("credential_id"),
                community=d.get("community"),
                company_name=d.get("company_name"),
                to_masked=d.get("to_masked"),
                channel=d.get("channel"),
                status=d.get("status"),
                actor=d.get("actor"),
                ts=ts_dt,
                last4=d.get("last4"),
                window_override=d.get("window_override", False)
            ))
            
        db.commit()
        print("Database successfully seeded!")
    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
    finally:
        db.close()
