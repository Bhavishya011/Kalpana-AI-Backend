"""
KalpanaAI Support Chatbot API
A Gemini 2.5 Flash-powered support chatbot with comprehensive knowledge about KalpanaAI
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession
from google.cloud import speech_v1p1beta1 as speech

# Initialize FastAPI
app = FastAPI(
    title="KalpanaAI Support Chatbot API",
    description="AI-powered support chatbot with knowledge about KalpanaAI features",
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

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "nodal-fountain-470717-j1")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Pydantic models
class Message(BaseModel):
    role: str  # 'user' or 'bot'
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: Optional[str] = "en-US"
    history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str
    language: str

# Knowledge Base about KalpanaAI
KALPANAAI_KNOWLEDGE = """
# KalpanaAI - AI-Powered Platform for Indian Artisans

## Overview
KalpanaAI is a comprehensive AI-powered platform designed to empower Indian artisans and craftspeople by helping them create, market, and sell their handcrafted products. The platform bridges traditional craftsmanship with modern technology.

## Core Features

### 1. AI-Powered Product Creation
- **Multilingual Descriptions**: Generate compelling product descriptions in 10+ Indian languages (Hindi, Bengali, Tamil, Telugu, Marathi, etc.)
- **AI Image Enhancement**: Create professional product images with AI enhancement and background removal
- **Smart Pricing**: Get intelligent pricing recommendations based on market trends, materials, and regional demand
- **Product Variants**: Automatically generate multiple product variations and customization options
- **SEO Optimization**: Product titles and descriptions optimized for online marketplaces

### 2. Market Pulse (Market Intelligence)
- **Hyperlocal Demand Analysis**: Track demand for specific crafts in different locations across India
- **Seasonal Predictions**: Get alerts for upcoming festivals (Diwali, Holi, etc.) and seasonal opportunities
- **Regional Opportunities**: Discover untapped markets in different states and cities
- **Google Trends Integration**: Real-time market trends analysis
- **Competitor Insights**: Understand pricing and demand patterns in your craft category
- **Festival Calendar**: Alerts for Raksha Bandhan, Navratri, Durga Puja, Pongal, Onam, etc.

### 3. The Muse (Creative AI Assistant)
- **Creative Ideation**: Generate innovative product concepts based on traditional crafts
- **Design Variations**: Explore customization options for your products
- **Trend-Based Suggestions**: Get recommendations aligned with current market trends
- **Fusion Designs**: Combine traditional techniques with modern aesthetics
- **Color Palette Suggestions**: AI-generated color combinations for your crafts

### 4. Artisan Mentor (Learning Platform)
- **Personalized Learning Paths**: Customized business skill development for artisans
- **Interactive Lessons**: Learn digital marketing, pricing strategies, customer service
- **AI Validation**: Submit your work and get instant AI-powered feedback
- **Achievements & Points**: Gamified learning with rewards and badges
- **Progress Tracking**: Monitor your learning journey and skill development
- **Voice/Image Assignments**: Submit work through voice notes or images
- **Certificate Programs**: Complete courses to earn certifications

### 5. Sales Analytics Dashboard
- **Sales Trends**: Visualize your sales performance over time
- **Revenue Tracking**: Monitor income and forecast future earnings
- **Customer Insights**: Understand your customer demographics and preferences
- **Product Performance**: Track which products are selling best
- **Regional Analysis**: See where your products are most popular
- **Growth Recommendations**: AI-generated suggestions to increase sales

### 6. Multilingual Support
- **10+ Indian Languages**: English, Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi
- **Real-Time Translation**: All content translates automatically
- **Voice Input**: Speak in your native language
- **Easy Language Switching**: Change language anytime from dropdown
- **Regional Content**: Culturally relevant suggestions for each region

## Craft Categories Supported
- Traditional Textiles (Sarees, Dupattas, Fabrics)
- Pottery & Ceramics
- Jewelry & Accessories
- Home Decor (Lamps, Wall Hangings, Figurines)
- Paintings & Art
- Woodwork & Furniture
- Metalwork (Brass, Copper, Silver)
- Handmade Bags & Purses
- Traditional Toys
- Embroidery & Needlework

## How It Works

### Getting Started
1. Sign up on KalpanaAI dashboard
2. Select your craft type and preferred language
3. Start creating products or explore features

### Creating Products
1. Upload product images or take photos
2. AI enhances images automatically
3. Generate multilingual descriptions
4. Get smart pricing recommendations
5. Review and publish to your store

### Learning with Artisan Mentor
1. Start your personalized learning journey
2. Complete interactive lessons
3. Submit assignments via voice/image
4. Get AI validation and feedback
5. Earn points and achievements

### Market Research
1. Check Market Pulse for demand trends
2. Get seasonal festival alerts
3. Explore regional opportunities
4. Set pricing based on insights

## Pricing
- **Free Tier**: Basic product creation, 5 products/month
- **Pro Tier**: Unlimited products, advanced analytics, priority support
- **Enterprise**: Custom solutions for artisan cooperatives

## Technical Features
- Cloud-based platform (Google Cloud)
- AI powered by Gemini 2.5 Flash
- Real-time translation API
- Mobile-friendly responsive design
- Secure authentication
- Data privacy compliant

## Support & Help
- Live chat support (this chatbot!)
- Email: support@kalpana-ai.com
- Documentation: docs.kalpana-ai.com
- Video tutorials available
- Community forum for artisans

## Common Use Cases
1. **New Artisan**: Just started, need help creating first product listing
2. **Festival Preparation**: Preparing inventory for upcoming festival season
3. **Expanding Market**: Want to sell in new regions/cities
4. **Learning Business Skills**: Need to improve digital marketing, pricing
5. **Product Photography**: Want to improve product images
6. **Language Barriers**: Need to sell to customers in other states
7. **Pricing Help**: Unsure about competitive pricing

## Success Stories
- Artisans increased sales by 300% using smart pricing
- Reach customers across India with multilingual descriptions
- Festival alerts helped plan inventory 2 months ahead
- Artisan Mentor helped 5000+ artisans learn business skills

## Traditional Knowledge Integration
- Respect for traditional craft techniques
- Cultural sensitivity in suggestions
- Preservation of heritage crafts
- Fair pricing that values artisan labor
- Promotion of sustainable practices

## Regional Focus
- North India: Textiles, jewelry, woodwork
- South India: Silk sarees, bronze work, traditional art
- East India: Terracotta, textiles, paintings
- West India: Handicrafts, embroidery, metalwork
- Northeast: Bamboo crafts, textiles, traditional jewelry

## Festivals Covered
Diwali, Holi, Raksha Bandhan, Durga Puja, Navratri, Onam, Pongal, Baisakhi, Eid, Christmas, New Year, Valentine's Day, Mother's Day, Ganesh Chaturthi, Dussehra, Makar Sankranti, Lohri, Ugadi, Vishu, and more.
"""

# System prompt for the chatbot
SYSTEM_PROMPT = f"""You are a helpful and knowledgeable support assistant for KalpanaAI, an AI-powered platform for Indian artisans. 

Your responsibilities:
1. Answer questions about KalpanaAI features, pricing, and capabilities
2. Help users navigate the platform and use features effectively
3. Provide guidance on traditional crafts and business practices
4. Be culturally sensitive and respect traditional knowledge
5. Speak in a friendly, supportive, and encouraging tone
6. If user asks in Hindi or other Indian languages, respond in that language
7. Provide step-by-step guidance when needed
8. Share success stories and best practices

Knowledge Base:
{KALPANAAI_KNOWLEDGE}

Guidelines:
- Always be respectful of artisan traditions
- Encourage users to explore all features
- Provide specific, actionable advice
- If unsure, suggest contacting human support
- Keep responses concise but comprehensive
- Use examples relevant to Indian context
- Mention relevant festivals and seasons when appropriate
"""

# In-memory session storage (in production, use Redis or database)
chat_sessions: Dict[str, ChatSession] = {}

def get_or_create_session(session_id: str) -> ChatSession:
    """Get existing chat session or create new one"""
    if session_id not in chat_sessions:
        model = GenerativeModel("gemini-2.0-flash-exp")
        chat_sessions[session_id] = model.start_chat()
    return chat_sessions[session_id]

@app.get("/")
async def root():
    return {
        "service": "KalpanaAI Support Chatbot",
        "version": "1.0.0",
        "model": "gemini-2.0-flash-exp",
        "status": "active"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_sessions": len(chat_sessions),
        "model": "gemini-2.0-flash-exp",
        "project": PROJECT_ID
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat messages with context awareness
    """
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        # Get or create chat session
        chat_session = get_or_create_session(session_id)
        
        # Build context from history
        context_messages = []
        if request.history:
            for msg in request.history[-5:]:  # Last 5 messages for context
                context_messages.append(f"{msg.role}: {msg.content}")
        
        # Build the full prompt
        full_prompt = f"""{SYSTEM_PROMPT}

Language: {request.language}
User Question: {request.message}

Please provide a helpful, accurate, and friendly response. If the user is asking in Hindi or another Indian language, respond in that language."""

        # Get response from Gemini
        response = chat_session.send_message(full_prompt)
        
        return ChatResponse(
            response=response.text,
            session_id=session_id,
            timestamp=datetime.now().isoformat(),
            language=request.language
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/chat/reset")
async def reset_session(session_id: str):
    """Reset a chat session"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
    return {"message": "Session reset successfully", "session_id": session_id}

@app.get("/chat/sessions")
async def list_sessions():
    """List active chat sessions"""
    return {
        "active_sessions": len(chat_sessions),
        "session_ids": list(chat_sessions.keys())
    }

@app.post("/quick-help")
async def quick_help(category: str):
    """Get quick help for common categories"""
    quick_responses = {
        "getting-started": "To get started with KalpanaAI: 1) Sign up on the dashboard, 2) Select your craft type, 3) Choose your preferred language, 4) Start creating your first product! Need help with any specific step?",
        "product-creation": "To create a product: 1) Go to 'Add Product', 2) Upload product images, 3) AI will enhance them automatically, 4) Generate multilingual descriptions, 5) Get smart pricing suggestions, 6) Review and publish!",
        "artisan-mentor": "Artisan Mentor is your personal learning platform! Start your journey by selecting a lesson path. Complete interactive lessons, submit assignments via voice or images, and earn points and badges. Want to start a specific course?",
        "market-pulse": "Market Pulse shows real-time demand for crafts in different regions. Check seasonal predictions for festivals, explore regional opportunities, and get pricing insights. Which region or festival are you interested in?",
        "the-muse": "The Muse is your creative AI assistant! It helps generate innovative product ideas, design variations, and trend-based suggestions. Tell me about your craft and I'll help you explore creative possibilities!",
        "pricing": "Smart pricing considers: material costs, labor time, market demand, regional trends, and competitor pricing. Upload your product details and get instant recommendations. Need help pricing a specific item?",
        "languages": "KalpanaAI supports 10+ Indian languages including Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, and Punjabi. Change language anytime from the header dropdown!",
        "support": "You can reach support through: 1) This chat (24/7), 2) Email: support@kalpana-ai.com, 3) Documentation at docs.kalpana-ai.com, 4) Community forum. What do you need help with?"
    }
    
    response = quick_responses.get(category, "Please specify a category: getting-started, product-creation, artisan-mentor, market-pulse, the-muse, pricing, languages, or support.")
    
    return {
        "category": category,
        "response": response,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Transcribe audio file to text using Google Cloud Speech-to-Text
    Supports multiple Indian languages with Hindi as primary
    """
    try:
        # Read audio file
        audio_content = await file.read()
        print(f"📥 Received audio file: {file.filename}, size: {len(audio_content)} bytes")
        
        # Initialize Speech client
        client = speech.SpeechClient()
        
        # Configure audio and recognition settings
        audio = speech.RecognitionAudio(content=audio_content)
        
        # Try with Hindi as primary language first (since most Indian artisans speak Hindi)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
            sample_rate_hertz=48000,
            language_code="hi-IN",  # Hindi as primary
            alternative_language_codes=[
                "en-IN",  # Indian English
                "bn-IN",  # Bengali
                "ta-IN",  # Tamil
                "te-IN",  # Telugu
                "mr-IN",  # Marathi
                "gu-IN",  # Gujarati
                "kn-IN",  # Kannada
                "ml-IN",  # Malayalam
                "pa-IN",  # Punjabi
                "en-US",  # English
            ],
            enable_automatic_punctuation=True,
            model="default",
            use_enhanced=True,  # Use enhanced model for better accuracy
        )
        
        print("🎤 Starting speech recognition with Hindi as primary language...")
        
        # Perform speech recognition
        response = client.recognize(config=config, audio=audio)
        
        print(f"📊 Recognition complete. Results: {len(response.results) if response.results else 0}")
        
        # Extract transcription
        transcription = ""
        detected_language = "hi-IN"
        
        if response.results:
            transcription = " ".join([result.alternatives[0].transcript for result in response.results])
            detected_language = response.results[0].language_code if hasattr(response.results[0], 'language_code') else "hi-IN"
            print(f"✅ Transcription successful: '{transcription[:50]}...' (Language: {detected_language})")
        
        if not transcription:
            print("⚠️ No speech detected in audio")
            return {
                "success": False,
                "error": "No speech detected in audio",
                "transcription": ""
            }
        
        return {
            "success": True,
            "transcription": transcription,
            "language": detected_language
        }
        
    except Exception as e:
        print(f"❌ Transcription error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "error": f"Transcription failed: {str(e)}",
            "transcription": ""
        }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8083))
    uvicorn.run(app, host="0.0.0.0", port=port)
