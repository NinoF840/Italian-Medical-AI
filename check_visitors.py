#!/usr/bin/env python3
"""
Visitor Data Checker for New Medical Italian
Checks current analytics and usage data
"""

import os
import json
from datetime import datetime, timedelta

def check_visitor_data():
    """Check for any stored visitor or analytics data"""
    print("🔍 Checking for Visitor Data...")
    print("=" * 50)
    
    # Check for any analytics files
    analytics_found = False
    
    # Common locations for analytics data
    possible_locations = [
        './analytics.json',
        './visitor_log.json', 
        './usage_data.json',
        './.streamlit/analytics.json',
        './logs/',
        './data/'
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            print(f"📁 Found: {location}")
            analytics_found = True
            
            if location.endswith('.json'):
                try:
                    with open(location, 'r') as f:
                        data = json.load(f)
                    print(f"   📊 Contains {len(data)} entries")
                except Exception as e:
                    print(f"   ❌ Error reading: {e}")
    
    if not analytics_found:
        print("📭 No stored visitor data files found")
    
    print("\n🚀 Current App Status:")
    print("=" * 30)
    
    # Check if app is running
    try:
        import psutil
        streamlit_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if cmdline and isinstance(cmdline, list):
                    cmdline_str = ' '.join(cmdline).lower()
                    if 'streamlit' in cmdline_str:
                        streamlit_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, TypeError):
                pass
        
        if streamlit_processes:
            print(f"✅ Streamlit app is running ({len(streamlit_processes)} process(es))")
            for proc in streamlit_processes:
                print(f"   PID: {proc['pid']}")
        else:
            print("❌ No Streamlit processes found")
    except ImportError:
        print("⚠️  psutil not available - cannot check running processes")
        # Alternative method using Windows commands
        try:
            import subprocess
            result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq streamlit.exe'], 
                                  capture_output=True, text=True, shell=True)
            if 'streamlit.exe' in result.stdout:
                print("✅ Streamlit process found via tasklist")
            else:
                print("❌ No Streamlit processes found via tasklist")
        except:
            print("⚠️  Could not check running processes")
    
    print("\n📊 Analytics Status:")
    print("=" * 25)
    
    # Check app.py for analytics configuration
    app_file = './app.py'
    if os.path.exists(app_file):
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'GA_MEASUREMENT_ID' in content:
            print("🔧 Google Analytics configured but not activated (placeholder IDs)")
        if 'FACEBOOK_PIXEL_ID' in content:
            print("🔧 Facebook Pixel configured but not activated (placeholder IDs)")
        if 'session_state' in content:
            print("✅ Internal session tracking enabled")
        if 'usage_tracking' in content:
            print("✅ Usage tracking system implemented")
    
    print("\n💡 Current Visitor Tracking Capabilities:")
    print("=" * 45)
    print("📝 Session-based tracking (in-memory only)")
    print("📊 Usage limits and demo counts per user")
    print("🔒 Email-based user identification")
    print("⏱️  Demo timing and interaction tracking")
    print("🎯 Button click and conversion events (ready for external analytics)")
    
    print("\n🚨 Important Notes:")
    print("=" * 20)
    print("• Visitor data is stored in Streamlit session state (temporary)")
    print("• Data is lost when the app restarts")
    print("• External analytics (GA4, Facebook) need activation with real IDs")
    print("• For persistent visitor data, activate external analytics")
    
    print("\n🔧 Next Steps to Get Full Visitor Analytics:")
    print("=" * 50)
    print("1. Set up Google Analytics 4 account")
    print("2. Create Facebook Pixel (optional)")
    print("3. Replace placeholder IDs in app.py")
    print("4. Deploy with real analytics tracking")
    
    # Check if app is accessible
    print("\n🌐 App Access:")
    print("=" * 15)
    print("Local URL: http://localhost:8501")
    print("To view current session data, access the running app")

if __name__ == "__main__":
    check_visitor_data()

