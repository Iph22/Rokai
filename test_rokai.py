# test_rokai.py
import requests

# Send message to Rokai
response = requests.post(
    "http://127.0.0.1:8000/ask",
    json={
        "user": "Dave",
        "text": "Hello Rokai, what are you?"
    }
)

# Print response
print(response.json()["response"])