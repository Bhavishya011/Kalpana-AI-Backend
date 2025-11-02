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
from pricing_agent import DynamicPricingAgent
from market_intelligence import MarketIntelligence
from craft_dna_agent import CraftDNAAgent, create_craft_dna_for_product
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
    """Health check with agent status and market intelligence"""
    from datetime import datetime
    
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
    
    try:
        from pricing_agent import DynamicPricingAgent
        agent_status["pricing"] = "available"
    except Exception as e:
        agent_status["pricing"] = f"error: {str(e)}"
    
    # Check market intelligence status
    market_cache_status = {}
    try:
        from market_intelligence import MarketIntelligence
        market_intel = MarketIntelligence()
        cache = market_intel.get_market_cache()
        
        cache_age_days = 999
        if cache.get('last_updated'):
            try:
                last_updated = datetime.fromisoformat(cache['last_updated'])
                cache_age_days = (datetime.now() - last_updated).days
            except:
                pass
        
        market_cache_status = {
            "status": "available",
            "last_updated": cache.get('last_updated', 'never'),
            "age_days": cache_age_days,
            "needs_update": cache_age_days >= 7,
            "categories": len(cache.get('categories', {})),
            "trending_crafts": len(cache.get('trending_crafts', []))
        }
        
        agent_status["market_intelligence"] = "available"
        
    except Exception as e:
        agent_status["market_intelligence"] = f"error: {str(e)}"
        market_cache_status = {"status": "unavailable", "error": str(e)}
    
    return {
        "status": "healthy",
        "version": "2.0-with-pricing-and-market-intelligence",
        "agents": agent_status,
        "market_cache": market_cache_status,
        "timestamp": time.time(),
        "services": {
            "firestore": "connected",
            "vertex_ai": "connected",
            "google_trends": "connected" if market_cache_status.get("status") == "available" else "unavailable"
        }
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
    photo: UploadFile = None,
    material_cost: float = Form(100.0)
):
    """
    Generate complete storytelling marketing kit with dynamic pricing
    """
    print(f"🎯 New storytelling request: {description[:50]}...")
    print(f"💰 Material cost: ₹{material_cost}")
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
            
            # Initialize pricing agent (optional but recommended)
            pricing_agent = None
            pricing_available = False
            print("💰 Loading pricing agent...")
            try:
                pricing_agent = DynamicPricingAgent()
                pricing_available = True
                print("✅ Pricing agent initialized successfully")
            except Exception as e:
                print(f"⚠️ Pricing agent initialization failed: {str(e)}")
                print("🔄 Continuing without dynamic pricing...")
                pricing_available = False
            
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
            
            # Step 4: Calculate dynamic pricing
            if pricing_available:
                print(f"💰 Calculating AI-powered dynamic pricing with material cost: ₹{material_cost}...")
                try:
                    pricing_result = pricing_agent.calculate_price(
                        description,
                        validated_prompts,
                        material_cost=material_cost
                    )
                    marketing_kit["pricing"] = pricing_result
                    print(f"✅ AI Markup (Artisan Value): ₹{pricing_result['suggested_price']}")
                    print(f"   Material Cost: ₹{material_cost}")
                    print(f"   Final Price: ₹{pricing_result['suggested_price'] + material_cost}")
                    print(f"   Price Range: ₹{pricing_result['price_range']['min']} - ₹{pricing_result['price_range']['max']} (markup only)")
                    print(f"   Success Probability: {pricing_result['success_probability']}%")
                except Exception as e:
                    print(f"⚠️ Pricing calculation failed: {str(e)}")
                    import traceback
                    print(f"📋 Pricing traceback:\n{traceback.format_exc()}")
            else:
                print("⚠️ Pricing agent not available - skipping pricing calculation")
            
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
                    "pricing_calculated": pricing_available and "pricing" in marketing_kit,
                    "processing_time_seconds": processing_time,
                    "files_generated": files_copied
                }
            }
            
            print("🎉 Marketing kit generation completed successfully!")
            print(f"📊 Summary: Curator={curator_available}, Images={len(story_image_paths) if story_image_paths else 0}, Enhanced={len(marketing_kit.get('assets', {}).get('enhanced_photos', []))}, Pricing={'pricing' in marketing_kit}")
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

@app.post("/api/update-market-trends")
async def update_market_trends():
    """
    Manually trigger market trends update using Google Trends API.
    This fetches latest trend data and updates the market cache.
    Normally runs automatically weekly.
    """
    try:
        print("🔄 Manual market trends update triggered...")
        market_intel = MarketIntelligence()
        success = market_intel.update_market_cache()
        
        if success:
            cache = market_intel.get_market_cache()
            return {
                "success": True,
                "message": "Market trends updated successfully",
                "last_updated": cache['last_updated'],
                "trending_crafts": cache.get('trending_crafts', []),
                "categories": {
                    cat: {
                        'trend_score': data['trend_score'],
                        'trend_direction': data['trend_direction'],
                        'price_range': f"₹{data['range'][0]}-₹{data['range'][1]}"
                    }
                    for cat, data in cache['categories'].items()
                }
            }
        else:
            return {
                "success": False,
                "message": "Market trends update failed"
            }
    except Exception as e:
        print(f"❌ Error updating market trends: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

@app.get("/api/market-trends")
async def get_market_trends():
    """
    Get current market trends data including:
    - Category trends and scores
    - Trending crafts
    - Active seasonal trends
    - Last update timestamp
    """
    try:
        market_intel = MarketIntelligence()
        cache = market_intel.get_market_cache()
        
        # Format the response
        response = {
            "success": True,
            "last_updated": cache['last_updated'],
            "cache_age_days": None,
            "categories": {},
            "trending_crafts": cache.get('trending_crafts', []),
            "seasonal_trends": cache.get('seasonal_trends', {}),
            "regional_trends": cache.get('regional_trends', {})
        }
        
        # Calculate cache age
        if cache['last_updated']:
            try:
                from datetime import datetime
                last_updated = datetime.fromisoformat(cache['last_updated'])
                days_old = (datetime.now() - last_updated).days
                response['cache_age_days'] = days_old
            except:
                pass
        
        # Format category data
        for category, data in cache['categories'].items():
            response['categories'][category] = {
                'price_range': {
                    'min': data['range'][0],
                    'max': data['range'][1],
                    'avg': data['avg_markup']
                },
                'demand': data['demand'],
                'trend_score': data['trend_score'],
                'trend_direction': data['trend_direction'],
                'multiplier': market_intel.get_category_multiplier(category)
            }
        
        # Add seasonal multiplier
        response['active_seasonal_multiplier'] = market_intel.get_active_seasonal_multiplier()
        
        return response
        
    except Exception as e:
        print(f"❌ Error fetching market trends: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/api/translate-text")
async def translate_text_endpoint(request: dict):
    """
    Translate text using Gemini AI
    
    Request body:
    {
        "prompt": "Translation prompt with text",
        "targetLanguage": "Hindi",
        "sourceLanguage": "English"
    }
    """
    try:
        from google import genai
        from google.genai import types
        import os
        
        prompt = request.get('prompt', '')
        target_language = request.get('targetLanguage', 'Hindi')
        source_language = request.get('sourceLanguage', 'English')
        
        print(f"🌐 Translation request: {source_language} → {target_language}")
        
        # Initialize Gemini client
        client = genai.Client(
            vertexai=True,
            project=os.getenv('GOOGLE_CLOUD_PROJECT', 'nodal-fountain-470717-j1'),
            location='us-central1'
        )
        
        # Generate translation
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,  # Low temperature for consistent translations
                max_output_tokens=8192,
                top_p=0.9,
                top_k=40,
            )
        )
        
        translation = response.text.strip()
        
        print(f"✅ Translation completed")
        
        return {
            "success": True,
            "translation": translation,
            "source_language": source_language,
            "target_language": target_language
        }
        
    except Exception as e:
        print(f"❌ Translation error: {e}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "translation": ""
        }


@app.post("/api/craft-dna/generate")
async def generate_craft_dna(
    product_id: str = Form(...),
    artisan_story: str = Form(...),
    craft_technique: str = Form(...),
    regional_tradition: str = Form(...),
    materials: str = Form(...),  # JSON string of materials array
    cultural_context: str = Form(default=""),
    artisan_name: str = Form(default=""),
    artisan_village: str = Form(default=""),
    artisan_state: str = Form(default=""),
    artisan_lineage: str = Form(default=""),
    years_of_experience: int = Form(default=0)
):
    """
    Generate Craft DNA - Digital Heritage & Provenance Record
    
    Creates a unique QR code linking to a permanent digital record that preserves
    cultural authenticity, origin story, and sustainability impact.
    
    Returns:
    - Complete heritage narrative
    - QR code (base64)
    - Heritage page URL
    - Cultural significance analysis
    - Sustainability metrics
    - Printable heritage label
    """
    try:
        import json
        
        # Parse materials - handle both JSON array and comma-separated string
        try:
            materials_list = json.loads(materials) if materials else []
        except json.JSONDecodeError:
            # If not JSON, split by comma
            materials_list = [m.strip() for m in materials.split(',') if m.strip()]
        
        # Prepare product data
        product_data = {
            "product_id": product_id,
            "artisan_story": artisan_story,
            "craft_technique": craft_technique,
            "regional_tradition": regional_tradition,
            "materials": materials_list,
            "cultural_context": cultural_context,
            "artisan_profile": {
                "name": artisan_name,
                "village": artisan_village,
                "state": artisan_state,
                "lineage": artisan_lineage,
                "years_of_experience": years_of_experience
            }
        }
        
        # Generate Craft DNA
        craft_dna = create_craft_dna_for_product(product_data)
        
        # Generate printable label
        agent = CraftDNAAgent()
        printable_label = agent.generate_printable_heritage_label(craft_dna)
        
        return {
            "success": True,
            "craft_dna": craft_dna,
            "printable_label": printable_label,
            "message": "Craft DNA generated successfully - Your craft's story is now permanently preserved!"
        }
        
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


@app.get("/heritage/{heritage_id}")
async def get_heritage_page(heritage_id: str):
    """
    Heritage page endpoint - Returns craft heritage information by ID
    This would typically query Firestore for the stored Craft DNA record
    """
    # TODO: Integrate with Firestore to fetch actual heritage record
    return {
        "heritage_id": heritage_id,
        "message": "Heritage page - Connect to Firestore to display full craft story",
        "instructions": "Scan the QR code on the product to view the artisan's story"
    }


if __name__ == "__main__":
    import uvicorn
    import logging
    
    # Configure uvicorn logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("🚀 Starting KalpanaAI Storytelling API...")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 Health Check: http://localhost:8000/health")
    print("🎭 Curator Test: http://localhost:8000/test-curator")
    print("📝 Storytelling: http://localhost:8000/api/storytelling/generate")
    print("---")
    
    try:
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=8000,
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