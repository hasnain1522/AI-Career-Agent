import os
import json

from supabase import create_client, Client


# ============================================================
# SUPABASE CONNECTION
# ============================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is missing from .env")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY,
)


# ============================================================
# DEFAULT USER PROFILE
# ============================================================

DEFAULT_PROFILE = {
    "education": "",
    "experience_level": "",
    "skills": [],
    "target_career": "",
    "career_goals": [],
    "available_time": "",
    "learning_style": "",
    "constraints": [],
}


# ============================================================
# PROFILE FUNCTIONS
# ============================================================

def load_profile(user_id: str) -> dict:
    """
    Load one user's career profile from Supabase.
    """

    response = (
        supabase
        .table("user_profiles")
        .select("*")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if not response.data:
        return DEFAULT_PROFILE.copy()

    row = response.data[0]

    return {
        "education": row.get("education", ""),
        "experience_level": row.get("experience_level", ""),
        "skills": row.get("skills", []) or [],
        "target_career": row.get("target_career", ""),
        "career_goals": row.get("career_goals", []) or [],
        "available_time": row.get("available_time", ""),
        "learning_style": row.get("learning_style", ""),
        "constraints": row.get("constraints", []) or [],
    }


def save_profile_data(user_id: str, profile: dict) -> None:
    """
    Save or update one user's career profile in Supabase.
    """

    data = {
        "user_id": user_id,
        "education": profile.get("education", ""),
        "experience_level": profile.get("experience_level", ""),
        "skills": profile.get("skills", []),
        "target_career": profile.get("target_career", ""),
        "career_goals": profile.get("career_goals", []),
        "available_time": profile.get("available_time", ""),
        "learning_style": profile.get("learning_style", ""),
        "constraints": profile.get("constraints", []),
    }

    supabase \
        .table("user_profiles") \
        .upsert(data, on_conflict="user_id") \
        .execute()


# ============================================================
# SUPABASE SESSION
# ============================================================

class SupabaseSession:
    """
    Supabase-backed conversation session compatible with
    the OpenAI Agents SDK session interface.

    Every user gets a separate session based on user_id.
    """

    def __init__(self, session_id: str):
        self.session_id = session_id

    # --------------------------------------------------------
    # Get conversation history
    # --------------------------------------------------------

    def get_items(self, limit: int | None = None) -> list:
        """
        Return conversation items in chronological order.
        """

        query = (
            supabase
            .table("conversation_messages")
            .select("id, content")
            .eq("user_id", self.session_id)
            .order("id", desc=False)
        )

        if limit is not None:
            query = query.limit(limit)

        response = query.execute()

        items = []

        for row in response.data or []:
            try:
                item = json.loads(row["content"])
                items.append(item)
            except (json.JSONDecodeError, TypeError):
                continue

        return items

    # --------------------------------------------------------
    # Add conversation items
    # --------------------------------------------------------

    def add_items(self, items: list) -> None:
        """
        Save conversation items to Supabase.
        """

        rows = []

        for item in items:

            if not isinstance(item, dict):
                continue

            role = item.get("role", "user")

            try:
                content = json.dumps(
                    item,
                    ensure_ascii=False,
                    default=str,
                )
            except (TypeError, ValueError):
                continue

            rows.append(
                {
                    "user_id": self.session_id,
                    "role": role,
                    "content": content,
                }
            )

        if rows:
            (
                supabase
                .table("conversation_messages")
                .insert(rows)
                .execute()
            )

    # --------------------------------------------------------
    # Remove latest conversation item
    # --------------------------------------------------------

    def pop_item(self):
        """
        Remove and return the most recent conversation item.
        """

        response = (
            supabase
            .table("conversation_messages")
            .select("id, content")
            .eq("user_id", self.session_id)
            .order("id", desc=True)
            .limit(1)
            .execute()
        )

        if not response.data:
            return None

        row = response.data[0]

        try:
            item = json.loads(row["content"])
        except (json.JSONDecodeError, TypeError):
            item = None

        (
            supabase
            .table("conversation_messages")
            .delete()
            .eq("id", row["id"])
            .execute()
        )

        return item

    # --------------------------------------------------------
    # Clear conversation
    # --------------------------------------------------------

    def clear_session(self) -> None:
        """
        Delete all conversation history for this user.
        """

        (
            supabase
            .table("conversation_messages")
            .delete()
            .eq("user_id", self.session_id)
            .execute()
        )

    # --------------------------------------------------------
    # Close session
    # --------------------------------------------------------

    def close(self) -> None:
        """
        Supabase does not require a local database connection
        to be closed.
        """

        return None