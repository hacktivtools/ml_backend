from fastapi import FastAPI, Request
from gemini_handler import generate_gemini_response

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Gemini API is live!"}

@app.get("/ask")
def ask(prompt: str):
    response = generate_gemini_response(prompt)
    return {"response": response}
