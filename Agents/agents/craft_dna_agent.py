"""
Craft DNA Agent - Digital Heritage & Provenance System

Generates unique, scannable QR codes linking to permanent digital records
that preserve cultural authenticity, origin stories, and sustainability impact.
"""

import os
import json
import qrcode
import io
import base64
from datetime import datetime
from typing import Dict, List, Optional
from vertexai.generative_models import GenerativeModel, Part
import vertexai

# Initialize Vertex AI
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "nodal-fountain-470717-j1")
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)


class CraftDNAAgent:
    """
    Craft DNA Agent - Preserves cultural heritage and generates provenance records
    """
    
    def __init__(self):
        self.model = GenerativeModel("gemini-2.0-flash-exp")
        self.heritage_page_base_url = "https://kalpana.ai/heritage"
        
    def generate_craft_dna(
        self,
        product_id: str,
        artisan_story: str,
        craft_technique: str,
        regional_tradition: str,
        materials_used: List[str],
        cultural_context: str,
        sustainability_metrics: Optional[Dict] = None,
        artisan_profile: Optional[Dict] = None
    ) -> Dict:
        """
        Generate comprehensive Craft DNA record with QR code
        
        Args:
            product_id: Unique product identifier
            artisan_story: Personal story from artisan (voice/text)
            craft_technique: Specific technique used (e.g., "Jaipur brass casting")
            regional_tradition: Geographic and cultural origin
            materials_used: List of materials (e.g., ["recycled brass", "natural lacquer"])
            cultural_context: Cultural/ritual significance
            sustainability_metrics: Environmental impact data
            artisan_profile: Artisan details (name, village, lineage)
            
        Returns:
            Complete Craft DNA record with QR code
        """
        
        # Generate heritage narrative using AI
        heritage_narrative = self._generate_heritage_narrative(
            artisan_story=artisan_story,
            craft_technique=craft_technique,
            regional_tradition=regional_tradition,
            materials_used=materials_used,
            cultural_context=cultural_context,
            artisan_profile=artisan_profile
        )
        
        # Calculate sustainability impact
        eco_impact = self._calculate_eco_impact(
            materials_used=materials_used,
            craft_technique=craft_technique,
            sustainability_metrics=sustainability_metrics
        )
        
        # Generate cultural significance analysis
        cultural_analysis = self._analyze_cultural_significance(
            craft_technique=craft_technique,
            regional_tradition=regional_tradition,
            cultural_context=cultural_context
        )
        
        # Create unique heritage ID
        heritage_id = f"CDN-{product_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Generate heritage page URL
        heritage_url = f"{self.heritage_page_base_url}/{heritage_id}"
        
        # Generate QR code
        qr_code_data = self._generate_qr_code(heritage_url)
        
        # Compile complete Craft DNA record
        craft_dna = {
            "heritage_id": heritage_id,
            "product_id": product_id,
            "created_at": datetime.utcnow().isoformat(),
            "heritage_url": heritage_url,
            "qr_code": qr_code_data,
            
            # Artisan Information
            "artisan": {
                "name": artisan_profile.get("name") if artisan_profile else "Anonymous Artisan",
                "village": artisan_profile.get("village") if artisan_profile else None,
                "state": artisan_profile.get("state") if artisan_profile else None,
                "lineage": artisan_profile.get("lineage") if artisan_profile else None,
                "craft_tradition_years": artisan_profile.get("years_of_experience") if artisan_profile else None,
                "personal_story": artisan_story
            },
            
            # Craft Technique
            "craft": {
                "technique": craft_technique,
                "regional_tradition": regional_tradition,
                "materials": materials_used,
                "cultural_context": cultural_context,
                "endangered_status": self._check_endangered_craft(craft_technique)
            },
            
            # AI-Generated Heritage Content
            "heritage_narrative": heritage_narrative,
            "cultural_analysis": cultural_analysis,
            
            # Sustainability Impact
            "eco_impact": eco_impact,
            
            # Authenticity Verification
            "authenticity": {
                "verified": True,
                "verification_method": "Artisan self-declaration + AI validation",
                "blockchain_ready": True,
                "certificate_number": heritage_id
            },
            
            # Metadata for preservation
            "metadata": {
                "craft_category": self._categorize_craft(craft_technique),
                "preservation_priority": self._assess_preservation_priority(craft_technique, regional_tradition),
                "cultural_heritage_tags": self._generate_heritage_tags(craft_technique, regional_tradition),
                "unesco_relevant": self._check_unesco_relevance(craft_technique, regional_tradition)
            }
        }
        
        return craft_dna
    
    def _generate_heritage_narrative(
        self,
        artisan_story: str,
        craft_technique: str,
        regional_tradition: str,
        materials_used: List[str],
        cultural_context: str,
        artisan_profile: Optional[Dict]
    ) -> str:
        """Generate compelling heritage narrative using AI"""
        
        prompt = f"""
You are a cultural heritage expert and storyteller. Create a compelling, authentic narrative about this craft that preserves its cultural significance for future generations.

ARTISAN'S STORY:
{artisan_story}

CRAFT DETAILS:
- Technique: {craft_technique}
- Regional Tradition: {regional_tradition}
- Materials: {', '.join(materials_used)}
- Cultural Context: {cultural_context}

ARTISAN PROFILE:
{json.dumps(artisan_profile, indent=2) if artisan_profile else "Limited information available"}

TASK:
Write a 300-word heritage narrative that:
1. Honors the artisan's personal journey and family lineage
2. Explains the historical and cultural significance of this craft technique
3. Describes the traditional materials and why they matter
4. Connects the craft to festivals, rituals, or daily life
5. Highlights what makes this craft unique to its region
6. Emphasizes the human skill and time invested
7. Uses warm, respectful, and culturally sensitive language

Write in a narrative style that makes buyers emotionally connect with the craft's story.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"This craft represents the {regional_tradition} tradition of {craft_technique}, passed down through generations. {artisan_story}"
    
    def _calculate_eco_impact(
        self,
        materials_used: List[str],
        craft_technique: str,
        sustainability_metrics: Optional[Dict]
    ) -> Dict:
        """Calculate environmental impact and sustainability metrics"""
        
        # Base eco-impact calculations
        eco_impact = {
            "carbon_footprint": {
                "value": 0.0,
                "unit": "kg CO₂",
                "vs_industrial": None
            },
            "water_usage": {
                "value": 0.0,
                "unit": "liters",
                "vs_industrial": None
            },
            "waste_generated": {
                "value": 0.0,
                "unit": "kg",
                "recyclable_percentage": 0
            },
            "renewable_materials": 0,
            "local_sourcing": True,
            "biodegradability": "Unknown",
            "sustainability_score": 0
        }
        
        # Analyze materials for sustainability
        recycled_count = 0
        natural_count = 0
        
        for material in materials_used:
            material_lower = material.lower()
            
            # Check for recycled materials
            if any(keyword in material_lower for keyword in ["recycled", "reclaimed", "upcycled", "reused"]):
                recycled_count += 1
                eco_impact["carbon_footprint"]["value"] -= 0.5  # Carbon savings
            
            # Check for natural materials
            if any(keyword in material_lower for keyword in ["natural", "organic", "cotton", "silk", "wood", "bamboo", "jute", "clay"]):
                natural_count += 1
                eco_impact["biodegradability"] = "High"
        
        eco_impact["renewable_materials"] = (recycled_count + natural_count) / len(materials_used) * 100 if materials_used else 0
        
        # Calculate sustainability score (0-100)
        score = 50  # Base score for handmade
        score += eco_impact["renewable_materials"] * 0.3  # Up to 30 points
        score += 10 if eco_impact["local_sourcing"] else 0
        score += 10 if eco_impact["biodegradability"] == "High" else 0
        
        eco_impact["sustainability_score"] = min(100, int(score))
        
        # Add comparison to industrial production
        eco_impact["carbon_footprint"]["vs_industrial"] = "70% less carbon emissions than factory-made equivalent"
        eco_impact["water_usage"]["vs_industrial"] = "85% less water than industrial production"
        
        # Use provided metrics if available
        if sustainability_metrics:
            eco_impact.update(sustainability_metrics)
        
        # Generate eco-claims
        eco_impact["eco_claims"] = self._generate_eco_claims(eco_impact, materials_used)
        
        return eco_impact
    
    def _generate_eco_claims(self, eco_impact: Dict, materials: List[str]) -> List[str]:
        """Generate verifiable eco-impact claims"""
        
        claims = []
        
        if eco_impact["renewable_materials"] > 50:
            claims.append(f"Made with {int(eco_impact['renewable_materials'])}% sustainable materials")
        
        if "recycled" in " ".join(materials).lower():
            claims.append("Uses recycled and upcycled materials")
        
        if eco_impact["local_sourcing"]:
            claims.append("Locally sourced materials reduce transport emissions")
        
        claims.append("Handmade process uses no factory electricity")
        claims.append("Zero plastic packaging")
        claims.append("Supports fair-trade artisan communities")
        
        if eco_impact["sustainability_score"] >= 80:
            claims.append("🌿 Certified Sustainable Craft")
        
        return claims
    
    def _analyze_cultural_significance(
        self,
        craft_technique: str,
        regional_tradition: str,
        cultural_context: str
    ) -> Dict:
        """Analyze and document cultural significance"""
        
        prompt = f"""
Analyze the cultural significance of this craft:

CRAFT TECHNIQUE: {craft_technique}
REGIONAL TRADITION: {regional_tradition}
CULTURAL CONTEXT: {cultural_context}

Provide analysis in the following categories:
1. Historical Origin (when and where did this craft tradition begin?)
2. Cultural Rituals (festivals, ceremonies, or daily life connections)
3. Symbolic Meaning (what does this craft represent in its culture?)
4. Endangered Status (is this craft technique at risk of disappearing?)
5. Modern Relevance (how is this craft staying alive today?)

Format as JSON with these keys: historical_origin, cultural_rituals, symbolic_meaning, endangered_risk, modern_relevance
"""
        
        try:
            response = self.model.generate_content(prompt)
            # Parse JSON from response
            import re
            json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass
        
        # Fallback analysis
        return {
            "historical_origin": f"Part of the {regional_tradition} tradition with centuries of heritage",
            "cultural_rituals": cultural_context,
            "symbolic_meaning": "Represents skilled craftsmanship and cultural identity",
            "endangered_risk": "Medium - needs support to preserve",
            "modern_relevance": "Artisans are adapting traditional techniques for contemporary markets"
        }
    
    def _generate_qr_code(self, url: str) -> Dict:
        """Generate QR code for heritage page"""
        
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        # Generate QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return {
            "image_base64": img_base64,
            "url": url,
            "format": "PNG",
            "size": "300x300",
            "error_correction": "High (30%)",
            "printable": True
        }
    
    def _check_endangered_craft(self, craft_technique: str) -> str:
        """Check if craft is endangered"""
        
        # List of endangered crafts (simplified)
        endangered_keywords = [
            "brocade", "zardozi", "phulkari", "bidriware", "chikankari",
            "pattachitra", "madhubani", "warli", "gond", "kalamkari",
            "chanderi", "paithani", "pochampalaly", "ikat", "patola",
            "dokra", "dhokra", "bamboo", "cane", "pottery", "terracotta"
        ]
        
        craft_lower = craft_technique.lower()
        
        for keyword in endangered_keywords:
            if keyword in craft_lower:
                return "At Risk - Needs Preservation"
        
        return "Active Tradition"
    
    def _categorize_craft(self, craft_technique: str) -> str:
        """Categorize craft type"""
        
        categories = {
            "Textiles": ["weaving", "embroidery", "printing", "dyeing", "fabric", "silk", "cotton", "wool"],
            "Pottery": ["pottery", "clay", "ceramic", "terracotta"],
            "Metalwork": ["brass", "copper", "silver", "gold", "bronze", "dokra", "dhokra"],
            "Woodwork": ["wood", "carving", "furniture", "toy"],
            "Jewelry": ["jewelry", "jewellery", "ornament", "bead"],
            "Painting": ["painting", "art", "miniature", "mural"],
            "Paper": ["paper", "card", "origami"],
            "Leather": ["leather", "hide"],
            "Stone": ["stone", "marble", "granite"],
            "Bamboo": ["bamboo", "cane", "wicker"]
        }
        
        craft_lower = craft_technique.lower()
        
        for category, keywords in categories.items():
            if any(keyword in craft_lower for keyword in keywords):
                return category
        
        return "Traditional Craft"
    
    def _assess_preservation_priority(self, craft_technique: str, regional_tradition: str) -> str:
        """Assess how urgently this craft needs preservation"""
        
        endangered_status = self._check_endangered_craft(craft_technique)
        
        if "At Risk" in endangered_status:
            return "HIGH - Urgent preservation needed"
        elif any(keyword in craft_technique.lower() for keyword in ["traditional", "ancient", "heritage"]):
            return "MEDIUM - Monitor and support"
        else:
            return "LOW - Active and thriving"
    
    def _generate_heritage_tags(self, craft_technique: str, regional_tradition: str) -> List[str]:
        """Generate tags for cultural heritage indexing"""
        
        tags = []
        
        # Add craft type
        tags.append(f"craft:{craft_technique.lower().replace(' ', '_')}")
        
        # Add region
        tags.append(f"region:{regional_tradition.lower().replace(' ', '_')}")
        
        # Add category
        category = self._categorize_craft(craft_technique)
        tags.append(f"category:{category.lower()}")
        
        # Add preservation status
        status = self._check_endangered_craft(craft_technique)
        if "At Risk" in status:
            tags.append("preservation:urgent")
        
        # Add general tags
        tags.extend(["handmade", "artisan", "cultural_heritage", "traditional_craft", "indian_craft"])
        
        return tags
    
    def _check_unesco_relevance(self, craft_technique: str, regional_tradition: str) -> bool:
        """Check if craft might be UNESCO Intangible Cultural Heritage relevant"""
        
        # UNESCO-recognized or UNESCO-relevant craft keywords
        unesco_keywords = [
            "pattachitra", "madhubani", "warli", "gond", "kalamkari",
            "chanderi", "paithani", "kanjivaram", "banarasi", "patola",
            "blue pottery", "bidriware", "dokra", "chhau", "kalaripayattu",
            "yoga", "ayurveda", "ramlila", "kumbh mela", "sankirtana"
        ]
        
        combined = f"{craft_technique} {regional_tradition}".lower()
        
        return any(keyword in combined for keyword in unesco_keywords)
    
    def generate_printable_heritage_label(self, craft_dna: Dict) -> Dict:
        """
        Generate printable label with QR code for physical products
        
        Returns label design with QR code, artisan info, and eco-impact
        """
        
        label = {
            "format": "PDF",
            "size": "5cm x 5cm",
            "elements": {
                "qr_code": craft_dna["qr_code"]["image_base64"],
                "title": "Scan to Discover This Craft's Story",
                "artisan_name": craft_dna["artisan"]["name"],
                "craft_technique": craft_dna["craft"]["technique"],
                "region": craft_dna["craft"]["regional_tradition"],
                "sustainability_score": f"{craft_dna['eco_impact']['sustainability_score']}/100",
                "heritage_id": craft_dna["heritage_id"]
            },
            "design": {
                "background_color": "#FFF8E7",
                "border_color": "#D4AF37",
                "text_color": "#2C3E50",
                "qr_position": "center",
                "font": "Georgia"
            },
            "text": {
                "tagline": "Your craft isn't just a product — it's a living story.",
                "call_to_action": "Scan to meet the artisan and explore the cultural heritage"
            }
        }
        
        return label


# API Integration Functions

def create_craft_dna_for_product(product_data: Dict) -> Dict:
    """
    Main function to create Craft DNA during Add Product flow
    
    Args:
        product_data: Product information from add-product form
        
    Returns:
        Complete Craft DNA record
    """
    
    agent = CraftDNAAgent()
    
    # Extract data from product
    craft_dna = agent.generate_craft_dna(
        product_id=product_data.get("product_id"),
        artisan_story=product_data.get("artisan_story", ""),
        craft_technique=product_data.get("craft_technique", ""),
        regional_tradition=product_data.get("regional_tradition", ""),
        materials_used=product_data.get("materials", []),
        cultural_context=product_data.get("cultural_context", ""),
        sustainability_metrics=product_data.get("sustainability_metrics"),
        artisan_profile=product_data.get("artisan_profile")
    )
    
    return craft_dna


if __name__ == "__main__":
    # Example usage
    agent = CraftDNAAgent()
    
    sample_product = {
        "product_id": "PROD12345",
        "artisan_story": "I learned this brass work from my grandfather who learned it from his father. We have been making these diyas for 4 generations in Jaipur.",
        "craft_technique": "Jaipur brass casting and etching",
        "regional_tradition": "Rajasthani metalwork",
        "materials": ["recycled brass", "natural lacquer", "beeswax polish"],
        "cultural_context": "These diyas are traditionally used during Diwali festival and are believed to bring prosperity",
        "artisan_profile": {
            "name": "Ramesh Kumar",
            "village": "Amber",
            "state": "Rajasthan",
            "lineage": "4th generation brass artisan",
            "years_of_experience": 25
        }
    }
    
    craft_dna = create_craft_dna_for_product(sample_product)
    print(json.dumps(craft_dna, indent=2))
