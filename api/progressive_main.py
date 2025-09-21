#!/usr/bin/env python3
"""
Progressive test API - Add imports one by one to find the issue
"""

from fastapi import FastAPI
import tempfile
import os
import json

app = FastAPI(title="KalpanaAI Progressive Test API")

@app.get("/")
async def root():
    return {"message": "KalpanaAI Progressive Test API"}

@app.get("/health")
async def health():
    return {"status": "healthy", "imports": "basic"}

@app.post("/test-storyteller")
async def test_storyteller():
    """Test storyteller import only"""
    try:
        from storyteller_agent import StorytellerAgent
        storyteller = StorytellerAgent()
        return {"status": "success", "message": "Storyteller agent imported successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Storyteller import failed: {str(e)}"}

@app.post("/test-image-generator")
async def test_image_generator():
    """Test image generator import only"""
    try:
        from image_generator_agent import ImageGeneratorAgent
        generator = ImageGeneratorAgent()
        return {"status": "success", "message": "Image generator agent imported successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Image generator import failed: {str(e)}"}

@app.post("/test-synthesizer")
async def test_synthesizer():
    """Test synthesizer import only"""
    try:
        from synthesizer_agent import ContentSynthesizer
        synthesizer = ContentSynthesizer()
        return {"status": "success", "message": "Synthesizer agent imported successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Synthesizer import failed: {str(e)}"}

@app.post("/test-curator")
async def test_curator():
    """Test curator import only"""
    try:
        from curator_agent import CuratorAgent
        curator = CuratorAgent()
        return {"status": "success", "message": "Curator agent imported successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Curator import failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)