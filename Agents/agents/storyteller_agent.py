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
            self.model = GenerativeModel("gemini-2.5-flash")
            logger.info("✅ Gemini 2.5 Flash (auto-updated alias) loaded successfully")
        except Exception as e:
            logger.error(f"❌ Vertex AI initialization failed: {str(e)}")
            # Fallback to specific version
            try:
                self.model = GenerativeModel("gemini-2.5-flash")
                logger.info("✅ Gemini 2.5 Flash (specific version) loaded successfully")
            except Exception as e2:
                logger.error(f"❌ Fallback model initialization failed: {str(e2)}")
                raise
    
    def _retrieve_context(self, description: str) -> str:
        """
        Retrieve relevant cultural context from Firestore using RAG
        Dynamically searches the cultural_knowledge_base for matching art forms
        """
        description_lower = description.lower()
        logger.info(f"🔍 Searching cultural knowledge base for: {description}")
        
        # Fetch ALL documents from cultural_knowledge_base
        all_docs = self.db.collection(self.collection).stream()
        
        matched_contexts = []
        all_keywords_from_db = []
        
        # Process each document and check for keyword matches
        for doc in all_docs:
            data = doc.to_dict()
            
            # Extract keywords from the document
            doc_keywords = data.get('keywords', [])
            all_keywords_from_db.extend(doc_keywords)
            
            # Check if any keyword from the document appears in the description
            keyword_matches = [kw for kw in doc_keywords if kw.lower() in description_lower]
            
            if keyword_matches:
                # Calculate match score (how many keywords matched)
                match_score = len(keyword_matches)
                
                # Build rich context from matched document
                context_parts = []
                
                # Art form name
                if data.get('art_form'):
                    context_parts.append(f"Art Form: {data['art_form']}")
                elif data.get('artifact_type'):
                    context_parts.append(f"Artifact Type: {data['artifact_type']}")
                
                # Region
                if data.get('region'):
                    context_parts.append(f"Region: {data['region']}")
                
                # Cultural significance
                if data.get('cultural_significance'):
                    context_parts.append(f"Cultural Significance: {data['cultural_significance']}")
                
                # Historical context
                if data.get('historical_context'):
                    context_parts.append(f"Historical Context: {data['historical_context']}")
                
                # Techniques
                if data.get('technique'):
                    context_parts.append(f"Technique: {data['technique']}")
                elif data.get('techniques'):
                    techniques = ', '.join(data['techniques']) if isinstance(data['techniques'], list) else data['techniques']
                    context_parts.append(f"Techniques: {techniques}")
                
                # Traditional motifs
                if data.get('traditional_motifs'):
                    motifs = ', '.join(data['traditional_motifs']) if isinstance(data['traditional_motifs'], list) else data['traditional_motifs']
                    context_parts.append(f"Traditional Motifs: {motifs}")
                
                # Materials
                if data.get('materials'):
                    materials = ', '.join(data['materials']) if isinstance(data['materials'], list) else data['materials']
                    context_parts.append(f"Materials: {materials}")
                
                # Colors/Palette
                if data.get('colors'):
                    colors = ', '.join(data['colors']) if isinstance(data['colors'], list) else data['colors']
                    context_parts.append(f"Color Palette: {colors}")
                
                # Visual characteristics
                if data.get('visual_characteristics'):
                    context_parts.append(f"Visual Characteristics: {data['visual_characteristics']}")
                
                # Famous artisans/centers
                if data.get('famous_artisans'):
                    context_parts.append(f"Famous Artisans: {data['famous_artisans']}")
                if data.get('famous_centers'):
                    centers = ', '.join(data['famous_centers']) if isinstance(data['famous_centers'], list) else data['famous_centers']
                    context_parts.append(f"Famous Centers: {centers}")
                
                # Story elements
                if data.get('story_elements'):
                    story = ', '.join(data['story_elements']) if isinstance(data['story_elements'], list) else data['story_elements']
                    context_parts.append(f"Story Elements: {story}")
                
                # Common uses
                if data.get('common_uses'):
                    uses = ', '.join(data['common_uses']) if isinstance(data['common_uses'], list) else data['common_uses']
                    context_parts.append(f"Common Uses: {uses}")
                
                # Philosophy
                if data.get('philosophy'):
                    context_parts.append(f"Philosophy: {data['philosophy']}")
                
                # Example descriptions for image generation
                if data.get('example_description'):
                    context_parts.append(f"Visual Example: {data['example_description']}")
                
                matched_context = {
                    'score': match_score,
                    'matched_keywords': keyword_matches,
                    'context': '\n'.join(context_parts)
                }
                
                matched_contexts.append(matched_context)
                logger.info(f"✅ Matched document with keywords: {keyword_matches} (score: {match_score})")
        
        # Sort by match score (highest first) and take top 3
        matched_contexts.sort(key=lambda x: x['score'], reverse=True)
        top_matches = matched_contexts[:3]
        
        if top_matches:
            # Combine top matches into a single context string
            context_string = "\n\n---\n\n".join([
                f"Matched Keywords: {', '.join(match['matched_keywords'])}\n{match['context']}"
                for match in top_matches
            ])
            
            logger.info(f"📚 Retrieved {len(top_matches)} relevant context(s) from knowledge base")
            return context_string
        else:
            # No keyword matches found - provide fallback guidance
            logger.warning(f"⚠️ No direct matches found in knowledge base for description: {description[:100]}")
            logger.info(f"💡 Available keywords in database: {', '.join(set(all_keywords_from_db[:50]))}")
            
            # Return a generic Indian craft context
            return f"""
No specific art form matched in the cultural knowledge base.

Description provided: {description}

Please create authentic Indian artisan storytelling based on the general description.
Focus on:
- Traditional Indian craftsmanship values
- Heritage and cultural preservation
- Artisan journey and emotional connection
- Authentic regional characteristics if any are mentioned

Available art forms in database: {', '.join(set(all_keywords_from_db[:20]))}
"""
    
    def _extract_json(self, response_text: str) -> dict:
        """
        Robust JSON extraction from LLM responses
        Handles common formatting issues:
        - Markdown code blocks (```json ...)
        - Double quotes inside strings
        - Trailing commas
        - Multi-line strings
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
        cleaned = cleaned.strip()
        
        # Fix trailing commas before } and ]
        cleaned = re.sub(r',\s*}', '}', cleaned)
        cleaned = re.sub(r',\s*]', ']', cleaned)
        
        # Try parsing the cleaned version
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass
        
        # More aggressive cleaning: fix common issues with newlines in strings
        # Replace literal newlines within JSON strings with \n
        try:
            # Find the JSON object boundaries
            json_match = re.search(r'(\{[\s\S]*\})', cleaned)
            if json_match:
                json_str = json_match.group(1)
                
                # Use a more lenient parser by replacing problematic newlines
                # This regex finds string values and escapes newlines within them
                def fix_string_newlines(match):
                    content = match.group(1)
                    # Replace actual newlines with escaped newlines
                    fixed = content.replace('\n', '\\n').replace('\r', '\\r')
                    # Also escape any unescaped quotes
                    fixed = fixed.replace('\\"', '"').replace('"', '\\"')
                    return f'"{fixed}"'
                
                # This pattern matches string values in JSON (very simplified)
                # We'll try a different approach: parse line by line
                lines = json_str.split('\n')
                fixed_lines = []
                in_string = False
                current_key = None
                
                for line in lines:
                    stripped = line.strip()
                    
                    # Detect if we're starting a string value
                    if ':' in stripped and '"' in stripped:
                        # Check if this line has a complete string value
                        parts = stripped.split(':', 1)
                        if len(parts) == 2:
                            key_part = parts[0].strip()
                            value_part = parts[1].strip()
                            
                            # Count quotes in value part
                            quote_count = value_part.count('"')
                            
                            # If odd number of quotes, we have an unterminated string
                            if quote_count % 2 == 1:
                                in_string = True
                                current_key = key_part
                                fixed_lines.append(line.rstrip())
                                continue
                    
                    # If we're in a multi-line string, continue building it
                    if in_string:
                        # Check if this line closes the string
                        if '"' in stripped and stripped.endswith('"') or stripped.endswith('",'):
                            in_string = False
                            fixed_lines.append(line.rstrip())
                        else:
                            # Continue the string on this line (escape the content)
                            fixed_lines.append(line.rstrip())
                        continue
                    
                    fixed_lines.append(line)
                
                fixed_json = '\n'.join(fixed_lines)
                
                try:
                    return json.loads(fixed_json)
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            logger.warning(f"Advanced JSON cleaning failed: {str(e)}")
        
        # Last resort: try to extract fields manually with regex
        try:
            logger.info("🔧 Attempting manual field extraction from AI response...")
            
            # Extract individual fields with more lenient patterns
            title_match = re.search(r'"story_title"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
            theme_match = re.search(r'"emotional_theme"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
            
            # Extract story_text (may span multiple lines)
            story_match = re.search(r'"story_text"\s*:\s*"((?:[^"\\]|\\.)*)"', response_text, re.DOTALL | re.IGNORECASE)
            if not story_match:
                # Try alternative pattern for multi-line text
                story_match = re.search(r'"story_text"\s*:\s*"([^"]*(?:"[^"]*)*)"', response_text, re.IGNORECASE)
            
            # Extract image_prompts array
            prompts_match = re.search(r'"image_prompts"\s*:\s*\[(.*?)\]', response_text, re.DOTALL | re.IGNORECASE)
            prompts = []
            if prompts_match:
                prompts_str = prompts_match.group(1)
                # Extract individual prompts
                individual_prompts = re.findall(r'"((?:[^"\\]|\\.)*)"', prompts_str)
                prompts = individual_prompts[:3]  # Take first 3
            
            # Extract cultural_elements array
            cultural_match = re.search(r'"cultural_elements"\s*:\s*\[(.*?)\]', response_text, re.DOTALL | re.IGNORECASE)
            cultural = []
            if cultural_match:
                cultural_str = cultural_match.group(1)
                cultural = re.findall(r'"((?:[^"\\]|\\.)*)"', cultural_str)
            
            # Extract hashtags array  
            hashtags_match = re.search(r'"recommended_hashtags"\s*:\s*\[(.*?)\]', response_text, re.DOTALL | re.IGNORECASE)
            hashtags = []
            if hashtags_match:
                hashtags_str = hashtags_match.group(1)
                hashtags = re.findall(r'"((?:[^"\\]|\\.)*)"', hashtags_str)
            
            if title_match and theme_match:
                logger.info("✅ Successfully extracted fields manually")
                return {
                    "story_title": title_match.group(1),
                    "emotional_theme": theme_match.group(1),
                    "story_text": story_match.group(1) if story_match else "Story text could not be extracted.",
                    "image_prompts": prompts if prompts else [
                        "A traditional Indian artisan working with traditional materials, warm lighting, cultural authenticity",
                        "Hands crafting artwork with traditional tools, soft focus, heritage preservation", 
                        "Finished artwork with cultural motifs, golden hour lighting, artistic composition"
                    ],
                    "cultural_elements": cultural if cultural else ["traditional techniques", "cultural heritage", "artisan craftsmanship"],
                    "recommended_hashtags": hashtags if hashtags else ["#IndianCraft", "#CulturalHeritage", "#TraditionalArt"]
                }
        except Exception as fallback_error:
            logger.error(f"Manual field extraction failed: {str(fallback_error)}")
        
        # Ultimate fallback
        logger.error(f"All JSON parsing attempts failed")
        raise ValueError(f"Could not extract valid JSON from AI response. Response preview: {response_text[:200]}")
    
    def generate_image_prompts(self, artisan_description: str) -> dict:
        """
        Generate complete storytelling package including narrative text and visual prompts
        Creates both story text for sharing and prompts for image generation
        """
        logger.info(f"🎨 Generating image prompts for: {artisan_description}")
        
        context = self._retrieve_context(artisan_description)
        logger.info(f"📚 Retrieved context:\n{context}")
        
        prompt = f"""
        You are a cultural storyteller for Indian artisans. Create storytelling content with image prompts.
        
        Use this cultural context:
        {context}
        
        Create:
        1. Story Title (5-10 words)
        2. Story Text (150-200 words) - ONE continuous line, no line breaks
        3. Emotional Theme (one word: heritage/pride/tradition/craftsmanship/legacy)
        4. Three Image Prompts (80-100 words each) - ONE line each, describe specific visual scenes
        5. Three Cultural Elements (key cultural aspects)
        6. Three Hashtags (relevant social media tags)
        
        Return ONLY this JSON format:
        {{
          "story_title": "Title here",
          "story_text": "Complete story in one line",
          "emotional_theme": "Theme",
          "image_prompts": [
            "First visual scene with lighting and composition details",
            "Second visual scene with mood and cultural elements",
            "Third visual scene with artisan focus and authenticity"
          ],
          "cultural_elements": ["element1", "element2", "element3"],
          "recommended_hashtags": ["hashtag1", "hashtag2", "hashtag3"]
        }}
        
        RULES: No line breaks in strings. Write everything in single lines. Valid JSON only.
        """
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4,
                    "max_output_tokens": 4096,  # Increased from 2048 to allow longer responses
                    "top_p": 0.85,
                    "top_k": 40
                }
            )
            
            # Check if response was completed or hit token limit
            if hasattr(response, 'candidates') and response.candidates:
                candidate = response.candidates[0]
                if hasattr(candidate, 'finish_reason'):
                    if candidate.finish_reason == 3:  # MAX_TOKENS
                        logger.warning("⚠️ Response hit max token limit, retrying with shorter prompt...")
                        # Retry with shorter, more focused prompt
                        short_prompt = f"""
                        Create a storytelling package for this Indian craft:
                        
                        Cultural Context:
                        {context[:500]}...
                        
                        Return ONLY this JSON (keep story_text under 200 words, each image prompt under 100 words):
                        {{
                          "story_title": "Short title",
                          "story_text": "Brief story in ONE line",
                          "emotional_theme": "Theme",
                          "image_prompts": ["Prompt 1", "Prompt 2", "Prompt 3"],
                          "cultural_elements": ["element1", "element2", "element3"],
                          "recommended_hashtags": ["tag1", "tag2", "tag3"]
                        }}
                        """
                        
                        response = self.model.generate_content(
                            short_prompt,
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