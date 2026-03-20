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

if not MONGO_URI:
    raise ValueError("MONGO_URI not found. Please set it in your .env file.")

client = MongoClient(MONGO_URI)
db = client["ThynxAI_db"]
collection = db["analyses"]


# ─── Operations ───────────────────────────────────────────────────────────────

def save_analysis(analysis: dict) -> bool:
    """
    Saves one analysis result to MongoDB.
    Returns True if saved successfully, False if failed.
    """
    try:
        # 1. Create a copy so PyMongo doesn't mutate the original dict
        db_data = analysis.copy()

        # 2. Add timestamp to the copy
        db_data["saved_at"] = datetime.now().isoformat()

        # 3. Insert the copy into MongoDB
        collection.insert_one(db_data)

        return True

    except Exception as e:
        print(f"Database save failed: {str(e)}")
        return False


# -Will be used in admin dashboard (Phase 2 in future)-------

def get_all_analyses() -> list:
    """
    Returns all saved analyses from MongoDB.
    """
    try:
        results = list(collection.find({}, {"_id": 0}))
        return results
    except Exception as e:
        print(f"Database fetch failed: {str(e)}")
        return []