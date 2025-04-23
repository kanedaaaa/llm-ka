from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, List

app = FastAPI()

class Message(BaseModel):
    role: Literal["user", "assistant"]
    ge: str
    en: str

class ChatRequest(BaseModel):
    new_message_ge: str
    history: List[Message]


class ChatResponse(BaseModel):
    history: List[Message]

@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest):
    try:
        en_input = payload.new_message_ge # todo actually translate

        updated_history = payload.history = [{
            "role": "user",
            "get": payload.new_message_ge,
            "en": en_input
        }]

        mistral_messages = [
            {"role": m.role, "content": m.en} for m in updated_history
        ]

        en_response = mistral_messages # todo actually call mistral 
        ge_response = en_response # todo actually translate 

        updated_history.append({
            "role": "assistant",
            "ge": ge_response,
            "en": en_response
        })

        return {"history": updated_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
