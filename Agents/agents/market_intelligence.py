"""
Market Intelligence Module
Fetches real-time market trends using Google Trends API
Updates market cache with trending data for Indian crafts
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
from pytrends.request import TrendReq
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketIntelligence:
    """Fetches and analyzes market trends for Indian crafts using Google Trends"""
    
    def __init__(self, cache_file: str = "market_cache.json"):
        """Initialize market intelligence with Google Trends"""
        self.cache_file = cache_file
        
        try:
            self.pytrends = TrendReq(hl='en-IN', tz=330)  # India timezone (IST = UTC+5:30)
            logger.info("✅ Google Trends API initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google Trends: {e}")
            self.pytrends = None
        
        # Craft keywords for trend tracking
        self.craft_keywords = {
            'pottery': ['indian pottery', 'handmade pottery', 'ceramic pottery india'],
            'embroidery': ['indian embroidery', 'hand embroidery', 'chikankari'],
            'jewelry': ['handmade jewelry india', 'silver jewelry', 'oxidized jewelry'],
            'textile': ['handloom textile', 'indian saree', 'handwoven fabric'],
            'woodwork': ['wooden handicraft', 'wood carving india', 'handmade furniture'],
            'metalwork': ['brass handicraft', 'copper utensils', 'metal craft india'],
            'painting': ['madhubani painting', 'warli art', 'indian folk art'],
            'leather': ['leather handicraft', 'handmade leather bag', 'leather goods india']
        }
        
        # Regional keywords
        self.regional_keywords = {
            'rajasthan': ['rajasthan handicraft', 'jaipur craft', 'blue pottery'],
            'gujarat': ['gujarat handicraft', 'kutch embroidery', 'bandhani'],
            'kerala': ['kerala handicraft', 'kathakali mask', 'coir products'],
            'west bengal': ['bengal handicraft', 'kolkata craft', 'terracotta bengal'],
            'madhya pradesh': ['gond art', 'chanderi silk', 'mp handicraft'],
            'uttar pradesh': ['chikankari lucknow', 'brassware', 'up handicraft'],
            'karnataka': ['mysore silk', 'sandalwood craft', 'karnataka handicraft'],
            'tamil nadu': ['tanjore painting', 'kanchipuram silk', 'tamil handicraft']
        }
        
        # Festival/Seasonal keywords
        self.seasonal_keywords = [
            'diwali gifts',
            'wedding gifts india',
            'holi colors',
            'raksha bandhan gifts',
            'christmas decorations india'
        ]
        
        # Load or initialize cache
        self.cache = self._load_cache()
        
        logger.info("✅ Market Intelligence initialized")
    
    def _load_cache(self) -> Dict:
        """Load market cache from file"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
                logger.info(f"📂 Loaded market cache from {self.cache_file}")
                return cache
            except Exception as e:
                logger.error(f"❌ Failed to load cache: {e}")
        
        # Return default cache
        logger.info("📦 Creating default market cache")
        return self._get_default_cache()
    
    def _save_cache(self):
        """Save market cache to file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, indent=2, ensure_ascii=False)
            logger.info(f"💾 Market cache saved to {self.cache_file}")
        except Exception as e:
            logger.error(f"❌ Failed to save cache: {e}")
    
    def _get_default_cache(self) -> Dict:
        """Get default market cache structure"""
        return {
            'last_updated': None,
            'categories': {
                'pottery': {
                    'range': (100, 400),
                    'avg_markup': 200.0,
                    'demand': 'medium',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'embroidery': {
                    'range': (200, 600),
                    'avg_markup': 350.0,
                    'demand': 'high',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'jewelry': {
                    'range': (300, 1000),
                    'avg_markup': 500.0,
                    'demand': 'very_high',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'textile': {
                    'range': (150, 500),
                    'avg_markup': 300.0,
                    'demand': 'high',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'woodwork': {
                    'range': (150, 450),
                    'avg_markup': 275.0,
                    'demand': 'medium',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'metalwork': {
                    'range': (250, 700),
                    'avg_markup': 425.0,
                    'demand': 'medium',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'painting': {
                    'range': (250, 800),
                    'avg_markup': 475.0,
                    'demand': 'high',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                },
                'leather': {
                    'range': (150, 450),
                    'avg_markup': 275.0,
                    'demand': 'medium',
                    'trend_score': 50,
                    'trend_direction': 'stable',
                    'last_updated': datetime.now().isoformat()
                }
            },
            'regional_trends': {},
            'seasonal_trends': {},
            'trending_crafts': []
        }
    
    def fetch_craft_trends(self, category: str) -> Dict:
        """Fetch Google Trends data for a craft category"""
        if not self.pytrends:
            logger.warning("⚠️ Google Trends not available, using defaults")
            return {'trend_score': 50, 'trend_direction': 'stable'}
        
        try:
            keywords = self.craft_keywords.get(category, [category])
            
            # Build payload
            self.pytrends.build_payload(
                keywords[:1],  # Use only first keyword to avoid rate limits
                cat=0,  # All categories
                timeframe='today 3-m',  # Last 3 months
                geo='IN'  # India
            )
            
            # Get interest over time
            interest_df = self.pytrends.interest_over_time()
            
            if interest_df.empty:
                logger.warning(f"⚠️ No trend data for {category}")
                return {'trend_score': 50, 'trend_direction': 'stable'}
            
            # Calculate trend score (0-100)
            recent_avg = interest_df[keywords[0]].tail(4).mean()  # Last month
            overall_avg = interest_df[keywords[0]].mean()  # 3-month avg
            
            trend_score = int(recent_avg) if recent_avg > 0 else 50
            
            # Determine trend direction
            if recent_avg > overall_avg * 1.15:
                trend_direction = 'rising'
            elif recent_avg < overall_avg * 0.85:
                trend_direction = 'falling'
            else:
                trend_direction = 'stable'
            
            logger.info(f"📈 {category}: Score={trend_score}, Direction={trend_direction}")
            
            return {
                'trend_score': trend_score,
                'trend_direction': trend_direction,
                'recent_interest': float(recent_avg),
                'avg_interest': float(overall_avg)
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch trends for {category}: {e}")
            return {'trend_score': 50, 'trend_direction': 'stable'}
    
    def fetch_regional_trends(self, region: str) -> Dict:
        """Fetch regional interest trends"""
        if not self.pytrends:
            return {'regional_score': 50}
        
        try:
            keywords = self.regional_keywords.get(region.lower(), [f"{region} handicraft"])
            
            self.pytrends.build_payload(
                keywords[:1],
                cat=0,
                timeframe='today 3-m',
                geo='IN'
            )
            
            interest_df = self.pytrends.interest_over_time()
            
            if interest_df.empty:
                return {'regional_score': 50}
            
            regional_score = int(interest_df[keywords[0]].mean())
            
            logger.info(f"🌍 {region}: Regional Score={regional_score}")
            
            return {'regional_score': regional_score}
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch regional trends: {e}")
            return {'regional_score': 50}
    
    def fetch_seasonal_trends(self) -> Dict:
        """Fetch current seasonal/festival trends"""
        if not self.pytrends:
            return {}
        
        try:
            self.pytrends.build_payload(
                self.seasonal_keywords[:5],  # Max 5 keywords
                cat=0,
                timeframe='today 1-m',  # Last month
                geo='IN'
            )
            
            interest_df = self.pytrends.interest_over_time()
            
            seasonal_data = {}
            
            for keyword in self.seasonal_keywords[:5]:
                if keyword in interest_df.columns:
                    score = int(interest_df[keyword].tail(7).mean())  # Last week avg
                    
                    # Determine multiplier based on score
                    if score > 70:
                        multiplier = 1.3
                    elif score > 50:
                        multiplier = 1.2
                    elif score > 30:
                        multiplier = 1.1
                    else:
                        multiplier = 1.0
                    
                    seasonal_data[keyword] = {
                        'score': score,
                        'multiplier': multiplier,
                        'active': score > 30
                    }
                    
                    logger.info(f"🎉 {keyword}: Score={score}, Multiplier={multiplier}")
            
            return seasonal_data
            
        except Exception as e:
            logger.error(f"❌ Failed to fetch seasonal trends: {e}")
            return {}
    
    def get_trending_crafts(self) -> List[Dict]:
        """Get list of currently trending craft categories"""
        if not self.pytrends:
            return []
        
        try:
            # Compare all craft categories
            all_keywords = []
            for keywords in self.craft_keywords.values():
                all_keywords.append(keywords[0])
            
            # Google Trends allows max 5 keywords at once
            trending = []
            
            for i in range(0, len(all_keywords), 5):
                batch = all_keywords[i:i+5]
                
                self.pytrends.build_payload(
                    batch,
                    cat=0,
                    timeframe='today 1-m',
                    geo='IN'
                )
                
                interest_df = self.pytrends.interest_over_time()
                
                if not interest_df.empty:
                    # Get top trending from this batch
                    recent_means = interest_df[batch].tail(7).mean()
                    top_trending = recent_means.nlargest(2)
                    
                    for keyword, score in top_trending.items():
                        if score > 60:  # High interest threshold
                            # Map back to category
                            for category, keywords in self.craft_keywords.items():
                                if keyword in keywords:
                                    trending.append({
                                        'category': category,
                                        'score': int(score),
                                        'keyword': keyword
                                    })
                
                time.sleep(1)  # Rate limiting
            
            # Sort by score
            trending.sort(key=lambda x: x['score'], reverse=True)
            
            logger.info(f"🔥 Trending crafts: {[t['category'] for t in trending[:3]]}")
            
            return trending[:5]  # Top 5
            
        except Exception as e:
            logger.error(f"❌ Failed to get trending crafts: {e}")
            return []
    
    def update_market_cache(self) -> bool:
        """Update market cache with latest trends (run weekly)"""
        logger.info("=" * 60)
        logger.info("🔄 UPDATING MARKET CACHE WITH GOOGLE TRENDS")
        logger.info("=" * 60)
        
        if not self.pytrends:
            logger.warning("⚠️ Google Trends not available, skipping update")
            return False
        
        try:
            # Update category trends
            for category in self.craft_keywords.keys():
                trend_data = self.fetch_craft_trends(category)
                
                if category in self.cache['categories']:
                    self.cache['categories'][category].update({
                        'trend_score': trend_data['trend_score'],
                        'trend_direction': trend_data['trend_direction']
                    })
                    
                    # Adjust price ranges based on trend
                    min_price, max_price = self.cache['categories'][category]['range']
                    
                    if trend_data['trend_direction'] == 'rising':
                        # Increase max price by 10%
                        new_max = max_price * 1.1
                        self.cache['categories'][category]['range'] = (min_price, new_max)
                        logger.info(f"📈 {category}: Max price adjusted to ₹{new_max:.0f} (rising trend)")
                    elif trend_data['trend_direction'] == 'falling':
                        # Decrease max price by 5%
                        new_max = max_price * 0.95
                        self.cache['categories'][category]['range'] = (min_price, new_max)
                        logger.info(f"📉 {category}: Max price adjusted to ₹{new_max:.0f} (falling trend)")
                    
                    self.cache['categories'][category]['last_updated'] = datetime.now().isoformat()
                
                time.sleep(2)  # Rate limiting between requests
            
            # Update regional trends
            logger.info("\n🌍 Updating regional trends...")
            for region in list(self.regional_keywords.keys())[:3]:  # Limit to 3 to avoid rate limits
                regional_data = self.fetch_regional_trends(region)
                self.cache['regional_trends'][region] = regional_data
                time.sleep(2)
            
            # Update seasonal trends
            logger.info("\n🎉 Updating seasonal trends...")
            seasonal_data = self.fetch_seasonal_trends()
            self.cache['seasonal_trends'] = seasonal_data
            
            # Get trending crafts
            logger.info("\n🔥 Finding trending crafts...")
            trending = self.get_trending_crafts()
            self.cache['trending_crafts'] = trending
            
            # Update timestamp
            self.cache['last_updated'] = datetime.now().isoformat()
            
            # Save to file
            self._save_cache()
            
            logger.info("\n" + "=" * 60)
            logger.info("✅ Market cache updated successfully!")
            logger.info(f"📅 Last updated: {self.cache['last_updated']}")
            logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Market cache update failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def should_update_cache(self) -> bool:
        """Check if cache needs updating (older than 7 days)"""
        if not self.cache.get('last_updated'):
            return True
        
        try:
            last_updated = datetime.fromisoformat(self.cache['last_updated'])
            days_old = (datetime.now() - last_updated).days
            
            return days_old >= 7
        except:
            return True
    
    def get_category_multiplier(self, category: str) -> float:
        """Get trend-based multiplier for a category"""
        if category not in self.cache['categories']:
            return 1.0
        
        trend_score = self.cache['categories'][category].get('trend_score', 50)
        
        # Convert trend score (0-100) to multiplier (0.8-1.2)
        if trend_score > 80:
            return 1.2  # Very hot
        elif trend_score > 65:
            return 1.15  # Hot
        elif trend_score > 50:
            return 1.05  # Warm
        elif trend_score > 35:
            return 1.0  # Stable
        elif trend_score > 20:
            return 0.95  # Cool
        else:
            return 0.9  # Cold
    
    def get_active_seasonal_multiplier(self) -> float:
        """Get current active seasonal multiplier"""
        if not self.cache.get('seasonal_trends'):
            return 1.0
        
        max_multiplier = 1.0
        
        for keyword, data in self.cache['seasonal_trends'].items():
            if data.get('active', False):
                max_multiplier = max(max_multiplier, data['multiplier'])
        
        return max_multiplier
    
    def get_market_cache(self) -> Dict:
        """Get current market cache"""
        # Auto-update if needed (but not on every call - check flag)
        if self.should_update_cache():
            logger.info("📅 Market cache is outdated (>7 days old)")
            logger.info("💡 Tip: Run 'python update_market_trends.py' to update trends")
        
        return self.cache


# Example usage
if __name__ == "__main__":
    market_intel = MarketIntelligence()
    
    # Test fetch
    print("\n🧪 Testing market intelligence...")
    pottery_trends = market_intel.fetch_craft_trends('pottery')
    print(f"\nPottery trends: {pottery_trends}")
    
    # Get current cache
    cache = market_intel.get_market_cache()
    print(f"\nCache last updated: {cache.get('last_updated', 'Never')}")
    print(f"\nCategories in cache: {list(cache['categories'].keys())}")
