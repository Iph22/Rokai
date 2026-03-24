# app/agent_handler.py
# ── Swapped: Anthropic → Ollama (llama3, local) ────────────
import os
import ollama
from dotenv import load_dotenv
from app.agents import get_agent, AGENTS

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def generate_agent_response(agent_id: str, messages: list, context: dict = None) -> str:
    agent = get_agent(agent_id)
    if not agent:
        return f"Error: Agent '{agent_id}' not found"

    system_prompt = agent["system_prompt"]

    if context and context.get("memories"):
        memory_context = "\n".join([f"- {m['content']}" for m in context["memories"]])
        system_prompt += f"\n\n[Relevant context from Rokai memory:\n{memory_context}]"

    try:
        ollama_messages = [{"role": "system", "content": system_prompt}] + messages
        resp = ollama.chat(model=OLLAMA_MODEL, messages=ollama_messages)
        return resp["message"]["content"]
    except Exception as e:
        return f"⚠️ {agent['name']} Error: {str(e)} — Is Ollama running?"


def route_to_agent(query: str, context: dict = None) -> str:
    q = query.lower()
    if any(k in q for k in ['code','function','api','debug','error','database','implement','build','python','javascript','sql']):
        return "eye-1.3"
    if any(k in q for k in ['analyze','performance','metrics','monitor','optimize','statistics','data','usage']):
        return "eye-2"
    if any(k in q for k in ['design','ui','ux','visual','layout','color','brand','aesthetic','interface','component']):
        return "eye-3"
    return "eye-1"