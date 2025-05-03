from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict
import random

# Initialize FastAPI app
app = FastAPI()

# Sample in-memory "memory" storage
memory_storage = {}

# Placeholder AI Core Logic (for now)
def wisbo_core_logic(query: str, mode: str) -> str:
    # Simple example of behavior change based on mode
    responses = {
        "casual": f"Chill, here's what I think about {query}!",
        "formal": f"Regarding {query}, the answer is as follows...",
        "tech": f"Technically speaking, {query} involves a complex set of principles...",
    }
    return responses.get(mode, f"Here's a response to {query}.")

# Pydantic models for input validation
class AskRequest(BaseModel):
    message: str
    mode: str = "casual"  # Default mode is casual

class SwitchModeRequest(BaseModel):
    mode: str

class MemoryRequest(BaseModel):
    key: str
    value: str

# API Endpoints

@app.post("/ask")
async def ask(request: AskRequest):
    message = request.message
    mode = request.mode

    # Update logic for casual mode
    if mode == "casual":
        reply = f"Chill, here's what I think about {message}?!"
    elif mode == "default":
        reply = f"Here's a response to {message}."
    elif mode == "friendly":
        reply = f"Hey there! Great question: {message}. Let me help 😊"
    else:
        reply = f"Mode '{mode}' is not recognized. Defaulting: {message}."

    return {"response": reply}

@app.post("/switch-mode")
async def switch_mode(request: SwitchModeRequest):
    # Switch the mode (for now, we just simulate with a message)
    return {"status": f"Mode switched to {request.mode}"}

@app.get("/memory")
def get_memory():
    return {"memory": memory_storage}

@app.post("/memory")
async def set_memory(request: MemoryRequest):
    # Store some "memory" for the AI (basic key-value store)
    memory_storage[request.key] = request.value
    return {"status": "Memory updated successfully"}

# Run with 'uvicorn wisbo_api:app --reload' to test
