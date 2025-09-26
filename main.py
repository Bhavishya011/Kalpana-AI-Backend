import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
agents_path = os.path.join(project_root, 'Agents', 'agents')
sys.path.insert(0, agents_path)
sys.path.insert(0, os.path.join(project_root, 'api'))

# Import the app with a different approach to avoid circular import
import importlib.util
spec = importlib.util.spec_from_file_location("api_main", os.path.join(project_root, 'api', 'main2.0.py'))
api_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api_main)
app = api_main.app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
