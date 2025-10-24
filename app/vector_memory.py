# app/vector_memory.py
import os
from supabase import create_client, Client
from anthropic import Anthropic
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize clients
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def create_embedding(text: str) -> list:
    """
    Convert text to vector embedding using Claude
    
    Args:
        text: The text to embed
    
    Returns:
        List of 1024 floats representing the embedding
    """
    # Note: As of now, we'll use a placeholder approach
    # Anthropic doesn't have a public embeddings API yet
    # We'll implement a workaround using text hashing
    # When Anthropic releases embeddings API, we'll update this
    
    # For now, we'll store text and use simple keyword matching
    # This is temporary until proper embeddings are available
    return None


def store_memory(content: str, metadata: dict = None):
    """
    Store a memory in the vector database
    
    Args:
        content: The text content to store
        metadata: Optional metadata (user, timestamp, tags, etc.)
    """
    try:
        data = {
            "content": content,
            "metadata": metadata or {}
        }
        
        result = supabase.table("memories").insert(data).execute()
        return result.data[0] if result.data else None
        
    except Exception as e:
        print(f"Error storing memory: {e}")
        return None


def search_memories(query: str, limit: int = 5):
    """
    Search for relevant memories
    
    Args:
        query: The search query
        limit: Maximum number of results
    
    Returns:
        List of relevant memories
    """
    try:
        # For now, use full-text search
        # We'll upgrade to vector search when embeddings are available
        result = supabase.table("memories") \
            .select("*") \
            .text_search("content", query) \
            .limit(limit) \
            .execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"Error searching memories: {e}")
        # Fallback to getting recent memories
        result = supabase.table("memories") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return result.data if result.data else []


def get_recent_memories(limit: int = 10):
    """
    Get the most recent memories
    
    Args:
        limit: Number of memories to retrieve
    
    Returns:
        List of recent memories
    """
    try:
        result = supabase.table("memories") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        return result.data if result.data else []
        
    except Exception as e:
        print(f"Error getting recent memories: {e}")
        return []