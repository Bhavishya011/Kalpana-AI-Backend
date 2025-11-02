"""Tools for the Artisan Mentor Agent"""
from .tutor import HybridArtisanTutor

# Initialize the hybrid tutor
hybrid_tutor = HybridArtisanTutor()

def start_artisan_journey(user_profile: dict) -> dict:
    """Start personalized learning journey for artisan"""
    return hybrid_tutor.create_personalized_learning_journey(user_profile)

def get_adaptive_lesson(user_id: str, lesson_id: str, format: str = "multimodal") -> dict:
    """Get adaptive interactive lesson"""
    return hybrid_tutor.get_interactive_lesson(user_id, lesson_id, format)

def submit_adaptive_work(user_id: str, lesson_id: str, submission: dict) -> dict:
    """Submit work with AI-powered validation"""
    return hybrid_tutor.submit_lesson_work(user_id, lesson_id, submission)

def get_comprehensive_dashboard(user_id: str) -> dict:
    """Get comprehensive business and learning dashboard"""
    return hybrid_tutor.get_business_dashboard(user_id)

def analyze_craft_for_learning(image_input: str) -> dict:
    """Comprehensive craft analysis for personalized learning"""
    return hybrid_tutor.analyze_craft_comprehensive(image_input)

def text_to_speech_assist(text: str, language: str = "en") -> dict:
    """Text to speech assistance for low-literacy users"""
    try:
        audio_url = hybrid_tutor.text_to_speech_multilingual(text, language)
        return {"status": "success", "audio_url": audio_url, "language": language}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def speech_to_text_assist(audio_uri: str, language: str = "en") -> dict:
    """Speech to text assistance for voice inputs"""
    try:
        text = hybrid_tutor.speech_to_text_multilingual(audio_uri, language)
        return {"status": "success", "text": text, "language": language}
    except Exception as e:
        return {"status": "error", "message": str(e)}