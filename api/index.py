import os
import sys

# Add project root to sys.path for Vercel
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.server.app import app

# Export FastAPI app for Vercel Python runtime
app = app
