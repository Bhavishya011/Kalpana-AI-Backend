#!/bin/bash

# Deploy multilingual translation system

echo "🌐 Deploying Multilingual Translation System..."
echo ""

# Step 1: Deploy Backend API with translation endpoint
echo "📦 Step 1: Building and deploying backend API..."
cd "$(dirname "$0")"

# Build Docker image
echo "🔨 Building Docker image..."
gcloud builds submit --tag gcr.io/nodal-fountain-470717-j1/kalpana-ai-api

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy kalpana-ai-api \
    --image gcr.io/nodal-fountain-470717-j1/kalpana-ai-api \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --min-instances 1 \
    --port 8080 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1,PORT=8080

if [ $? -ne 0 ]; then
    echo "❌ Cloud Run deployment failed!"
    exit 1
fi

echo ""
echo "✅ Backend API deployed successfully!"
echo ""

# Step 2: Deploy Frontend (if needed)
echo "📦 Step 2: Frontend deployment info..."
echo "The frontend with translation hooks has been updated."
echo "Please rebuild and deploy your Next.js frontend:"
echo ""
echo "  cd Kalpana-AI"
echo "  npm run build"
echo "  # Deploy to your hosting platform"
echo ""

echo "🎉 Deployment complete!"
echo ""
echo "✨ Features added:"
echo "  - Dynamic translation using Gemini AI"
echo "  - Automatic API response translation"
echo "  - Support for all 8 Indian languages"
echo "  - Client-side translation hooks"
echo ""
echo "📝 Usage:"
echo "  1. Change language in the UI"
echo "  2. All content (including API responses) will be automatically translated"
echo "  3. Translations are done on-the-fly using AI"
