"""
FastAPI wrapper for Artisan Mentor Agent
Provides REST API endpoints for the artisan tutoring system
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uvicorn
import os
import base64
from datetime import datetime

# Import the artisan mentor tools
from artisan_mentor.tools import (
    start_artisan_journey,
    get_adaptive_lesson,
    submit_adaptive_work,
    get_comprehensive_dashboard,
    analyze_craft_for_learning,
    text_to_speech_assist,
    speech_to_text_assist
)

app = FastAPI(
    title="Artisan Mentor API",
    description="Comprehensive AI tutor API for artisan business education",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class UserProfile(BaseModel):
    user_id: Optional[str] = None
    name: Optional[str] = None
    learning_style: str = "visual"
    language: str = "en"
    current_skill_level: str = "beginner"
    craft_analysis: Optional[Dict[str, Any]] = None

class LessonRequest(BaseModel):
    user_id: str
    lesson_id: str
    format: str = "multimodal"

class SubmissionRequest(BaseModel):
    user_id: str
    lesson_id: str
    submission: Dict[str, Any]

class DashboardRequest(BaseModel):
    user_id: str

class TTSRequest(BaseModel):
    text: str
    language: str = "en"

class STTRequest(BaseModel):
    audio_uri: str
    language: str = "en"

class AnalyzeCraftRequest(BaseModel):
    image_uri: Optional[str] = None

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Artisan Mentor API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "start_journey": "/start-journey",
            "get_lesson": "/get-lesson",
            "submit_work": "/submit-work",
            "dashboard": "/dashboard",
            "analyze_craft": "/analyze-craft",
            "text_to_speech": "/tts",
            "speech_to_text": "/stt"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "artisan-mentor-api",
        "timestamp": datetime.now().isoformat(),
        "google_cloud_project": os.getenv("GOOGLE_CLOUD_PROJECT", "not-set"),
        "storage_bucket": os.getenv("CLOUD_STORAGE_BUCKET", "not-set")
    }

@app.post("/start-journey")
async def start_journey(profile: UserProfile):
    """
    Start a personalized learning journey for an artisan
    
    - **user_id**: Optional unique identifier (auto-generated if not provided)
    - **name**: Artisan's name
    - **learning_style**: visual, auditory, kinesthetic, or read_write
    - **language**: Language code (en, hi, ta, te, kn, ml, bn, mr, gu)
    - **current_skill_level**: beginner, intermediate, advanced, or expert
    - **craft_analysis**: Optional craft analysis data from analyze-craft endpoint
    """
    try:
        result = start_artisan_journey(profile.dict())
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/get-lesson")
async def get_lesson(request: LessonRequest):
    """
    Get an interactive lesson with multimodal content
    
    - **user_id**: User's unique identifier
    - **lesson_id**: Lesson identifier (e.g., F1.1, M2.1)
    - **format**: Content format (multimodal, text-only, audio-only)
    """
    try:
        result = get_adaptive_lesson(request.user_id, request.lesson_id, request.format)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/submit-work")
async def submit_work(request: SubmissionRequest):
    """
    Submit lesson work for AI-powered validation
    
    - **user_id**: User's unique identifier
    - **lesson_id**: Lesson identifier
    - **submission**: Work submission (text, image URLs, audio URLs, etc.)
    """
    try:
        result = submit_adaptive_work(request.user_id, request.lesson_id, request.submission)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dashboard")
async def dashboard(request: DashboardRequest):
    """
    Get comprehensive business and learning dashboard
    
    - **user_id**: User's unique identifier
    
    Returns learning progress, business metrics, achievements, and recommendations
    """
    try:
        result = get_comprehensive_dashboard(request.user_id)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-craft")
async def analyze_craft(
    image: Optional[UploadFile] = File(None),
    image_uri: Optional[str] = Form(None)
):
    """
    Analyze a craft image for comprehensive insights
    
    Upload an image file or provide a GCS URI (gs://...)
    Returns detailed craft analysis including materials, techniques, market potential, etc.
    """
    try:
        if image:
            # Read uploaded file and convert to base64
            contents = await image.read()
            image_b64 = base64.b64encode(contents).decode('utf-8')
            image_input = f"data:image/jpeg;base64,{image_b64}"
        elif image_uri:
            image_input = image_uri
        else:
            raise HTTPException(status_code=400, detail="Either image file or image_uri must be provided")
        
        result = analyze_craft_for_learning(image_input)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech in multiple Indian languages
    
    - **text**: Text to convert
    - **language**: Language code (en, hi, ta, te, kn, ml, bn, mr, gu)
    
    Returns URL to audio file
    """
    try:
        result = text_to_speech_assist(request.text, request.language)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/stt")
async def speech_to_text(request: STTRequest):
    """
    Convert speech to text in multiple Indian languages
    
    - **audio_uri**: GCS URI of audio file (gs://...)
    - **language**: Language code (en, hi, ta, te, kn, ml, bn, mr, gu)
    
    Returns transcribed text
    """
    try:
        result = speech_to_text_assist(request.audio_uri, request.language)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
