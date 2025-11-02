"""
Safe runner for artisan_mentor agent.
This script attempts to import the agent module while stubbing heavy/optional runtime
modules (like vertexai) to avoid side-effects at import time. It then calls the
module-level tool function `start_artisan_journey` with a small test profile.

Run with the ADK environment python executable, e.g.:
C:/Google_ADK/.adk/Scripts/python.exe c:\Google_ADK\run_artisan_tutor.py
"""
import sys
import types
import json

# --- Minimal stubs to avoid heavy imports/side-effects during import ---
# If the real packages are present in the ADK environment these stubs will be
# ignored because the real modules will be loaded instead.
if 'vertexai' not in sys.modules:
    vertexai = types.SimpleNamespace()
    def dummy_init(*args, **kwargs):
        # no-op init used only to satisfy imports
        return None
    vertexai.init = dummy_init
    sys.modules['vertexai'] = vertexai

# create a minimal vertexai.generative_models with GenerativeModel and Part
if 'vertexai.generative_models' not in sys.modules:
    gm = types.SimpleNamespace()
    class GenerativeModel:
        def __init__(self, *args, **kwargs):
            pass
        def generate_content(self, parts):
            # return a simple object with a text attribute to mimic responses
            return types.SimpleNamespace(text='{"mock": "response"}')
    class Part:
        @staticmethod
        def from_uri(uri, mime_type=None):
            return f"PART_URI:{uri}"
        @staticmethod
        def from_data(data, mime_type=None):
            return f"PART_DATA(len={len(data) if hasattr(data, '__len__') else 'unknown'})"
    gm.GenerativeModel = GenerativeModel
    gm.Part = Part
    sys.modules['vertexai.generative_models'] = gm

# If google.adk.agents is not present, provide a tiny stub Agent so import succeeds
if 'google' not in sys.modules:
    # create package structure in sys.modules only if missing
    google = types.ModuleType('google')
    sys.modules['google'] = google

if 'google.adk' not in sys.modules:
    google_adk = types.ModuleType('google.adk')
    sys.modules['google.adk'] = google_adk

if 'google.adk.agents' not in sys.modules:
    agents_mod = types.ModuleType('google.adk.agents')
    class Agent:
        def __init__(self, *args, **kwargs):
            self.name = kwargs.get('name') or (args[0] if args else 'agent')
            self.tools = {}
        def __repr__(self):
            return f"<Stub Agent name={self.name}>"
    agents_mod.Agent = Agent
    sys.modules['google.adk.agents'] = agents_mod

# --- Stub google.cloud.* modules to avoid network/auth side-effects ---
def _make_client_stub(name):
    mod = types.ModuleType(name)
    # Provide basic Client classes. For some cloud services provide simple
    # minimal methods used by the agent (collection, bucket, blob, document, set)
    class Client:
        def __init__(self, *a, **k):
            return None

    # Firestore minimal stubs
    class DocumentRef:
        def __init__(self, name=None):
            self.name = name
        def set(self, data, merge=False):
            # pretend to write; no-op
            return None
        def to_dict(self):
            return {}

    class CollectionRef:
        def __init__(self, name=None):
            self.name = name
        def document(self, doc_id=None):
            return DocumentRef(doc_id)

    class FirestoreClient(Client):
        def collection(self, name):
            return CollectionRef(name)

    # Storage minimal stubs
    class Blob:
        def __init__(self, name=None):
            self.name = name
        def upload_from_string(self, data, content_type=None):
            return None
        def make_public(self):
            return None

    class Bucket:
        def __init__(self, name=None):
            self.name = name
        def blob(self, name):
            return Blob(name)

    class StorageClient(Client):
        def bucket(self, name):
            return Bucket(name)

    # Assign appropriate client classes depending on module
    if name.endswith('firestore'):
        setattr(mod, 'Client', FirestoreClient)
    elif name.endswith('storage'):
        setattr(mod, 'Client', StorageClient)
    else:
        setattr(mod, 'Client', Client)

    # Additional named client classes used directly
    setattr(mod, 'TextToSpeechClient', Client)
    setattr(mod, 'SpeechClient', Client)
    setattr(mod, 'ImageAnnotatorClient', Client)
    sys.modules[name] = mod

cloud_submods = [
    'google.cloud.storage',
    'google.cloud.firestore',
    'google.cloud.texttospeech',
    'google.cloud.speech',
    'google.cloud.translate_v2',
    'google.cloud.vision'
]
for sub in cloud_submods:
    if sub not in sys.modules:
        _make_client_stub(sub)

# --- Import the artisan_mentor agent module ---
try:
    # ensure working directory includes workspace root
    import os
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

    print("Importing artisan_mentor.agent...")
    from artisan_mentor import agent as am_agent
    print("Import succeeded.")
except Exception as e:
    print("Import failed:", repr(e))
    raise

# --- Invoke a safe tool function if available ---
try:
    # prefer the module-level helper function start_artisan_journey if present
    if hasattr(am_agent, 'start_artisan_journey'):
        print("Found start_artisan_journey tool. Calling with test profile...")
        test_profile = {
            "user_id": "test_user_1",
            "learning_style": "visual",
            "language": "en",
            "current_skill_level": "beginner"
        }
        out = am_agent.start_artisan_journey(test_profile)
        print("Tool output:")
        try:
            print(json.dumps(out, indent=2, default=str))
        except Exception:
            print(out)
    else:
        print("Module does not expose start_artisan_journey. Listing attributes:")
        for name in dir(am_agent):
            if not name.startswith('_'):
                print(' -', name)
except Exception as e:
    print("Tool call failed:", repr(e))
    raise

print("Runner finished.")
