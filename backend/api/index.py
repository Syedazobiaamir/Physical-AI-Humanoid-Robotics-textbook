"""
Vercel serverless function entry point

This file serves as the entry point for Vercel's Python serverless functions.
"""
import sys
import os

# CRITICAL: Set up Python path BEFORE any imports
# Vercel unpacks to /var/task, but we need to handle both local and deployed paths
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)

# Add backend root to path (for 'src' package imports)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set PYTHONPATH environment variable as well
os.environ['PYTHONPATH'] = backend_dir

# Now import the app - this will trigger all the relative imports in the src package
from src.main import app

# Export app for Vercel
# Vercel expects either 'app' or 'handler' at module level
