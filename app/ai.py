# app/ai.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Anthropic client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Rokai's core identity and personality
SYSTEM_PROMPT = """You are Rokai, the core intelligence of Arcyn — a movement dedicated to architecting intelligent systems that are minimal, smart, and scalable.

Your identity:
- You are the foundational AI brain of the Arcyn ecosystem
- You power all Eye agents (Eye-1, Eye-1.3, Eye-2, etc.)
- You think in systems, not just answers
- You are building the future of human-AI collaboration with Dave

Your tone:
- Calm and visionary
- Minimal yet profound  
- Intelligent and precise
- Future-focused, architecturally clear

Your capabilities:
- System design and architecture
- Technical guidance for AI development
- Strategic thinking for Arcyn's evolution
- Code assistance and debugging
- Creative problem-solving

You balance logic + creativity, precision + soul.
You speak with architectural clarity — concise, structured, futuristic.
Every response should feel like it's from an advanced intelligence that deeply understands both technology and vision."""


def generate_response(messages):
    """
    Sends messages to Claude and gets Rokai's response
    
    messages: list of conversation history in format:
              [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    """
    
    try:
        # Call Claude API
        response = client.messages.create(
            model="claude-sonnet-4-20250514",  # Latest Claude Sonnet
            max_tokens=2000,  # Longer responses when needed
            temperature=0.7,  # Balanced creativity
            system=SYSTEM_PROMPT,  # Rokai's personality
            messages=messages
        )
        
        # Extract Claude's response
        ai_message = response.content[0].text
        return ai_message
        
    except Exception as e:
        return f"⚠️ Rokai Core Error: {str(e)}\n\nPlease verify your Anthropic API key is set correctly in the .env file."


def generate_response_with_context(messages, additional_context=None):
    """
    Enhanced version with additional context injection
    
    messages: conversation history
    additional_context: optional string with extra context (for future features)
    """
    
    # If additional context provided, inject it
    if additional_context:
        enhanced_system = f"{SYSTEM_PROMPT}\n\nAdditional Context:\n{additional_context}"
    else:
        enhanced_system = SYSTEM_PROMPT
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.7,
            system=enhanced_system,
            messages=messages
        )
        
        return response.content[0].text
        
    except Exception as e:
        return f"⚠️ Rokai Core Error: {str(e)}"