"""Artisan Mentor Agent - Standalone Version"""
from . import tools

class ArtisanMentorAgent:
    """
    The Ultimate Artisan Business Tutor - A comprehensive, adaptive AI mentor.
    
    This agent helps traditional artisans become global entrepreneurs through:
    - Personalized learning journeys adapted to skill level and learning style
    - Progressive curriculum from Foundation to Global Expansion
    - Multimodal support in 9 Indian languages
    - Advanced gamification with points, badges, and metrics
    - Full Google Cloud integration
    """
    
    def __init__(self):
        self.name = "ultimate-artisan-tutor"
        self.model = "gemini-2.0-flash-001"
        self.description = "A comprehensive, adaptive AI tutor that transforms traditional artisans into global entrepreneurs"
        
        # Available tools
        self.tools = {
            "start_artisan_journey": tools.start_artisan_journey,
            "get_adaptive_lesson": tools.get_adaptive_lesson,
            "submit_adaptive_work": tools.submit_adaptive_work,
            "get_comprehensive_dashboard": tools.get_comprehensive_dashboard,
            "analyze_craft_for_learning": tools.analyze_craft_for_learning,
            "text_to_speech_assist": tools.text_to_speech_assist,
            "speech_to_text_assist": tools.speech_to_text_assist
        }
    
    def get_tool(self, tool_name: str):
        """Get a tool function by name"""
        return self.tools.get(tool_name)
    
    def list_tools(self):
        """List all available tools"""
        return list(self.tools.keys())

# Create singleton agent instance
agent = ArtisanMentorAgent()