from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from app.services.chat_analysis.main import ChatAnalysis
from app.services.personality_engine.main import PersonalityEngine
from langchain_core.messages import HumanMessage
from app.services.personality_engine.prompts import PERSONAS

app = FastAPI(title="Companion AI Memory & Persona Engine")

class ChatRequest(BaseModel):
    user_id: str
    message: str
    persona: str = "calm_mentor"

class HistoryMessage(BaseModel):
    role: str
    content: str

class AnalysisRequest(BaseModel):
    history: List[HistoryMessage]

user_sessions: Dict[str, PersonalityEngine] = {}

def get_engine(user_id: str, persona: str) -> PersonalityEngine:
    """
    Retrieve or create a PersonalityEngine for a specific user.
    If the user exists but requests a new persona, we update the persona 
    but KEEP the conversation history (context).
    """
    if user_id not in user_sessions:
        user_sessions[user_id] = PersonalityEngine(
            model="gemini-2.5-flash",
            persona=persona
        )
    else:
        new_prompt = PERSONAS.get(persona)
        if new_prompt:
            user_sessions[user_id].persona_prompt = new_prompt
            
    return user_sessions[user_id]

@app.get("/")
def health_check():
    return {"status": "active", "service": "Companion AI"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """
    Chat with a specific persona. 
    State is maintained per user_id.
    """
    try:
        engine = get_engine(request.user_id, request.persona)
        
        user_msg = HumanMessage(content=request.message)
        
        response = await engine.invoke(user_message=user_msg)
        
        return {
            "user_id": request.user_id,
            "persona": request.persona,
            "response": response.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze")
async def analyze_memory(request: AnalysisRequest):
    """
    Takes a list of 30+ messages and extracts structured memory.
    State-less endpoint (analyzes the provided history blob).
    """
    try:
        analyzer = ChatAnalysis(model="gemini-2.5-flash")
        
        formatted_history = [
            {"role": msg.role, "content": msg.content} for msg in request.history
        ]
        
        result = await analyzer.invoke(chat_history=formatted_history)
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))