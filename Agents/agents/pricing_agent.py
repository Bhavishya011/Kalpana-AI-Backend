# Agents/agents/pricing_agent.py
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import google.cloud.firestore
import requests
import time
import re
import json

# Import Market Intelligence
try:
    from .market_intelligence import MarketIntelligence
except ImportError:
    from market_intelligence import MarketIntelligence

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DynamicPricingAgent:
    """
    Calculates dynamic prices based on Heritage Value, Craft Complexity, and Market Demand.
    Integrates with Firestore for cultural knowledge and uses Vertex AI for analysis.
    Includes market price cache for validation.
    """
    
    def __init__(self):
        try:
            # Initialize Firestore
            self.db = google.cloud.firestore.Client()
            self.collection = "cultural_knowledge_base"
            logger.info("✅ Firestore client initialized successfully for pricing")
        except Exception as e:
            logger.error(f"❌ Firestore initialization failed: {str(e)}")
            raise
        
        try:
            # Initialize Vertex AI with correct billing-enabled project
            vertexai.init(project=os.getenv("GOOGLE_CLOUD_PROJECT", "nodal-fountain-470717-j1"), location="us-central1")
            self.model = GenerativeModel("gemini-2.0-flash")
            logger.info("✅ Vertex AI initialized successfully for pricing")
        except Exception as e:
            logger.error(f"❌ Vertex AI initialization failed: {str(e)}")
            raise
        
        # Initialize Market Intelligence with Google Trends
        try:
            logger.info("📊 Initializing Market Intelligence...")
            self.market_intel = MarketIntelligence()
            
            # Load market cache from Market Intelligence
            cache_data = self.market_intel.get_market_cache()
            self.market_cache = cache_data['categories']
            
            logger.info("✅ Market Intelligence initialized successfully")
            logger.info(f"📅 Market data last updated: {cache_data.get('last_updated', 'Never')}")
        except Exception as e:
            logger.warning(f"⚠️ Market Intelligence initialization failed: {e}")
            logger.info("📦 Falling back to default market cache")
            # Fall back to manual initialization
            self._init_market_cache()
            self.market_intel = None
        
        logger.info("✅ Pricing Agent fully initialized")
    
    def _init_market_cache(self):
        """Initialize market price cache with typical Indian craft categories"""
        # This data would ideally come from a weekly scraping job or API
        # For now, using curated baseline data
        self.market_cache = {
            'pottery': {
                'avg_markup': 200.0,
                'range': (100, 400),
                'demand': 'high',
                'last_updated': datetime.now()
            },
            'embroidery': {
                'avg_markup': 350.0,
                'range': (200, 600),
                'demand': 'high',
                'last_updated': datetime.now()
            },
            'jewelry': {
                'avg_markup': 500.0,
                'range': (300, 1000),
                'demand': 'very_high',
                'last_updated': datetime.now()
            },
            'textile': {
                'avg_markup': 300.0,
                'range': (150, 500),
                'demand': 'high',
                'last_updated': datetime.now()
            },
            'woodwork': {
                'avg_markup': 250.0,
                'range': (150, 450),
                'demand': 'medium',
                'last_updated': datetime.now()
            },
            'metalwork': {
                'avg_markup': 400.0,
                'range': (250, 700),
                'demand': 'high',
                'last_updated': datetime.now()
            },
            'painting': {
                'avg_markup': 450.0,
                'range': (250, 800),
                'demand': 'high',
                'last_updated': datetime.now()
            },
            'leather': {
                'avg_markup': 280.0,
                'range': (150, 450),
                'demand': 'medium',
                'last_updated': datetime.now()
            }
        }
        
        # Cache expiry time (7 days)
        self.cache_expiry_days = 7

    def calculate_price(self, product_description: str, storyteller_output: Dict[str, Any], material_cost: Optional[float] = 0.0) -> Dict[str, Any]:
        """
        Calculates a dynamic price based on input factors.

        Args:
            product_description: The artisan's description of the product.
            storyteller_output: The output dictionary from the Storyteller Agent.
            material_cost: Optional material cost provided by the artisan.

        Returns:
            A dictionary containing the price suggestion, range, justification, and probability estimate.
        """
        logger.info("=" * 60)
        logger.info("🎯 Starting Dynamic Pricing Calculation")
        logger.info("=" * 60)
        logger.info(f"📝 Description: {product_description[:100]}...")
        logger.info(f"💰 Material cost: ₹{material_cost}")
        
        # --- 1. Analyze Heritage Value ---
        logger.info("\n" + "=" * 60)
        logger.info("📊 COMPONENT ANALYSIS")
        logger.info("=" * 60)
        
        heritage_score = self._analyze_heritage_value(storyteller_output)
        logger.info(f"🏛️ Heritage Score: {heritage_score}/10")
        
        # --- 2. Analyze Craft Complexity ---
        complexity_score = self._analyze_complexity(product_description, storyteller_output)
        logger.info(f"🎨 Complexity Score: {complexity_score}/10")
        
        # --- 3. Analyze Market Demand ---
        market_score = self._analyze_market_demand(product_description, storyteller_output)
        logger.info(f"📈 Market Score: {market_score}/10")
        
        # --- 4. Combine Scores (Weighted Average) ---
        logger.info("\n" + "=" * 60)
        logger.info("⚖️ WEIGHTED CALCULATION")
        logger.info("=" * 60)
        
        # Adjust weights based on importance
        heritage_weight = 0.3
        complexity_weight = 0.4
        market_weight = 0.3
        
        weighted_heritage = heritage_score * heritage_weight
        weighted_complexity = complexity_score * complexity_weight
        weighted_market = market_score * market_weight
        
        logger.info(f"Heritage (30%): {heritage_score} × 0.3 = {weighted_heritage:.2f}")
        logger.info(f"Complexity (40%): {complexity_score} × 0.4 = {weighted_complexity:.2f}")
        logger.info(f"Market (30%): {market_score} × 0.3 = {weighted_market:.2f}")
        
        combined_score = weighted_heritage + weighted_complexity + weighted_market
        logger.info(f"\n📊 Combined Score: {combined_score:.2f}/10")
        
        # --- 5. Base Price Calculation (Artisan Markup) ---
        # Calculate markup based on craft value (not material cost)
        base_markup = 250.0  # Base artisan value
        complexity_bonus = complexity_score * 25.0  # Each complexity point adds ₹25
        heritage_bonus = heritage_score * 20.0  # Each heritage point adds ₹20
        market_bonus = market_score * 15.0  # Each market point adds ₹15
        
        artisan_markup = base_markup + complexity_bonus + heritage_bonus + market_bonus
        
        # Apply combined score multiplier
        price_multiplier = 1.0 + (combined_score / 20.0)  # Score of 10 adds 50% multiplier
        suggested_price = artisan_markup * price_multiplier
        
        logger.info("\n" + "=" * 60)
        logger.info("💰 PRICING BREAKDOWN")
        logger.info("=" * 60)
        logger.info(f"Base Artisan Value: ₹{base_markup:.2f}")
        logger.info(f"Complexity Bonus: ₹{complexity_bonus:.2f}")
        logger.info(f"Heritage Bonus: ₹{heritage_bonus:.2f}")
        logger.info(f"Market Bonus: ₹{market_bonus:.2f}")
        logger.info(f"Subtotal: ₹{artisan_markup:.2f}")
        logger.info(f"Combined Score Multiplier: {price_multiplier:.2f}x")
        logger.info(f"Final Artisan Markup: ₹{suggested_price:.2f}")
        
        # --- 6. Generate Range and Justification ---
        range_lower = suggested_price * 0.9
        range_upper = suggested_price * 1.1
        
        logger.info(f"\n✨ FINAL PRICING:")
        logger.info(f"Recommended Markup: ₹{suggested_price:.2f}")
        logger.info(f"Price Range: ₹{range_lower:.2f} - ₹{range_upper:.2f}")
        
        justification = self._generate_justification(heritage_score, complexity_score, market_score, storyteller_output)
        
        # --- 7. Market Validation ---
        logger.info("\n" + "=" * 60)
        logger.info("🔍 MARKET VALIDATION")
        logger.info("=" * 60)
        
        validation_result = self._validate_with_market_cache(suggested_price, product_description, storyteller_output)
        
        logger.info(f"Category Detected: {validation_result.get('category', 'Unknown')}")
        logger.info(f"Original AI Price: ₹{validation_result['original_price']:.2f}")
        logger.info(f"Adjusted Price: ₹{validation_result['adjusted_price']:.2f}")
        logger.info(f"Validation: {validation_result['message']}")
        logger.info(f"Reason: {validation_result['adjustment_reason']}")
        
        # Use validated price
        final_price = validation_result['adjusted_price']
        final_range_lower = final_price * 0.9
        final_range_upper = final_price * 1.1
        
        logger.info(f"\n✨ FINAL VALIDATED PRICING:")
        logger.info(f"Recommended Markup: ₹{final_price:.2f}")
        logger.info(f"Price Range: ₹{final_range_lower:.2f} - ₹{final_range_upper:.2f}")
        
        # --- 8. Estimate Success Probability ---
        success_probability = min(95.0, max(50.0, 50.0 + combined_score * 4.5))
        logger.info(f"🎯 Success Probability: {success_probability:.1f}%")
        logger.info("=" * 60)
        
        result = {
            "suggested_price": round(final_price, 2),
            "price_range": {"min": round(final_range_lower, 2), "max": round(final_range_upper, 2)},
            "justification": justification,
            "success_probability": round(success_probability, 2),
            "market_validation": {
                "category": validation_result.get('category', 'Unknown'),
                "original_ai_price": round(validation_result['original_price'], 2),
                "adjusted_price": round(validation_result['adjusted_price'], 2),
                "adjustment_reason": validation_result['adjustment_reason'],
                "validation_message": validation_result['message']
            },
            "breakdown": {
                "heritage_score": round(heritage_score, 2),
                "complexity_score": round(complexity_score, 2),
                "market_score": round(market_score, 2),
                "combined_score": round(combined_score, 2),
                "base_price": round(base_markup, 2),
                "price_multiplier": round(price_multiplier, 2)
            }
        }
        
        return result

    def _analyze_heritage_value(self, storyteller_output: Dict[str, Any]) -> float:
        """
        Analyzes heritage value based on storyteller output.
        Returns a score between 0 and 10.
        """
        # Check for religious/cultural significance
        cultural_elements = storyteller_output.get("cultural_elements", [])
        story_text = " ".join(storyteller_output.get("image_prompts", [])) + " " + storyteller_output.get("story_title", "")
        story_text_lower = story_text.lower()
        
        score = 0.0
        
        # Check for religious/cultural significance keywords
        religious_keywords = ["religious", "spiritual", "temple", "worship", "deity", "ganesha", "krishna", "durga", "diwali", "holi", "festival"]
        if any(keyword in story_text_lower for keyword in religious_keywords):
            score += 3.0
        
        # Check for endangered/rare techniques (requires knowledge base lookup)
        # This is a simplified check - could be enhanced with Firestore lookup
        rare_techniques = ["kutch pottery", "manjusha art", "kalamkari", "warli", "madhubani"]
        if any(technique.lower() in story_text_lower for technique in rare_techniques):
            score += 4.0
        
        # Check for regional significance
        overview_region = storyteller_output.get("overview", {}).get("region", "").lower()
        if "rajasthan" in overview_region or "kutch" in overview_region or "gujarat" in overview_region:
            score += 2.0
        
        # Check for "generational" and "traditional" in story
        if "generational" in story_text_lower or "traditional" in story_text_lower:
            score += 1.0
        
        return min(10.0, score)

    def _analyze_complexity(self, product_description: str, storyteller_output: Dict[str, Any]) -> float:
        """
        Analyzes craft complexity based on description and story using Gemini AI.
        Returns a score between 0 and 10.
        """
        try:
            # Combine description and image prompts for comprehensive analysis
            image_prompts = storyteller_output.get("image_prompts", [])
            full_context = f"""
Craft Description: {product_description}

Visual Elements from Story: {', '.join(image_prompts[:3]) if image_prompts else 'No additional visual context'}

Cultural Elements: {', '.join(storyteller_output.get("cultural_elements", []))}
"""
            
            complexity_prompt = f"""Analyze this Indian craft for complexity and assign a score from 1-10.

Context:
{full_context}

Rate based on these factors:
1. Technical Skill Required (1-10):
   - Simple crafts (basic pottery, weaving): 1-3
   - Moderate skills (painted pottery, embroidery): 4-6
   - Advanced skills (filigree, inlay work, meenakari): 7-10

2. Time Investment:
   - Quick crafts (few hours): +0 points
   - Moderate time (1-2 days): +1 point
   - Long process (weeks): +2 points

3. Detail & Intricacy:
   - Basic patterns: +0 points
   - Moderate detail: +1 point
   - Highly intricate: +2 points

4. Special Techniques:
   - Standard methods: +0 points
   - Traditional specialized techniques: +1 point
   - Rare/difficult techniques: +2 points

Respond with ONLY a number between 1-10 representing the overall complexity score.
Example: 7.5"""

            logger.info(f"🎨 Analyzing complexity with Gemini AI...")
            response = self.model.generate_content(complexity_prompt)
            
            # Extract score from response
            response_text = response.text.strip()
            logger.info(f"📝 Gemini response: {response_text}")
            
            # Try to extract number from response
            import re
            numbers = re.findall(r'\d+\.?\d*', response_text)
            
            if numbers:
                base_score = float(numbers[0])
                # Ensure score is within range
                base_score = max(1.0, min(10.0, base_score))
                logger.info(f"✅ Base complexity score from AI: {base_score}/10")
            else:
                logger.warning("⚠️ Could not extract score from Gemini, using heuristic analysis")
                base_score = self._heuristic_complexity_analysis(product_description, storyteller_output)
            
            # Check for advanced techniques (case-insensitive)
            advanced_techniques = [
                'hand_painted', 'hand painted', 'handpainted', 'hand-painted',
                'embroidery', 'embroidered',
                'filigree',
                'inlay_work', 'inlay work', 'inlay',
                'damascene',
                'meenakari', 'minakari',
                'zardozi', 'zardozi work',
                'block print', 'block printing',
                'tie dye', 'bandhani', 'tie-dye',
                'kalamkari',
                'warli', 'madhubani', 'pattachitra',
                'peacock', 'lotus', 'geometric patterns',
                'intricate', 'detailed', 'multi-layered'
            ]
            
            # Convert to lowercase for comparison
            desc_lower = product_description.lower()
            cultural_elements = [elem.lower() for elem in storyteller_output.get("cultural_elements", [])]
            story_text = ' '.join(image_prompts).lower()
            full_text = desc_lower + ' ' + story_text + ' ' + ' '.join(cultural_elements)
            
            technique_bonus = 0
            found_techniques = []
            
            for technique in advanced_techniques:
                if technique in full_text:
                    technique_bonus += 0.5  # +0.5 per technique
                    found_techniques.append(technique)
            
            # Cap technique bonus at +3 points
            technique_bonus = min(3.0, technique_bonus)
            
            if found_techniques:
                logger.info(f"🎯 Found advanced techniques: {', '.join(set(found_techniques))}")
                logger.info(f"💫 Technique bonus: +{technique_bonus}")
            
            # Calculate final score with bonus (cap at 10)
            final_score = min(10.0, base_score + technique_bonus)
            
            logger.info(f"✅ Final complexity score: {final_score}/10")
            return final_score
            
        except Exception as e:
            logger.error(f"❌ Complexity analysis failed: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            # Fall back to heuristic analysis
            logger.info("⚠️ Using heuristic complexity analysis as fallback")
            return self._heuristic_complexity_analysis(product_description, storyteller_output)
    
    def _heuristic_complexity_analysis(self, product_description: str, storyteller_output: Dict[str, Any]) -> float:
        """Fallback heuristic-based complexity analysis when AI fails"""
        score = 5.0  # Start with medium complexity
        
        desc_lower = product_description.lower()
        
        # Check for complexity indicators
        if any(word in desc_lower for word in ["hand-painted", "handpainted", "hand painted"]):
            score += 1.5
        if any(word in desc_lower for word in ["intricate", "detailed", "elaborate"]):
            score += 1.0
        if any(word in desc_lower for word in ["multi-layered", "multi-colored", "multicolored"]):
            score += 1.0
        if any(word in desc_lower for word in ["peacock", "lotus", "floral"]):
            score += 1.0
        
        # Check cultural elements
        cultural_elements = storyteller_output.get("cultural_elements", [])
        if len(cultural_elements) > 3:
            score += 1.0
        
        # Check story for time investment
        story_text = " ".join(storyteller_output.get("image_prompts", [])).lower()
        if any(word in story_text for word in ["hours", "days", "weeks", "time-consuming"]):
            score += 1.0
        
        return min(10.0, max(1.0, score))

    def _analyze_market_demand(self, product_description: str, storyteller_output: Dict[str, Any]) -> float:
        """
        Analyzes market demand using Google Trends data and regional factors.
        Returns a score between 0 and 10.
        """
        logger.info("\n🔍 Analyzing Market Demand...")
        
        # Start with base regional score
        region = storyteller_output.get("overview", {}).get("region", "").lower()
        
        regional_demand = {
            'rajasthan': 0.9,
            'gujarat': 0.85,
            'madhya pradesh': 0.8,
            'kerala': 0.75,
            'karnataka': 0.75,
            'west bengal': 0.8,
            'odisha': 0.7,
            'tamil nadu': 0.75,
            'uttar pradesh': 0.8
        }
        
        base_score = 5.0
        for reg, weight in regional_demand.items():
            if reg in region:
                base_score = weight * 10
                logger.info(f"📍 Region '{reg}' detected: Base score = {base_score}/10")
                break
        
        # Apply Google Trends multiplier if available
        if self.market_intel:
            try:
                # Detect category from description
                category = self._detect_craft_category(product_description, storyteller_output)
                
                # Get trend-based multiplier
                trend_multiplier = self.market_intel.get_category_multiplier(category)
                logger.info(f"📈 Google Trends multiplier for '{category}': {trend_multiplier}x")
                
                base_score *= trend_multiplier
                
                # Apply seasonal multiplier
                seasonal_multiplier = self.market_intel.get_active_seasonal_multiplier()
                if seasonal_multiplier > 1.0:
                    logger.info(f"🎉 Active seasonal trend: {seasonal_multiplier}x multiplier")
                    base_score *= seasonal_multiplier
                
            except Exception as e:
                logger.warning(f"⚠️ Could not apply trend multipliers: {e}")
        else:
            # Fallback to manual seasonal logic
            current_month = datetime.now().month
            seasonal_trends = {
                'diwali': {'multiplier': 1.3, 'months': [10, 11]},
                'wedding_season': {'multiplier': 1.2, 'months': [11, 12, 1, 2]},
                'holi': {'multiplier': 1.1, 'months': [3]},
            }
            
            for season, data in seasonal_trends.items():
                if current_month in data['months']:
                    logger.info(f"🎉 {season.title()} season detected: {data['multiplier']}x multiplier")
                    base_score *= data['multiplier']
                    break
        
        # Cap at 10
        final_score = min(10.0, base_score)
        logger.info(f"✅ Final Market Demand Score: {final_score}/10")
        
        return final_score

    def _get_trend_score(self, product_description: str, storyteller_output: Dict[str, Any]) -> float:
        """
        Fetches trend data using Google Trends API.
        Returns a normalized score contribution (e.g., -2 to +2).
        """
        # This method is now integrated into _analyze_market_demand
        # Keeping for backward compatibility
        desc_lower = product_description.lower()
        story_text_lower = " ".join(storyteller_output.get("image_prompts", [])) + " " + storyteller_output.get("story_title", "").lower()
        
        # Example: Check for seasonal keywords
        high_season_keywords = ["diwali", "festival", "decorative", "home decor", "handicraft"]
        found_high_season = any(kw in desc_lower or kw in story_text_lower for kw in high_season_keywords)
        
        # This is a placeholder - in production, you'd use Google Trends API
        return 1.5 if found_high_season else 0.0

    def _get_regional_demand_score(self, storyteller_output: Dict[str, Any]) -> float:
        """
        Uses hyperlocal demand data or region-specific market knowledge.
        Returns a normalized score contribution (e.g., -1 to +1).
        """
        region = storyteller_output.get("overview", {}).get("region", "").lower()
        
        # Example regions with potentially higher/lower demand
        high_demand_regions = ["jaipur", "kutch", "banaras", "puri", "mumbai", "delhi"]
        low_demand_regions = ["remote", "less known"]
        
        if any(r in region for r in high_demand_regions):
            return 0.5  # Small positive boost
        elif any(r in region for r in low_demand_regions):
            return -0.5  # Small negative adjustment
        else:
            return 0.0  # Neutral

    def _get_seasonal_score(self, product_description: str, storyteller_output: Dict[str, Any]) -> float:
        """
        Determines if the product is seasonal based on description/story.
        Returns a normalized score contribution (e.g., -1 to +2).
        """
        desc_lower = product_description.lower()
        story_text_lower = " ".join(storyteller_output.get("image_prompts", [])) + " " + storyteller_output.get("story_title", "").lower()
        
        # Check for seasonal keywords
        high_season_keywords = ["diya", "diyas", "rangoli", "festival", "decorative", "diwali", "dhanteras", "karva chauth", "halloween", "christmas", "new year"]
        medium_season_keywords = ["wedding", "ceremony", "occasion"]
        
        found_high_season = any(kw in desc_lower or kw in story_text_lower for kw in high_season_keywords)
        found_medium_season = any(kw in desc_lower or kw in story_text_lower for kw in medium_season_keywords)
        
        if found_high_season:
            # Check if currently in season (simplified)
            current_month = datetime.now().month
            if "diwali" in desc_lower or "diya" in desc_lower:
                if current_month in [10, 11]:
                    return 2.0  # High boost if in season
                elif current_month in [9, 10]:
                    return 1.0  # Slight boost earlier
                else:
                    return -0.5  # Slight penalty if off-season
            return 1.5  # Default high season boost
        elif found_medium_season:
            return 1.0  # Medium boost
        else:
            return 0.0  # Neutral

    def _get_competitor_pricing_score(self, product_description: str, storyteller_output: Dict[str, Any]) -> float:
        """
        Fetches competitor prices for similar products.
        Returns a normalized score contribution based on relative pricing.
        """
        # This is where you'd implement a competitor data source
        # For now, return a neutral score
        logger.warning("Competitor pricing data source not implemented yet.")
        return 0.0

    def _generate_justification(self, heritage_score: float, complexity_score: float, market_score: float, storyteller_output: Dict[str, Any]) -> str:
        """
        Generates a human-readable justification for the price suggestion.
        """
        parts = ["Suggested price based on:"]
        
        if heritage_score >= 7:
            parts.append("High cultural/heritage significance.")
        elif heritage_score >= 4:
            parts.append("Moderate cultural/heritage significance.")
        
        if complexity_score >= 7:
            parts.append("High craft complexity and time investment.")
        elif complexity_score >= 4:
            parts.append("Moderate craft complexity.")
        
        if market_score >= 7:
            parts.append("High current market demand.")
        elif market_score >= 4:
            parts.append("Moderate market demand.")
        
        # Add specific elements from storyteller output
        cultural_elements = storyteller_output.get("cultural_elements", [])
        if cultural_elements:
            parts.append(f"Includes cultural elements: {', '.join(cultural_elements[:2])}.")
        
        story_title = storyteller_output.get("story_title", "")
        if story_title:
            parts.append(f"Story theme: '{story_title}'.")
        
        return " ".join(parts)
    
    def _detect_craft_category(self, product_description: str, storyteller_output: Dict[str, Any]) -> str:
        """Detect the craft category from description and story"""
        desc_lower = product_description.lower()
        cultural_elements = ' '.join(storyteller_output.get("cultural_elements", [])).lower()
        combined_text = desc_lower + ' ' + cultural_elements
        
        # Check for category keywords
        if any(word in combined_text for word in ['pot', 'pottery', 'clay', 'ceramic', 'terracotta']):
            return 'pottery'
        elif any(word in combined_text for word in ['embroidery', 'embroidered', 'stitch', 'needlework', 'zardozi']):
            return 'embroidery'
        elif any(word in combined_text for word in ['jewelry', 'jewellery', 'necklace', 'earring', 'bangle']):
            return 'jewelry'
        elif any(word in combined_text for word in ['textile', 'fabric', 'cloth', 'saree', 'dupatta', 'weaving']):
            return 'textile'
        elif any(word in combined_text for word in ['wood', 'wooden', 'carving', 'carved']):
            return 'woodwork'
        elif any(word in combined_text for word in ['metal', 'brass', 'copper', 'silver', 'gold', 'filigree']):
            return 'metalwork'
        elif any(word in combined_text for word in ['painting', 'painted', 'warli', 'madhubani', 'pattachitra']):
            return 'painting'
        elif any(word in combined_text for word in ['leather', 'hide', 'skin']):
            return 'leather'
        else:
            return 'pottery'  # Default category
    
    def _validate_with_market_cache(self, suggested_price: float, product_description: str, storyteller_output: Dict[str, Any]) -> Dict[str, Any]:
        """Validate AI-suggested price against market cache data"""
        try:
            # Detect craft category
            category = self._detect_craft_category(product_description, storyteller_output)
            logger.info(f"🏷️ Detected craft category: {category}")
            
            # Get market data for this category
            if category not in self.market_cache:
                logger.warning(f"⚠️ No market data for category: {category}")
                return {
                    'category': category,
                    'validated': False,
                    'original_price': suggested_price,
                    'adjusted_price': suggested_price,
                    'adjustment_reason': 'no_market_data',
                    'message': 'No market data available for validation'
                }
            
            market_data = self.market_cache[category]
            min_market, max_market = market_data['range']
            avg_market = market_data['avg_markup']
            
            logger.info(f"📊 Market data for {category}:")
            logger.info(f"   Average markup: ₹{avg_market}")
            logger.info(f"   Market range: ₹{min_market} - ₹{max_market}")
            
            # Check if cache is stale (optional - skip if parsing fails)
            try:
                if market_data.get('last_updated'):
                    last_updated = datetime.fromisoformat(market_data['last_updated'])
                    cache_age = (datetime.now() - last_updated).days
                    if cache_age > 7:  # 7 days expiry
                        logger.warning(f"⚠️ Market cache is {cache_age} days old")
            except Exception:
                pass  # Skip cache age check if date parsing fails
            
            # Validate price against market range
            if suggested_price < min_market:
                # AI price is too low
                adjusted_price = min_market * 1.1  # Slightly above minimum
                logger.warning(f"⚠️ AI price (₹{suggested_price}) below market min (₹{min_market})")
                logger.info(f"✅ Adjusted to: ₹{adjusted_price}")
                return {
                    'category': category,
                    'validated': True,
                    'original_price': suggested_price,
                    'adjusted_price': adjusted_price,
                    'adjustment_reason': 'below_market_minimum',
                    'message': f'Price adjusted from ₹{suggested_price:.2f} to ₹{adjusted_price:.2f} to match market floor'
                }
            
            elif suggested_price > max_market * 1.2:  # Allow 20% above max for exceptional pieces
                # AI price is significantly too high
                adjusted_price = max_market
                logger.warning(f"⚠️ AI price (₹{suggested_price}) significantly above market max (₹{max_market})")
                logger.info(f"✅ Adjusted to: ₹{adjusted_price}")
                return {
                    'category': category,
                    'validated': True,
                    'original_price': suggested_price,
                    'adjusted_price': adjusted_price,
                    'adjustment_reason': 'above_market_maximum',
                    'message': f'Price adjusted from ₹{suggested_price:.2f} to ₹{adjusted_price:.2f} to match market ceiling'
                }
            
            else:
                # Price is within acceptable range
                logger.info(f"✅ AI price (₹{suggested_price}) is within market range")
                return {
                    'category': category,
                    'validated': True,
                    'original_price': suggested_price,
                    'adjusted_price': suggested_price,
                    'adjustment_reason': 'within_market_range',
                    'message': f'Price validated against {category} market data'
                }
        
        except Exception as e:
            logger.error(f"❌ Market validation failed: {str(e)}")
            return {
                'category': 'Unknown',
                'validated': False,
                'original_price': suggested_price,
                'adjusted_price': suggested_price,
                'adjustment_reason': 'validation_error',
                'message': f'Validation error: {str(e)}'
            }

# Example usage (for testing):
# if __name__ == "__main__":
#     agent = DynamicPricingAgent()
#     # Mock storyteller output based on your system
#     mock_story_output = {
#         "story_title": "The Soul of the Clay: A Potter's Journey",
#         "emotional_theme": "Hope and Perseverance",
#         "image_prompts": [
#             "A close-up, ground-level shot of an artisan's hands, weathered and stained with earth, gently shapin...",
#             "An aerial view of a village courtyard in Rajasthhan during the monsoon season. A female artisan, dres...",
#             "A low-angle shot inside a dimly lit workshop in  Gujarat. An elderly artisan, his face etched with ye..."
#         ],
#         "cultural_elements": ["blue pottery", "Jaipur technique", "generational knowledge"],
#         "recommended_hashtags": ["#IndianPottery", "#CulturalHeritage", "#TraditionalArt"],
#         "overview": {"region": "Rajasthan (Jaipur Blue Pottery)"}
#     }
#     result = agent.calculate_price("Blue pot with peacock and lotus flowers, traditional Jaipur techniques", mock_story_output, material_cost=100.0)
#     print(result)