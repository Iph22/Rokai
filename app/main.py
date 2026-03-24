# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent_handler import generate_agent_response, route_to_agent
from app.agents import get_agent, list_agents
from app.ai import generate_response
from app.database import init_db, store_message, get_recent_messages
from app.vector_memory import store_memory, search_memories, get_recent_memories as get_vector_memories

VERSION = "v0.3"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print(f"[ROKAI] Core Intelligence {VERSION} online")
    print("[ROKAI] Enhanced memory system active")
    print("[ROKAI] Eye Agent System loaded")
    yield


# Create FastAPI application
app = FastAPI(title=f"Rokai Core Intelligence {VERSION}", lifespan=lifespan)


# Define what a message looks like
class Message(BaseModel):
    user: str
    text: str


# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "system": f"Rokai Core Intelligence {VERSION}",
        "features": ["Enhanced Memory", "Semantic Search", "Context-Aware", "Eye Agent System"],
        "message": "AIP-X protocols active",
    }


# Main chat endpoint with enhanced memory
@app.post("/ask")
async def ask_rokai(message: Message):
    """Enhanced chat endpoint with semantic memory."""

    # 1. Store user's message in both systems
    user_message = f"{message.user}: {message.text}"
    store_message("user", user_message)
    store_memory(user_message, metadata={"user": message.user, "type": "query"})

    # 2. Search for relevant past memories
    relevant_memories = search_memories(message.text, limit=3)

    # 3. Get recent conversation history
    recent_history = get_recent_messages(limit=4)

    # 4. Build enhanced context
    context_messages = []

    # Add relevant memories as context (if any found)
    if relevant_memories:
        memory_context = "\n".join([f"- {mem['content']}" for mem in relevant_memories])
        context_messages.append({
            "role": "user",
            "content": f"[Relevant past context:\n{memory_context}]",
        })

    # Add recent history then current message
    context_messages.extend(recent_history)
    context_messages.append({"role": "user", "content": message.text})

    # 5. Generate Rokai's response
    rokai_response = generate_response(context_messages)

    # 6. Store Rokai's response in both systems
    store_message("assistant", rokai_response)
    store_memory(rokai_response, metadata={"user": "rokai", "type": "response"})

    return {
        "user": message.user,
        "query": message.text,
        "response": rokai_response,
        "context_used": {
            "relevant_memories": len(relevant_memories),
            "recent_messages": len(recent_history),
        },
        "status": "success",
    }


# Get conversation history
@app.get("/history")
async def get_history(limit: int = 10):
    """Retrieves recent conversation history."""
    messages = get_recent_messages(limit)
    return {"count": len(messages), "messages": messages}


# Search memories
@app.get("/memories/search")
async def search_memory(query: str, limit: int = 5):
    """Search stored memories by relevance."""
    memories = search_memories(query, limit)
    return {"query": query, "count": len(memories), "memories": memories}


# Get recent memories
@app.get("/memories")
async def get_memories(limit: int = 20):
    """Get recent memories from vector storage."""
    memories = get_vector_memories(limit)
    return {"count": len(memories), "memories": memories}


# List agents
@app.get("/agents")
async def get_agents():
    """List all available Eye agents."""
    agents = list_agents()
    return {"count": len(agents), "agents": agents}


@app.post("/agent/{agent_id}")
async def talk_to_agent(agent_id: str, message: Message):
    """
    Talk to a specific Eye agent.
    Routes conversation through a specialized AI personality.
    """
    # Validate agent exists — return proper 404 if not found
    agent_config = get_agent(agent_id)
    if not agent_config:
        raise HTTPException(
            status_code=404,
            detail={
                "error": f"Agent '{agent_id}' not found",
                "available_agents": [a["id"] for a in list_agents()],
            },
        )

    # Store user message
    user_message = f"{message.user}: {message.text}"
    store_message("user", user_message)
    store_memory(user_message, metadata={"user": message.user, "agent": agent_id, "type": "query"})

    # Get relevant memories and recent history
    relevant_memories = search_memories(message.text, limit=3)
    recent_history = get_recent_messages(limit=4)

    # Build context messages
    context_messages = []
    context_messages.extend(recent_history)
    context_messages.append({"role": "user", "content": message.text})

    # Generate agent response
    response = generate_agent_response(
        agent_id=agent_id,
        messages=context_messages,
        context={"memories": relevant_memories},
    )

    # Store agent response
    agent_message = f"{agent_config['name']}: {response}"
    store_message("assistant", agent_message)
    store_memory(agent_message, metadata={"agent": agent_id, "type": "response"})

    return {
        "agent": agent_config["name"],
        "agent_id": agent_id,
        "title": agent_config["title"],
        "user": message.user,
        "query": message.text,
        "response": response,
        "status": "success",
    }


@app.post("/ask/smart")
async def smart_routing(message: Message):
    """Intelligent routing — automatically selects best agent for the query."""

    # Determine which agent to use
    agent_id = route_to_agent(message.text)
    agent_config = get_agent(agent_id)

    # Store user message
    user_message = f"{message.user}: {message.text}"
    store_message("user", user_message)
    store_memory(user_message, metadata={
        "user": message.user, "agent": agent_id, "type": "query", "routed": True,
    })

    # Get context
    relevant_memories = search_memories(message.text, limit=3)
    recent_history = get_recent_messages(limit=4)

    # Build messages
    context_messages = []
    context_messages.extend(recent_history)
    context_messages.append({"role": "user", "content": message.text})

    # Generate response
    response = generate_agent_response(
        agent_id=agent_id,
        messages=context_messages,
        context={"memories": relevant_memories},
    )

    # Store response
    agent_message = f"{agent_config['name']}: {response}"
    store_message("assistant", agent_message)
    store_memory(agent_message, metadata={"agent": agent_id, "type": "response"})

    return {
        "agent": agent_config["name"],
        "agent_id": agent_id,
        "title": agent_config["title"],
        "routing": "automatic",
        "user": message.user,
        "query": message.text,
        "response": response,
        "status": "success",
    }