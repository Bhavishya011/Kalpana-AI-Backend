"""
FastAPI application for Sales Analytics & Inventory Management
Standalone deployment for Sales_analytics module
"""

from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
from pydantic import BaseModel
import uvicorn

from sales_analytics_agent import SalesAnalyticsAgent
from inventory_management_agent import InventoryManagementAgent

# Initialize FastAPI app
app = FastAPI(
    title="KalpanaAI Sales Analytics & Inventory Management API",
    description="AI-powered sales analytics and inventory management for artisan marketplace",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
sales_agent = SalesAnalyticsAgent()
inventory_agent = InventoryManagementAgent()

# Pydantic models for request bodies
class NewProduct(BaseModel):
    name: str
    category: str
    stock_quantity: int
    reorder_point: int
    price: float

class StockUpdate(BaseModel):
    product_name: str
    new_quantity: int

# Health check endpoint
@app.get("/")
async def root():
    return {
        "service": "KalpanaAI Sales Analytics & Inventory Management",
        "status": "running",
        "version": "1.0.0",
        "endpoints": {
            "sales": [
                "/api/analytics/sales-overview",
                "/api/analytics/product/{product_id}",
                "/api/analytics/forecast",
                "/api/analytics/seller/{seller_id}"
            ],
            "inventory": [
                "/api/inventory/status",
                "/api/inventory/restock",
                "/api/inventory/dead-stock",
                "/api/inventory/alerts",
                "/api/inventory/seasonal"
            ]
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sales-analytics-api"}

# ============================================================================
# SALES ANALYTICS ENDPOINTS
# ============================================================================

@app.get("/api/analytics/sales-overview")
async def get_sales_overview(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get comprehensive sales overview for specified period
    
    - **days**: Number of days to analyze (1-365, default: 30)
    
    Returns:
    - Total GMV, orders, AOV
    - Growth rates
    - Top products and regions
    - Daily sales breakdown
    - AI-generated insights
    """
    try:
        overview = sales_agent.get_sales_overview(days=days)
        return overview
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting sales overview: {str(e)}")

@app.get("/api/analytics/product/{product_id}")
async def get_product_performance(
    product_id: str,
    days: int = Query(90, ge=1, le=365, description="Number of days to analyze")
):
    """
    Analyze individual product performance
    
    - **product_id**: Product identifier
    - **days**: Analysis period in days (1-365, default: 90)
    
    Returns:
    - Revenue, units sold, conversion rate
    - Daily sales trend
    - Stock status
    - AI recommendations
    """
    try:
        performance = sales_agent.get_product_performance(product_id, days=days)
        
        if 'error' in performance:
            raise HTTPException(status_code=404, detail=performance['error'])
        
        return performance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing product: {str(e)}")

@app.get("/api/analytics/forecast")
async def get_revenue_forecast(
    days_ahead: int = Query(30, ge=1, le=90, description="Number of days to forecast")
):
    """
    Predict revenue for upcoming period
    
    - **days_ahead**: Number of days to forecast (1-90, default: 30)
    
    Returns:
    - Predicted GMV and daily average
    - Confidence level (LOW/MEDIUM/HIGH)
    - Growth rate trend
    - AI analysis and recommendations
    """
    try:
        forecast = sales_agent.get_revenue_forecast(days_ahead=days_ahead)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating forecast: {str(e)}")

@app.get("/api/analytics/seller/{seller_id}")
async def get_seller_performance(
    seller_id: str,
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Analyze individual seller/artisan performance
    
    - **seller_id**: Seller/artisan identifier
    - **days**: Analysis period in days (1-365, default: 30)
    
    Returns:
    - Total revenue, orders, AOV
    - Active products count
    - Top performing products
    - Seller rating
    """
    try:
        performance = sales_agent.get_seller_performance(seller_id, days=days)
        
        if 'error' in performance:
            raise HTTPException(status_code=404, detail=performance['error'])
        
        return performance
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing seller: {str(e)}")

# ============================================================================
# INVENTORY MANAGEMENT ENDPOINTS
# ============================================================================

@app.get("/api/inventory/status")
async def get_inventory_status(
    seller_id: Optional[str] = Query(None, description="Filter by seller ID")
):
    """
    Get comprehensive inventory status report
    
    - **seller_id**: Optional - Filter by specific seller
    
    Returns:
    - Total products and stock value
    - Stock alerts (out of stock, critical, low, overstock)
    - Category breakdown
    - AI recommendations
    """
    try:
        status = inventory_agent.get_inventory_status(seller_id=seller_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting inventory status: {str(e)}")

@app.get("/api/inventory/restock")
async def get_restock_recommendations(
    seller_id: Optional[str] = Query(None, description="Filter by seller ID"),
    priority_only: bool = Query(True, description="Return only priority restocks")
):
    """
    Get restock recommendations with quantities and timing
    
    - **seller_id**: Optional - Filter by specific seller
    - **priority_only**: Only return urgent restocks (default: true)
    
    Returns:
    - Prioritized restock list
    - Recommended quantities (30 days of stock)
    - Urgency levels (CRITICAL/HIGH/MEDIUM)
    - Estimated costs and potential revenue
    """
    try:
        recommendations = inventory_agent.get_restock_recommendations(
            seller_id=seller_id,
            priority_only=priority_only
        )
        return recommendations
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting restock recommendations: {str(e)}")

@app.get("/api/inventory/dead-stock")
async def get_dead_stock(
    seller_id: Optional[str] = Query(None, description="Filter by seller ID"),
    days: int = Query(90, ge=30, le=365, description="Analysis period in days")
):
    """
    Identify products with no or very low sales (dead stock)
    
    - **seller_id**: Optional - Filter by specific seller
    - **days**: Period to analyze (30-365 days, default: 90)
    
    Returns:
    - Dead stock items (0 sales)
    - Slow-moving items (< 0.1 units/day)
    - Total dead stock value
    - AI liquidation strategies
    """
    try:
        dead_stock = inventory_agent.identify_dead_stock(seller_id=seller_id, days=days)
        return dead_stock
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing dead stock: {str(e)}")

@app.get("/api/inventory/alerts")
async def get_inventory_alerts(
    seller_id: Optional[str] = Query(None, description="Filter by seller ID")
):
    """
    Get real-time inventory alerts for urgent actions
    
    - **seller_id**: Optional - Filter by specific seller
    
    Returns:
    - Categorized alerts (CRITICAL/HIGH/MEDIUM/INFO)
    - Out of stock products
    - Critical low stock (< 7 days remaining)
    - Low stock (< 14 days remaining)
    - Overstock items
    """
    try:
        alerts = inventory_agent.get_inventory_alerts(seller_id=seller_id)
        return alerts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting inventory alerts: {str(e)}")

@app.get("/api/inventory/seasonal")
async def get_seasonal_planning(
    category: Optional[str] = Query(None, description="Filter by product category")
):
    """
    Generate seasonal inventory planning recommendations
    
    - **category**: Optional - Focus on specific product category
    
    Returns:
    - Current and upcoming season
    - Seasonal trends by category
    - Festival and event planning (Diwali, Holi, weddings)
    - AI recommendations for stock preparation
    """
    try:
        planning = inventory_agent.get_seasonal_planning(category=category)
        return planning
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating seasonal planning: {str(e)}")

@app.post("/api/inventory/add-product")
async def add_product(product: NewProduct):
    """
    Add a new product to inventory
    
    Request body:
    - **name**: Product name
    - **category**: Product category
    - **stock_quantity**: Initial stock quantity
    - **reorder_point**: Minimum stock level before reorder alert
    - **price**: Product price in ₹
    
    Returns:
    - Success message with product details
    """
    try:
        # Add product to Firestore
        from google.cloud import firestore
        db = firestore.Client()
        
        product_data = {
            "name": product.name,
            "category": product.category,
            "stock_quantity": product.stock_quantity,
            "reorder_point": product.reorder_point,
            "price": product.price,
            "created_at": firestore.SERVER_TIMESTAMP,
            "last_updated": firestore.SERVER_TIMESTAMP,
        }
        
        # Add to products collection
        doc_ref = db.collection("products").add(product_data)
        
        return {
            "success": True,
            "message": f"Product '{product.name}' added successfully",
            "product_id": doc_ref[1].id,
            "product": product_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding product: {str(e)}")

@app.post("/api/inventory/update-stock")
async def update_stock(update: StockUpdate):
    """
    Update stock quantity for an existing product
    
    Request body:
    - **product_name**: Name of the product to update
    - **new_quantity**: New stock quantity
    
    Returns:
    - Success message with updated quantity
    """
    try:
        from google.cloud import firestore
        db = firestore.Client()
        
        # Find product by name
        products_ref = db.collection("products")
        query = products_ref.where("name", "==", update.product_name).limit(1)
        docs = list(query.stream())
        
        if not docs:
            raise HTTPException(status_code=404, detail=f"Product '{update.product_name}' not found")
        
        # Update stock quantity
        doc_ref = docs[0].reference
        doc_ref.update({
            "stock_quantity": update.new_quantity,
            "last_updated": firestore.SERVER_TIMESTAMP
        })
        
        return {
            "success": True,
            "message": f"Stock updated for '{update.product_name}'",
            "product_name": update.product_name,
            "new_quantity": update.new_quantity
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating stock: {str(e)}")

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
        log_level="info"
    )
