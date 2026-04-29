# app/services/session_store.py

from collections import defaultdict

SESSIONS = defaultdict(lambda: {
    "state": "BROWSING",
    "order": [],
    "last_items": [],
    "user_type": None
})


def get_session(user_id: str):
    return SESSIONS[user_id]


def update_session(user_id: str, data: dict):
    SESSIONS[user_id].update(data)