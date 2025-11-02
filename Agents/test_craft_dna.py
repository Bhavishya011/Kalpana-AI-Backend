"""
Test script for Craft DNA Agent

Run this to see how Craft DNA generates heritage records and QR codes
"""

import sys
import os
import json

# Add agents to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
agents_path = os.path.join(project_root, 'Agents', 'agents')
sys.path.insert(0, agents_path)

from craft_dna_agent import CraftDNAAgent, create_craft_dna_for_product


def test_brass_diya():
    """Test with traditional brass diya"""
    print("🧬 Testing Craft DNA Agent - Brass Diya Example\n")
    print("="*60)
    
    sample_product = {
        "product_id": "PROD_BRASS_DIYA_001",
        "artisan_story": """I learned this brass work from my grandfather who learned 
it from his father. We have been making these diyas for 4 generations in Jaipur. 
Each diya takes 3 days to complete - first we melt the recycled brass, then cast 
it in clay molds, and finally we etch the designs by hand using traditional chisels. 
My family has been lighting up Diwali celebrations for over 100 years.""",
        
        "craft_technique": "Jaipur brass casting and hand etching",
        "regional_tradition": "Rajasthani metalwork tradition",
        
        "materials": [
            "recycled brass", 
            "natural lacquer", 
            "beeswax polish",
            "vegetable-based dyes"
        ],
        
        "cultural_context": """These diyas are traditionally used during Diwali festival 
and are believed to bring prosperity and ward off negative energy. In Rajasthani 
tradition, families light these brass diyas at sunset for 5 days during Diwali. 
The etched patterns represent sacred symbols like the lotus and peacock.""",
        
        "artisan_profile": {
            "name": "Ramesh Kumar",
            "village": "Amber Fort area",
            "state": "Rajasthan",
            "lineage": "4th generation brass artisan",
            "years_of_experience": 25
        },
        
        "sustainability_metrics": {
            "carbon_footprint": {
                "value": 0.3,
                "unit": "kg CO₂",
                "vs_industrial": "75% less than factory-made brass items"
            },
            "water_usage": {
                "value": 5.0,
                "unit": "liters",
                "vs_industrial": "90% less than industrial brass production"
            }
        }
    }
    
    print("📝 Input Product Data:")
    print(f"  Product ID: {sample_product['product_id']}")
    print(f"  Craft: {sample_product['craft_technique']}")
    print(f"  Artisan: {sample_product['artisan_profile']['name']}")
    print(f"  Location: {sample_product['artisan_profile']['village']}, {sample_product['artisan_profile']['state']}")
    print()
    
    print("🔄 Generating Craft DNA...")
    print()
    
    # Generate Craft DNA
    craft_dna = create_craft_dna_for_product(sample_product)
    
    print("✅ Craft DNA Generated Successfully!")
    print("="*60)
    print()
    
    # Display key information
    print("🏷️  HERITAGE INFORMATION")
    print(f"  Heritage ID: {craft_dna['heritage_id']}")
    print(f"  Heritage URL: {craft_dna['heritage_url']}")
    print(f"  Created: {craft_dna['created_at']}")
    print()
    
    print("👨‍🎨 ARTISAN DETAILS")
    print(f"  Name: {craft_dna['artisan']['name']}")
    print(f"  Village: {craft_dna['artisan']['village']}")
    print(f"  Lineage: {craft_dna['artisan']['lineage']}")
    print(f"  Experience: {craft_dna['artisan']['craft_tradition_years']} years")
    print()
    
    print("🎨 CRAFT INFORMATION")
    print(f"  Technique: {craft_dna['craft']['technique']}")
    print(f"  Regional Tradition: {craft_dna['craft']['regional_tradition']}")
    print(f"  Materials: {', '.join(craft_dna['craft']['materials'])}")
    print(f"  Endangered Status: {craft_dna['craft']['endangered_status']}")
    print()
    
    print("📖 HERITAGE NARRATIVE (AI-Generated)")
    print("="*60)
    print(craft_dna['heritage_narrative'])
    print()
    
    print("🌍 CULTURAL ANALYSIS")
    print("="*60)
    for key, value in craft_dna['cultural_analysis'].items():
        print(f"  {key.replace('_', ' ').title()}: {value}")
    print()
    
    print("🌿 SUSTAINABILITY IMPACT")
    print("="*60)
    print(f"  Carbon Footprint: {craft_dna['eco_impact']['carbon_footprint']['value']} {craft_dna['eco_impact']['carbon_footprint']['unit']}")
    print(f"  vs Industrial: {craft_dna['eco_impact']['carbon_footprint']['vs_industrial']}")
    print(f"  Water Usage: {craft_dna['eco_impact']['water_usage']['vs_industrial']}")
    print(f"  Renewable Materials: {craft_dna['eco_impact']['renewable_materials']:.0f}%")
    print(f"  Sustainability Score: {craft_dna['eco_impact']['sustainability_score']}/100")
    print()
    print("  Eco-Claims:")
    for claim in craft_dna['eco_impact']['eco_claims']:
        print(f"    ✓ {claim}")
    print()
    
    print("🔐 AUTHENTICITY VERIFICATION")
    print(f"  Verified: {craft_dna['authenticity']['verified']}")
    print(f"  Certificate: {craft_dna['authenticity']['certificate_number']}")
    print(f"  Blockchain Ready: {craft_dna['authenticity']['blockchain_ready']}")
    print()
    
    print("📊 METADATA")
    print(f"  Category: {craft_dna['metadata']['craft_category']}")
    print(f"  Preservation Priority: {craft_dna['metadata']['preservation_priority']}")
    print(f"  UNESCO Relevant: {craft_dna['metadata']['unesco_relevant']}")
    print(f"  Heritage Tags: {', '.join(craft_dna['metadata']['cultural_heritage_tags'][:5])}")
    print()
    
    print("📱 QR CODE")
    print("="*60)
    print(f"  URL: {craft_dna['qr_code']['url']}")
    print(f"  Format: {craft_dna['qr_code']['format']}")
    print(f"  Size: {craft_dna['qr_code']['size']}")
    print(f"  Printable: {craft_dna['qr_code']['printable']}")
    print(f"  Base64 Length: {len(craft_dna['qr_code']['image_base64'])} characters")
    print()
    
    # Generate printable label
    agent = CraftDNAAgent()
    label = agent.generate_printable_heritage_label(craft_dna)
    
    print("🏷️  PRINTABLE LABEL")
    print("="*60)
    print(f"  Format: {label['format']}")
    print(f"  Size: {label['size']}")
    print(f"  Tagline: {label['text']['tagline']}")
    print()
    
    # Save full JSON
    output_file = "craft_dna_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(craft_dna, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Full Craft DNA saved to: {output_file}")
    print()
    
    # Save QR code image
    import base64
    qr_file = "craft_dna_qr_code.png"
    with open(qr_file, 'wb') as f:
        f.write(base64.b64decode(craft_dna['qr_code']['image_base64']))
    
    print(f"📸 QR Code saved to: {qr_file}")
    print()
    
    print("="*60)
    print("✅ Test Complete!")
    print()
    print("🎉 Your craft's story is now permanently preserved!")
    print(f"🔗 Heritage Page: {craft_dna['heritage_url']}")
    print()


def test_kanjivaram_silk():
    """Test with Kanjivaram silk saree"""
    print("\n\n🧬 Testing Craft DNA Agent - Kanjivaram Silk Example\n")
    print("="*60)
    
    sample_product = {
        "product_id": "PROD_SILK_SAREE_001",
        "artisan_story": """My mother taught me weaving when I was 12 years old. 
Our family has been weaving Kanjivaram silk for 6 generations. Each saree takes 
15-20 days to complete on our traditional handloom. The intricate patterns you see 
are inspired by temple architecture and nature.""",
        
        "craft_technique": "Kanjivaram silk handloom weaving",
        "regional_tradition": "Tamil Nadu temple silk tradition",
        
        "materials": [
            "pure mulberry silk",
            "natural zari thread (gold-plated silver)",
            "organic vegetable dyes"
        ],
        
        "cultural_context": """Kanjivaram silk sarees are considered auspicious and 
are traditionally worn during weddings and temple ceremonies. The silk is blessed 
at local temples before weaving begins. Each color and pattern has deep symbolic 
meaning in South Indian culture.""",
        
        "artisan_profile": {
            "name": "Lakshmi Devi",
            "village": "Kanchipuram",
            "state": "Tamil Nadu",
            "lineage": "6th generation silk weaver",
            "years_of_experience": 30
        }
    }
    
    craft_dna = create_craft_dna_for_product(sample_product)
    
    print("✅ Craft DNA Generated!")
    print(f"🏷️  Heritage ID: {craft_dna['heritage_id']}")
    print(f"🌿 Sustainability Score: {craft_dna['eco_impact']['sustainability_score']}/100")
    print(f"📜 Preservation Status: {craft_dna['metadata']['preservation_priority']}")
    print()


if __name__ == "__main__":
    try:
        # Test 1: Brass Diya (detailed)
        test_brass_diya()
        
        # Test 2: Kanjivaram Silk (quick)
        test_kanjivaram_silk()
        
        print("\n" + "="*60)
        print("🎊 All tests completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
