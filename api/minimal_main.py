#!/usr/bin/env python3
"""
Minimal test API to debug deployment issues
"""

from fastapi import FastAPI

app = FastAPI(title="KalpanaAI Test API")

@app.get("/")
async def root():
    return {"message": "KalpanaAI Test API - Minimal Version"}

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "minimal"}

@app.post("/test")
async def test_endpoint():
    return {"message": "Test endpoint working", "status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)