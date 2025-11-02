#!/bin/bash
# Pre-deployment checklist and setup

echo "🔍 Pre-Deployment Checklist for Cloud Run"
echo "=========================================="
echo ""

# Check gcloud CLI
echo "1️⃣ Checking Google Cloud SDK..."
if command -v gcloud &> /dev/null; then
    echo "   ✅ gcloud CLI installed"
    gcloud --version | head -1
else
    echo "   ❌ gcloud CLI not installed"
    echo "   📥 Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check authentication
echo ""
echo "2️⃣ Checking authentication..."
ACCOUNT=$(gcloud config get-value account 2>/dev/null)
if [ -n "$ACCOUNT" ]; then
    echo "   ✅ Authenticated as: $ACCOUNT"
else
    echo "   ❌ Not authenticated"
    echo "   🔐 Run: gcloud auth login"
    exit 1
fi

# Check project
echo ""
echo "3️⃣ Checking project configuration..."
PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$PROJECT" = "nodal-fountain-470717-j1" ]; then
    echo "   ✅ Project set correctly: $PROJECT"
else
    echo "   ⚠️  Current project: $PROJECT"
    echo "   🔧 Setting correct project..."
    gcloud config set project nodal-fountain-470717-j1
fi

# Check Docker
echo ""
echo "4️⃣ Checking Docker..."
if command -v docker &> /dev/null; then
    echo "   ✅ Docker installed"
    docker --version
else
    echo "   ⚠️  Docker not installed (required for local testing only)"
    echo "   📥 Install from: https://docs.docker.com/get-docker/"
fi

# Check required files
echo ""
echo "5️⃣ Checking required files..."
cd api
if [ -f "Dockerfile" ]; then
    echo "   ✅ Dockerfile exists"
else
    echo "   ❌ Dockerfile missing"
    exit 1
fi

if [ -f "requirements.txt" ]; then
    echo "   ✅ requirements.txt exists"
else
    echo "   ❌ requirements.txt missing"
    exit 1
fi

if [ -f "main2.0.py" ]; then
    echo "   ✅ main2.0.py exists"
else
    echo "   ❌ main2.0.py missing"
    exit 1
fi

# Check agents
echo ""
echo "6️⃣ Checking agent modules..."
if [ -d "../Agents/agents" ]; then
    echo "   ✅ Agents directory exists"
    AGENT_COUNT=$(find ../Agents/agents -name "*_agent.py" | wc -l)
    echo "   📦 Found $AGENT_COUNT agent modules"
else
    echo "   ❌ Agents directory missing"
    exit 1
fi

# Enable APIs
echo ""
echo "7️⃣ Checking Google Cloud APIs..."
echo "   🔧 Enabling required APIs (this may take a minute)..."
gcloud services enable run.googleapis.com --quiet
gcloud services enable cloudscheduler.googleapis.com --quiet
gcloud services enable cloudbuild.googleapis.com --quiet
gcloud services enable firestore.googleapis.com --quiet
gcloud services enable aiplatform.googleapis.com --quiet
gcloud services enable storage.googleapis.com --quiet
echo "   ✅ All required APIs enabled"

# Check IAM permissions
echo ""
echo "8️⃣ Checking IAM permissions..."
PERMISSIONS=$(gcloud projects get-iam-policy nodal-fountain-470717-j1 --flatten="bindings[].members" --filter="bindings.members:user:$ACCOUNT" --format="value(bindings.role)" 2>/dev/null | wc -l)
if [ "$PERMISSIONS" -gt 0 ]; then
    echo "   ✅ You have permissions on this project"
else
    echo "   ⚠️  Warning: Could not verify permissions"
fi

echo ""
echo "=========================================="
echo "✅ Pre-deployment checks complete!"
echo "=========================================="
echo ""
echo "📋 Next Steps:"
echo "1. Review your configuration in Dockerfile and requirements.txt"
echo "2. Run deployment script:"
echo "   ./deploy-cloud-run.sh"
echo ""
echo "💡 Or deploy manually:"
echo "   cd api"
echo "   gcloud builds submit --tag gcr.io/nodal-fountain-470717-j1/kalpana-ai-api ."
echo "   gcloud run deploy kalpana-ai-api --image gcr.io/nodal-fountain-470717-j1/kalpana-ai-api --region us-central1"
echo ""
