"""
Hugging Face Spaces entry point for Physical AI & Humanoid Robotics API

This file serves as the entry point for Hugging Face Spaces deployment.
It imports and runs the FastAPI application from the src module.
"""
import os
import sys

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the FastAPI app
from src.main import app

# For Hugging Face Spaces, we need to expose the app
# The Space will run this with: uvicorn app:app --host 0.0.0.0 --port 7860
