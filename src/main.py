from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, List

from mistral import call_mistral
from translator import translate_to_georgian, translate_to_english

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
        en_input = translate_to_english(payload.new_message_ge) 

        updated_history = payload.history = [{
            "role": "user",
            "get": payload.new_message_ge,
            "en": en_input
        }]

        mistral_messages = [
            {"role": m.role, "content": m.en} for m in updated_history
        ]

        en_response = call_mistral(mistral_messages) 
        ge_response = translate_to_georgian(en_response) 

        updated_history.append({
            "role": "assistant",
            "ge": ge_response,
            "en": en_response
        })

        return {"history": updated_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
