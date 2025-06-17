#!/usr/bin/env python3
"""
Analytics Setup Assistant for New Medical Italian
Guides through setting up real tracking IDs
"""

import webbrowser
import time

def setup_analytics():
    """Interactive setup for analytics tracking IDs"""
    print("🚀 ANALYTICS ACTIVATION WIZARD")
    print("=" * 50)
    
    print("\n📊 Step 1: Google Analytics 4 Setup")
    print("-" * 35)
    
    print("I'll open Google Analytics for you...")
    time.sleep(2)
    webbrowser.open('https://analytics.google.com')
    
    print("\n📋 Follow these steps in Google Analytics:")
    setup_steps = [
        "1. Click 'Start measuring' or 'Get started'",
        "2. Create Account: Name it 'New Medical Italian AI'", 
        "3. Create Property: Name it 'Italian Medical AI Demo'",
        "4. Select Industry: 'Health & Medicine'",
        "5. Choose 'Web' platform",
        "6. Enter website URL: http://localhost:8501 (or your domain)",
        "7. Accept terms and create property"
    ]
    
    for step in setup_steps:
        print(f"   {step}")
    
    print("\n⚠️  IMPORTANT: After creating the property, you'll see:")
    print("   'Measurement ID: G-XXXXXXXXXX'")
    print("   📝 COPY THIS ID - you'll need it next!")
    
    input("\nPress Enter when you have your GA4 Measurement ID...")
    
    # Get GA4 ID from user
    ga4_id = input("\n📊 Enter your GA4 Measurement ID (format: G-XXXXXXXXXX): ").strip()
    
    while not ga4_id.startswith('G-') or len(ga4_id) < 10:
        print("❌ Invalid format. Should be G-XXXXXXXXXX")
        ga4_id = input("Enter GA4 ID again: ").strip()
    
    print(f"✅ GA4 ID saved: {ga4_id}")
    
    # Optional: Google Ads setup
    print("\n💰 Step 2: Google Ads Setup (Optional but Recommended)")
    print("-" * 55)
    
    setup_ads = input("Do you want to set up Google Ads tracking? (y/n): ").lower().startswith('y')
    
    ads_id = None
    conversion_label = None
    contact_label = None
    
    if setup_ads:
        print("\nOpening Google Ads...")
        webbrowser.open('https://ads.google.com')
        
        print("\n📋 Google Ads Setup Steps:")
        ads_steps = [
            "1. Create Google Ads account (if you don't have one)",
            "2. Go to 'Tools & Settings' → 'Conversions'",
            "3. Click '+ New conversion action'",
            "4. Select 'Website'",
            "5. Create conversion: 'Medical AI Demo Completed'",
            "6. Category: 'Lead', Value: €25, Count: 'One'",
            "7. Create another: 'Contact Sales Intent'", 
            "8. Category: 'Lead', Value: €100, Count: 'One'"
        ]
        
        for step in ads_steps:
            print(f"   {step}")
        
        input("\nPress Enter when you've created conversions...")
        
        ads_id = input("\n💰 Enter Google Ads ID (format: AW-XXXXXXXXX): ").strip()
        while not ads_id.startswith('AW-'):
            print("❌ Invalid format. Should be AW-XXXXXXXXX")
            ads_id = input("Enter Google Ads ID again: ").strip()
        
        conversion_label = input("📊 Enter 'Demo Completed' conversion label: ").strip()
        contact_label = input("📞 Enter 'Contact Sales' conversion label: ").strip()
        
        print(f"✅ Google Ads ID: {ads_id}")
        print(f"✅ Demo conversion label: {conversion_label}")
        print(f"✅ Contact conversion label: {contact_label}")
    
    # Optional: Facebook Pixel
    print("\n📘 Step 3: Facebook Pixel Setup (Optional)")
    print("-" * 40)
    
    setup_facebook = input("Do you want to set up Facebook Pixel? (y/n): ").lower().startswith('y')
    
    facebook_id = None
    
    if setup_facebook:
        print("\nOpening Facebook Business Manager...")
        webbrowser.open('https://business.facebook.com')
        
        print("\n📋 Facebook Pixel Setup:")
        fb_steps = [
            "1. Go to 'Events Manager'",
            "2. Click 'Connect Data Sources' → 'Web'", 
            "3. Select 'Facebook Pixel'",
            "4. Name it 'New Medical Italian AI Pixel'",
            "5. Enter website URL",
            "6. Copy the Pixel ID (15-16 digit number)"
        ]
        
        for step in fb_steps:
            print(f"   {step}")
        
        input("\nPress Enter when you have your Facebook Pixel ID...")
        
        facebook_id = input("\n📘 Enter Facebook Pixel ID (numbers only): ").strip()
        while not facebook_id.isdigit() or len(facebook_id) < 10:
            print("❌ Invalid format. Should be a 15-16 digit number")
            facebook_id = input("Enter Facebook Pixel ID again: ").strip()
        
        print(f"✅ Facebook Pixel ID: {facebook_id}")
    
    # Update the app.py file
    print("\n🔧 Step 4: Updating Your App")
    print("-" * 30)
    
    return {
        'ga4_id': ga4_id,
        'ads_id': ads_id or 'AW-XXXXXXXXX',
        'facebook_id': facebook_id or 'XXXXXXXXXX',
        'conversion_label': conversion_label or 'XXXXXXXXX',
        'contact_label': contact_label or 'XXXXXXXXX'
    }

def update_app_with_ids(tracking_ids):
    """Update app.py with real tracking IDs"""
    print("\n🔧 Updating app.py with your tracking IDs...")
    
    # Read current app.py
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create backup
    with open('app.py.backup', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ Backup created: app.py.backup")
    
    # Replace placeholder IDs
    replacements = {
        'G-XXXXXXXXXX': tracking_ids['ga4_id'],
        'AW-XXXXXXXXX': tracking_ids['ads_id'], 
        'FACEBOOK_PIXEL_ID': tracking_ids['facebook_id'],
        'CONVERSION_LABEL': tracking_ids['conversion_label'],
        'CONTACT_CONVERSION_LABEL': tracking_ids['contact_label']
    }
    
    updated_content = content
    for placeholder, real_id in replacements.items():
        if real_id != placeholder and real_id not in ['XXXXXXXXX', 'XXXXXXXXXX']:
            updated_content = updated_content.replace(placeholder, real_id)
            print(f"✅ Replaced {placeholder} with {real_id}")
        else:
            print(f"⏭️  Skipped {placeholder} (not provided)")
    
    # Write updated content
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("\n🎉 App updated successfully!")
    print("\n📊 Your analytics are now active!")
    
    print("\n🚀 Next Steps:")
    print("-" * 15)
    next_steps = [
        "1. Restart your Streamlit app",
        "2. Test the analytics by running demos", 
        "3. Check Google Analytics in 24-48 hours for data",
        "4. Monitor conversions in Google Ads (if set up)",
        "5. Check Facebook Events Manager (if set up)"
    ]
    
    for step in next_steps:
        print(f"   {step}")
    
    print("\n🎯 Testing Your Setup:")
    print("-" * 20)
    print("• Visit your app and enter an email")
    print("• Run a demo analysis")
    print("• Click 'Contact Sales' button")
    print("• Check browser developer tools for tracking events")
    
    return True

if __name__ == "__main__":
    try:
        tracking_ids = setup_analytics()
        update_app_with_ids(tracking_ids)
        
        print("\n" + "=" * 50)
        print("🎉 ANALYTICS ACTIVATION COMPLETE!")
        print("=" * 50)
        print("Your visitor tracking is now fully active.")
        print("Data will appear in your analytics dashboards within 24-48 hours.")
        
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
    except Exception as e:
        print(f"\n\n❌ Error during setup: {e}")
        print("Please check your inputs and try again.")

