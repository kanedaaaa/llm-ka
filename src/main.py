from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, List
from fastapi.middleware.cors import CORSMiddleware

from mistral import call_mistral
from translator import translate_to_georgian, translate_to_english

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        updated_history = payload.history.copy()
        user_msg = Message(role="user", ge=payload.new_message_ge, en=en_input)

        updated_history.append(user_msg)

        mistral_messages = [{"role": m.role, "content": m.en} for m in updated_history]
        en_response = call_mistral(mistral_messages)
        ge_response = translate_to_georgian(en_response)
        assistant_msg = Message(role="assistant", ge=ge_response, en=en_response)
        
        updated_history.append(assistant_msg)

        return ChatResponse(history=updated_history)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"status": "ok"}

