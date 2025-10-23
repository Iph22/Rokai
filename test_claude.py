# test_claude.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

print("Testing Claude API connection...\n")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=500,
    system="You are Rokai, Arcyn's core intelligence.",
    messages=[
        {"role": "user", "content": "Introduce yourself briefly."}
    ]
)

print("✓ Connection successful!\n")
print("Rokai says:")
print(response.content[0].text)