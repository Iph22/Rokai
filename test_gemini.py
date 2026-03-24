import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

print("Testing Gemini API connection...\n")

api_key = os.getenv("GEMINI_KEY")
genai.configure(api_key=api_key)

model_name = 'gemini-1.5-flash'
print(f"Trying to use model: {model_name}...")

try:
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Introduce yourself briefly.")
    print(f"✓ Connection successful with {model_name}!\n")
    print(response.text)
except Exception as e:
    print(f"Error with {model_name}: {e}")
