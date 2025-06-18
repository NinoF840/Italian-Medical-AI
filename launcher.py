#!/usr/bin/env python3
"""
Medico-Italiano-IA - Executable Launcher
Advanced Italian Medical AI for Named Entity Recognition
This script launches the Streamlit web application.
"""

import subprocess
import sys
import os
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open browser after a delay"""
    webbrowser.open('http://localhost:8501')

def main():
    print("🏥 Medico-Italiano-IA - Starting Advanced Medical AI...")
    print("🤖 Italian Medical Named Entity Recognition System")
    print("📍 Application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("❌ To stop the application, press Ctrl+C")
    print("-" * 60)
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    app_path = os.path.join(script_dir, "app.py")
    
    # Schedule browser opening after 3 seconds
    timer = Timer(3.0, open_browser)
    timer.start()
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Medico-Italiano-IA stopped by user")
        timer.cancel()
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running application: {e}")
        timer.cancel()
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        timer.cancel()

if __name__ == "__main__":
    main()

