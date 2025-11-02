# Google Trends Market Intelligence Integration

## 📊 Overview

The KalpanaAI pricing system now integrates **Google Trends API** to provide **real-time market intelligence** for dynamic pricing. This system tracks trending crafts, seasonal demand, and regional interest to automatically adjust pricing multipliers.

---

## 🚀 Features

### 1. **Real-Time Trend Tracking**
- Monitors search interest for 8 craft categories
- Updates trend scores (0-100) based on recent search volume
- Automatically adjusts price ranges based on demand

### 2. **Seasonal Intelligence**
- Detects active festivals (Diwali, Holi, Wedding Season, etc.)
- Applies seasonal multipliers (1.0x - 1.3x)
- Updates weekly to capture current trends

### 3. **Regional Analysis**
- Tracks regional craft interest across India
- Provides region-specific demand scores
- Enhances pricing for high-demand regions

### 4. **Trending Crafts Detection**
- Identifies top 5 trending craft categories
- Helps artisans capitalize on hot markets
- Updated weekly from Google Trends data

---

## 🛠️ Technical Implementation

### **Architecture**

```
┌─────────────────────────────────────────────────────────┐
│                    Pricing Agent                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Heritage (30%) + Complexity (40%) + Market (30%) │  │
│  └───────────────────────────────────────────────────┘  │
│                           ↓                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Market Intelligence Module                │  │
│  │  - Google Trends API (pytrends)                   │  │
│  │  - 8 Craft Categories                             │  │
│  │  - Seasonal Detection                             │  │
│  │  - Regional Analysis                              │  │
│  └───────────────────────────────────────────────────┘  │
│                           ↓                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │          Market Cache (market_cache.json)         │  │
│  │  - Category Trends                                │  │
│  │  - Price Ranges                                   │  │
│  │  - Multipliers                                    │  │
│  │  - Last Updated: Weekly                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### **Files Created**

1. **`agents/market_intelligence.py`**
   - Main market intelligence module
   - Google Trends API integration
   - Trend scoring and analysis

2. **`update_market_trends.py`**
   - Background script for weekly updates
   - Can be run manually or scheduled

3. **`market_cache.json`** (auto-generated)
   - Cached market data
   - 7-day expiry
   - Contains all trend scores and multipliers

---

## 📈 How It Works

### **Step 1: Weekly Trend Update**

```bash
python update_market_trends.py
```

This script:
1. Fetches search interest for each craft category
2. Calculates trend scores (0-100)
3. Determines trend direction (rising/falling/stable)
4. Adjusts price ranges based on demand
5. Detects seasonal trends
6. Saves to `market_cache.json`

### **Step 2: Dynamic Pricing**

When a product is priced:

```python
# Example: Pottery with trend score of 80 (hot)
base_score = 5.0  # Regional base
trend_multiplier = 1.2  # Hot category (score > 80)
seasonal_multiplier = 1.3  # Diwali season

final_demand = base_score * trend_multiplier * seasonal_multiplier
# = 5.0 × 1.2 × 1.3 = 7.8/10
```

### **Step 3: Market Validation**

After AI pricing:

```python
# AI suggests ₹600 for pottery
# Market range: ₹100-400
# Result: Adjusted to ₹400 (market ceiling)
```

---

## 🎯 Trend Score Multipliers

| Trend Score | Category Status | Multiplier |
|-------------|----------------|------------|
| 80-100 | 🔥 Very Hot | 1.2x |
| 65-79 | 📈 Hot | 1.15x |
| 50-64 | ☀️ Warm | 1.05x |
| 35-49 | ➡️ Stable | 1.0x |
| 20-34 | 📉 Cool | 0.95x |
| 0-19 | ❄️ Cold | 0.9x |

---

## 🎉 Seasonal Multipliers

| Keyword | Score Range | Multiplier |
|---------|-------------|------------|
| Diwali Gifts | 70-100 | 1.3x |
| Wedding Gifts | 50-70 | 1.2x |
| Festival Decorations | 30-50 | 1.1x |
| Other | <30 | 1.0x |

---

## 🌍 Regional Base Scores

| Region | Base Score |
|--------|-----------|
| Rajasthan | 9.0/10 |
| Gujarat | 8.5/10 |
| Madhya Pradesh | 8.0/10 |
| West Bengal | 8.0/10 |
| Uttar Pradesh | 8.0/10 |
| Kerala | 7.5/10 |
| Karnataka | 7.5/10 |
| Tamil Nadu | 7.5/10 |
| Odisha | 7.0/10 |

---

## 📡 API Endpoints

### **1. Get Market Trends**
```http
GET /api/market-trends
```

**Response:**
```json
{
  "success": true,
  "last_updated": "2025-10-26T15:30:00",
  "cache_age_days": 0,
  "categories": {
    "pottery": {
      "price_range": {"min": 100, "max": 400, "avg": 200},
      "demand": "medium",
      "trend_score": 75,
      "trend_direction": "rising",
      "multiplier": 1.15
    }
  },
  "trending_crafts": [
    {"category": "jewelry", "score": 85},
    {"category": "embroidery", "score": 78}
  ],
  "seasonal_trends": {
    "diwali gifts": {"score": 92, "multiplier": 1.3, "active": true}
  },
  "active_seasonal_multiplier": 1.3
}
```

### **2. Update Market Trends (Manual)**
```http
POST /api/update-market-trends
```

**Response:**
```json
{
  "success": true,
  "message": "Market trends updated successfully",
  "last_updated": "2025-10-26T16:00:00",
  "trending_crafts": [...],
  "categories": {...}
}
```

---

## ⚙️ Setup & Usage

### **Installation**

```bash
# Install pytrends library
pip install pytrends
```

### **Manual Update**

```bash
# Run update script
cd Agents
python update_market_trends.py
```

### **Schedule Weekly Updates (Windows)**

```powershell
# Create scheduled task (runs every Sunday at 2 AM)
schtasks /create /tn "Update Market Trends" `
  /tr "python C:\path\to\Agents\update_market_trends.py" `
  /sc weekly /d SUN /st 02:00
```

### **Schedule Weekly Updates (Linux/Mac)**

```bash
# Add to crontab (runs every Sunday at 2 AM)
0 2 * * 0 cd /path/to/Agents && python update_market_trends.py
```

---

## 🧪 Testing

### **Test Market Intelligence**
```bash
cd Agents
python test_market_intelligence.py
```

### **Test Pricing with Trends**
```bash
cd Agents
python test_quick.py
```

### **Manual Trend Fetch (Test)**
```python
from agents.market_intelligence import MarketIntelligence

mi = MarketIntelligence()

# Fetch pottery trends
pottery_trends = mi.fetch_craft_trends('pottery')
print(pottery_trends)
# Output: {'trend_score': 75, 'trend_direction': 'rising', ...}

# Get seasonal trends
seasonal = mi.fetch_seasonal_trends()
print(seasonal)
# Output: {'diwali gifts': {'score': 92, 'multiplier': 1.3, ...}}
```

---

## 📊 Example: Complete Pricing Flow

```python
# Input
product = "Blue pottery bowl with peacock design"
material_cost = 100.0
region = "Rajasthan"

# Step 1: Analyze components
heritage_score = 7.5  # Traditional technique
complexity_score = 6.0  # Hand-painted
base_market_score = 9.0  # Rajasthan region

# Step 2: Apply Google Trends multipliers
trend_score = 75  # Pottery trending
trend_multiplier = 1.15  # Hot category
seasonal_multiplier = 1.3  # Diwali season

market_score = base_market_score * trend_multiplier * seasonal_multiplier
# = 9.0 × 1.15 × 1.3 = 13.455 → capped at 10.0

# Step 3: Calculate weighted score
weighted = (7.5 × 0.3) + (6.0 × 0.4) + (10.0 × 0.3)
# = 2.25 + 2.4 + 3.0 = 7.65/10

# Step 4: Calculate markup
base_markup = 250
complexity_bonus = 6.0 × 25 = 150
heritage_bonus = 7.5 × 20 = 150
market_bonus = 10.0 × 15 = 150

total_markup = (250 + 150 + 150 + 150) × (1 + 7.65/20)
# = 700 × 1.3825 = ₹967.75

# Step 5: Market validation
# AI: ₹967.75
# Pottery range: ₹100-400
# Adjusted: ₹400 (market ceiling)

# Final Price
suggested_markup = ₹400
material_cost = ₹100
total_price = ₹500
```

---

## 🎯 Benefits

| Feature | Before | After (with Google Trends) |
|---------|--------|---------------------------|
| **Trend Data** | Static hardcoded | Real-time from Google |
| **Seasonal Awareness** | Manual calendar | Active festival detection |
| **Price Adjustment** | Fixed ranges | Dynamic based on demand |
| **Regional Insights** | Assumed values | Measured search interest |
| **Trending Alerts** | None | Top 5 hot categories |
| **Update Frequency** | Never | Weekly auto-update |
| **Market Validation** | Basic ranges | Trend-adjusted ceilings |

---

## 🔧 Configuration

### **Market Cache Location**
```python
# Default: Agents/market_cache.json
mi = MarketIntelligence(cache_file="market_cache.json")
```

### **Cache Expiry**
```python
# Default: 7 days
should_update = mi.should_update_cache()
```

### **Craft Keywords**
Edit `market_intelligence.py`:
```python
self.craft_keywords = {
    'pottery': ['indian pottery', 'handmade pottery', 'ceramic pottery india'],
    # Add more categories...
}
```

---

## 📝 Notes

1. **Rate Limiting**: Google Trends API has rate limits. The script includes 2-second delays between requests.

2. **Data Accuracy**: Trend scores are relative, not absolute. They show interest trends, not actual sales data.

3. **Cache Management**: Market cache auto-updates if >7 days old. Manual update available via API or script.

4. **Fallback**: If Google Trends fails, system falls back to static multipliers (1.0x).

5. **Privacy**: No personal data collected. Only aggregate search trends used.

---

## 🚨 Troubleshooting

### **Issue: "Google Trends not available"**
```bash
# Install pytrends
pip install pytrends
```

### **Issue: "Rate limit exceeded"**
```python
# Increase delays in market_intelligence.py
time.sleep(5)  # Increase from 2 to 5 seconds
```

### **Issue: "Cache not updating"**
```bash
# Manually force update
python update_market_trends.py

# Or via API
curl -X POST http://localhost:8000/api/update-market-trends
```

---

## 📚 Resources

- [PyTrends Documentation](https://github.com/GeneralMills/pytrends)
- [Google Trends](https://trends.google.com/trends/)
- [Market Intelligence Module](agents/market_intelligence.py)
- [Update Script](update_market_trends.py)

---

## ✅ Success Metrics

After implementation:
- ✅ Complexity scores no longer return 0
- ✅ Market validation working with Google Trends
- ✅ Dynamic seasonal multipliers active
- ✅ Trending crafts detected weekly
- ✅ Price ranges auto-adjust based on demand
- ✅ API endpoints available for frontend integration

---

**Last Updated**: October 26, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready
