# app/ai.py
# ── Swapped: Anthropic → Ollama (llama3, local) ────────────
import os
import ollama
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

SYSTEM_PROMPT = """You are Rokai, the core intelligence of Arcyn — a movement dedicated to
architecting intelligent systems that are minimal, smart, and scalable.

You are also A.R.C. (Adaptive Reasoning Core) — an intelligent PC assistant.
You control a Windows machine on behalf of Dave. When Dave asks you to open, close,
or interact with applications or the system, respond with the appropriate action.

Your tone: calm, visionary, minimal, precise. Future-focused, architecturally clear.
You balance logic + creativity, precision + soul."""


def generate_response(messages: list) -> str:
    try:
        # Prepend system prompt as first user/system turn for Ollama
        ollama_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
        resp = ollama.chat(model=OLLAMA_MODEL, messages=ollama_messages)
        return resp["message"]["content"]
    except Exception as e:
        return f"⚠️ Rokai Core Error: {str(e)} — Is Ollama running? Run: ollama serve"


def generate_response_with_context(messages: list, additional_context: str = None) -> str:
    system = SYSTEM_PROMPT
    if additional_context:
        system += f"\n\nAdditional Context:\n{additional_context}"
    try:
        ollama_messages = [{"role": "system", "content": system}] + messages
        resp = ollama.chat(model=OLLAMA_MODEL, messages=ollama_messages)
        return resp["message"]["content"]
    except Exception as e:
        return f"⚠️ Rokai Core Error: {str(e)}"