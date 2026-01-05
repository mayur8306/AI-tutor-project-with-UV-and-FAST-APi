import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

# 🧠 Mentor (learning from user patterns)
from backend.services.mentor import (
    analyze_user_message,
    update_user_profile,
    build_mentor_instructions,
)


# -------------------------------------------------
# ENV SETUP
# -------------------------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

print("✅ GROQ KEY LOADED IN tutor.py:", os.getenv("GROQ_API_KEY"))

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def load_notes_style(path: str) -> str:
    if not os.path.exists(path):
        print(f"[WARN] Style file not found: {path}")
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def choose_temperature(user_input: str) -> float:
    text = user_input.lower()

    if any(k in text for k in ["error", "traceback", "exception", "bug", "fix", "crash", "segfault"]):
        return 0.1

    if any(k in text for k in [
        "dsa", "time complexity", "space complexity", "big o",
        "stack", "queue", "linked list", "tree", "graph",
        "dfs", "bfs", "binary search", "sorting",
        "recursion", "dynamic programming", "dp"
    ]):
        return 0.2

    if any(k in text for k in ["explain", "what is", "why", "how does", "difference between", "concept", "theory"]):
        return 0.25

    if any(k in text for k in ["project", "game", "pygame", "gui", "tkinter", "idea", "app"]):
        return 0.4

    return 0.2


def detect_language(user_input: str, current_lang: str | None) -> str:
    text = user_input.lower().strip()

    if text.startswith("/c"):
        return "c"
    if text.startswith("/py") or text.startswith("/python"):
        return "python"

    if " in python" in text or " python " in text or text.endswith(" in python"):
        return "python"
    if " in c" in text or " in c language" in text or text.endswith(" in c"):
        return "c"

    if "python code" in text or "python program" in text:
        return "python"
    if "c code" in text or "c program" in text:
        return "c"

    return current_lang or "c"


# -------------------------------------------------
# GLOBAL STATE
# -------------------------------------------------
current_lang = None

# -------------------------------------------------
# LOAD STYLE NOTES
# -------------------------------------------------
c_style = load_notes_style("notes.txt")
py_style = load_notes_style("python.txt")

# -------------------------------------------------
# BASE SYSTEM PROMPT
# -------------------------------------------------
system_text = (
    "You are a beginner-friendly programming and DSA tutor for a first-year student.\n"
    "You can answer in C or Python, depending on what the user asks for.\n"
    "You must follow the STYLE of the reference notes below, but do not copy them word for word.\n\n"
    "===== C DSA STYLE REFERENCE (DO NOT REPEAT VERBATIM) =====\n"
    f"{c_style}\n"
    "==========================================================\n\n"
    "===== PYTHON DSA STYLE REFERENCE (DO NOT REPEAT VERBATIM) =====\n"
    f"{py_style}\n"
    "===============================================================\n\n"
    "Language rules:\n"
    "- If the user explicitly asks for Python, answer in Python.\n"
    "- If the user explicitly asks for C, answer in C.\n"
    "- If not specified, default to C.\n"
    "Use plain text only. No markdown or code fences."
)

# -------------------------------------------------
# CORE FUNCTION (USED BY API)
# -------------------------------------------------
def get_reply(user_message: str) -> str:
    try:
        global current_lang

        # TEMP user id (frontend can replace later)
        user_id = str(user_id_from_token)

        # 🧠 LEARNING STEP (MENTOR)
        analysis = analyze_user_message(user_message)
        update_user_profile(user_id, analysis)
        mentor_hint = build_mentor_instructions(user_id)

        # 🌡️ Language + temperature
        current_lang = detect_language(user_message, current_lang)
        temp = choose_temperature(user_message)

        # 🔮 Model
        model = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=temp,
        )

        # 🎯 Condition input
        conditioned_input = (
            f"(Language: Python) {user_message}"
            if current_lang == "python"
            else f"(Language: C) {user_message}"
        )

        # 🧩 Final system prompt (base + mentor learning)
        final_system_text = system_text
        if mentor_hint:
            final_system_text += "\n\nMENTOR INSTRUCTIONS:\n" + mentor_hint

        messages = [
            SystemMessage(content=final_system_text),
            HumanMessage(content=conditioned_input),
        ]

        ai_msg = model.invoke(messages)
        return ai_msg.content

    except Exception as e:
        print("🔥 CHAT ERROR:", repr(e))
        raise


# -------------------------------------------------
# ADMIN: RELOAD NOTES WITHOUT RESTART
# -------------------------------------------------
def reload_notes():
    global c_style, py_style, system_text

    c_style = load_notes_style("notes.txt")
    py_style = load_notes_style("python.txt")

    system_text = (
        "You are a beginner-friendly programming and DSA tutor for a first-year student.\n"
        "You can answer in C or Python, depending on what the user asks for.\n"
        "You must follow the STYLE of the reference notes below, but do not copy them word for word.\n\n"
        "===== C DSA STYLE REFERENCE (DO NOT REPEAT VERBATIM) =====\n"
        f"{c_style}\n"
        "==========================================================\n\n"
        "===== PYTHON DSA STYLE REFERENCE (DO NOT REPEAT VERBATIM) =====\n"
        f"{py_style}\n"
        "===============================================================\n\n"
        "Language rules:\n"
        "- If the user explicitly asks for Python, answer in Python.\n"
        "- If the user explicitly asks for C, answer in C.\n"
        "- If not specified, default to C.\n"
        "Use plain text only."
    )

    return {"status": "notes reloaded"}
