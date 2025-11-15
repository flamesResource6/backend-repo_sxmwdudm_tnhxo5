import os
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db

app = FastAPI(title="Study Group Community API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request models
class SignupRequest(BaseModel):
    name: str
    email: str
    interest: Optional[str] = None


@app.get("/")
def read_root():
    return {"message": "Study Group Community Backend is running"}


@app.get("/api/groups")
def list_groups(limit: int = 12):
    try:
        groups = get_documents("group", {}, limit)
        return {"items": groups}
    except Exception:
        # Graceful fallback sample
        sample = [
            {
                "name": "Math Masters",
                "subject": "Algebra & Calculus",
                "description": "Daily problem-solving and concept reviews.",
            },
            {
                "name": "Bio Buddies",
                "subject": "Biology",
                "description": "Cell biology to human anatomy study jams.",
            },
            {
                "name": "Code Crew",
                "subject": "Programming",
                "description": "Leetcode, projects, and pair programming.",
            },
        ][:limit]
        return {"items": sample, "sample": True}


@app.get("/api/sessions/upcoming")
def upcoming_sessions(limit: int = 6):
    try:
        now = datetime.now(timezone.utc)
        sessions = list(db["session"].find({"start_time": {"$gte": now}}).sort("start_time", 1).limit(limit)) if db else []
        return {"items": sessions}
    except Exception:
        base = datetime.now(timezone.utc).replace(microsecond=0)
        sample = [
            {
                "title": "Morning Focus Sprint",
                "description": "50-minute deep work + 10-minute break",
                "start_time": (base + timedelta(hours=idx + 1)).isoformat(),
                "duration_minutes": 60,
            }
            for idx in range(limit)
        ]
        return {"items": sample, "sample": True}


@app.get("/api/discussions/latest")
def latest_discussions(limit: int = 6):
    try:
        discussions = list(db["discussion"].find({}).sort("created_at", -1).limit(limit)) if db else []
        return {"items": discussions}
    except Exception:
        sample = [
            {"author": "Ava", "message": "Any tips for integrals by substitution?"},
            {"author": "Liam", "message": "Sharing notes from today’s bio lab."},
        ][:limit]
        return {"items": sample, "sample": True}


@app.get("/api/goals")
def list_goals(limit: int = 6):
    try:
        goals = list(db["goal"].find({}).sort("created_at", -1).limit(limit)) if db else []
        return {"items": goals}
    except Exception:
        sample = [
            {"member": "Maya", "content": "Finish 3 calculus chapters this week"},
            {"member": "Noah", "content": "Practice 2 coding challenges daily"},
        ][:limit]
        return {"items": sample, "sample": True}


@app.get("/api/notes")
def list_notes(limit: int = 8):
    try:
        notes = get_documents("note", {}, limit)
        return {"items": notes}
    except Exception:
        sample = [
            {
                "title": "Algebra Quick Guide",
                "description": "Formulas and practice set",
                "download_url": "https://example.com/algebra.pdf",
                "tag_list": ["math", "algebra"],
            },
            {
                "title": "Biology Diagrams Pack",
                "description": "High-res labeled diagrams",
                "download_url": "https://example.com/biology.zip",
                "tag_list": ["bio"],
            },
        ][:limit]
        return {"items": sample, "sample": True}


@app.post("/api/signup")
def signup(payload: SignupRequest):
    try:
        doc_id = create_document("signup", payload.model_dump())
        return {"ok": True, "id": doc_id}
    except Exception:
        # Accept signups even without DB to allow demo flow
        return {"ok": True, "id": "demo"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
