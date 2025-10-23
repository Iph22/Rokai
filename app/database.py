# app/database.py
import sqlite3
import time

# Database file location
DB_PATH = "rokai_memory.db"

# Connect to database
def get_connection():
    """Creates a connection to the SQLite database"""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

# Initialize database
def init_db():
    """Creates the database table if it doesn't exist"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create table for storing conversations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at REAL NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("✓ Database initialized")

# Store a message
def store_message(role, content):
    """
    Saves a message to the database
    
    role: either 'user' or 'assistant'
    content: the actual message text
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO conversations (role, content, created_at) VALUES (?, ?, ?)",
        (role, content, time.time())
    )
    
    conn.commit()
    conn.close()

# Get recent messages
def get_recent_messages(limit=10):
    """
    Retrieves the most recent messages from the database
    
    limit: how many messages to retrieve
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT role, content FROM conversations ORDER BY created_at DESC LIMIT ?",
        (limit,)
    )
    
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse to get chronological order
    rows.reverse()
    
    # Convert to dictionary format
    messages = []
    for role, content in rows:
        messages.append({"role": role, "content": content})
    
    return messages