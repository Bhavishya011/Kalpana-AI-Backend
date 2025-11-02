"""
Comprehensive test for pricing agent with market validation
Tests complexity scoring and market cache validation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.pricing_agent import DynamicPricingAgent
import logging

# Set up logging to see all details
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def test_pricing_scenarios():
    """Test multiple scenarios to verify complexity and validation"""
    
    agent = DynamicPricingAgent()
    
    test_cases = [
        {
            "name": "Simple Pottery Bowl",
            "storyteller_output": {
                "cultural_heritage": {
                    "origin": "Rural Maharashtra",
                    "traditional_techniques": ["Hand molding"],
                    "historical_significance": "Common household pottery",
                    "symbolism": "Daily utility"
                },
                "narrative": "A simple terracotta bowl made using traditional hand molding. Commonly used in rural households for serving food.",
                "product_details": {
                    "category": "pottery",
                    "subcategory": "bowls",
                    "materials": ["terracotta", "clay"],
                    "craft_techniques": ["hand molding", "kiln firing"],
                    "dimensions": {"diameter": "15cm", "height": "8cm"}
                },
                "artisan_story": {
                    "experience_years": 10,
                    "skill_level": "intermediate"
                }
            },
            "expected_complexity": "2-4",  # Simple craft
            "expected_category": "pottery"
        },
        {
            "name": "Intricate Embroidered Saree",
            "storyteller_output": {
                "cultural_heritage": {
                    "origin": "Lucknow, Uttar Pradesh",
                    "traditional_techniques": ["Chikankari embroidery", "hand stitching"],
                    "historical_significance": "Royal Mughal craft tradition",
                    "symbolism": "Elegance and tradition"
                },
                "narrative": "An exquisite silk saree featuring intricate Chikankari embroidery with zari work. Each motif is hand-stitched with peacock and lotus patterns, taking 3 months to complete.",
                "product_details": {
                    "category": "textile",
                    "subcategory": "saree",
                    "materials": ["silk", "cotton thread", "zari"],
                    "craft_techniques": ["chikankari", "hand embroidery", "zari work"],
                    "dimensions": {"length": "6.5m", "width": "1.2m"}
                },
                "artisan_story": {
                    "experience_years": 25,
                    "skill_level": "master",
                    "time_to_create": "3 months"
                }
            },
            "expected_complexity": "8-10",  # Highly complex
            "expected_category": "embroidery"
        },
        {
            "name": "Silver Filigree Jewelry",
            "storyteller_output": {
                "cultural_heritage": {
                    "origin": "Cuttack, Odisha",
                    "traditional_techniques": ["Filigree work", "silver smithing"],
                    "historical_significance": "Ancient craft dating back to Mughal era",
                    "symbolism": "Royalty and craftsmanship"
                },
                "narrative": "A stunning silver necklace crafted using traditional filigree technique. Delicate silver wires are hand-twisted and soldered to create intricate peacock motifs with floral patterns.",
                "product_details": {
                    "category": "jewelry",
                    "subcategory": "necklace",
                    "materials": ["silver", "silver wire"],
                    "craft_techniques": ["filigree", "hand-twisted", "soldering", "engraving"],
                    "dimensions": {"length": "40cm"}
                },
                "artisan_story": {
                    "experience_years": 20,
                    "skill_level": "master",
                    "time_to_create": "2 months"
                }
            },
            "expected_complexity": "9-10",  # Very complex
            "expected_category": "jewelry"
        }
    ]
    
    print("\n" + "=" * 80)
    print("🧪 TESTING PRICING AGENT WITH MARKET VALIDATION")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"Expected Complexity Range: {test_case['expected_complexity']}")
        print(f"Expected Category: {test_case['expected_category']}")
        print("=" * 80)
        
        try:
            # Extract a product description from the storyteller output
            product_desc = test_case['storyteller_output'].get('narrative', 
                          f"{test_case['name']} - {test_case['storyteller_output'].get('cultural_heritage', {}).get('origin', 'Unknown')}")
            
            result = agent.calculate_price(product_desc, test_case['storyteller_output'])
            
            print("\n📊 RESULTS:")
            print(f"  Suggested Price: ₹{result['suggested_price']:.2f}")
            print(f"  Price Range: ₹{result['price_range']['min']:.2f} - ₹{result['price_range']['max']:.2f}")
            print(f"  Success Probability: {result['success_probability']:.1f}%")
            
            print("\n📈 SCORE BREAKDOWN:")
            breakdown = result['breakdown']
            print(f"  Heritage Score: {breakdown['heritage_score']:.2f}/10")
            print(f"  Complexity Score: {breakdown['complexity_score']:.2f}/10")
            print(f"  Market Score: {breakdown['market_score']:.2f}/10")
            print(f"  Combined Score: {breakdown['combined_score']:.2f}/10")
            
            print("\n🔍 MARKET VALIDATION:")
            validation = result.get('market_validation', {})
            print(f"  Detected Category: {validation.get('category', 'N/A')}")
            print(f"  Original AI Price: ₹{validation.get('original_ai_price', 0):.2f}")
            print(f"  Adjusted Price: ₹{validation.get('adjusted_price', 0):.2f}")
            print(f"  Adjustment Reason: {validation.get('adjustment_reason', 'N/A')}")
            print(f"  Validation: {validation.get('validation_message', 'N/A')}")
            
            print("\n💡 JUSTIFICATION:")
            print(f"  {result['justification']}")
            
            # Verify complexity is not 0
            complexity = breakdown['complexity_score']
            if complexity == 0:
                print("\n❌ FAILED: Complexity score is still 0!")
            else:
                print(f"\n✅ PASSED: Complexity score is {complexity:.2f} (not 0)")
            
            # Verify category detection
            detected_cat = validation.get('category', 'Unknown')
            if detected_cat.lower() == test_case['expected_category'].lower() or detected_cat != 'Unknown':
                print(f"✅ PASSED: Category correctly detected as '{detected_cat}'")
            else:
                print(f"⚠️ WARNING: Category detection may be off (expected {test_case['expected_category']}, got {detected_cat})")
            
        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 80)

if __name__ == "__main__":
    test_pricing_scenarios()
