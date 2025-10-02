#!/usr/bin/env python3
"""
Test the deployed Multi-Brand GPT Validator with Google Sheets integration
"""
import requests
import json

def test_deployed_api():
    """Test the deployed API endpoints"""
    base_url = "https://multi-brand-gpt-validator.onrender.com"
    token = "H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing Multi-Brand GPT Validator API...")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        if response.status_code == 200:
            print("   ✅ Health check passed")
        else:
            print("   ❌ Health check failed")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get All Brands (Google Sheets)
    print("\n2️⃣ Testing Brands Endpoint (Google Sheets)...")
    try:
        response = requests.get(f"{base_url}/brands", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {len(data.get('brands', []))} brands")
            print(f"   📊 Source: {data.get('source', 'unknown')}")
            if data.get('brands'):
                print(f"   🏷️  Brands: {[brand.get('name', 'Unknown') for brand in data['brands'][:3]]}...")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Get Specific Brand Info
    print("\n3️⃣ Testing Specific Brand Info...")
    try:
        response = requests.get(f"{base_url}/brands/Amar", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Brand: {data.get('brand', 'Unknown')}")
            print(f"   📝 Story: {data.get('story', '')[:100]}...")
            print(f"   🎯 Platforms: {data.get('platforms', [])}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Validate Content
    print("\n4️⃣ Testing Content Validation...")
    try:
        test_data = {
            "brand": "Amar",
            "platform": "Instagram",
            "caption": "Check out our latest refurbished phones!",
            "hashtags": ["#AmarMarketplace", "#RefurbishedPhones"],
            "cta": "Shop now",
            "media_suggestion": {
                "type": "single_image",
                "notes": "High-quality product photo"
            },
            "week": "W41",
            "post_id": "test_amar_ig_W41_001"
        }
        
        response = requests.post(f"{base_url}/validate", headers=headers, json=test_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Valid: {data.get('valid', False)}")
            if data.get('errors'):
                print(f"   ⚠️  Errors: {data.get('errors', [])}")
            if data.get('sha256'):
                print(f"   🔐 SHA256: {data.get('sha256', '')[:20]}...")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 Test Complete!")

if __name__ == "__main__":
    test_deployed_api()
