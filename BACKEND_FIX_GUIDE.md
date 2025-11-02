# Backend Issues - Comprehensive Fix Guide

## 🔍 Issues Identified

### 1. **Dashboard API Error: "NoneType object has no attribute 'get'"**
- **File**: `Artisan_mentor/artisan_mentor/tutor.py`
- **Method**: `get_business_dashboard()` and helper methods
- **Line**: ~270-280, 685-760
- **Root Cause**: Methods assume nested dict structure exists but it may be None or missing

### 2. **User Progress Not Persisting**
- **File**: `Artisan_mentor/artisan_mentor/tutor.py`
- **Method**: `_update_user_progress()`
- **Root Cause**: Missing implementation or Firestore update not working

### 3. **Current Lesson Field Returns Empty**
- **File**: `Artisan_mentor/artisan_mentor/tutor.py`
- **Method**: `create_personalized_learning_journey()`
- **Line**: ~143
- **Root Cause**: Sets empty string instead of actual starting lesson

---

## 🛠️ Fix #1: Dashboard NoneType Error

**Location**: `Artisan_mentor/artisan_mentor/tutor.py`, line 263-285

**Problem**:
```python
def get_business_dashboard(self, user_id: str) -> Dict:
    user_data = user_doc.to_dict()
    
    dashboard = {
        "learning_progress": self._calculate_learning_progress(user_data),
        "business_metrics": self._calculate_business_metrics(user_data),
        # ...
    }
```

The `_calculate_learning_progress` and `_calculate_business_metrics` methods try to access:
- `user_data.get("progress_metrics", {})` - might return None
- `user_data.get("learning_journey", {})` - might return None  
- `journey.get("personalized_curriculum", {}).get("curriculum", ...)` - chained gets fail if any return None

**Solution - Replace lines 685-720**:

```python
def _calculate_learning_progress(self, user_data: Dict) -> Dict:
    """Calculate comprehensive learning progress"""
    # Safe access with default empty dicts
    metrics = user_data.get("progress_metrics") or {}
    journey = user_data.get("learning_journey") or {}
    
    # Calculate completion percentage with safe access
    curriculum = {}
    if journey:
        personalized = journey.get("personalized_curriculum") or {}
        curriculum = personalized.get("curriculum") or PROGRESSIVE_CURRICULUM
    else:
        curriculum = PROGRESSIVE_CURRICULUM
    
    total_lessons = sum(
        len(module.get("lessons", []))
        for module in curriculum.values()
        if isinstance(module, dict)
    )
    completed = metrics.get("completed_lessons", 0) or 0
    completion_percent = (completed / total_lessons * 100) if total_lessons > 0 else 0
    
    # Determine current level
    current_level = "Beginner"
    if completed >= 15:
        current_level = "Expert"
    elif completed >= 10:
        current_level = "Advanced"
    elif completed >= 5:
        current_level = "Intermediate"
    
    # Safe access for achievements
    achievements = user_data.get("achievements") or {}
    unlocked = achievements.get("unlocked") or []
    completed_modules = journey.get("completed_modules") or []
    
    return {
        "total_points": metrics.get("total_points", 0) or 0,
        "completed_lessons": completed,
        "total_lessons": total_lessons,
        "completion_percentage": round(completion_percent, 1),
        "current_level": current_level,
        "current_streak": metrics.get("current_streak", 0) or 0,
        "modules_completed": len(completed_modules),
        "achievements_unlocked": len(unlocked),
        "time_invested_estimate": f"{completed * 30} minutes"
    }
```

**Solution - Replace lines 720-760**:

```python
def _calculate_business_metrics(self, user_data: Dict) -> Dict:
    """Calculate business readiness metrics"""
    # Safe access with defaults
    progress_metrics = user_data.get("progress_metrics") or {}
    completed = progress_metrics.get("completed_lessons", 0) or 0
    
    journey = user_data.get("learning_journey") or {}
    current_module = journey.get("current_module") or "foundation"
    
    # Calculate business readiness scores
    photography_ready = completed >= 1
    listing_ready = completed >= 3
    marketing_ready = completed >= 6
    export_ready = completed >= 9
    
    # Estimate potential impact
    potential_revenue_increase = min(completed * 10, 100)  # Up to 100% increase
    
    return {
        "business_readiness": {
            "photography": "Ready" if photography_ready else "In Progress",
            "product_listing": "Ready" if listing_ready else "Not Started" if completed < 1 else "In Progress",
            "digital_marketing": "Ready" if marketing_ready else "Not Started" if completed < 3 else "In Progress",
            "export_capability": "Ready" if export_ready else "Not Started" if completed < 6 else "In Progress"
        },
        "estimated_impact": {
            "potential_revenue_increase": f"{potential_revenue_increase}%",
            "market_reach_expansion": "Local" if completed < 3 else "National" if completed < 9 else "Global",
            "brand_strength": "Building" if completed < 5 else "Established" if completed < 10 else "Strong"
        },
        "next_milestone": self._get_next_business_milestone(completed),
        "skills_acquired": self._list_acquired_skills(completed)
    }
```

---

## 🛠️ Fix #2: User Progress Not Persisting

**Location**: `Artisan_mentor/artisan_mentor/tutor.py`, line 581

Find the `_update_user_progress` method and ensure it properly updates Firestore:

```python
def _update_user_progress(self, user_id: str, lesson_id: str, points: int, validation: Dict):
    """Update user progress after successful lesson completion"""
    try:
        user_ref = firestore_client.collection("users").document(user_id)
        user_doc = user_ref.get()
        
        if not user_doc.exists:
            return
        
        user_data = user_doc.to_dict()
        
        # Safe access to progress metrics
        current_metrics = user_data.get("progress_metrics") or {}
        current_journey = user_data.get("learning_journey") or {}
        current_achievements = user_data.get("achievements") or {}
        
        # Calculate new values
        new_total_points = (current_metrics.get("total_points") or 0) + points
        new_completed = (current_metrics.get("completed_lessons") or 0) + 1
        new_streak = (current_metrics.get("current_streak") or 0) + 1
        
        # Get completed lessons list
        completed_lessons_list = current_journey.get("completed_lessons") or []
        if lesson_id not in completed_lessons_list:
            completed_lessons_list.append(lesson_id)
        
        # Update Firestore document
        user_ref.update({
            "progress_metrics.total_points": new_total_points,
            "progress_metrics.completed_lessons": new_completed,
            "progress_metrics.current_streak": new_streak,
            "learning_journey.completed_lessons": completed_lessons_list,
            "learning_journey.last_active": datetime.now(),
            "learning_journey.last_completed_lesson": lesson_id,
            "learning_journey.last_completed_at": datetime.now()
        })
        
        print(f"✅ Progress updated for {user_id}: +{points} points, {new_completed} lessons completed")
        
    except Exception as e:
        print(f"❌ Error updating progress: {str(e)}")
        import traceback
        traceback.print_exc()
```

---

## 🛠️ Fix #3: Current Lesson Field Empty

**Location**: `Artisan_mentor/artisan_mentor/tutor.py`, line ~130-160

Find the `create_personalized_learning_journey` method and fix the starting lesson:

```python
def create_personalized_learning_journey(self, user_profile: Dict) -> Dict:
    """Create completely personalized learning journey"""
    user_id = user_profile.get("user_id", str(uuid.uuid4()))
    
    learning_style = user_profile.get("learning_style", LearningStyle.VISUAL.value)
    language = user_profile.get("language", "en")
    current_skill_level = user_profile.get("current_skill_level", SkillLevel.BEGINNER.value)
    craft_context = user_profile.get("craft_analysis", {})
    
    # Create personalized curriculum
    personalized_curriculum = self._build_personalized_curriculum(
        current_skill_level, learning_style, craft_context, language
    )
    
    # FIX: Get actual starting lesson from curriculum
    starting_module = personalized_curriculum.get("starting_module", "foundation")
    starting_lesson = personalized_curriculum.get("starting_lesson", "F1.1")  # Changed from empty string
    
    # If starting_lesson is still empty or not in curriculum, use default
    if not starting_lesson:
        # Try to get first lesson from foundation module
        foundation_module = personalized_curriculum.get("curriculum", {}).get("foundation", {})
        lessons = foundation_module.get("lessons", [])
        starting_lesson = lessons[0].get("id", "F1.1") if lessons else "F1.1"
    
    # Initialize user in Firestore
    user_doc_ref = firestore_client.collection("users").document(user_id)
    user_doc_ref.set({
        "profile": user_profile,
        "learning_journey": {
            "current_module": starting_module,
            "current_lesson": starting_lesson,  # Now has actual value
            "completed_modules": [],
            "completed_lessons": [],  # ADD THIS - track completed lessons list
            "personalized_curriculum": personalized_curriculum,
            "learning_style": learning_style,
            "language_preference": language,
            "created_at": datetime.now(),
            "last_active": datetime.now()
        },
        "progress_metrics": {
            "total_points": 0,
            "current_streak": 0,
            "completed_lessons": 0,
            "skill_level": current_skill_level
        },
        "achievements": {
            "unlocked": [],
            "in_progress": [],
            "next_milestones": personalized_curriculum.get("milestones", [])[:3] if personalized_curriculum.get("milestones") else []
        }
    }, merge=True)
    
    welcome_message = self._generate_welcome_message(user_profile, personalized_curriculum, language)
    
    return {
        "status": "success",
        "user_id": user_id,
        "welcome_message": welcome_message,
        "personalized_curriculum": personalized_curriculum,
        "starting_point": {
            "module": starting_module,
            "lesson": starting_lesson  # Now returns actual lesson ID
        }
    }
```

---

## 🛠️ Fix #4: Additional Safety Improvements

**Add to `_calculate_skill_matrix` method** (find around line 760):

```python
def _calculate_skill_matrix(self, user_data: Dict) -> Dict:
    """Calculate skill development matrix"""
    # Safe access
    journey = user_data.get("learning_journey") or {}
    completed_modules = journey.get("completed_modules") or []
    
    skills = {
        "photography": 0,
        "digital_marketing": 0,
        "business_planning": 0,
        "export_readiness": 0
    }
    
    # Update skills based on completed modules
    for module in completed_modules:
        if isinstance(module, str):  # Safety check
            if module == "foundation":
                skills["photography"] = 100
            elif module == "marketing":
                skills["digital_marketing"] = 100
            elif module == "business":
                skills["business_planning"] = 100
            elif module == "export":
                skills["export_readiness"] = 100
    
    return skills
```

---

## 📋 Testing After Fixes

### Test 1: Dashboard API
```powershell
$body = @{
    user_id = "test_user_123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://artisan-mentor-api-508329185712.us-central1.run.app/dashboard" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

**Expected**: Dashboard data with no errors

### Test 2: Progress Persistence
```powershell
# 1. Start journey
$profile = @{
    user_id = "test_persist_123"
    name = "Test User"
    learning_style = "visual"
    language = "en"
    current_skill_level = "beginner"
} | ConvertTo-Json

$startResult = Invoke-RestMethod -Uri "https://artisan-mentor-api-508329185712.us-central1.run.app/start-journey" `
    -Method Post -Body $profile -ContentType "application/json"

Write-Host "Starting lesson: $($startResult.starting_point.lesson)"

# 2. Submit work
$submission = @{
    user_id = "test_persist_123"
    lesson_id = $startResult.starting_point.lesson
    submission = @{
        content = "Test submission for progress tracking"
        metadata = @{
            type = "text"
        }
    }
} | ConvertTo-Json -Depth 5

$submitResult = Invoke-RestMethod -Uri "https://artisan-mentor-api-508329185712.us-central1.run.app/submit-work" `
    -Method Post -Body $submission -ContentType "application/json"

Write-Host "Submission passed: $($submitResult.passed)"
Write-Host "Points earned: $($submitResult.points_earned)"

# 3. Check dashboard
$dashboard = @{
    user_id = "test_persist_123"
} | ConvertTo-Json

$dashResult = Invoke-RestMethod -Uri "https://artisan-mentor-api-508329185712.us-central1.run.app/dashboard" `
    -Method Post -Body $dashboard -ContentType "application/json"

Write-Host "Total points in dashboard: $($dashResult.dashboard.learning_progress.total_points)"
Write-Host "Completed lessons: $($dashResult.dashboard.learning_progress.completed_lessons)"
```

**Expected**: 
- Starting lesson = "F1.1" (not empty)
- Points earned = 25 (or lesson points)
- Dashboard shows points and completed lessons

---

## 🚀 Deployment Steps

### 1. **Apply All Fixes**
Edit `Artisan_mentor/artisan_mentor/tutor.py` and apply all the fixes above.

### 2. **Test Locally**
```powershell
cd C:\Users\rockb\OneDrive\Desktop\Projects\Exchange
python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

Test with the PowerShell commands above.

### 3. **Deploy to Google Cloud Run**
```powershell
cd C:\Users\rockb\OneDrive\Desktop\Projects\Exchange

# Build and deploy
gcloud run deploy artisan-mentor-api `
  --source . `
  --region us-central1 `
  --platform managed `
  --allow-unauthenticated `
  --set-env-vars "GOOGLE_CLOUD_PROJECT=nodal-fountain-470717-j1,CLOUD_STORAGE_BUCKET=kalpana-artisan-tutor"
```

### 4. **Verify Deployment**
```powershell
Invoke-RestMethod -Uri "https://artisan-mentor-api-508329185712.us-central1.run.app/health"
```

---

## 📝 Summary of Changes

| Issue | Root Cause | Fix Applied |
|-------|-----------|-------------|
| **Dashboard NoneType Error** | Unsafe dict access with `.get()` chaining | Added `or {}` checks and safe access patterns |
| **Progress Not Persisting** | Missing/incomplete Firestore update logic | Added proper `user_ref.update()` with all fields |
| **Empty Starting Lesson** | Returned empty string instead of "F1.1" | Changed default to "F1.1" and added fallback logic |
| **Skill Matrix Errors** | Assumed module format without validation | Added `isinstance()` checks |

---

## ⚠️ Important Notes

1. **These are backend fixes** - you need to edit the Python files on your backend
2. **Redeploy required** - changes won't take effect until you redeploy to Cloud Run
3. **Frontend works without these fixes** - your localStorage-based solution keeps the app functional
4. **Database migration not needed** - Firestore will adapt to new structure automatically

---

## 🎯 Next Steps

1. ✅ Apply all code fixes to `tutor.py`
2. ✅ Test locally with PowerShell commands
3. ✅ Deploy to Google Cloud Run
4. ✅ Test deployed API
5. ✅ Frontend will automatically start using backend data when available
6. ✅ Keep localStorage as backup for reliability

The frontend already has fallbacks, so even if backend has issues, users can keep learning! 🎉
