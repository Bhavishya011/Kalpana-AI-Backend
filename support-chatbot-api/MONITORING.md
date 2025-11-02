# Monitoring & Analytics Guide

## Overview

This guide covers monitoring, logging, and analytics for your chatbot API deployed on Google Cloud Run.

---

## 1. Cloud Run Metrics

### Access Metrics Dashboard

```bash
# Open Cloud Run console
gcloud run services describe support-chatbot-api \
  --region us-central1 \
  --format="value(status.url)"
```

Visit: [Google Cloud Console](https://console.cloud.google.com/run)

### Key Metrics to Monitor

| Metric | Description | Threshold |
|--------|-------------|-----------|
| **Request Count** | Total API calls | > 1000/hour = scale up |
| **Request Latency** | Response time | > 3s = investigate |
| **Error Rate** | Failed requests | > 5% = critical |
| **CPU Utilization** | Processing load | > 80% = add resources |
| **Memory Utilization** | RAM usage | > 90% = increase memory |
| **Instance Count** | Active containers | > 8 = check traffic |
| **Billable Time** | Compute costs | Track monthly |

---

## 2. View Logs

### Real-time Logs

```bash
# Stream live logs
gcloud run services logs tail support-chatbot-api \
  --region us-central1
```

### Filter by Severity

```bash
# Errors only
gcloud run services logs read support-chatbot-api \
  --region us-central1 \
  --filter="severity>=ERROR" \
  --limit 50

# Warnings and above
gcloud run services logs read support-chatbot-api \
  --filter="severity>=WARNING"
```

### Filter by Time

```bash
# Last hour
gcloud run services logs read support-chatbot-api \
  --filter="timestamp>=\"2025-01-01T12:00:00Z\""

# Last 24 hours
gcloud run services logs read support-chatbot-api \
  --filter="timestamp>=\"$(date -u -d '24 hours ago' +%Y-%m-%dT%H:%M:%SZ)\""
```

### Filter by Content

```bash
# Find chat errors
gcloud run services logs read support-chatbot-api \
  --filter="textPayload:\"Chat error\""

# Find specific session
gcloud run services logs read support-chatbot-api \
  --filter="textPayload:\"session_1735738800\""
```

---

## 3. Enhanced Logging in Code

### Update main.py with Structured Logging

Add after imports:

```python
import logging
from datetime import datetime
import json

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_chat_event(event_type: str, data: dict):
    """Log chat events in structured format"""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "data": data
    }
    logger.info(json.dumps(log_entry))
```

### Add to /chat endpoint:

```python
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Log incoming request
        log_chat_event("chat_request", {
            "session_id": request.session_id,
            "language": request.language,
            "message_length": len(request.message)
        })
        
        start_time = datetime.utcnow()
        
        # ... existing chat logic ...
        
        # Log successful response
        duration = (datetime.utcnow() - start_time).total_seconds()
        log_chat_event("chat_response", {
            "session_id": session_id,
            "duration_seconds": duration,
            "response_length": len(response_text)
        })
        
        return ChatResponse(...)
        
    except Exception as e:
        # Log error with context
        log_chat_event("chat_error", {
            "session_id": request.session_id,
            "error": str(e),
            "language": request.language
        })
        raise HTTPException(...)
```

---

## 4. Set Up Alerts

### Create Alert Policy

```bash
# Install gcloud alpha components
gcloud components install alpha

# Create alert for high error rate
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID \
  --display-name="Support Chatbot High Error Rate" \
  --condition-display-name="Error rate > 5%" \
  --condition-threshold-value=5 \
  --condition-threshold-duration=300s
```

### Common Alert Policies

1. **High Error Rate Alert**
   - Condition: Error rate > 5%
   - Duration: 5 minutes
   - Action: Email team

2. **High Latency Alert**
   - Condition: P95 latency > 3s
   - Duration: 5 minutes
   - Action: Email + Slack

3. **Cost Alert**
   - Condition: Daily cost > $10
   - Duration: Daily
   - Action: Email billing team

4. **Low Availability Alert**
   - Condition: Uptime < 99%
   - Duration: 1 hour
   - Action: Page on-call engineer

---

## 5. Custom Analytics

### Create Analytics Endpoint

Add to `main.py`:

```python
from collections import defaultdict
from datetime import datetime, timedelta

# Analytics storage (in production, use Redis/Firestore)
analytics_data = {
    "total_requests": 0,
    "total_sessions": 0,
    "requests_by_language": defaultdict(int),
    "requests_by_hour": defaultdict(int),
    "average_response_time": [],
    "quick_help_usage": defaultdict(int),
    "error_count": 0
}

@app.get("/analytics")
async def get_analytics():
    """Get chatbot usage analytics"""
    total_requests = analytics_data["total_requests"]
    
    return {
        "total_requests": total_requests,
        "total_sessions": analytics_data["total_sessions"],
        "active_sessions": len(chat_sessions),
        "requests_by_language": dict(analytics_data["requests_by_language"]),
        "top_languages": sorted(
            analytics_data["requests_by_language"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5],
        "average_response_time": (
            sum(analytics_data["average_response_time"]) / 
            len(analytics_data["average_response_time"])
        ) if analytics_data["average_response_time"] else 0,
        "error_rate": (
            analytics_data["error_count"] / total_requests * 100
        ) if total_requests > 0 else 0,
        "quick_help_usage": dict(analytics_data["quick_help_usage"])
    }

# Update chat endpoint to track analytics
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    analytics_data["total_requests"] += 1
    analytics_data["requests_by_language"][request.language] += 1
    
    hour_key = datetime.utcnow().strftime("%Y-%m-%d %H:00")
    analytics_data["requests_by_hour"][hour_key] += 1
    
    start_time = datetime.utcnow()
    
    try:
        # ... existing logic ...
        
        duration = (datetime.utcnow() - start_time).total_seconds()
        analytics_data["average_response_time"].append(duration)
        
        return response
        
    except Exception as e:
        analytics_data["error_count"] += 1
        raise
```

### Query Analytics

```bash
curl https://your-api-url/analytics | jq
```

---

## 6. Export Logs to BigQuery

### Enable Log Export

```bash
# Create BigQuery dataset
bq mk --dataset nodal-fountain-470717-j1:chatbot_logs

# Create log sink
gcloud logging sinks create chatbot-logs-sink \
  bigquery.googleapis.com/projects/nodal-fountain-470717-j1/datasets/chatbot_logs \
  --log-filter='resource.type="cloud_run_revision" AND resource.labels.service_name="support-chatbot-api"'
```

### Query Logs in BigQuery

```sql
-- Total requests by language
SELECT
  JSON_EXTRACT_SCALAR(jsonPayload, '$.data.language') as language,
  COUNT(*) as request_count
FROM `nodal-fountain-470717-j1.chatbot_logs.cloudaudit_googleapis_com_data_access_*`
WHERE JSON_EXTRACT_SCALAR(jsonPayload, '$.event_type') = 'chat_request'
GROUP BY language
ORDER BY request_count DESC

-- Average response time
SELECT
  DATE(timestamp) as date,
  AVG(CAST(JSON_EXTRACT_SCALAR(jsonPayload, '$.data.duration_seconds') AS FLOAT64)) as avg_duration
FROM `nodal-fountain-470717-j1.chatbot_logs.cloudaudit_googleapis_com_data_access_*`
WHERE JSON_EXTRACT_SCALAR(jsonPayload, '$.event_type') = 'chat_response'
GROUP BY date
ORDER BY date DESC

-- Error rate by day
SELECT
  DATE(timestamp) as date,
  COUNTIF(JSON_EXTRACT_SCALAR(jsonPayload, '$.event_type') = 'chat_error') as errors,
  COUNT(*) as total,
  ROUND(COUNTIF(JSON_EXTRACT_SCALAR(jsonPayload, '$.event_type') = 'chat_error') / COUNT(*) * 100, 2) as error_rate_pct
FROM `nodal-fountain-470717-j1.chatbot_logs.cloudaudit_googleapis_com_data_access_*`
GROUP BY date
ORDER BY date DESC
```

---

## 7. Performance Monitoring

### Create Dashboard Script

Create `monitor.sh`:

```bash
#!/bin/bash

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "=== Support Chatbot API Monitoring ==="
echo

# Check service status
echo -n "Service Status: "
STATUS=$(gcloud run services describe support-chatbot-api \
  --region us-central1 \
  --format="value(status.conditions[0].status)")

if [ "$STATUS" == "True" ]; then
  echo -e "${GREEN}RUNNING${NC}"
else
  echo -e "${RED}NOT RUNNING${NC}"
fi

# Get service URL
URL=$(gcloud run services describe support-chatbot-api \
  --region us-central1 \
  --format="value(status.url)")
echo "URL: $URL"
echo

# Check health
echo -n "Health Check: "
HEALTH=$(curl -s "$URL/health" | jq -r .status)
if [ "$HEALTH" == "healthy" ]; then
  echo -e "${GREEN}HEALTHY${NC}"
else
  echo -e "${RED}UNHEALTHY${NC}"
fi

# Get metrics
ACTIVE_SESSIONS=$(curl -s "$URL/health" | jq -r .active_sessions)
echo "Active Sessions: $ACTIVE_SESSIONS"
echo

# Recent errors (last hour)
echo "Recent Errors (last hour):"
gcloud run services logs read support-chatbot-api \
  --region us-central1 \
  --filter="severity>=ERROR AND timestamp>=\"$(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)\"" \
  --limit 5 \
  --format="table(timestamp,textPayload)"
echo

# Request count (last hour)
echo "Request Count (last hour):"
gcloud logging read \
  "resource.type=cloud_run_revision AND resource.labels.service_name=support-chatbot-api" \
  --limit 1000 \
  --format="value(timestamp)" \
  --freshness=1h | wc -l

echo
echo "=== Monitoring Complete ==="
```

Run:
```bash
chmod +x monitor.sh
./monitor.sh
```

---

## 8. Cost Monitoring

### Check Current Costs

```bash
# Get billing info
gcloud billing accounts list

# View usage
gcloud alpha billing accounts list
```

### Set Budget Alert

1. Go to [Cloud Console > Billing > Budgets](https://console.cloud.google.com/billing/budgets)
2. Create budget:
   - Name: "Support Chatbot Monthly Budget"
   - Amount: $50/month
   - Alert: 50%, 90%, 100%

### Estimate Costs

```python
# Cost calculator
requests_per_day = 10000
avg_duration_seconds = 2
cpu_seconds_per_day = requests_per_day * avg_duration_seconds

# Cloud Run pricing (us-central1)
cpu_price_per_second = 0.00002400  # $0.024 per vCPU-second
memory_price_per_gb_second = 0.00000250  # $0.0025 per GB-second
request_price = 0.40 / 1000000  # $0.40 per million requests

# Calculate
cpu_cost = cpu_seconds_per_day * cpu_price_per_second * 30  # Monthly
memory_cost = cpu_seconds_per_day * 2 * memory_price_per_gb_second * 30  # 2GB memory
request_cost = requests_per_day * request_price * 30

total_monthly = cpu_cost + memory_cost + request_cost

print(f"Estimated Monthly Cost: ${total_monthly:.2f}")
# Typical: $10-30/month for moderate traffic
```

---

## 9. User Feedback Tracking

### Add Feedback Endpoint

```python
@app.post("/feedback")
async def submit_feedback(
    session_id: str,
    message_id: str,
    rating: int,  # 1-5 stars
    comment: str = ""
):
    """Collect user feedback on responses"""
    feedback = {
        "session_id": session_id,
        "message_id": message_id,
        "rating": rating,
        "comment": comment,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Log feedback (in production, save to database)
    log_chat_event("feedback", feedback)
    
    return {"message": "Thank you for your feedback!"}
```

### Frontend Integration

```typescript
const rateBotResponse = async (messageIdx: number, helpful: boolean) => {
  await fetch(`${API_URL}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      message_id: messages[messageIdx].timestamp,
      rating: helpful ? 5 : 2,
      comment: ""
    })
  })
}
```

---

## 10. Weekly Report Generator

Create `generate_report.py`:

```python
from datetime import datetime, timedelta
import subprocess
import json

def generate_weekly_report():
    """Generate weekly analytics report"""
    
    # Get logs from last week
    week_ago = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    cmd = f"""
    gcloud logging read \
      'resource.type=cloud_run_revision AND 
       resource.labels.service_name=support-chatbot-api AND
       timestamp>="{week_ago}"' \
      --format=json \
      --limit=10000
    """
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    logs = json.loads(result.stdout)
    
    # Parse logs
    total_requests = 0
    languages = {}
    errors = 0
    
    for log in logs:
        if 'jsonPayload' in log:
            payload = log['jsonPayload']
            
            if payload.get('event_type') == 'chat_request':
                total_requests += 1
                lang = payload.get('data', {}).get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
            
            if payload.get('event_type') == 'chat_error':
                errors += 1
    
    # Generate report
    error_rate = (errors / total_requests * 100) if total_requests > 0 else 0
    
    report = f"""
    === Weekly Chatbot Report ===
    Period: {week_ago} to now
    
    Total Requests: {total_requests}
    Error Rate: {error_rate:.2f}%
    
    Top Languages:
    """
    
    for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]:
        percentage = (count / total_requests * 100) if total_requests > 0 else 0
        report += f"  {lang}: {count} ({percentage:.1f}%)\n"
    
    print(report)
    
    # Save to file
    with open(f"report_{datetime.now().strftime('%Y-%m-%d')}.txt", "w") as f:
        f.write(report)

if __name__ == "__main__":
    generate_weekly_report()
```

Run weekly:
```bash
python generate_report.py
```

---

## 11. Monitoring Checklist

### Daily Checks
- [ ] Service is running
- [ ] Error rate < 5%
- [ ] Response time < 3s
- [ ] No critical errors in logs

### Weekly Checks
- [ ] Review analytics trends
- [ ] Check cost vs. budget
- [ ] Review user feedback
- [ ] Update knowledge base if needed

### Monthly Checks
- [ ] Generate monthly report
- [ ] Review and optimize costs
- [ ] Update model if new version available
- [ ] Review and improve prompts

---

## 12. Troubleshooting Common Issues

### High Latency
1. Check Vertex AI quotas
2. Increase CPU/memory
3. Optimize prompts
4. Add caching for common queries

### High Error Rate
1. Check logs for specific errors
2. Verify Vertex AI credentials
3. Check network connectivity
4. Review recent code changes

### High Costs
1. Review request count
2. Optimize instance settings
3. Add request caching
4. Implement rate limiting

---

## Support

For monitoring issues:
- Cloud Run Docs: https://cloud.google.com/run/docs/monitoring
- Logging Docs: https://cloud.google.com/logging/docs
- Contact: dev@kalpana-ai.com
