# services/mentor.py
# ---------------------------------------
# This file handles USER LEARNING PATTERNS
# It does NOT train the AI model.
# It only adapts answers based on user style.
# ---------------------------------------

from typing import Dict

# In-memory user profiles (later can be DB / JSON / Redis)
USER_PROFILES: Dict[str, dict] = {}


def analyze_user_message(text: str) -> dict:
    """
    Analyze how the user asks questions.
    This detects LEARNING STYLE, not intelligence.
    """
    text_lower = text.lower()

    analysis = {
        "needs_simple_explanation": False,
        "prefers_code": False,
        "prefers_theory": False,
        "language_style": None,  # "c" or "python"
    }

    # Beginner / simplicity signals
    if any(word in text_lower for word in ["simple", "easy", "basic", "explain like", "beginner"]):
        analysis["needs_simple_explanation"] = True

    # Code preference
    if any(word in text_lower for word in ["code", "program", "example", "implementation"]):
        analysis["prefers_code"] = True

    # Theory preference
    if any(word in text_lower for word in ["theory", "definition", "concept"]):
        analysis["prefers_theory"] = True

    # Language preference
    if "python" in text_lower:
        analysis["language_style"] = "python"
    elif " in c" in text_lower or text_lower.startswith("/c"):
        analysis["language_style"] = "c"

    return analysis


def update_user_profile(user_id: str, analysis: dict):
    """
    Update stored user learning preferences.
    Preferences accumulate over time.
    """
    if user_id not in USER_PROFILES:
        USER_PROFILES[user_id] = {
            "needs_simple_explanation": False,
            "prefers_code": False,
            "prefers_theory": False,
            "language_style": None,
        }

    # Only update fields that were detected as True
    for key, value in analysis.items():
        if value is not None and value is True:
            USER_PROFILES[user_id][key] = value

        # language_style is special (string)
        if key == "language_style" and value is not None:
            USER_PROFILES[user_id]["language_style"] = value


def build_mentor_instructions(user_id: str) -> str:
    """
    Convert stored preferences into instructions
    that are appended to the system prompt.
    """
    profile = USER_PROFILES.get(user_id)

    if not profile:
        return ""

    instructions = []

    if profile.get("needs_simple_explanation"):
        instructions.append("Explain concepts in very simple language, step by step.")

    if profile.get("prefers_code"):
        instructions.append("Focus more on code examples than long theory.")

    if profile.get("prefers_theory"):
        instructions.append("Explain theory clearly before showing code.")

    if profile.get("language_style") == "python":
        instructions.append("Use Python-style explanations suitable for beginners.")
    elif profile.get("language_style") == "c":
        instructions.append("Use C-style explanations with simple variables and logic.")

    return "\n".join(instructions)
