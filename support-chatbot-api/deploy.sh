#!/bin/bash

# KalpanaAI Support Chatbot - Cloud Run Deployment Script

# Configuration
PROJECT_ID="nodal-fountain-470717-j1"
SERVICE_NAME="support-chatbot-api"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "🚀 Deploying KalpanaAI Support Chatbot to Cloud Run..."

# Build the Docker image
echo "📦 Building Docker image..."
gcloud builds submit --tag ${IMAGE_NAME} --project ${PROJECT_ID}

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully!"

# Deploy to Cloud Run
echo "🌐 Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --set-env-vars GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=${REGION} \
    --project ${PROJECT_ID}

if [ $? -ne 0 ]; then
    echo "❌ Deployment failed!"
    exit 1
fi

echo "✅ Deployment successful!"

# Get the service URL
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} \
    --platform managed \
    --region ${REGION} \
    --format 'value(status.url)' \
    --project ${PROJECT_ID})

echo ""
echo "🎉 Support Chatbot API is live!"
echo "📍 URL: ${SERVICE_URL}"
echo ""
echo "Test endpoints:"
echo "  Health: ${SERVICE_URL}/health"
echo "  Chat: ${SERVICE_URL}/chat"
echo "  Quick Help: ${SERVICE_URL}/quick-help"
echo ""
echo "📝 Example curl command:"
echo "curl -X POST ${SERVICE_URL}/chat \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"message\": \"How do I create a product?\", \"language\": \"en-US\"}'"
