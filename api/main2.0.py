# api/main.py
import sys
import os
import tempfile
import time
import json
import shutil
import uuid
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add the correct paths to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
agents_path = os.path.join(project_root, "Agents", "agents")
sys.path.insert(0, agents_path)

# Import all the agents directly
from curator_agent import CuratorAgent
from storyteller_agent import StorytellerAgent
from image_generator_agent import ImageGeneratorAgent
from synthesizer_agent import ContentSynthesizer
# from orchestrator import Orchestrator  # Disabled to fix crash issues

app = FastAPI()

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directory for serving generated assets
os.makedirs("generated_assets", exist_ok=True)
app.mount("/generated", StaticFiles(directory="generated_assets"), name="generated")

@app.get("/")
async def root():
    return {"message": "KalpanaAI Storytelling API"}

@app.get("/favicon.ico")
async def favicon():
    """Handle favicon requests to prevent 404 errors"""
    return {"message": "No favicon available"}

@app.get("/health")
async def health():
    """Health check with agent status"""
    agent_status = {}
    
    try:
        from storyteller_agent import StorytellerAgent
        agent_status["storyteller"] = "available"
    except Exception as e:
        agent_status["storyteller"] = f"error: {str(e)}"
    
    try:
        from image_generator_agent import ImageGeneratorAgent
        agent_status["image_generator"] = "available"
    except Exception as e:
        agent_status["image_generator"] = f"error: {str(e)}"
    
    try:
        from synthesizer_agent import ContentSynthesizer
        agent_status["synthesizer"] = "available"
    except Exception as e:
        agent_status["synthesizer"] = f"error: {str(e)}"
    
    try:
        from curator_agent import CuratorAgent
        agent_status["curator"] = "available"
    except Exception as e:
        agent_status["curator"] = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "version": "2.0-with-curator",
        "agents": agent_status,
        "timestamp": time.time()
    }

@app.post("/test-curator")
async def test_curator_only():
    """Test curator agent initialization specifically"""
    try:
        print("🎭 Testing curator agent initialization...")
        from curator_agent import CuratorAgent
        curator = CuratorAgent()
        print("✅ Curator agent test successful")
        return {
            "status": "success",
            "message": "Curator agent initialized successfully",
            "agent": "curator"
        }
    except Exception as e:
        print(f"❌ Curator agent test failed: {str(e)}")
        import traceback
        print(f"📋 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__,
            "agent": "curator"
        }

@app.post("/test-curator-full")
async def test_curator_full_pipeline(photo: UploadFile):
    """Test complete curator pipeline like the test script"""
    try:
        print("🎭 Testing full curator pipeline...")
        from curator_agent import CuratorAgent
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Save uploaded photo
            input_image = os.path.join(temp_dir, photo.filename)
            with open(input_image, "wb") as buffer:
                content = await photo.read()
                buffer.write(content)
            print(f"📁 Saved test image: {input_image}")
            
            # Initialize curator
            curator = CuratorAgent()
            print("✅ Curator agent initialized")
            
            # Step 1: Test mask generation
            print("🔍 Step 1: Generating mask...")
            try:
                mask = curator.create_mask(input_image)
                mask_path = os.path.join(temp_dir, "mask_debug.png")
                mask.save(mask_path)
                print("✅ mask_debug.png saved! (Check: product should be BLACK)")
            except Exception as e:
                return {"status": "error", "step": "mask", "message": str(e)}
            
            # Step 2: Test studio enhancement
            print("🖼️ Step 2: Creating studio enhancement...")
            try:
                studio = curator.create_studio_shot(input_image)
                studio_path = os.path.join(temp_dir, "studio_test.png")
                
                if hasattr(studio, 'save'):
                    studio.save(studio_path)
                    print("✅ Studio image saved as PIL Image")
                elif hasattr(studio, '_image_bytes'):
                    with open(studio_path, "wb") as f:
                        f.write(studio._image_bytes)
                    print("✅ Studio image saved as VertexImage")
                else:
                    return {"status": "error", "step": "studio", "message": f"Unknown result type: {type(studio)}"}
            except Exception as e:
                print(f"❌ Studio shot failed: {str(e)}")
                return {"status": "error", "step": "studio", "message": str(e)}
            
            # Step 3: Test lifestyle mockup
            print("🏡 Step 3: Creating lifestyle mockup...")
            try:
                lifestyle = curator.create_lifestyle_mockup(input_image)
                lifestyle_path = os.path.join(temp_dir, "lifestyle_test.png")
                
                if hasattr(lifestyle, 'save'):
                    lifestyle.save(lifestyle_path)
                    print("✅ Lifestyle image saved as PIL Image")
                elif hasattr(lifestyle, '_image_bytes'):
                    with open(lifestyle_path, "wb") as f:
                        f.write(lifestyle._image_bytes)
                    print("✅ Lifestyle image saved as VertexImage")
                else:
                    return {"status": "error", "step": "lifestyle", "message": f"Unknown result type: {type(lifestyle)}"}
            except Exception as e:
                print(f"❌ Lifestyle mockup failed: {str(e)}")
                return {"status": "error", "step": "lifestyle", "message": str(e)}
            
            # Copy files to served directory for access
            asset_id = str(uuid.uuid4())
            served_dir = os.path.join("generated_assets", asset_id)
            os.makedirs(served_dir, exist_ok=True)
            
            result_files = []
            for file in ["mask_debug.png", "studio_test.png", "lifestyle_test.png"]:
                src = os.path.join(temp_dir, file)
                if os.path.exists(src):
                    dst = os.path.join(served_dir, file)
                    shutil.copy2(src, dst)
                    result_files.append(f"/generated/{asset_id}/{file}")
            
            print("🎉 SUCCESS! Curator Agent is working with Imagen 4.0 Ultra!")
            
            return {
                "status": "success",
                "message": "Curator Agent is NOW WORKING with Imagen 4.0 Ultra!",
                "test_results": {
                    "mask_generated": True,
                    "studio_enhanced": True,
                    "lifestyle_created": True
                },
                "result_files": result_files,
                "asset_id": asset_id
            }
            
        finally:
            # Cleanup
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
                
    except Exception as e:
        print(f"❌ Curator full test failed: {str(e)}")
        import traceback
        print(f"📋 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }

@app.post("/api/storytelling/generate")
async def generate_storytelling_kit(
    description: str = Form(...),
    photo: UploadFile = None
):
    """
    Generate complete storytelling marketing kit
    """
    print(f"🎯 New storytelling request: {description[:50]}...")
    start_time = time.time()
    
    try:
        # Create temporary directory for processing
        temp_dir = tempfile.mkdtemp()
        print(f"📁 Created temp directory: {temp_dir}")
        
        try:
            # Save uploaded photo if provided
            photo_path = None
            if photo and photo.filename:
                photo_path = os.path.join(temp_dir, photo.filename)
                with open(photo_path, "wb") as buffer:
                    content = await photo.read()
                    buffer.write(content)
                print(f"📷 Photo saved: {photo.filename} ({len(content)} bytes)")
            
            # Initialize agents individually instead of using orchestrator
            print("🚀 Initializing AI agents...")
            
            # Initialize storyteller (required)
            print("📖 Loading storyteller agent...")
            try:
                storyteller = StorytellerAgent()
                print("✅ Storyteller agent initialized successfully")
            except Exception as e:
                print(f"❌ Storyteller initialization failed: {str(e)}")
                raise Exception(f"Critical agent failure - Storyteller: {str(e)}")
            
            # Initialize image generator (required)
            print("🖼️ Loading image generator agent...")
            try:
                image_generator = ImageGeneratorAgent()
                print("✅ Image generator agent initialized successfully")
            except Exception as e:
                print(f"❌ Image generator initialization failed: {str(e)}")
                raise Exception(f"Critical agent failure - Image Generator: {str(e)}")
            
            # Initialize synthesizer (required)
            print("🎨 Loading synthesizer agent...")
            try:
                synthesizer = ContentSynthesizer()
                print("✅ Synthesizer agent initialized successfully")
            except Exception as e:
                print(f"❌ Synthesizer initialization failed: {str(e)}")
                raise Exception(f"Critical agent failure - Synthesizer: {str(e)}")
            
            # Initialize curator (optional - might fail)
            curator = None
            curator_available = False
            if photo_path:
                print("🎭 Attempting to load curator agent for image enhancement...")
                try:
                    curator = CuratorAgent()
                    curator_available = True
                    print("✅ Curator agent initialized successfully")
                except Exception as e:
                    print(f"⚠️ Curator agent initialization failed: {str(e)}")
                    print("🔄 Continuing without image enhancement...")
                    curator_available = False
            else:
                print("📷 No photo provided - skipping curator agent initialization")
            
            # Run storytelling pipeline directly
            print("\n🎬 Starting storytelling pipeline...")
            
            # Step 0: Enhance uploaded photo if curator is available
            enhanced_photo_path = photo_path
            if photo_path and curator_available:
                print(f"🎨 Enhancing uploaded photo: {photo_path}")
                try:
                    # First, test mask generation (for debugging)
                    print("🔍 Testing mask generation...")
                    try:
                        mask = curator.create_mask(photo_path)
                        mask_debug_path = os.path.join(temp_dir, "mask_debug.png")
                        mask.save(mask_debug_path)
                        print("✅ Mask generated successfully (check: product should be BLACK)")
                    except Exception as mask_error:
                        print(f"⚠️ Mask generation failed: {str(mask_error)}")
                        print("🔄 Continuing with enhancement anyway...")
                    
                    # Create both studio and lifestyle versions
                    print("🖼️ Creating studio enhancement...")
                    studio_result = curator.create_studio_shot(photo_path, upscale=False)
                    
                    print("🏡 Creating lifestyle mockup...")
                    lifestyle_result = curator.create_lifestyle_mockup(photo_path, upscale=False)
                    
                    # Save enhanced images to temp directory
                    studio_path = os.path.join(temp_dir, "enhanced_studio.jpg")
                    lifestyle_path = os.path.join(temp_dir, "enhanced_lifestyle.jpg")
                    
                    # Handle different result types (PIL Image vs VertexImage)
                    print("💾 Saving studio enhancement...")
                    if hasattr(studio_result, 'save'):
                        # It's a PIL Image
                        studio_result.save(studio_path)
                        print("✅ Studio image saved as PIL Image")
                    elif hasattr(studio_result, '_image_bytes'):
                        # It's a VertexImage
                        with open(studio_path, "wb") as f:
                            f.write(studio_result._image_bytes)
                        print("✅ Studio image saved as VertexImage")
                    else:
                        # Try to handle it as a generic object
                        print(f"🔍 Studio result type: {type(studio_result)}")
                        # Fallback: try to save directly
                        studio_result.save(studio_path)
                        print("✅ Studio image saved (fallback method)")
                    
                    print("💾 Saving lifestyle enhancement...")
                    if hasattr(lifestyle_result, 'save'):
                        # It's a PIL Image
                        lifestyle_result.save(lifestyle_path)
                        print("✅ Lifestyle image saved as PIL Image")
                    elif hasattr(lifestyle_result, '_image_bytes'):
                        # It's a VertexImage
                        with open(lifestyle_path, "wb") as f:
                            f.write(lifestyle_result._image_bytes)
                        print("✅ Lifestyle image saved as VertexImage")
                    else:
                        # Try to handle it as a generic object
                        print(f"🔍 Lifestyle result type: {type(lifestyle_result)}")
                        # Fallback: try to save directly
                        lifestyle_result.save(lifestyle_path)
                        print("✅ Lifestyle image saved (fallback method)")
                    
                    enhanced_photo_path = studio_path  # Use studio version as primary
                    print(f"✅ Photo enhanced successfully: {studio_path}, {lifestyle_path}")
                    
                except Exception as e:
                    print(f"❌ Photo enhancement failed: {str(e)}")
                    print(f"🔍 Error type: {type(e).__name__}")
                    import traceback
                    print(f"📋 Enhancement traceback:\n{traceback.format_exc()}")
                    print("🔄 Using original photo...")
                    enhanced_photo_path = photo_path
            
            # Step 1: Generate storytelling content
            print("📝 Generating storytelling content...")
            image_prompts = storyteller.generate_image_prompts(description)
            print("✅ Image prompts generated")
            
            print("🔍 Validating prompts...")
            validated_prompts = storyteller.validate_prompts(image_prompts, description)
            print("✅ Prompts validated successfully")
            
            # Step 2: Generate images
            print("🖼️ Generating story images...")
            story_image_paths = image_generator.create_story_images(validated_prompts, output_dir=temp_dir)
            print(f"✅ Generated {len(story_image_paths) if story_image_paths else 0} story images")
            
            # Step 3: Create marketing kit
            print("📦 Creating marketing kit...")
            marketing_kit = {
                "story_title": validated_prompts.get("story_title", ""),
                "story_text": validated_prompts.get("story_text", ""),
                "emotional_theme": validated_prompts.get("emotional_theme", ""),
                "assets": {
                    "story_images": story_image_paths if story_image_paths else [],
                    "image_prompts": validated_prompts.get("image_prompts", [])
                }
            }
            
            # Add enhanced photos if curator was used
            if photo_path and curator_available:
                marketing_kit["assets"]["enhanced_photos"] = []
                studio_path = os.path.join(temp_dir, "enhanced_studio.jpg")
                lifestyle_path = os.path.join(temp_dir, "enhanced_lifestyle.jpg")
                mask_debug_path = os.path.join(temp_dir, "mask_debug.png")
                
                if os.path.exists(studio_path):
                    marketing_kit["assets"]["enhanced_photos"].append("enhanced_studio.jpg")
                if os.path.exists(lifestyle_path):
                    marketing_kit["assets"]["enhanced_photos"].append("enhanced_lifestyle.jpg")
                if os.path.exists(mask_debug_path):
                    marketing_kit["assets"]["enhanced_photos"].append("mask_debug.png")
                    
                print(f"✅ Added {len(marketing_kit['assets']['enhanced_photos'])} enhanced photos to kit")
                
                # Also add the original uploaded photo for comparison
                if photo_path and os.path.exists(photo_path):
                    original_filename = os.path.basename(photo_path)
                    marketing_kit["assets"]["original_photo"] = original_filename
                    print(f"✅ Added original photo: {original_filename}")
            
            print("✅ Marketing kit structure created")
            
            # Create social post if we have images
            if story_image_paths and len(story_image_paths) > 0:
                print("📱 Creating social media post...")
                social_post_path = os.path.join(temp_dir, "story_post.jpg")
                try:
                    social_post = synthesizer.create_story_post(
                        validated_prompts, 
                        story_image_paths[0],
                        output_path=social_post_path
                    )
                    marketing_kit["assets"]["social_post"] = "story_post.jpg"
                    print("✅ Social media post created successfully")
                except Exception as e:
                    print(f"⚠️ Social post creation failed: {str(e)}")
            
            # Save marketing kit
            print("💾 Saving marketing kit to JSON...")
            kit_path = os.path.join(temp_dir, "marketing_kit.json")
            with open(kit_path, "w", encoding="utf-8") as f:
                json.dump(marketing_kit, f, indent=2, ensure_ascii=False)
            print("✅ Marketing kit saved successfully")
            
            # Copy assets to served directory
            print("📂 Copying assets to served directory...")
            asset_id = str(uuid.uuid4())
            served_dir = os.path.join("generated_assets", asset_id)
            os.makedirs(served_dir, exist_ok=True)
            print(f"📁 Created served directory: {served_dir}")
            
            # Copy all generated files
            files_copied = 0
            for file in os.listdir(temp_dir):
                src = os.path.join(temp_dir, file)
                dst = os.path.join(served_dir, file)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    files_copied += 1
            print(f"✅ Copied {files_copied} files to served directory")
            
            # Update paths to use served URLs
            if "assets" in marketing_kit:
                if "story_images" in marketing_kit["assets"]:
                    marketing_kit["assets"]["story_images"] = [
                        f"/generated/{asset_id}/{os.path.basename(img)}" 
                        for img in marketing_kit["assets"]["story_images"]
                    ]
                if "social_post" in marketing_kit["assets"]:
                    marketing_kit["assets"]["social_post"] = f"/generated/{asset_id}/{marketing_kit['assets']['social_post']}"
                if "enhanced_photos" in marketing_kit["assets"]:
                    marketing_kit["assets"]["enhanced_photos"] = [
                        f"/generated/{asset_id}/{photo}" 
                        for photo in marketing_kit["assets"]["enhanced_photos"]
                    ]
                if "original_photo" in marketing_kit["assets"]:
                    marketing_kit["assets"]["original_photo"] = f"/generated/{asset_id}/{marketing_kit['assets']['original_photo']}"
            
            print("🔗 Updated asset URLs for serving")
            
            # Calculate processing time
            end_time = time.time()
            processing_time = round(end_time - start_time, 2)
            
            # Create response with detailed status
            response_data = {
                "status": "success",
                "marketing_kit": marketing_kit,
                "asset_id": asset_id,
                "message": "Storytelling marketing kit generated successfully!",
                "processing_info": {
                    "curator_used": curator_available,
                    "photo_enhanced": curator_available and photo_path is not None,
                    "story_images_generated": len(story_image_paths) if story_image_paths else 0,
                    "social_post_created": "social_post" in marketing_kit.get("assets", {}),
                    "enhanced_photos_count": len(marketing_kit.get("assets", {}).get("enhanced_photos", [])),
                    "processing_time_seconds": processing_time,
                    "files_generated": files_copied
                }
            }
            
            print("🎉 Marketing kit generation completed successfully!")
            print(f"📊 Summary: Curator={curator_available}, Images={len(story_image_paths) if story_image_paths else 0}, Enhanced={len(marketing_kit.get('assets', {}).get('enhanced_photos', []))}")
            print(f"⏱️ Total processing time: {processing_time} seconds")
            print(f"📁 Files generated: {files_copied}")
            print(f"🆔 Asset ID: {asset_id}")
            
            return response_data
                
        finally:
            # Clean up temp directory with retry logic for Windows
            print("🧹 Cleaning up temporary files...")
            try:
                shutil.rmtree(temp_dir)
                print("✅ Temporary directory cleaned successfully")
            except Exception as e:
                print(f"⚠️ First cleanup attempt failed: {str(e)}")
                # On Windows, sometimes files are locked briefly
                time.sleep(1)  # Wait a moment
                try:
                    shutil.rmtree(temp_dir)
                    print("✅ Temporary directory cleaned on retry")
                except Exception as e2:
                    print(f"⚠️ Cleanup failed completely: {str(e2)}")
                    print("💡 This is OK - OS will clean it up later")
                    # This is OK, OS will clean it up later
                
    except Exception as e:
        print(f"❌ Error in storytelling pipeline: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        import traceback
        print(f"📋 Full traceback:\n{traceback.format_exc()}")
        return {
            "status": "error",
            "message": str(e),
            "error_type": type(e).__name__
        }

if __name__ == "__main__":
    import uvicorn
    import logging
    
    # Configure uvicorn logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Get port from environment (Cloud Run sets this)
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Starting KalpanaAI Storytelling API...")
    print(f"📍 Server will be available at: http://localhost:{port}")
    print(f"📖 API Documentation: http://localhost:{port}/docs")
    print(f"🔧 Health Check: http://localhost:{port}/health")
    print(f"🎭 Curator Test: http://localhost:{port}/test-curator")
    print(f"📝 Storytelling: http://localhost:{port}/api/storytelling/generate")
    print("---")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=port,
            log_level="info",
            access_log=True,
            reload=False,  # Disable reload to prevent crashes
            workers=1      # Single worker for stability
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user (Ctrl+C)")
    except Exception as e:
        print(f"❌ Server error: {str(e)}")
        import traceback
        print(f"📋 Server traceback:\n{traceback.format_exc()}")
    finally:
        print("👋 KalpanaAI API Server shutdown complete")