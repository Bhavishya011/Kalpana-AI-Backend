#!/usr/bin/env python3
"""
Working API with all agents - rebuild the functionality step by step
"""

from fastapi import FastAPI, Form, UploadFile
import tempfile
import os
import json
import shutil
import uuid

app = FastAPI(title="KalpanaAI Storytelling API - Working Version")

@app.get("/")
async def root():
    return {"message": "KalpanaAI Storytelling API"}

@app.get("/health")
async def health():
    return {"status": "healthy", "agents": "all_available"}

@app.post("/api/storytelling/generate")
async def generate_storytelling_kit(
    description: str = Form(...),
    photo: UploadFile = None
):
    """
    Generate complete storytelling marketing kit
    """
    try:
        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save uploaded photo if provided
            photo_path = None
            if photo and photo.filename:
                photo_path = os.path.join(temp_dir, photo.filename)
                with open(photo_path, "wb") as buffer:
                    content = await photo.read()
                    buffer.write(content)
            
            # Import and initialize agents individually (safer than orchestrator)
            from storyteller_agent import StorytellerAgent
            from image_generator_agent import ImageGeneratorAgent
            from synthesizer_agent import ContentSynthesizer
            
            storyteller = StorytellerAgent()
            image_generator = ImageGeneratorAgent()
            synthesizer = ContentSynthesizer()
            
            # Step 1: Generate storytelling content
            image_prompts = storyteller.generate_image_prompts(description)
            validated_prompts = storyteller.validate_prompts(image_prompts, description)
            
            # Step 2: Generate storytelling images
            story_image_paths = image_generator.create_story_images(validated_prompts, output_dir=temp_dir)
            
            # Step 3: Create marketing assets
            marketing_kit = {
                "story_title": validated_prompts.get("story_title", ""),
                "story_text": validated_prompts.get("story_text", ""),
                "emotional_theme": validated_prompts.get("emotional_theme", ""),
                "assets": {
                    "story_images": story_image_paths if story_image_paths else [],
                    "image_prompts": validated_prompts.get("image_prompts", [])
                }
            }
            
            # Create social post if we have images
            if story_image_paths and len(story_image_paths) > 0:
                social_post_path = os.path.join(temp_dir, "story_post.jpg")
                social_post = synthesizer.create_story_post(
                    validated_prompts, 
                    story_image_paths[0],
                    output_path=social_post_path
                )
                marketing_kit["assets"]["social_post"] = "story_post.jpg"
            
            # Save marketing kit
            kit_path = os.path.join(temp_dir, "marketing_kit.json")
            with open(kit_path, "w", encoding="utf-8") as f:
                json.dump(marketing_kit, f, indent=2, ensure_ascii=False)
            
            # Copy assets to served directory
            asset_id = str(uuid.uuid4())
            served_dir = os.path.join("generated_assets", asset_id)
            os.makedirs(served_dir, exist_ok=True)
            
            # Copy all generated files
            for file in os.listdir(temp_dir):
                src = os.path.join(temp_dir, file)
                dst = os.path.join(served_dir, file)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
            
            # Update paths in marketing kit for serving
            if "assets" in marketing_kit:
                if "story_images" in marketing_kit["assets"]:
                    marketing_kit["assets"]["story_images"] = [
                        f"/generated/{asset_id}/{os.path.basename(img)}" 
                        for img in marketing_kit["assets"]["story_images"]
                    ]
                if "social_post" in marketing_kit["assets"]:
                    marketing_kit["assets"]["social_post"] = f"/generated/{asset_id}/{marketing_kit['assets']['social_post']}"
            
            return {
                "status": "success",
                "asset_id": asset_id,
                "marketing_kit": marketing_kit,
                "message": "Storytelling kit generated successfully"
            }
        
        finally:
            # Cleanup temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except Exception as e:
        return {
            "status": "error",
            "message": f"Generation failed: {str(e)}",
            "error_type": type(e).__name__
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)