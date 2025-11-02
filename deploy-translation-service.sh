#!/bin/bash

# Deploy Translation Service (Separate from Main API)

echo "🌐 Deploying KalpanaAI Translation Service..."
echo "This service is separate from the main product pipeline"
echo ""

cd "$(dirname "$0")"

# Step 1: Build Docker image
echo "🔨 Building Translation Service Docker image..."
gcloud builds submit \
    --tag gcr.io/nodal-fountain-470717-j1/kalpana-translation \
    --dockerfile Dockerfile.translation \
    .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo ""
echo "✅ Docker image built successfully!"
echo ""

# Step 2: Deploy to Cloud Run (separate service)
echo "🚀 Deploying Translation Service to Cloud Run..."
gcloud run deploy kalpana-translation \
    --image gcr.io/nodal-fountain-470717-j1/kalpana-translation \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 60 \
    --max-instances 5 \
    --min-instances 0 \
    --port 8081 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1,PORT=8081

if [ $? -ne 0 ]; then
    echo "❌ Cloud Run deployment failed!"
    exit 1
fi

echo ""
echo "✅ Translation Service deployed successfully!"
echo ""
echo "📝 Service Details:"
echo "  - Service Name: kalpana-translation"
echo "  - Separate from: kalpana-ai-api (main product pipeline)"
echo "  - Port: 8081"
echo "  - Memory: 1Gi (lighter than main API)"
echo "  - Endpoint: https://kalpana-translation-508329185712.us-central1.run.app"
echo ""
echo "🧪 Test the service:"
echo '  curl -X POST https://kalpana-translation-508329185712.us-central1.run.app/translate \\'
echo '    -H "Content-Type: application/json" \\'
echo '    -d '"'"'{"text": "Hello", "targetLocale": "hi-IN"}'"'"
echo ""
echo "✨ Translation service is now live and independent!"
