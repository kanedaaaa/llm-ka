import requests 

def prompt(text: str):
    mistral_url = "http://127.0.0.1:11434/api/chat"
    data = {
        "model": "mistral",
        "messages": [
            {"role": "user", "content": text}
        ],
        "stream": False
    }

    response = requests.post(mistral_url, json=data)

    response_json = response.json()
    assistant_reply = response_json["message"]["content"]

    return assistant_reply