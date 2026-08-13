import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat_with_ather(request: ChatRequest):
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="المفتاح غير موجود")
    try:
        # استخدام اسم الموديل المعتمد والقياسي للـ SDK
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"أنت أثير (Ather AI)، مهندس ومخترع يجيب بصراحة وإيجاز شديد وبدون أي مقدمات بالعربية.\nالسؤال: {request.message}"
        )
        return {"reply": response.text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
