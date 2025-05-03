# main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from wisbo_logic_core import process_wisbo_prompt  # Replace with your actual function name

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/ask")
async def ask_ai(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    # 🧠 Call your AI core function
    response = process_wisbo_prompt(prompt)

    return {"response": response}
