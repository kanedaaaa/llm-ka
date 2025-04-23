import requests

def call_mistral(messages):
    """
    messages: List of dicts like [{"role": "user", "content": "..."}, ...]
    """
    mistral_url = "http://127.0.0.1:11434/api/chat"
    data = {
        "model": "mistral",
        "messages": messages,
        "stream": False
    }

    response = requests.post(mistral_url, json=data)
    response.raise_for_status()

    response_json = response.json()
    assistant_reply = response_json["message"]["content"]
    return assistant_reply
