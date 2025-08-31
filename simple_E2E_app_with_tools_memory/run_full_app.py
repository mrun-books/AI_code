#!/usr/bin/env python3
"""
Script to run the complete application stack:
1. FastAPI backend server
2. Streamlit UI
"""

import subprocess
import sys
import time
import os
from threading import Thread

def run_fastapi():
    """Run the FastAPI backend server"""
    print("Starting FastAPI backend on http://127.0.0.1:8000")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("FastAPI backend stopped")

def run_streamlit():
    """Run the Streamlit UI"""
    print("Starting Streamlit UI on http://localhost:8501")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", "stremlit_ui.py",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("Streamlit UI stopped")

def main():
    print("=" * 60)
    print("AI Agent with Chat History - Full Stack Application")
    print("=" * 60)
    print()
    print("This will start:")
    print("• FastAPI Backend (http://127.0.0.1:8000)")
    print("• Streamlit UI (http://localhost:8501)")
    print()
    print("Press Ctrl+C to stop both servers")
    print("=" * 60)
    
    # Check if required packages are installed
    required_packages = ['fastapi', 'uvicorn', 'streamlit', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print(f"Install with: pip install {' '.join(missing_packages)}")
        return
    
    try:
        # Start FastAPI in a separate thread
        fastapi_thread = Thread(target=run_fastapi, daemon=True)
        fastapi_thread.start()
        
        # Wait a bit for FastAPI to start
        time.sleep(3)
        
        # Start Streamlit (this will block)
        run_streamlit()
        
    except KeyboardInterrupt:
        print("\nShutting down all servers...")
        print("Application stopped")

if __name__ == "__main__":
    main()