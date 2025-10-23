# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from app.database import init_db, store_message, get_recent_messages
from app.ai import generate_response

# Create FastAPI application
app = FastAPI(title="Rokai Core Intelligence")

# Initialize database when server starts
@app.on_event("startup")
async def startup_event():
    init_db()
    print("🧠 Rokai Core Intelligence online")

# Define what a message looks like
class Message(BaseModel):
    user: str  # Who's sending the message
    text: str  # What they're saying

# Health check endpoint
@app.get("/")
async def root():
    return {
        "status": "online",
        "system": "Rokai Core Intelligence v0.1",
        "message": "AIP-X protocols active"
    }

# Main chat endpoint
@app.post("/ask")
async def ask_rokai(message: Message):
    """
    Main endpoint for talking to Rokai
    
    Receives a message, generates response, stores everything
    """
    
    # 1. Store user's message
    user_message = f"{message.user}: {message.text}"
    store_message("user", user_message)
    
    # 2. Get recent conversation history
    history = get_recent_messages(limit=6)
    
    # 3. Generate Rokai's response
    rokai_response = generate_response(history)
    
    # 4. Store Rokai's response
    store_message("assistant", rokai_response)
    
    # 5. Return response to user
    return {
        "user": message.user,
        "query": message.text,
        "response": rokai_response,
        "status": "success"
    }

# Get conversation history
@app.get("/history")
async def get_history(limit: int = 10):
    """
    Retrieves recent conversation history
    """
    messages = get_recent_messages(limit)
    return {
        "count": len(messages),
        "messages": messages
    }