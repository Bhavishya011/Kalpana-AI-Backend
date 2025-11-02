"""Quick test of Market Intelligence module"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.market_intelligence import MarketIntelligence

print("🧪 Testing Market Intelligence...")
print("=" * 60)

try:
    mi = MarketIntelligence()
    print("✅ Market Intelligence initialized successfully")
    
    cache = mi.get_market_cache()
    print(f"\n📦 Cache Status:")
    print(f"  Categories: {len(cache['categories'])}")
    print(f"  Last updated: {cache.get('last_updated', 'Never')}")
    
    print(f"\n🏷️ Available Categories:")
    for category in cache['categories'].keys():
        print(f"  • {category}")
    
    # Test multipliers
    print(f"\n📊 Testing Multipliers:")
    pottery_mult = mi.get_category_multiplier('pottery')
    print(f"  Pottery multiplier: {pottery_mult}x")
    
    seasonal_mult = mi.get_active_seasonal_multiplier()
    print(f"  Seasonal multiplier: {seasonal_mult}x")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
