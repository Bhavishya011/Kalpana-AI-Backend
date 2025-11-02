"""Core tutor implementation."""
from vertexai.generative_models import GenerativeModel, Part
from google.cloud import storage, firestore
from google.cloud import texttospeech, speech
from google.cloud import translate_v2 as translate
from google.cloud import vision
import vertexai
import os
import json
import uuid
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

# Initialize Google Cloud services
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "nodal-fountain-470717-j1")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
BUCKET_NAME = os.getenv("CLOUD_STORAGE_BUCKET", "kalpana-artisan-tutor")

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Cloud service clients
storage_client = storage.Client()
firestore_client = firestore.Client()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()
stt_client = speech.SpeechClient()
vision_client = vision.ImageAnnotatorClient()

class SkillLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate" 
    ADVANCED = "advanced"
    EXPERT = "expert"

class LearningStyle(Enum):
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READ_WRITE = "read_write"

# Load curriculum from external file to keep this module clean
import pkgutil
curriculum_json = pkgutil.get_data(__package__, "data/curriculum.json")
PROGRESSIVE_CURRICULUM = json.loads(curriculum_json) if curriculum_json else {}


class HybridArtisanTutor:
    """Comprehensive AI tutor for artisan business education"""
    
    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'hi': 'Hindi', 
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'gu': 'Gujarati'
        }
    
    def analyze_craft_comprehensive(self, image_input: str) -> Dict[str, Any]:
        """Comprehensive craft analysis using Gemini Vision"""
        try:
            model = GenerativeModel("gemini-2.0-flash-001")
            
            analysis_prompt = """
            Analyze this craft image comprehensively and return detailed JSON:
            {
                "craft_name": "Specific name and type",
                "materials": ["list", "of", "primary", "materials"],
                "techniques": ["crafting", "techniques", "visible"],
                "style": "Artistic style description",
                "cultural_context": "Cultural/regional significance", 
                "region": "Geographic origin if identifiable",
                "unique_selling_points": ["what", "makes", "it", "special"],
                "target_markets": ["potential", "customer", "segments"],
                "skill_level_required": "Beginner/Intermediate/Expert",
                "time_estimate_hours": "Estimated creation time",
                "material_cost_estimate": "Approximate material cost in INR",
                "complexity_score": 1-10,
                "dominant_colors": ["#hex1", "#hex2", "#hex3"],
                "cultural_significance": "Importance in local culture",
                "modern_adaptation_potential": "How it can be modernized",
                "export_potential": "International appeal assessment"
            }
            Be detailed and practical for business planning.
            """
            
            if image_input.startswith('gs://'):
                image_part = Part.from_uri(image_input, mime_type="image/jpeg")
            else:
                # Handle base64 or direct upload
                image_data = base64.b64decode(image_input.split(',')[1]) if ',' in image_input else image_input
                image_part = Part.from_data(image_data, mime_type="image/jpeg")
            
            response = model.generate_content([analysis_prompt, image_part])
            analysis = self._parse_json_response(response.text)
            
            # Store analysis in Firestore
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            firestore_client.collection("craft_analyses").document(analysis_id).set({
                "analysis": analysis,
                "created_at": datetime.now(),
                "confidence_score": self._calculate_analysis_confidence(analysis)
            })
            
            return {
                "status": "success",
                "analysis_id": analysis_id,
                "analysis": analysis,
                "recommended_learning_path": self._suggest_learning_path(analysis)
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Craft analysis failed: {str(e)}"}
    
    def create_personalized_learning_journey(self, user_profile: Dict) -> Dict:
        """Create completely personalized learning journey"""
        user_id = user_profile.get("user_id", str(uuid.uuid4()))
        
        learning_style = user_profile.get("learning_style", LearningStyle.VISUAL.value)
        language = user_profile.get("language", "en")
        current_skill_level = user_profile.get("current_skill_level", SkillLevel.BEGINNER.value)
        craft_context = user_profile.get("craft_analysis", {})
        
        # Create personalized curriculum
        personalized_curriculum = self._build_personalized_curriculum(
            current_skill_level, learning_style, craft_context, language
        )
        
        # FIX: Get actual starting lesson from curriculum, default to F1.1
        starting_module = personalized_curriculum.get("starting_module", "foundation")
        starting_lesson = personalized_curriculum.get("starting_lesson", "F1.1")
        
        # If starting_lesson is still empty or not valid, use default
        if not starting_lesson:
            # Try to get first lesson from foundation module
            foundation_module = personalized_curriculum.get("curriculum", {}).get("foundation", {})
            lessons = foundation_module.get("lessons", [])
            starting_lesson = lessons[0].get("id", "F1.1") if lessons else "F1.1"
        
        # Initialize user in Firestore
        user_doc_ref = firestore_client.collection("users").document(user_id)
        user_doc_ref.set({
            "profile": user_profile,
            "learning_journey": {
                "current_module": starting_module,
                "current_lesson": starting_lesson,  # Now has actual value, not empty string
                "completed_modules": [],
                "completed_lessons": [],  # ADD: track completed lessons list
                "personalized_curriculum": personalized_curriculum,
                "learning_style": learning_style,
                "language_preference": language,
                "created_at": datetime.now(),
                "last_active": datetime.now()
            },
            "progress_metrics": {
                "total_points": 0,
                "current_streak": 0,
                "completed_lessons": 0,
                "skill_level": current_skill_level
            },
            "achievements": {
                "unlocked": [],
                "in_progress": [],
                "next_milestones": personalized_curriculum.get("milestones", [])[:3] if personalized_curriculum.get("milestones") else []
            }
        }, merge=True)
        
        welcome_message = self._generate_welcome_message(user_profile, personalized_curriculum, language)
        
        return {
            "status": "success",
            "user_id": user_id,
            "welcome_message": welcome_message,
            "personalized_curriculum": personalized_curriculum,
            "starting_point": {
                "module": starting_module,
                "lesson": starting_lesson  # Now returns actual lesson ID like "F1.1"
            }
        }
    
    def get_interactive_lesson(self, user_id: str, lesson_id: str, format: str = "multimodal") -> Dict:
        """Get interactive lesson with multimodal support"""
        try:
            user_doc = firestore_client.collection("users").document(user_id).get()
            if not user_doc.exists:
                return {"status": "error", "message": "User not found"}
            
            user_data = user_doc.to_dict()
            learning_journey = user_data["learning_journey"]
            profile = user_data["profile"]
            language = learning_journey.get("language_preference", "en")
            
            lesson = self._find_lesson_in_curriculum(lesson_id, learning_journey["personalized_curriculum"])
            if not lesson:
                return {"status": "error", "message": "Lesson not found"}
            
            craft_context = profile.get("craft_analysis", {})
            lesson_content = self._generate_lesson_content(lesson, craft_context, language)
            multimodal_content = self._enhance_with_multimodal_elements(
                lesson_content, lesson, format, language, craft_context
            )
            
            self._track_lesson_access(user_id, lesson_id)
            
            return {
                "status": "success",
                "lesson": {
                    **lesson,
                    "multimodal_content": multimodal_content,
                    "estimated_completion_time": f"{lesson.get('difficulty', 1) * 15} minutes"
                },
                "progress": self._get_user_progress(user_id),
                "next_actions": self._suggest_next_actions(lesson_id, learning_journey["personalized_curriculum"])
            }
            
        except Exception as e:
            return {"status": "error", "message": f"Lesson retrieval failed: {str(e)}"}
    
    def submit_lesson_work(self, user_id: str, lesson_id: str, submission: Dict) -> Dict:
        """Submit and validate lesson work with AI-powered feedback"""
        try:
            user_doc = firestore_client.collection("users").document(user_id).get()
            if not user_doc.exists:
                return {"status": "error", "message": "User not found"}
            
            user_data = user_doc.to_dict()
            lesson = self._find_lesson_in_curriculum(
                lesson_id, 
                user_data["learning_journey"]["personalized_curriculum"]
            )
            
            if not lesson:
                return {"status": "error", "message": "Lesson not found"}
            
            validation_result = self._validate_submission_with_ai(lesson, submission, user_data)
            
            if validation_result["passed"]:
                self._update_user_progress(user_id, lesson_id, lesson["points"], validation_result)
                new_achievements = self._check_achievement_unlocks(user_id)
                feedback = self._generate_personalized_feedback(
                    validation_result, 
                    user_data["profile"].get("language", "en")
                )
                next_lesson = self._get_next_lesson_recommendation(user_id, lesson_id)
                
                return {
                    "status": "success",
                    "passed": True,
                    "feedback": feedback,
                    "points_earned": lesson["points"],
                    "new_achievements": new_achievements,
                    "progress_update": self._get_user_progress(user_id),
                    "next_lesson": next_lesson
                }
            else:
                return {
                    "status": "success", 
                    "passed": False,
                    "feedback": validation_result["feedback"],
                    "improvement_suggestions": validation_result["suggestions"],
                    "retry_guidance": self._generate_retry_guidance(
                        lesson, 
                        user_data["profile"].get("language", "en")
                    )
                }
                
        except Exception as e:
            return {"status": "error", "message": f"Submission failed: {str(e)}"}
    
    def get_business_dashboard(self, user_id: str) -> Dict:
        """Comprehensive business and learning dashboard"""
        try:
            user_doc = firestore_client.collection("users").document(user_id).get()
            if not user_doc.exists:
                return {"status": "error", "message": "User not found"}
            
            user_data = user_doc.to_dict()
            
            dashboard = {
                "learning_progress": self._calculate_learning_progress(user_data),
                "business_metrics": self._calculate_business_metrics(user_data),
                "skill_development": self._calculate_skill_matrix(user_data),
                "achievements": user_data.get("achievements", {}),
                "personalized_recommendations": self._generate_recommendations(user_data),
                "growth_opportunities": self._identify_growth_opportunities(user_data)
            }
            
            return {"status": "success", "dashboard": dashboard}
            
        except Exception as e:
            return {"status": "error", "message": f"Dashboard retrieval failed: {str(e)}"}
    
    def text_to_speech_multilingual(self, text: str, language: str = "en") -> str:
        """Convert text to speech in multiple languages"""
        language_codes = {
            'en': 'en-IN', 'hi': 'hi-IN', 'ta': 'ta-IN', 'te': 'te-IN',
            'kn': 'kn-IN', 'ml': 'ml-IN', 'bn': 'bn-IN', 'mr': 'mr-IN', 'gu': 'gu-IN'
        }
        
        lang_code = language_codes.get(language, 'en-IN')
        
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,
            pitch=0.0
        )
        
        response = tts_client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        filename = f"audio/{uuid.uuid4()}.mp3"
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(filename)
        blob.upload_from_string(response.audio_content, content_type="audio/mp3")
        blob.make_public()
        
        return f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
    
    def speech_to_text_multilingual(self, audio_uri: str, language: str = "en") -> str:
        """Convert speech to text in multiple languages"""
        language_codes = {
            'en': 'en-IN', 'hi': 'hi-IN', 'ta': 'ta-IN', 'te': 'te-IN',
            'kn': 'kn-IN', 'ml': 'ml-IN', 'bn': 'bn-IN', 'mr': 'mr-IN', 'gu': 'gu-IN'
        }
        
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code=language_codes.get(language, 'en-IN'),
            enable_automatic_punctuation=True
        )
        
        audio = speech.RecognitionAudio(uri=audio_uri)
        response = stt_client.recognize(config=config, audio=audio)
        
        return " ".join([result.alternatives[0].transcript for result in response.results])
    
    # Helper methods
    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from Gemini response"""
        try:
            # Remove markdown code blocks if present
            text = text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            return json.loads(text.strip())
        except:
            return {}
    
    def _calculate_analysis_confidence(self, analysis: Dict) -> float:
        """Calculate confidence score for analysis"""
        score = 0.0
        if analysis.get("craft_name"): score += 0.2
        if analysis.get("materials"): score += 0.2
        if analysis.get("cultural_context"): score += 0.2
        if analysis.get("target_markets"): score += 0.2
        if analysis.get("region"): score += 0.2
        return score
    
    def _suggest_learning_path(self, analysis: Dict) -> Dict:
        """Suggest learning path based on analysis"""
        skill_level = analysis.get("skill_level_required", "Beginner").lower()
        return {
            "recommended_start": "foundation" if "beginner" in skill_level else "marketplace_ready",
            "focus_areas": ["photography", "storytelling", "pricing"]
        }
    
    def _build_personalized_curriculum(self, skill_level: str, learning_style: str, 
                                     craft_context: Dict, language: str) -> Dict:
        """Build personalized curriculum"""
        starting_module = "foundation"
        first_lesson = None
        
        if PROGRESSIVE_CURRICULUM and starting_module in PROGRESSIVE_CURRICULUM:
            lessons = PROGRESSIVE_CURRICULUM[starting_module].get("lessons", [])
            if lessons:
                first_lesson = lessons[0].get("id")
        
        return {
            "starting_module": starting_module,
            "starting_lesson": first_lesson or "F1.1",
            "curriculum": PROGRESSIVE_CURRICULUM,
            "milestones": [first_lesson or "F1.1"],
            "estimated_timeline": "2-3 weeks"
        }
    
    def _generate_welcome_message(self, user_profile: Dict, curriculum: Dict, language: str) -> str:
        """Generate welcome message"""
        name = user_profile.get("name", "Artisan")
        return f"Welcome {name}! Let's begin your journey to becoming a successful artisan entrepreneur."
    
    def _find_lesson_in_curriculum(self, lesson_id: str, curriculum: Dict) -> Optional[Dict]:
        """Find lesson by ID in curriculum"""
        curr = curriculum.get("curriculum", PROGRESSIVE_CURRICULUM)
        for module_key, module_data in curr.items():
            for lesson in module_data.get("lessons", []):
                if lesson.get("id") == lesson_id:
                    return lesson
        return None
    
    def _generate_lesson_content(self, lesson: Dict, craft_context: Dict, language: str) -> Dict:
        """Generate personalized lesson content using AI"""
        try:
            model = GenerativeModel("gemini-2.0-flash-001")
            
            # Get craft details for personalization
            craft_name = craft_context.get("craft_name", "your craft")
            craft_type = craft_context.get("style", "traditional craft")
            materials = ", ".join(craft_context.get("materials", ["materials"]))
            region = craft_context.get("region", "your region")
            
            # Fill in template variables
            prompt_template = lesson.get("prompt_template", "")
            personalized_prompt = prompt_template.format(
                craft_name=craft_name,
                craft_type=craft_type,
                materials=materials,
                region=region,
                craft_business=f"{craft_name} business",
                craft_product=craft_name,
                unique_features=craft_context.get("unique_selling_points", ["unique features"])[0] if craft_context.get("unique_selling_points") else "unique features",
                dominant_colors=", ".join(craft_context.get("dominant_colors", ["natural colors"])),
                cultural_context=craft_context.get("cultural_context", "traditional heritage"),
                unique_selling_points=", ".join(craft_context.get("unique_selling_points", ["handmade quality"])),
                material_cost_estimate=craft_context.get("material_cost_estimate", "₹500"),
                time_estimate=craft_context.get("time_estimate_hours", "2-3"),
                skill_level=craft_context.get("skill_level_required", "intermediate"),
                target_markets=", ".join(craft_context.get("target_markets", ["local market"]))
            )
            
            # Generate detailed lesson instructions
            content_prompt = f"""
            Create detailed, actionable lesson content for this artisan business lesson:
            
            LESSON: {lesson.get('title')}
            OBJECTIVE: {lesson.get('objective')}
            DIFFICULTY: {lesson.get('difficulty')}/5
            
            CRAFT CONTEXT:
            {personalized_prompt}
            
            Provide:
            1. Clear step-by-step instructions (5-7 steps)
            2. Practical examples specific to {craft_name}
            3. Common mistakes to avoid (3 items)
            4. Success criteria checklist (4 items)
            5. Pro tips from successful artisans (2 items)
            
            Make it culturally relevant, encouraging, and actionable for someone working with {craft_name} from {region}.
            Keep language simple and practical.
            """
            
            response = model.generate_content(content_prompt)
            detailed_instructions = response.text
            
            return {
                "title": lesson.get("title", ""),
                "objective": lesson.get("objective", ""),
                "difficulty": lesson.get("difficulty", 1),
                "points": lesson.get("points", 25),
                "reward": lesson.get("reward", ""),
                "action_type": lesson.get("action_type", ""),
                "instructions": detailed_instructions,
                "personalized_guidance": personalized_prompt,
                "craft_context": craft_context,
                "estimated_time": f"{lesson.get('difficulty', 1) * 15-20} minutes"
            }
            
        except Exception as e:
            # Fallback to basic content
            return {
                "title": lesson.get("title", ""),
                "objective": lesson.get("objective", ""),
                "instructions": lesson.get("prompt_template", ""),
                "craft_context": craft_context
            }
    
    def _enhance_with_multimodal_elements(self, content: Dict, lesson: Dict,
                                        format: str, language: str, craft_context: Dict) -> Dict:
        """Add multimodal elements"""
        content["media"] = {"images": [], "audio": [], "videos": []}
        return content
    
    def _track_lesson_access(self, user_id: str, lesson_id: str):
        """Track lesson access"""
        firestore_client.collection("users").document(user_id).update({
            "learning_journey.last_active": datetime.now()
        })
    
    def _get_user_progress(self, user_id: str) -> Dict:
        """Get user progress"""
        user_doc = firestore_client.collection("users").document(user_id).get()
        if user_doc.exists:
            metrics = user_doc.to_dict().get("progress_metrics", {})
            return metrics
        return {}
    
    def _suggest_next_actions(self, lesson_id: str, curriculum: Dict) -> List[str]:
        """Suggest next actions"""
        return ["Complete the lesson objective", "Submit your work", "Review feedback"]
    
    def _validate_submission_with_ai(self, lesson: Dict, submission: Dict, user_data: Dict) -> Dict:
        """Validate submission using AI"""
        try:
            content = submission.get("content", "")
            
            # Basic validation
            if not content or len(str(content)) < 20:
                return {
                    "passed": False,
                    "feedback": "Please provide more detailed content for your submission.",
                    "suggestions": [
                        "Add more specific details",
                        "Include examples from your craft",
                        "Explain your thought process"
                    ]
                }
            
            # Use Gemini to validate the submission
            model = GenerativeModel("gemini-2.0-flash-001")
            
            validation_prompt = f"""
            You are an expert tutor for artisan business education.
            
            LESSON DETAILS:
            - Title: {lesson.get('title')}
            - Objective: {lesson.get('objective')}
            - Action Type: {lesson.get('action_type')}
            - Validation Criteria: {', '.join(lesson.get('validation_criteria', []))}
            
            STUDENT SUBMISSION:
            {content}
            
            CRAFT CONTEXT:
            {json.dumps(user_data.get('profile', {}).get('craft_analysis', {}), indent=2)}
            
            Evaluate this submission and return JSON:
            {{
                "passed": true/false,
                "score": 0.0-1.0,
                "feedback": "Detailed constructive feedback (2-3 sentences)",
                "strengths": ["strength1", "strength2"],
                "suggestions": ["improvement1", "improvement2"],
                "criteria_scores": {{
                    "criterion1": 0.0-1.0,
                    "criterion2": 0.0-1.0
                }}
            }}
            
            Be encouraging but honest. Focus on practical business impact.
            Pass if score >= 0.7 and meets core objective.
            """
            
            response = model.generate_content(validation_prompt)
            validation_result = self._parse_json_response(response.text)
            
            # Ensure all required fields exist
            if not validation_result:
                validation_result = {
                    "passed": True,
                    "score": 0.75,
                    "feedback": "Good submission! You've demonstrated understanding of the lesson objective.",
                    "suggestions": []
                }
            
            return validation_result
            
        except Exception as e:
            # Fallback validation if AI fails
            return {
                "passed": True,
                "feedback": "Thank you for your submission! Your work has been recorded.",
                "suggestions": ["Continue practicing", "Try to add more details next time"],
                "score": 0.7
            }
    
    def _update_user_progress(self, user_id: str, lesson_id: str, points: int, validation: Dict):
        """Update user progress after successful lesson completion"""
        try:
            user_ref = firestore_client.collection("users").document(user_id)
            user_doc = user_ref.get()
            
            if not user_doc.exists:
                print(f"⚠️ User {user_id} not found for progress update")
                return
            
            user_data = user_doc.to_dict()
            
            # Safe access to progress metrics
            current_metrics = user_data.get("progress_metrics") or {}
            current_journey = user_data.get("learning_journey") or {}
            
            # Calculate new values
            new_total_points = (current_metrics.get("total_points") or 0) + points
            new_completed = (current_metrics.get("completed_lessons") or 0) + 1
            new_streak = (current_metrics.get("current_streak") or 0) + 1
            
            # Get completed lessons list
            completed_lessons_list = current_journey.get("completed_lessons") or []
            if lesson_id not in completed_lessons_list:
                completed_lessons_list.append(lesson_id)
            
            # Update Firestore document with all progress fields
            user_ref.update({
                "progress_metrics.total_points": new_total_points,
                "progress_metrics.completed_lessons": new_completed,
                "progress_metrics.current_streak": new_streak,
                "learning_journey.completed_lessons": completed_lessons_list,
                "learning_journey.last_active": datetime.now(),
                "learning_journey.last_completed_lesson": lesson_id,
                "learning_journey.last_completed_at": datetime.now()
            })
            
            print(f"✅ Progress updated for {user_id}: +{points} points, {new_completed} lessons completed")
            
        except Exception as e:
            print(f"❌ Error updating progress: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def _check_achievement_unlocks(self, user_id: str) -> List[Dict]:
        """Check for new achievements"""
        return []
    
    def _generate_personalized_feedback(self, validation: Dict, language: str) -> str:
        """Generate personalized feedback"""
        return validation.get("feedback", "Good work!")
    
    def _get_next_lesson_recommendation(self, user_id: str, current_lesson_id: str) -> Optional[Dict]:
        """Get next lesson recommendation based on progress"""
        try:
            user_doc = firestore_client.collection("users").document(user_id).get()
            if not user_doc.exists:
                return None
            
            user_data = user_doc.to_dict()
            curriculum = user_data["learning_journey"]["personalized_curriculum"]["curriculum"]
            
            # Find current module and lesson
            current_module = None
            current_lesson_idx = None
            
            for module_key, module_data in curriculum.items():
                lessons = module_data.get("lessons", [])
                for idx, lesson in enumerate(lessons):
                    if lesson.get("id") == current_lesson_id:
                        current_module = module_key
                        current_lesson_idx = idx
                        break
                if current_module:
                    break
            
            if not current_module:
                return None
            
            # Get next lesson in same module
            module_lessons = curriculum[current_module].get("lessons", [])
            if current_lesson_idx < len(module_lessons) - 1:
                next_lesson = module_lessons[current_lesson_idx + 1]
                return {
                    "id": next_lesson.get("id"),
                    "title": next_lesson.get("title"),
                    "module": current_module,
                    "objective": next_lesson.get("objective"),
                    "points": next_lesson.get("points"),
                    "difficulty": next_lesson.get("difficulty"),
                    "message": f"Great! Ready for the next lesson in {curriculum[current_module]['title']}?"
                }
            
            # Module complete - suggest next module
            module_order = ["foundation", "marketplace_ready", "digital_marketing", "global_expansion"]
            try:
                current_module_idx = module_order.index(current_module)
                if current_module_idx < len(module_order) - 1:
                    next_module_key = module_order[current_module_idx + 1]
                    next_module = curriculum.get(next_module_key)
                    if next_module and next_module.get("lessons"):
                        next_lesson = next_module["lessons"][0]
                        return {
                            "id": next_lesson.get("id"),
                            "title": next_lesson.get("title"),
                            "module": next_module_key,
                            "objective": next_lesson.get("objective"),
                            "points": next_lesson.get("points"),
                            "difficulty": next_lesson.get("difficulty"),
                            "message": f"🎉 Module complete! Ready to start {next_module['title']}?"
                        }
            except ValueError:
                pass
            
            # All modules complete!
            return {
                "id": "complete",
                "title": "🎓 Journey Complete!",
                "message": "Congratulations! You've completed all lessons. You're now ready to scale your artisan business globally!",
                "next_steps": [
                    "Review your dashboard for growth opportunities",
                    "Connect with other successful artisans",
                    "Start implementing your global expansion plan"
                ]
            }
            
        except Exception as e:
            return {"id": "F1.2", "title": "Next Lesson"}
    
    def _generate_retry_guidance(self, lesson: Dict, language: str) -> str:
        """Generate retry guidance"""
        return "Please review the lesson objectives and try again with more detail."
    
    def _calculate_learning_progress(self, user_data: Dict) -> Dict:
        """Calculate comprehensive learning progress"""
        # Safe access with default empty dicts - prevents NoneType errors
        metrics = user_data.get("progress_metrics") or {}
        journey = user_data.get("learning_journey") or {}
        
        # Calculate completion percentage with safe access
        curriculum = {}
        if journey:
            personalized = journey.get("personalized_curriculum") or {}
            curriculum = personalized.get("curriculum") or PROGRESSIVE_CURRICULUM
        else:
            curriculum = PROGRESSIVE_CURRICULUM
        
        total_lessons = sum(
            len(module.get("lessons", []))
            for module in curriculum.values()
            if isinstance(module, dict)
        )
        completed = metrics.get("completed_lessons", 0) or 0
        completion_percent = (completed / total_lessons * 100) if total_lessons > 0 else 0
        
        # Determine current level
        current_level = "Beginner"
        if completed >= 15:
            current_level = "Expert"
        elif completed >= 10:
            current_level = "Advanced"
        elif completed >= 5:
            current_level = "Intermediate"
        
        # Safe access for achievements
        achievements = user_data.get("achievements") or {}
        unlocked = achievements.get("unlocked") or []
        completed_modules = journey.get("completed_modules") or []
        
        return {
            "total_points": metrics.get("total_points", 0) or 0,
            "completed_lessons": completed,
            "total_lessons": total_lessons,
            "completion_percentage": round(completion_percent, 1),
            "current_level": current_level,
            "current_streak": metrics.get("current_streak", 0) or 0,
            "modules_completed": len(completed_modules),
            "achievements_unlocked": len(unlocked),
            "time_invested_estimate": f"{completed * 30} minutes"
        }
    
    def _calculate_business_metrics(self, user_data: Dict) -> Dict:
        """Calculate business readiness metrics"""
        # Safe access with defaults - prevents NoneType errors
        progress_metrics = user_data.get("progress_metrics") or {}
        completed = progress_metrics.get("completed_lessons", 0) or 0
        
        journey = user_data.get("learning_journey") or {}
        current_module = journey.get("current_module") or "foundation"
        
        # Calculate business readiness scores
        photography_ready = completed >= 1
        listing_ready = completed >= 3
        marketing_ready = completed >= 6
        export_ready = completed >= 9
        
        # Estimate potential impact
        potential_revenue_increase = min(completed * 10, 100)  # Up to 100% increase
        
        return {
            "business_readiness": {
                "photography": "Ready" if photography_ready else "In Progress",
                "product_listing": "Ready" if listing_ready else "Not Started" if completed < 1 else "In Progress",
                "digital_marketing": "Ready" if marketing_ready else "Not Started" if completed < 3 else "In Progress",
                "export_capability": "Ready" if export_ready else "Not Started" if completed < 6 else "In Progress"
            },
            "estimated_impact": {
                "potential_revenue_increase": f"{potential_revenue_increase}%",
                "market_reach_expansion": "Local" if completed < 3 else "National" if completed < 9 else "Global",
                "brand_strength": "Building" if completed < 5 else "Established" if completed < 10 else "Strong"
            },
            "next_milestone": self._get_next_business_milestone(completed),
            "skills_acquired": self._list_acquired_skills(completed)
        }
    
    def _get_next_business_milestone(self, completed: int) -> str:
        """Get next business milestone"""
        milestones = [
            (1, "Professional craft photography"),
            (3, "Multi-platform product listings"),
            (6, "Active social media presence"),
            (9, "International market entry"),
            (12, "Scalable business operations")
        ]
        
        for threshold, milestone in milestones:
            if completed < threshold:
                return f"Complete {threshold - completed} more lessons to achieve: {milestone}"
        
        return "All major business milestones achieved! 🎉"
    
    def _list_acquired_skills(self, completed: int) -> List[str]:
        """List skills acquired based on progress"""
        skills = []
        if completed >= 1: skills.append("Professional Photography")
        if completed >= 2: skills.append("Storytelling")
        if completed >= 3: skills.append("Pricing Strategy")
        if completed >= 4: skills.append("SEO Optimization")
        if completed >= 5: skills.append("Market Positioning")
        if completed >= 6: skills.append("Packaging Design")
        if completed >= 7: skills.append("Content Marketing")
        if completed >= 8: skills.append("Paid Advertising")
        if completed >= 9: skills.append("Video Creation")
        if completed >= 10: skills.append("Export Management")
        if completed >= 11: skills.append("Team Leadership")
        if completed >= 12: skills.append("Brand Building")
        return skills
    
    def _calculate_skill_matrix(self, user_data: Dict) -> Dict:
        """Calculate detailed skill development matrix"""
        # Safe access with defaults
        progress_metrics = user_data.get("progress_metrics") or {}
        completed = progress_metrics.get("completed_lessons", 0) or 0
        
        # Map lessons to skills (simplified)
        skill_scores = {
            "photography": min(completed * 8, 100) if completed >= 1 else 0,
            "storytelling": min((completed - 1) * 12, 100) if completed >= 2 else 0,
            "pricing_strategy": min((completed - 2) * 10, 100) if completed >= 3 else 0,
            "seo_marketing": min((completed - 3) * 10, 100) if completed >= 4 else 0,
            "branding": min((completed - 4) * 10, 100) if completed >= 5 else 0,
            "social_media": min((completed - 6) * 12, 100) if completed >= 7 else 0,
            "advertising": min((completed - 7) * 12, 100) if completed >= 8 else 0,
            "video_content": min((completed - 8) * 15, 100) if completed >= 9 else 0,
            "export_management": min((completed - 9) * 15, 100) if completed >= 10 else 0,
            "team_building": min((completed - 10) * 20, 100) if completed >= 11 else 0
        }
        
        # Calculate overall readiness
        avg_score = sum(skill_scores.values()) / len(skill_scores) if skill_scores else 0
        readiness_level = (
            "Expert" if avg_score >= 80 else
            "Advanced" if avg_score >= 60 else
            "Intermediate" if avg_score >= 40 else
            "Developing"
        )
        
        return {
            "skills": skill_scores,
            "overall_readiness": readiness_level,
            "strongest_skills": sorted(
                [(k, v) for k, v in skill_scores.items() if v > 0],
                key=lambda x: x[1],
                reverse=True
            )[:3],
            "areas_for_growth": [
                k for k, v in skill_scores.items() if v < 50
            ][:3]
        }
    
    def _generate_recommendations(self, user_data: Dict) -> List[str]:
        """Generate AI-powered personalized recommendations"""
        try:
            # Safe access with defaults
            progress_metrics = user_data.get("progress_metrics") or {}
            learning_journey = user_data.get("learning_journey") or {}
            profile = user_data.get("profile") or {}
            craft_analysis = profile.get("craft_analysis") or {}
            
            completed = progress_metrics.get("completed_lessons", 0) or 0
            current_module = learning_journey.get("current_module") or "foundation"
            craft_name = craft_analysis.get("craft_name") or "craft"
            
            recommendations = []
            
            # Progress-based recommendations
            if completed == 0:
                recommendations.append("🎯 Start with craft photography to showcase your work professionally")
            elif completed < 3:
                recommendations.append("📖 Complete your origin story to build emotional connection with customers")
            elif completed < 6:
                recommendations.append("🛒 Focus on creating optimized marketplace listings to increase visibility")
            elif completed < 9:
                recommendations.append("📱 Start building your social media presence for long-term growth")
            else:
                recommendations.append("🌍 You're ready to explore international markets!")
            
            # Skill-gap recommendations
            skill_matrix = self._calculate_skill_matrix(user_data)
            weak_areas = skill_matrix.get("areas_for_growth", []) or []
            
            if "photography" in weak_areas:
                recommendations.append("📸 Improve your product photography - it directly impacts sales")
            if "seo_marketing" in weak_areas:
                recommendations.append("🔍 Learn SEO basics to help customers find your products online")
            if "social_media" in weak_areas:
                recommendations.append("📱 Invest time in social media - it's free marketing!")
            
            # Business-specific recommendations
            if completed >= 3:
                recommendations.append(f"💡 Consider creating product variations of your {craft_name}")
            if completed >= 6:
                recommendations.append("🤝 Network with other artisans in your community for collaboration")
            
            return recommendations[:5]  # Return top 5
            
        except Exception as e:
            return [
                "Continue your learning journey",
                "Practice what you've learned",
                "Connect with fellow artisans"
            ]
    
    def _identify_growth_opportunities(self, user_data: Dict) -> List[Dict]:
        """Identify specific growth opportunities"""
        # Safe access with defaults
        progress_metrics = user_data.get("progress_metrics") or {}
        profile = user_data.get("profile") or {}
        craft_context = profile.get("craft_analysis") or {}
        
        completed = progress_metrics.get("completed_lessons", 0) or 0
        export_potential = craft_context.get("export_potential") or "Medium"
        
        opportunities = []
        
        # E-commerce opportunities
        if completed >= 3:
            opportunities.append({
                "area": "Online Marketplaces",
                "potential": "High",
                "action": "List your products on Etsy, Amazon Handmade, and Indian platforms",
                "impact": "30-50% revenue increase",
                "timeline": "1-2 weeks"
            })
        
        # Social media opportunities
        if completed >= 6:
            opportunities.append({
                "area": "Social Media Sales",
                "potential": "High",
                "action": "Start Instagram/Facebook Shop for direct sales",
                "impact": "Direct customer relationships",
                "timeline": "2-3 weeks"
            })
        
        # Export opportunities
        if completed >= 9 and "high" in export_potential.lower():
            opportunities.append({
                "area": "International Export",
                "potential": "Very High",
                "action": "Start exporting to US/Europe markets",
                "impact": "100-200% revenue increase",
                "timeline": "1-2 months"
            })
        
        # Scaling opportunities
        if completed >= 11:
            opportunities.append({
                "area": "Team Expansion",
                "potential": "High",
                "action": "Hire apprentices to scale production",
                "impact": "2-3x production capacity",
                "timeline": "3-6 months"
            })
        
        # Always include skill development
        opportunities.append({
            "area": "Skill Development",
            "potential": "Medium",
            "action": f"Complete {12 - completed} more lessons to unlock all capabilities",
            "impact": "Full business readiness",
            "timeline": f"{(12 - completed) * 2} weeks"
        })
        
        return opportunities[:4]  # Return top 4# Last updated: 2025-11-01 16:12:25
# Build: 20251101161731
