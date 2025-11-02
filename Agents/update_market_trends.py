"""
Background script to update market trends weekly
Run this as a cron job or scheduled task

Usage:
    python update_market_trends.py
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_intelligence import MarketIntelligence
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Update market trends using Google Trends API"""
    logger.info("🚀 Starting market trends update...")
    logger.info("⏰ This may take 2-3 minutes due to API rate limits")
    
    try:
        market_intel = MarketIntelligence()
        success = market_intel.update_market_cache()
        
        if success:
            logger.info("\n" + "=" * 60)
            logger.info("✅ Market trends updated successfully!")
            logger.info("=" * 60)
            
            # Show summary
            cache = market_intel.get_market_cache()
            
            print("\n📊 MARKET TRENDS SUMMARY")
            print("=" * 60)
            print(f"Last Updated: {cache['last_updated']}")
            
            print("\n🏷️ Category Trends:")
            for category, data in cache['categories'].items():
                trend_icon = "📈" if data['trend_direction'] == 'rising' else "📉" if data['trend_direction'] == 'falling' else "➡️"
                print(f"  {trend_icon} {category.capitalize():15} Score: {data['trend_score']}/100  Range: ₹{data['range'][0]}-₹{data['range'][1]}")
            
            if cache.get('trending_crafts'):
                print("\n🔥 Trending Crafts:")
                for craft in cache['trending_crafts']:
                    print(f"  • {craft['category'].capitalize()} (Score: {craft['score']})")
            
            if cache.get('seasonal_trends'):
                print("\n🎉 Active Seasonal Trends:")
                for keyword, data in cache['seasonal_trends'].items():
                    if data['active']:
                        print(f"  • {keyword}: {data['multiplier']}x multiplier")
            
            print("=" * 60)
            
            return 0
        else:
            logger.error("\n❌ Market trends update failed!")
            return 1
            
    except Exception as e:
        logger.error(f"\n❌ Error updating market trends: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
