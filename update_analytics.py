#!/usr/bin/env python3
"""
Google Analytics Setup Helper
This script helps you update your Google Analytics Measurement ID in app.py

Usage:
    python update_analytics.py YOUR_GA4_MEASUREMENT_ID
    
Example:
    python update_analytics.py G-1234567890
"""

import sys
import re

def update_analytics_id(measurement_id):
    """Update the Google Analytics Measurement ID in app.py"""
    
    # Validate the measurement ID format
    if not re.match(r'^G-[A-Z0-9]{10}$', measurement_id):
        print(f"❌ Invalid Measurement ID format: {measurement_id}")
        print("Expected format: G-XXXXXXXXXX (e.g., G-1234567890)")
        return False
    
    app_file = 'app.py'
    
    try:
        # Read the current file
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the placeholder
        old_placeholder = "analytics_code.replace('GA_MEASUREMENT_ID', 'YOUR_GA4_MEASUREMENT_ID')"
        new_replacement = f"analytics_code.replace('GA_MEASUREMENT_ID', '{measurement_id}')"
        
        if old_placeholder in content:
            content = content.replace(old_placeholder, new_replacement)
            
            # Write back to file
            with open(app_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Successfully updated Google Analytics ID to: {measurement_id}")
            print(f"📝 Updated file: {app_file}")
            print("")
            print("🚀 Next steps:")
            print("1. Deploy your app to Streamlit Cloud")
            print("2. Visit your live app to test tracking")
            print("3. Check Google Analytics for data (may take 24-48 hours)")
            return True
        else:
            print(f"❌ Placeholder not found in {app_file}")
            print("The file may have already been updated or the format changed.")
            return False
            
    except FileNotFoundError:
        print(f"❌ File not found: {app_file}")
        print("Make sure you're running this script in the same directory as app.py")
        return False
    except Exception as e:
        print(f"❌ Error updating file: {e}")
        return False

def main():
    print("🏥 New Medical Italian - Google Analytics Setup")
    print("=" * 50)
    
    if len(sys.argv) != 2:
        print("Usage: python update_analytics.py YOUR_GA4_MEASUREMENT_ID")
        print("")
        print("Steps to get your Measurement ID:")
        print("1. Go to https://analytics.google.com")
        print("2. Sign in with your 'Antonino Piacenza' account")
        print("3. Create a new property for: https://new-medical-italian.streamlit.app")
        print("4. Get your Measurement ID (format: G-XXXXXXXXXX)")
        print("5. Run: python update_analytics.py G-XXXXXXXXXX")
        sys.exit(1)
    
    measurement_id = sys.argv[1].strip()
    
    print(f"🔄 Updating Google Analytics Measurement ID to: {measurement_id}")
    print("")
    
    if update_analytics_id(measurement_id):
        print("")
        print("✅ Setup complete! Your app is now ready for Google Analytics tracking.")
    else:
        print("")
        print("❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

