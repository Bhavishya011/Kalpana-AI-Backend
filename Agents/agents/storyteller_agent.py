# agents/storyteller_agent.py
"""
📖 The Storyteller Agent (Complete Storytelling Package)
- Generates narrative story text for social media sharing
- Creates visual prompts specifically for image generation
- Robust JSON parsing handles all LLM response formats
- Creates complete storytelling package based on artisan description
"""

import re
import json
import logging
from google.cloud import firestore
from vertexai.preview.generative_models import GenerativeModel


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorytellerAgent:
    """
    The Storyteller Agent (Complete Storytelling Package)
    Goal: Generate both narrative story text and visual prompts for a complete storytelling experience.
    
    Creates:
    - Engaging story text for social media sharing
    - Cultural scenes and artisan journey narratives
    - Heritage moments and emotional storytelling
    - Visual prompts for Imagen image generation
    """
    
    def __init__(self):
        try:
            # Initialize Firestore
            self.db = firestore.Client()
            self.collection = "cultural_knowledge_base"
            logger.info("✅ Firestore client initialized successfully")
        except Exception as e:
            logger.error(f"❌ Firestore initialization failed: {str(e)}")
            raise
        
        try:
            # Initialize Vertex AI with CORRECT model name (per knowledge base)
            # Using auto-updated alias as recommended
            self.model = GenerativeModel("gemini-2.0-flash")
            logger.info("✅ Gemini 2.0 Flash (auto-updated alias) loaded successfully")
        except Exception as e:
            logger.error(f"❌ Vertex AI initialization failed: {str(e)}")
            # Fallback to specific version
            try:
                self.model = GenerativeModel("gemini-2.5-flash")
                logger.info("✅ Gemini 2.5 Flash (specific version) loaded successfully")
            except Exception as e2:
                logger.error(f"❌ Fallback model initialization failed: {str(e2)}")
                raise
    
    def _extract_keywords(self, description: str) -> list:
        """Extract potential Indian pottery keywords from description"""
        description = description.lower()
        keywords = []
        
        # Indian-specific keyword extraction
        if "blue" in description or "neela" in description or "nila" in description:
            keywords.append("blue pottery")
        if "jaipur" in description or "rajasthan" in description or "rajasthani" in description:
            keywords.append("Jaipur")
        if "kutch" in description or "gujarat" in description or "gajarati" in description:
            keywords.append("Kutch")
        if "pot" in description or "ghada" in description or "kumbh" in description:
            keywords.append("pottery")
        if "flower" in description or "phool" in description or "pushp" in description:
            keywords.append("flowers")
        if "peacock" in description or "mayur" in description:
            keywords.append("peacocks")
        if "lotus" in description or "kamal" in description:
            keywords.append("lotus")
        
        # Default keywords if none found
        return keywords if keywords else ["pottery", "handmade", "Indian"]
    
    def _retrieve_context(self, description: str) -> str:
        """Retrieve relevant Indian cultural context from Firestore"""
        keywords = self._extract_keywords(description)
        logger.info(f"🔍 Extracted keywords: {keywords}")
        
        context = []
        
        # 1. First try specific region matches
        region_docs = []
        if "Jaipur" in keywords:
            region_docs = self.db.collection(self.collection)\
                .where("region", "==", "Jaipur, Rajasthan")\
                .limit(1)\
                .stream()
        
        elif "Kutch" in keywords:
            region_docs = self.db.collection(self.collection)\
                .where("region", "==", "Kutch, Gujarat")\
                .limit(1)\
                .stream()
        
        # Add region-specific context
        for doc in region_docs:
            data = doc.to_dict()
            context.append(
                f"Region: {data.get('region', 'N/A')}\n"
                f"Technique: {data.get('technique', 'N/A')}\n"
                f"Significance: {data.get('cultural_significance', 'N/A')}\n"
                f"Historical Context: {data.get('historical_context', 'N/A')}\n"
                f"Traditional Motifs: {', '.join(data.get('traditional_motifs', []))}"
            )
        
        # 2. Then add general Indian pottery context
        general_docs = self.db.collection(self.collection)\
            .where("artifact_type", "==", "general")\
            .limit(1)\
            .stream()
        
        for doc in general_docs:
            data = doc.to_dict()
            context.append(
                f"Indian Pottery Philosophy: {data.get('philosophy', 'N/A')}\n"
                f"Technique: {data.get('technique', 'N/A')}"
            )
        
        # 3. If no specific matches, use general blue pottery context
        if not context:
            logger.warning("⚠️ No specific matches found, using general blue pottery context")
            pottery_docs = self.db.collection(self.collection)\
                .where("artifact_type", "==", "blue_pottery")\
                .limit(1)\
                .stream()
            
            for doc in pottery_docs:
                data = doc.to_dict()
                context.append(
                    f"Region: {data.get('region', 'N/A')}\n"
                    f"Technique: {data.get('technique', 'N/A')}\n"
                    f"Significance: {data.get('cultural_significance', 'N/A')}"
                )
        
        return "\n\n".join(context) if context else "No specific Indian pottery context found."
    
    def _extract_json(self, response_text: str) -> dict:
        """
        Robust JSON extraction from LLM responses
        Handles common formatting issues:
        - Markdown code blocks (```json ...)
        - Double quotes inside strings
        - Trailing commas
        - Single quotes
        - Incomplete JSON
        """
        logger.debug(f"Raw AI response: {response_text[:500]}...")
        
        # Try direct JSON parsing first
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Remove markdown code block indicators
        cleaned = re.sub(r'```json\s*', '', response_text)
        cleaned = re.sub(r'\s*```', '', cleaned)
        
        # FIXED: Remove the problematic regex pattern that was causing the error
        # Instead, use a simpler approach to clean up common JSON issues
        
        # Fix trailing commas before } and ]
        cleaned = re.sub(r',\s*}', '}', cleaned)
        cleaned = re.sub(r',\s*]', ']', cleaned)
        
        # Fix unescaped quotes in string values (simplified approach)
        # This handles the most common case without complex lookbehind
        lines = cleaned.split('\n')
        fixed_lines = []
        
        for line in lines:
            # If line contains a JSON string value with unescaped quotes
            if ':' in line and '"' in line:
                # Split by colon to separate key from value
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key_part = parts[0]
                    value_part = parts[1]
                    
                    # If value part has quotes that aren't at the very beginning/end
                    value_stripped = value_part.strip()
                    if value_stripped.startswith('"') and value_stripped.endswith('"'):
                        # Extract the content between the outer quotes
                        inner_content = value_stripped[1:-1]
                        # Replace any remaining quotes with single quotes
                        fixed_inner = inner_content.replace('"', "'")
                        # Reconstruct the line
                        line = key_part + ': "' + fixed_inner + '"'
            
            fixed_lines.append(line)
        
        cleaned = '\n'.join(fixed_lines)
        
        # Try to find JSON object in the text
        json_match = re.search(r'(\{[\s\S]*\})', cleaned)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError as e:
                logger.warning(f"JSON parsing failed on extracted object: {str(e)}")
        
        # Final attempt with the cleaned text
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing failed after all attempts: {str(e)}")
            logger.error(f"Cleaned response: {cleaned[:500]}...")
            
            # As a last resort, try to create a basic structure from the response
            try:
                # Extract basic information if JSON parsing completely fails
                title_match = re.search(r'"story_title":\s*"([^"]*)"', response_text, re.IGNORECASE)
                theme_match = re.search(r'"emotional_theme":\s*"([^"]*)"', response_text, re.IGNORECASE)
                
                if title_match and theme_match:
                    logger.info("🔧 Creating fallback JSON structure from extracted fields")
                    return {
                        "story_title": title_match.group(1),
                        "emotional_theme": theme_match.group(1),
                        "image_prompts": [
                            "A traditional Indian artisan working with clay, warm lighting, cultural authenticity",
                            "Hands shaping pottery with traditional tools, soft focus, heritage preservation",
                            "Finished pottery with cultural motifs, golden hour lighting, artistic composition"
                        ],
                        "cultural_elements": ["traditional techniques", "cultural heritage", "artisan craftsmanship"],
                        "recommended_hashtags": ["#IndianPottery", "#CulturalHeritage", "#TraditionalArt"]
                    }
            except Exception as fallback_error:
                logger.error(f"Fallback JSON creation failed: {str(fallback_error)}")
            
            raise ValueError(f"Could not extract valid JSON from response: {str(e)}")
    
    def generate_image_prompts(self, artisan_description: str) -> dict:
        """
        Generate complete storytelling package including narrative text and visual prompts
        Creates both story text for sharing and prompts for image generation
        """
        logger.info(f"🎨 Generating image prompts for: {artisan_description}")
        
        context = self._retrieve_context(artisan_description)
        logger.info(f"📚 Retrieved context:\n{context}")
        
        prompt = f"""
        You are a cultural storyteller for Indian artisans. Create a complete storytelling package 
        that includes both a narrative story and 3 visual storytelling prompts for image generation.
        
        The storytelling package should:
        - Tell a compelling story about the artisan's journey and heritage
        - Include 3 detailed visual prompts for image generation with Imagen
        - Capture meaningful moments and cultural traditions
        - Evoke emotional responses and cultural pride
        - Focus on authentic Indian craftsmanship and heritage
        
        Use this verified Indian cultural context:
        {context}
        
        Guidelines:
        1. STORY TEXT: Write a 200-300 word narrative story that:
           - Tells the artisan's journey or heritage
           - Includes cultural context and traditions
           - Has emotional depth and connection
           - Celebrates the craft and craftsmanship
           - Is engaging and shareable for social media
        
        2. IMAGE PROMPTS: Create 3 detailed prompts for image generation (100-150 words each):
           - Each prompt should describe a specific scene with visual details
           - Include composition elements (lighting, angle, mood)
           - Incorporate cultural symbolism from the context
           - Write in English (for Imagen compatibility)
        
        Example story text:
        "In the heart of Jaipur, where the desert winds carry whispers of ancient traditions, 
        Maya's hands move with the rhythm of generations. Each morning, she awakens to the 
        familiar scent of clay and the promise of creation. Her blue pottery isn't just art—
        it's a living testament to her grandmother's teachings, each brushstroke a prayer, 
        each design a story passed down through time..."
        
        Return ONLY valid JSON with these fields:
        {{
          "story_title": "The title of the story",
          "story_text": "The complete narrative story (200-300 words)",
          "emotional_theme": "The core emotion being conveyed",
          "image_prompts": [
            "Prompt 1",
            "Prompt 2", 
            "Prompt 3"
          ],
          "cultural_elements": ["element1", "element2", "element3"],
          "recommended_hashtags": ["hashtag1", "hashtag2", "hashtag3"]
        }}
        
        IMPORTANT: Use only simple quotation marks in JSON strings. Avoid complex punctuation.
        Do NOT add any other text outside the JSON.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4,
                    "max_output_tokens": 2048,
                    "top_p": 0.85,
                    "top_k": 40
                }
            )
            
            response_text = response.text
            logger.info(f"🤖 AI response received: {response_text[:100]}...")
            
            # Use robust JSON extraction
            return self._extract_json(response_text)
                
        except Exception as e:
            logger.error(f"❌ Error generating image prompts: {str(e)}")
            raise
    
    def validate_prompts(self, image_prompts_dict, artisan_description: str) -> dict:
        """Validate image prompts for cultural accuracy and generation quality"""
        logger.info("🛡️ Validating image prompts for cultural accuracy...")
        
        # Ensure required fields exist
        required_fields = ["story_title", "story_text", "emotional_theme", "image_prompts", "cultural_elements", "recommended_hashtags"]
        for field in required_fields:
            if field not in image_prompts_dict:
                logger.error(f"❌ Missing required field: {field}")
                raise ValueError(f"Missing required field: {field}")
        
        # Check prompt quality for image generation
        for i, prompt in enumerate(image_prompts_dict["image_prompts"]):
            # Check for visual details
            visual_elements = ["lighting", "composition", "angle", "mood", "texture", "color"]
            if not any(element in prompt.lower() for element in visual_elements):
                logger.warning(f"⚠️ Prompt {i+1} lacks visual detail elements for good image generation")
            
            # Check for cultural accuracy
            indian_elements = ["india", "indian", "jaipur", "kutch", "rajasthan", "gujarat", 
                              "shilp", "kala", "karuna", "quartz", "cobalt", "handmade"]
            if not any(element in prompt.lower() for element in indian_elements):
                logger.warning(f"⚠️ Prompt {i+1} may lack Indian cultural references")
        
        # Validate story text quality
        story_text = image_prompts_dict.get("story_text", "")
        if len(story_text) < 100:
            logger.warning("⚠️ Story text appears to be too short for engaging content")
        elif len(story_text) > 500:
            logger.warning("⚠️ Story text might be too long for social media sharing")
        
        # Check if story text contains cultural elements
        if not any(element in story_text.lower() for element in ["india", "indian", "heritage", "tradition", "artisan", "craft"]):
            logger.warning("⚠️ Story text may lack cultural context")
        
        # Add metadata
        image_prompts_dict["artisan_input"] = artisan_description
        image_prompts_dict["prompt_count"] = len(image_prompts_dict["image_prompts"])
        image_prompts_dict["story_word_count"] = len(story_text.split())
        
        logger.info("✅ Image prompts and story text validated successfully!")
        return image_prompts_dict