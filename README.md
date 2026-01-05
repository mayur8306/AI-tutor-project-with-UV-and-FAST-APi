# FastAPI AI Tutor / Mentor Backend (Concept Project)

This project is a **backend-only AI Tutor / Mentor system** built using **FastAPI**.  
It was developed as an **experimental and learning-focused project** to explore how AI models can be guided using **custom notes**, backend logic, and user interaction patterns.

The goal was to go beyond a simple chatbot and build a **notes-driven tutoring system** that answers questions **according to provided study material**, while gradually adapting responses based on user behavior.

---

## 🧠 Project Idea & Motivation

The core idea of this project was to create a **Python mentor/tutor backend** that:

- Uses **custom notes uploaded by the developer**
- Answers questions **based on those notes**, not generic AI responses
- Explains concepts in a **teacher-like manner**
- Attempts to adjust answers depending on how the user interacts or makes mistakes

This project became complex very quickly because it involved:
- Backend architecture
- AI prompt design
- Context handling
- State and behavior awareness  
—all at the same time.

It is intentionally maintained as a **concept / prototype project** that reflects learning and experimentation.

---

## ✨ Key Features

- **FastAPI backend-only application**
- AI-powered answers using **Grok (via ChatGroq API)**
- Notes-based answering (answers are guided by custom notes)
- Teacher/mentor-style explanations
- Early experimentation with:
  - Learning from user behavior
  - Corrective responses when users make mistakes
- Modular backend structure (routers, services, utilities)

---

## 🛠 Tech Stack

- **Backend Framework:** FastAPI
- **Language:** Python
- **AI / LLM:** Grok API (via ChatGroq)
- **Dependency Management:** `uv`
- **Data Storage (local):** SQLite (for experimentation)
- **Environment Management:** `.env` (ignored in Git)
- **Version Control:** Git & GitHub

---

## 📦 About `uv` (Important Note)

This project uses **`uv`** for dependency and environment management.

At the time of building this project:
- `uv` was **new to me**
- I was **actively experimenting** with modern Python tooling
- The goal was to **learn and explore better workflows**, not just stick to familiar tools

This project reflects:
> A willingness to try new technologies, learn by building, and adapt to evolving ecosystems.

---

## 🗂 Project Structure (High-Level)

