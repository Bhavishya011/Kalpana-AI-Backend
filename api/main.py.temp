#!/usr/bin/env python3
"""
Ultra-minimal working API to fix 405 errors
"""

from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI(title="KalpanaAI Storytelling API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "KalpanaAI Storytelling API - Working"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "minimal-working"}

@app.post("/api/storytelling/generate")
async def generate_storytelling_kit(
    description: str = Form(...),
    photo: UploadFile = File(None)
):
    """
    Generate storytelling kit - minimal working version
    """
    try:
        # Return a simple success response for now
        return {
            "status": "success",
            "message": "API endpoint working correctly",
            "received_description": description,
            "photo_provided": photo.filename if photo else None,
            "marketing_kit": {
                "story_title": f"Story for {description}",
                "story_text": f"A beautiful story about {description}...",
                "emotional_theme": "authentic",
                "assets": {
                    "story_images": [],
                    "image_prompts": ["A beautiful scene showcasing the artisan's craft"]
                }
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error: {str(e)}",
            "error_type": type(e).__name__
        }

# Additional endpoints for testing
@app.post("/test")
async def test_endpoint():
    return {"message": "Test POST endpoint working"}

@app.get("/test")
async def test_get_endpoint():
    return {"message": "Test GET endpoint working"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)