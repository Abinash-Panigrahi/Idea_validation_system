"""
database.py — MongoDB Atlas connection and operations.
All database logic lives here.
"""

import os
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# ─── Connection ───────────────────────────────────────────────────────────────

MONGO_URI = os.environ.get("MONGO_URI")

client = None
db = None
collection = None

try:
    if MONGO_URI:
        client = MongoClient(MONGO_URI)
        db = client["ThynxAI_db"]
        collection = db["analyses"]
except Exception as e:
    print(f"MongoDB connection failed: {str(e)}")


# ─── Operations ───────────────────────────────────────────────────────────────

def save_analysis(analysis: dict) -> bool:
    """
    Saves one analysis result to MongoDB.
    Returns True if saved successfully, False if failed.
    """
    if collection is None:
        print("Database not connected. Skipping save.")
        return False
    try:
        db_data = analysis.copy()
        db_data["saved_at"] = datetime.now().isoformat()
        collection.insert_one(db_data)
        return True

    except Exception as e:
        print(f"Database save failed: {str(e)}")
        return False


# ─── Will be used in admin dashboard (Phase 2) ───────────────────────────────

def get_all_analyses() -> list:
    """
    Returns all saved analyses from MongoDB.
    """
    if collection is None:
        return []
    try:
        results = list(collection.find({}, {"_id": 0}))
        return results
    except Exception as e:
        print(f"Database fetch failed: {str(e)}")
        return []