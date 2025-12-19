
import subprocess
import sys
import time
import os
import threading
from pathlib import Path

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting FastAPI backend...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", "app:app",
            "--host", "0.0.0.0", 
            "--port", "8000"
        ], check=True)
    except KeyboardInterrupt:
        print("Backend stopped")
    except Exception as e:
        print(f"Backend error: {e}")

def start_frontend():
    """Start the Streamlit frontend"""
    port = os.getenv("PORT", "8501")
    print(f"🎨 Starting Streamlit frontend on port {port}...")
    time.sleep(5)
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "frontend.py",
            "--server.port", port,
            "--server.address", "0.0.0.0"
        ], check=True)
    except KeyboardInterrupt:
        print("Frontend stopped")
    except Exception as e:
        print(f"Frontend error: {e}")

def check_files():
    """Check if required files and environment variables exist"""
    required_files = ['app.py', 'frontend.py']
    missing = [f for f in required_files if not Path(f).exists()]
    
    if missing:
        print(f"❌ Missing required files: {', '.join(missing)}")
        return False
    
    # Check if we have API keys in system environment OR .env file
    has_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    
    if not Path('.env').exists() and not has_api_key:
        print("⚠️  No .env file found and no API keys in environment.")
        print("Creating a template .env file...")
        with open('.env', 'w') as f:
            f.write("# API Configuration\n")
            f.write("OPENROUTER_API_KEY=your_key_here\n")
            f.write("OPENAI_API_KEY=your_key_here\n")
        print("✅ Template .env file created.")
        # Don't exit if we're in a container, environment variables might still be loaded from the platform
    
    return True

def main():
    print("🏥 AI Medical Prescription Verification System")
    print("=" * 50)
    
    if not check_files():
        print("❌ Initialization failed. Check the logs above.")
        return
    
    print("✅ All required files found")
    
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    
    try:
        print("\n🌐 Starting services...")
        print("📡 Backend API will be at: http://localhost:8000")
        print("🖥️  Frontend UI will be at: http://localhost:8501")
        print("\n⚠️  Press Ctrl+C to stop both services")
        
        backend_thread.start()
        frontend_thread.start()
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()