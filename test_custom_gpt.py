#!/usr/bin/env python3
"""
Test script for Custom GPT integration
"""

import requests
import json

def test_custom_gpt_integration():
    """Test the Custom GPT integration endpoints"""
    
    base_url = "https://multi-brand-gpt-validator.onrender.com"
    token = "H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("🤖 Testing Custom GPT Integration...")
    print("=" * 50)
    
    # Test 1: Get all brands
    print("\n1️⃣ Testing getBrandInfo (get all brands)...")
    try:
        response = requests.get(f"{base_url}/brands", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {len(data.get('brands', []))} brands")
            print(f"   📊 Source: {data.get('source', 'unknown')}")
            brands = [brand.get('name', 'Unknown') for brand in data.get('brands', [])]
            print(f"   🏷️  Brands: {brands[:3]}...")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 2: Get specific brand info
    print("\n2️⃣ Testing getBrandInfo (specific brand)...")
    try:
        response = requests.get(f"{base_url}/brands/Amar", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Brand: {data.get('brand', 'Unknown')}")
            print(f"   📝 Story: {data.get('story', 'No story')[:50]}...")
            print(f"   🎯 Platforms: {data.get('platforms', [])[:3]}...")
            print(f"   🏷️  Hashtag banks: {list(data.get('hashtag_banks', {}).keys())}")
            print(f"   📢 CTA banks: {list(data.get('cta_banks', {}).keys())}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    # Test 3: Validate content
    print("\n3️⃣ Testing validateContent...")
    test_content = {
        "brand": "Amar",
        "platform": "Instagram",
        "caption": "Discover our premium refurbished phones! Quality guaranteed, prices that won't break the bank. Perfect for students and professionals alike.",
        "hashtags": ["#AmarMarketplace", "#RefurbishedPhones", "#QualityGuaranteed"],
        "cta": "Shop now",
        "media_suggestion": {
            "type": "carousel",
            "count": 3,
            "notes": "High-quality product photos showing different angles"
        },
        "links": [
            {
                "url": "https://amar.co.uk/products",
                "utm": True
            }
        ],
        "week": "W41",
        "post_id": "amar_ig_test_001"
    }
    
    try:
        response = requests.post(f"{base_url}/validate", headers=headers, json=test_content)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Valid: {data.get('valid', False)}")
            print(f"   📋 Errors: {data.get('errors', [])}")
            if data.get('sha256'):
                print(f"   🔐 SHA256: {data['sha256'][:20]}...")
            if data.get('proof_file'):
                print(f"   📄 Proof: {data['proof_file']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   📄 Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Custom GPT Integration Test Complete!")
    print("\n📋 Next Steps:")
    print("1. Copy the OpenAPI schema from custom_gpt_openapi_schema.json")
    print("2. Paste it into your Custom GPT Actions")
    print("3. Set authentication token: H1s7_weAheYVOIcWlZsiHykdDt-faaSx6lz0oAe56C0")
    print("4. Use the instructions from custom_gpt_instructions.md")
    print("5. Test with: 'Create an Instagram post for Amar brand'")

if __name__ == "__main__":
    test_custom_gpt_integration()
