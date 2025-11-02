from vertexai.generative_models import GenerativeModel, Part
from vertexai.vision_models import ImageGenerationModel
import vertexai
import os
import json
import base64
from typing import List, Dict
from google.cloud import storage
import uuid
from datetime import datetime
import time

# Initialize Vertex AI
vertexai.init(project="nodal-fountain-470717-j1", location="us-central1")

def generate_craft_images(image_input: str) -> Dict[str, List[str]]:
    """
    Complete workflow for analyzing a traditional craft image and generating 4 modern interpretations.
    
    Args:
        image_input (str): Base64 encoded image data or GCS path to an image of the craft.
        
    Returns:
        dict: Dictionary containing 4 generated image paths (2 traditional variations + 2 modern implementations)
    """
    try:
        # Step 1: Analyze the input image
        image_prompt = """
        Analyze this craft image and extract the following visual elements in JSON format:
        - craft_name: Name/type of the craft
        - color_palette: List of 5-7 dominant colors with hex codes and descriptions
        - motifs: Recurring patterns, symbols, or motifs
        - techniques: Inferred techniques based on visual evidence
        - materials: Primary materials used
        - design_structure: Overall design and form
        - style: Artistic style description
        - cultural_context: Cultural or religious significance if any
        - location: Geographic or cultural origin if identifiable
        """
        
        image_file = Part.from_uri(image_input, mime_type="image/jpeg")
        
        image_model = GenerativeModel("gemini-2.0-flash-001")
        image_response = image_model.generate_content([image_prompt, image_file])
        image_analysis = image_response.text

        # Step 2: Research techniques and materials
        research_prompt = f"""
        Based on the following craft analysis, research the specific techniques and materials mentioned with focus on ARTISAN FEASIBILITY:
        
        Image Analysis: {image_analysis}
        
        Provide detailed information about:
        1. Each technique mentioned - how it's traditionally performed by artisans, tools required, step-by-step process, and skill level needed
        2. Each material mentioned - its properties, traditional preparation methods, availability to artisans, and why it's used
        3. Cultural significance of these techniques and materials
        4. Any regional variations in how these techniques are applied
        5. PRACTICAL CONSTRAINTS: What makes these techniques achievable by traditional artisans (time, skill, tools, materials)
        6. ARTISAN WORKFLOW: The complete process from material preparation to final product that an artisan would follow
        
        CRITICAL: Focus on techniques and materials that are accessible and feasible for traditional artisans to work with.
        Format your response as a detailed JSON object with sections for techniques, materials, and artisan_constraints.
        """
        
        research_model = GenerativeModel("gemini-2.0-flash-001")
        research_response = research_model.generate_content(research_prompt)
        technique_material_research = research_response.text
        
        # Step 3: Generate 2 traditional innovative ideas
        traditional_ideas_prompt = f"""
        As a creative director, suggest 2 traditional variations for this craft that maintain the EXACT SAME STYLE as the original.
        CRITICAL CONSTRAINTS: 
        1. You MUST preserve the traditional techniques and materials exactly as they are
        2. Each idea MUST be achievable by traditional artisans using the same techniques and materials
        3. MAINTAIN THE SAME STYLE: Keep the overall form, structure, and artistic style identical to the original
        4. ONLY VARY: Colors, color combinations, or minor design patterns within the same style framework
        5. If there are religious deities involved, keep them respectful and decent
        
        Image Analysis: {image_analysis}
        Technique and Material Research: {technique_material_research}
        
        Generate 2 traditional variations that maintain the original style:
        1. Traditional Variation 1: [Same style as original, different color palette - describe specific color changes]
        2. Traditional Variation 2: [Same style as original, different color scheme - describe specific color changes]
        
        Each variation should:
        - Maintain the EXACT same artistic style, form, and structure as the original
        - Only change colors, color combinations, or minor pattern variations
        - Use the exact same traditional techniques and materials
        - Be achievable by artisans with their existing skills and tools
        - Preserve the cultural authenticity and visual identity of the original craft
        """
        
        traditional_model = GenerativeModel("gemini-2.0-flash-001")
        traditional_response = traditional_model.generate_content(traditional_ideas_prompt)
        traditional_ideas = traditional_response.text
        
        # Step 4: Generate 2 modern implementation ideas
        modern_ideas_prompt = f"""
        As a creative director, suggest 2 modern implementations of this traditional craft, keep some part of design same just applications different.
        CRITICAL CONSTRAINTS:
        1. These MUST be achievable by traditional artisans using their existing techniques and materials
        2. Blend traditional techniques with contemporary applications while preserving the craft's essence
        3. Focus on modern contexts where artisans can apply their traditional skills
        4. Ensure each idea is within the practical capabilities of traditional artisans
        
        Image Analysis: {image_analysis}
        Technique and Material Research: {technique_material_research}
        Traditional Ideas: {traditional_ideas}
        
        Generate 2 distinct modern implementation concepts that artisans can actually create:
        1. Modern Implementation 1: [description of modern application using traditional artisan techniques/materials]
        2. Modern Implementation 2: [description of modern application using traditional artisan techniques/materials]
        
        Each concept should:
        - Show how traditional craft techniques can be applied in modern contexts
        - Be achievable by artisans using their traditional skills and materials
        - Maintain the cultural essence while appealing to contemporary markets
        - Require no additional training or tools beyond what artisans already possess
        """
        
        modern_model = GenerativeModel("gemini-2.0-flash-001")
        modern_response = modern_model.generate_content(modern_ideas_prompt)
        modern_ideas = modern_response.text
        
        # Step 5: Generate image prompts for all 4 concepts
        prompts_prompt = f"""
        Create 4 detailed prompts for image generation based on these concepts:
        
        Image Analysis: {image_analysis}
        Technique and Material Research: {technique_material_research}
        Traditional Ideas: {traditional_ideas}
        Modern Ideas: {modern_ideas}
        
        Generate 4 prompts in this exact format:
        TRADITIONAL_1: [detailed prompt for traditional variation 1 - SAME STYLE as original, different colors only]
        TRADITIONAL_2: [detailed prompt for traditional variation 2 - SAME STYLE as original, different colors only]
        MODERN_1: [detailed prompt for modern implementation 1]
        MODERN_2: [detailed prompt for modern implementation 2]
        
        For TRADITIONAL prompts, emphasize:
        - IDENTICAL STYLE: Same artistic style, form, structure, and composition as the original
        - ONLY COLOR VARIATIONS: Different color palette, color scheme, or color combinations
        - Same traditional techniques and materials
        - Same cultural context and design elements
        
        For MODERN prompts, emphasize:
        - Preservation of traditional techniques and materials
        - Focus on making canvas changes for example: if materials are fabrics then you can change the craft applications preserving the design to pillow covers, fashion design, cloth bags, etc.
        if materials are brass or other metals, use them in other house decors preserving the design of craft, just changing the applications.
        if paintings are thehandicrafts, suggest a mix of traditional and contemporary design for craft.
        - High quality: "photorealistic", "4k", "detailed", "professional photography"
        - PRACTICAL FEASIBILITY: Show items that artisans can realistically create with their skills
        """
        
        prompts_model = GenerativeModel("gemini-2.0-flash-001")
        prompts_response = prompts_model.generate_content(prompts_prompt)
        all_prompts = prompts_response.text
        
        # Parse prompts
        prompt_lines = all_prompts.split('\n')
        prompts_dict = {}
        current_key = None
        current_prompt = []
        
        for line in prompt_lines:
            if line.startswith('TRADITIONAL_') or line.startswith('MODERN_'):
                if current_key:
                    prompts_dict[current_key] = ' '.join(current_prompt)
                current_key = line.split(':')[0].strip()
                current_prompt = [line.split(':', 1)[1].strip()] if ':' in line else []
            elif current_key and line.strip():
                current_prompt.append(line.strip())
        
        if current_key:
            prompts_dict[current_key] = ' '.join(current_prompt)
        
        # Setup cloud storage
        storage_client = storage.Client()
        bucket_name = "kalpana-ai-craft-images"
        bucket = storage_client.bucket(bucket_name)
        
        # Create unique session ID for this generation
        session_id = f"craft_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{str(uuid.uuid4())[:8]}"
        
        # Function to generate image with fallback
        def generate_image_with_fallback(prompt, key, max_retries=2):
            models_to_try = [
                ("imagen-4.0-generate-001", 0),
                ("imagen-3.0-generate-002", 1)
            ]
            
            for model_name, retry_count in models_to_try:
                try:
                    print(f"Attempting to generate {key} with {model_name}")
                    imagen_model = ImageGenerationModel.from_pretrained(model_name)
                    imagen_response = imagen_model.generate_images(
                        prompt=prompt,
                        number_of_images=1,
                    )
                    
                    # Get the image as bytes
                    image_bytes = imagen_response.images[0]._image_bytes
                    
                    # Save to Google Cloud Storage
                    blob_name = f"{session_id}/{key.lower()}.png"
                    blob = bucket.blob(blob_name)
                    
                    # Upload directly from bytes
                    blob.upload_from_string(image_bytes, content_type='image/png')
                    
                    # Make blob publicly accessible
                    blob.make_public()
                    
                    # Return public URL
                    output_path = f"https://storage.googleapis.com/{bucket_name}/{blob_name}"
                    
                    print(f"Successfully generated {key} with {model_name}")
                    return output_path
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"Error generating {key} with {model_name}: {error_msg}")
                    
                    # Check if it's a rate limit error
                    if "quota" in error_msg.lower() or "limit" in error_msg.lower() or "rate" in error_msg.lower():
                        print(f"Rate limit detected with {model_name}, trying next model...")
                        continue
                    
                    # For other errors, wait and retry with the same model
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # Exponential backoff
                        print(f"Waiting {wait_time} seconds before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        print(f"All retries exhausted for {model_name}")
                        continue
            
            # If all models fail
            print(f"All image generation attempts failed for {key}")
            return None
        
        # Generate images with fallback mechanism
        generated_images = {}
        for key, prompt in prompts_dict.items():
            try:
                output_path = generate_image_with_fallback(prompt, key)
                generated_images[key] = output_path
            except Exception as e:
                print(f"Unexpected error generating image for {key}: {str(e)}")
                generated_images[key] = None
        
        return {
            "status": "success",
            "storage_mode": "cloud",
            "image_analysis": image_analysis,
            "technique_material_research": technique_material_research,
            "traditional_ideas": traditional_ideas,
            "modern_ideas": modern_ideas,
            "generated_images": generated_images,
            "traditional_images": [generated_images.get("TRADITIONAL_1"), generated_images.get("TRADITIONAL_2")],
            "modern_images": [generated_images.get("MODERN_1"), generated_images.get("MODERN_2")]
        }
        
    except Exception as e:
        return {"status": "error", "error_message": f"Process failed: {str(e)}"}