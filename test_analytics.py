#!/usr/bin/env python3
"""
Google Analytics Setup Tester
This script checks if your Google Analytics setup is correct
"""

import re

def test_analytics_setup():
    """Test if Google Analytics is properly configured in app.py"""
    
    print("🏥 New Medical Italian - Analytics Setup Test")
    print("=" * 50)
    
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if GA4 ID is configured
        if "YOUR_GA4_MEASUREMENT_ID" in content:
            print("❌ Google Analytics not configured yet")
            print("   Still using placeholder: YOUR_GA4_MEASUREMENT_ID")
            print("   Run: python update_analytics.py G-XXXXXXXXXX")
            return False
        
        # Look for GA4 measurement ID pattern
        ga4_pattern = r"analytics_code\.replace\('GA_MEASUREMENT_ID', '(G-[A-Z0-9]{10})'\)"
        match = re.search(ga4_pattern, content)
        
        if match:
            measurement_id = match.group(1)
            print(f"✅ Google Analytics configured!")
            print(f"   Measurement ID: {measurement_id}")
            
            # Check for analytics injection
            if "inject_analytics()" in content:
                print("✅ Analytics injection code present")
            else:
                print("❌ Analytics injection code missing")
                return False
            
            # Check for tracking functions
            tracking_functions = [
                "trackDemoStart",
                "trackDemoCompletion", 
                "trackContactIntent",
                "trackUpgradePrompt"
            ]
            
            missing_functions = []
            for func in tracking_functions:
                if func not in content:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"❌ Missing tracking functions: {', '.join(missing_functions)}")
                return False
            else:
                print("✅ All tracking functions present")
            
            print("")
            print("🚀 Setup Status: READY FOR DEPLOYMENT")
            print("")
            print("Next steps:")
            print("1. Commit and push changes to GitHub")
            print("2. Streamlit Cloud will auto-deploy")
            print("3. Visit your live app to test tracking")
            print("4. Check Google Analytics in 24-48 hours")
            
            return True
        else:
            print("❌ No valid Google Analytics configuration found")
            return False
            
    except FileNotFoundError:
        print("❌ app.py not found")
        print("   Make sure you're in the correct directory")
        return False
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def check_streamlit_deployment():
    """Check if the app is ready for Streamlit deployment"""
    
    print("\n📦 Deployment Readiness Check")
    print("-" * 30)
    
    required_files = ['app.py', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        try:
            with open(file, 'r') as f:
                pass
            print(f"✅ {file} present")
        except FileNotFoundError:
            missing_files.append(file)
            print(f"❌ {file} missing")
    
    if missing_files:
        print(f"\n❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("\n✅ All required files present")
    print("\n🌐 Your app URL: https://new-medical-italian.streamlit.app")
    return True

if __name__ == "__main__":
    analytics_ok = test_analytics_setup()
    deployment_ok = check_streamlit_deployment()
    
    print("\n" + "=" * 50)
    if analytics_ok and deployment_ok:
        print("🎉 Everything looks good! Your app is ready for Google Analytics tracking.")
    else:
        print("⚠️  Please fix the issues above before deploying.")

