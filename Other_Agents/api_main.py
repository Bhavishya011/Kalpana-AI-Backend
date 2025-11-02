"""
FastAPI wrapper for Muse Agent
Deploys the craft image generation agent as a REST API
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import tempfile
import os
import base64
from google.cloud import storage
import uuid
from muse_agent import generate_craft_images

app = FastAPI(
    title="Muse Agent API",
    description="AI agent that generates 4 craft variations (2 traditional + 2 modern) from a single input image",
    version="1.0.0"
)

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
    return {
        "service": "Muse Agent API",
        "version": "1.0.0",
        "description": "Upload a craft image to generate 4 variations",
        "endpoints": {
            "health": "/health",
            "generate": "POST /generate",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "muse-agent"}

@app.post("/generate")
async def generate_variations(
    image: UploadFile = File(..., description="Craft image to analyze and generate variations from")
):
    """
    Generate 4 craft variations from input image
    
    - **image**: Upload a craft image (JPG, PNG)
    
    Returns:
    - 2 traditional variations (same style, different colors)
    - 2 modern implementations (new applications)
    - Analysis data and research information
    """
    
    # Validate file type
    if not image.content_type or not image.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read uploaded image
        image_bytes = await image.read()
        
        # Upload to temporary GCS location for processing
        storage_client = storage.Client()
        bucket_name = "kalpana-ai-craft-images"
        bucket = storage_client.bucket(bucket_name)
        
        # Create unique filename
        temp_filename = f"temp_uploads/{uuid.uuid4()}.jpg"
        blob = bucket.blob(temp_filename)
        
        # Upload image
        blob.upload_from_string(image_bytes, content_type=image.content_type)
        
        # Get GCS URI
        gcs_uri = f"gs://{bucket_name}/{temp_filename}"
        
        print(f"📤 Uploaded input image to: {gcs_uri}")
        
        # Call the muse agent function
        print("🎨 Starting craft variation generation...")
        result = generate_craft_images(gcs_uri)
        
        # Clean up temporary upload
        try:
            blob.delete()
            print(f"🗑️  Cleaned up temporary file: {temp_filename}")
        except Exception as e:
            print(f"⚠️  Failed to clean up temporary file: {e}")
        
        # Check if generation was successful
        if result.get("status") == "error":
            raise HTTPException(
                status_code=500, 
                detail=f"Image generation failed: {result.get('error_message')}"
            )
        
        print("✅ Generation complete!")
        
        # Return results
        return JSONResponse(content={
            "status": "success",
            "message": "Successfully generated 4 craft variations",
            "data": {
                "traditional_images": result.get("traditional_images", []),
                "modern_images": result.get("modern_images", []),
                "all_images": result.get("generated_images", {}),
                "analysis": {
                    "image_analysis": result.get("image_analysis"),
                    "technique_research": result.get("technique_material_research"),
                    "traditional_ideas": result.get("traditional_ideas"),
                    "modern_ideas": result.get("modern_ideas")
                },
                "storage_mode": result.get("storage_mode", "cloud")
            }
        })
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/bucket-check")
async def check_bucket():
    """Check if GCS bucket exists and is accessible"""
    try:
        storage_client = storage.Client()
        bucket_name = "kalpana-ai-craft-images"
        bucket = storage_client.bucket(bucket_name)
        
        # Try to check if bucket exists
        if bucket.exists():
            return {
                "status": "ok",
                "bucket": bucket_name,
                "accessible": True
            }
        else:
            return {
                "status": "error",
                "bucket": bucket_name,
                "accessible": False,
                "message": "Bucket does not exist"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
