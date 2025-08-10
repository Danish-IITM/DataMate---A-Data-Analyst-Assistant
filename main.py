from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

chat_history = []  # Stores (sender, message) tuples

@app.get("/", response_class=HTMLResponse)
async def get_chat(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})

@app.post("/send", response_class=HTMLResponse)
async def send_message(request: Request, prompt: str = Form(...)):
    # Save user message
    chat_history.append(("user", prompt))

    # Get Gemini response
    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content(prompt)

    # Save bot response
    chat_history.append(("assistant", result.text))

    return templates.TemplateResponse("index.html", {"request": request, "chat_history": chat_history})
