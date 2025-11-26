# Translation Service API
# Separate from main product pipeline
import sys
import os
from fastapi import UploadFile, File
import base64
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union, List, Dict, Any

app = FastAPI(title="KalpanaAI Translation Service")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Language mapping
LANGUAGE_NAMES = {
    'en-US': 'English',
    'hi-IN': 'Hindi',
    'bn-IN': 'Bengali',
    'ta-IN': 'Tamil',
    'te-IN': 'Telugu',
    'mr-IN': 'Marathi',
    'gu-IN': 'Gujarati',
    'kn-IN': 'Kannada',
}

class TranslationRequest(BaseModel):
    text: Union[str, None] = None
    texts: Union[List[str], None] = None
    object: Union[Dict[str, Any], None] = None
    targetLocale: str
    sourceLocale: str = 'en-US'

class TranslationResponse(BaseModel):
    translation: Union[str, Dict[str, Any], None] = None
    translations: Union[List[str], None] = None
    source_language: str
    target_language: str
    success: bool = True

def get_gemini_client():
    """Initialize Gemini client"""
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(
            vertexai=True,
            project=os.getenv('GOOGLE_CLOUD_PROJECT', 'nodal-fountain-470717-j1'),
            location='us-central1'
        )
        return client
    except Exception as e:
        print(f"❌ Error initializing Gemini client: {e}")
        raise HTTPException(status_code=500, detail="Translation service unavailable")

def translate_with_gemini(text: str, target_language: str, source_language: str) -> str:
    """Translate text using Gemini AI"""
    try:
        from google.genai import types
        
        client = get_gemini_client()
        
        # Build translation prompt
        prompt = f"""You are a professional translator specializing in Indian languages and craftsmanship terminology.

Translate the following text from {source_language} to {target_language}.

CRITICAL RULES:
1. Maintain exact tone, style, and emotional impact
2. Keep ALL formatting: emojis (🎨, 💰, ✨, etc.), line breaks, special characters
3. NEVER translate: "KalpanaAI", brand names, technical terms like "AI", "API"
4. Preserve numbers, percentages, currency symbols (₹, $)
5. Keep HTML/markdown formatting intact
6. Return ONLY the translation, no explanations

Text to translate:
{text}

Translation:"""

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
        
        return response.text.strip()
        
    except Exception as e:
        print(f"❌ Translation error: {e}")
        # Return original text on error
        return text

def translate_batch(texts: List[str], target_language: str, source_language: str) -> List[str]:
    """Translate multiple texts efficiently"""
    try:
        from google.genai import types
        
        client = get_gemini_client()
        
        # Join texts with delimiter
        combined_text = "\n|||SEPARATOR|||\n".join(texts)
        
        prompt = f"""You are a professional translator specializing in Indian languages and craftsmanship terminology.

Translate each section from {source_language} to {target_language}.

CRITICAL RULES:
1. Maintain exact tone, style, and emotional impact
2. Keep ALL formatting: emojis, line breaks, special characters
3. NEVER translate: "KalpanaAI", brand names, technical terms like "AI", "API"
4. Preserve numbers, percentages, currency symbols (₹, $)
5. Keep the |||SEPARATOR||| delimiter exactly as is
6. Return ONLY translations separated by |||SEPARATOR|||, no explanations

Texts to translate:
{combined_text}

Translations:"""

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
                max_output_tokens=8192,
                top_p=0.9,
                top_k=40,
            )
        )
        
        # Split back into array
        translations = response.text.strip().split('|||SEPARATOR|||')
        return [t.strip() for t in translations]
        
    except Exception as e:
        print(f"❌ Batch translation error: {e}")
        # Return original texts on error
        return texts

def translate_object_recursive(obj: Any, target_language: str, source_language: str) -> Any:
    """Recursively translate all string values in an object"""
    if isinstance(obj, str):
        return translate_with_gemini(obj, target_language, source_language)
    
    if isinstance(obj, list):
        # Collect all strings from array
        strings = []
        indices = []
        
        for i, item in enumerate(obj):
            if isinstance(item, str):
                strings.append(item)
                indices.append(i)
        
        # Translate strings in batch
        if strings:
            translations = translate_batch(strings, target_language, source_language)
            result = obj.copy()
            for idx, translation in zip(indices, translations):
                result[idx] = translation
            return result
        
        # Recursively translate objects in array
        return [translate_object_recursive(item, target_language, source_language) for item in obj]
    
    if isinstance(obj, dict):
        result = {}
        strings = []
        keys = []
        
        # Collect all string values
        for key, value in obj.items():
            if isinstance(value, str):
                strings.append(value)
                keys.append(key)
        
        # Translate strings in batch
        if strings:
            translations = translate_batch(strings, target_language, source_language)
            for key, translation in zip(keys, translations):
                result[key] = translation
        
        # Recursively translate nested objects
        for key, value in obj.items():
            if not isinstance(value, str):
                result[key] = translate_object_recursive(value, target_language, source_language)
        
        return result
    
    return obj

@app.get("/")
async def root():
    return {
        "service": "KalpanaAI Translation Service",
        "version": "1.0",
        "supported_languages": list(LANGUAGE_NAMES.values())
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        client = get_gemini_client()
        return {
            "status": "healthy",
            "service": "translation",
            "gemini": "connected",
            "supported_languages": LANGUAGE_NAMES
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """
    Translate text, texts, or objects
    
    Examples:
    - Single text: {"text": "Hello", "targetLocale": "hi-IN"}
    - Multiple texts: {"texts": ["Hello", "World"], "targetLocale": "hi-IN"}
    - Object: {"object": {"title": "Hello", "desc": "World"}, "targetLocale": "hi-IN"}
    """
    try:
        target_lang = LANGUAGE_NAMES.get(request.targetLocale, request.targetLocale)
        source_lang = LANGUAGE_NAMES.get(request.sourceLocale, request.sourceLocale)
        
        # Skip if same language
        if request.targetLocale == request.sourceLocale or request.targetLocale == 'en-US':
            return TranslationResponse(
                translation=request.text or request.object,
                translations=request.texts,
                source_language=source_lang,
                target_language=target_lang,
                success=True
            )
        
        # Single text translation
        if request.text:
            translation = translate_with_gemini(request.text, target_lang, source_lang)
            return TranslationResponse(
                translation=translation,
                source_language=source_lang,
                target_language=target_lang,
                success=True
            )
        
        # Batch text translation
        if request.texts:
            translations = translate_batch(request.texts, target_lang, source_lang)
            return TranslationResponse(
                translations=translations,
                source_language=source_lang,
                target_language=target_lang,
                success=True
            )
        
        # Object translation
        if request.object:
            translation = translate_object_recursive(request.object, target_lang, source_lang)
            return TranslationResponse(
                translation=translation,
                source_language=source_lang,
                target_language=target_lang,
                success=True
            )
        
        raise HTTPException(status_code=400, detail="Must provide text, texts, or object")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Translation error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    target_language: str = "English" # We keep this parameter to avoid breaking the frontend call, but we won't force translation
):
    """
    Transcribe audio exactly as spoken (Native Language -> Native Text)
    """
    try:
        from google.genai import types
        
        # Read audio bytes
        audio_content = await file.read()
        
        client = get_gemini_client()
        
        # 🟢 UPDATED PROMPT: Strictly Transcribe, Do Not Translate
        prompt = f"""
        You are a helpful assistant for Indian artisans. 
        Listen to this audio. The speaker might be speaking in English, Hindi, Tamil, Bengali, or another Indian language.
        
        Task:
        1. Transcribe the speech EXACTLY as spoken in the original language. 
           (e.g., If the audio is in Hindi, output Hindi script like "मिट्टी का बर्तन". If Tamil, output Tamil script).
        2. Do NOT translate it to English.
        3. Return ONLY the transcription text.
        4. Do not include markdown or timestamps.
        """

        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(data=audio_content, mime_type=file.content_type or "audio/webm")
            ]
        )
        
        return {
            "success": True,
            "transcription": response.text.strip()
        }
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8081))  # Different port from main API
    
    print("🌐 Starting KalpanaAI Translation Service...")
    print(f"📍 Server: http://localhost:{port}")
    print(f"📖 API Docs: http://localhost:{port}/docs")
    print("✨ Supported languages:", ", ".join(LANGUAGE_NAMES.values()))
    print("---")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
