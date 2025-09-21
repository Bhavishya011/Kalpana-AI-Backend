# C:\Users\rockb\OneDrive\Desktop\Projects\Exchange\main.py
import sys
import os

# --- Correctly set up the Python path ---
# Get the absolute path of the current directory (project root)
project_root = os.path.dirname(os.path.abspath(__file__))

# Add the 'api' directory to the path so we can import from it
api_path = os.path.join(project_root, 'api')
agents_path = os.path.join(project_root, 'Agents', 'agents')

# Insert paths at the beginning to prioritize them
sys.path.insert(0, project_root) # Add project root
sys.path.insert(0, api_path)     # Add api directory
sys.path.insert(0, agents_path)  # Add agents directory

# --- Import the FastAPI app ---
# This imports the 'app' object from the file located at api/main.py
try:
    from main import app
    print("✅ Successfully imported FastAPI app from main")
except ImportError as e:
    print(f"❌ Error importing app from main: {e}")
    print("Current sys.path:")
    for p in sys.path:
        print(f"  {p}")
    # Re-raise the error to stop the application if import fails
    raise

# --- Entry point for running the app ---
if __name__ == "__main__":
    import uvicorn
    # Cloud Run sets the PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting server on 0.0.0.0:{port}")
    # Use the imported 'app' object
    uvicorn.run(app, host="0.0.0.0", port=port)
