#!/usr/bin/env python3
"""
Debug script to check Google Sheets data structure
"""

import os
import json
from google_sheets_service import GoogleSheetsService

def debug_google_sheets():
    """Debug the Google Sheets data structure"""
    
    print("🔍 Debugging Google Sheets Data Structure...")
    print("=" * 50)
    
    try:
        # Initialize service
        sheets_service = GoogleSheetsService()
        
        if not sheets_service.is_available():
            print("❌ Google Sheets service not available")
            return
        
        print("✅ Google Sheets service initialized")
        
        # Get all brands
        brands = sheets_service.get_all_brands()
        print(f"📊 Found {len(brands)} brands: {brands}")
        
        # Check Amar brand specifically
        if 'Amar' in brands:
            print(f"\n🔍 Checking Amar brand data...")
            
            # Get raw data
            raw_data = sheets_service.get_sheet_data('Amar')
            print(f"📋 Raw data rows: {len(raw_data)}")
            
            if raw_data:
                print(f"📋 Headers: {raw_data[0]}")
                print(f"📋 First few rows:")
                for i, row in enumerate(raw_data[:5]):
                    print(f"   Row {i}: {row}")
            
            # Get processed config
            config = sheets_service.get_brand_config('Amar')
            print(f"\n⚙️ Processed config:")
            print(f"   Brand: {config.get('brand')}")
            print(f"   Platforms: {config.get('platforms')}")
            print(f"   Voice: {config.get('voice')}")
            print(f"   Story: {config.get('story')}")
            print(f"   Hashtag bank: {config.get('hashtag_bank')}")
            print(f"   CTA bank: {config.get('cta_bank')}")
            print(f"   Media policy: {config.get('media_policy')}")
            
        else:
            print(f"❌ Amar brand not found in sheets")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_google_sheets()
