#!/usr/bin/env python3
"""
Test script for Multi-Brand GPT Validator API
Run this to verify your API is working correctly
"""

import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"  # Change to your deployed URL
API_TOKEN = "change-me"  # Change to your actual token

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
            return True
        else:
            print("❌ Health check failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Health check error:", e)
        return False

def test_validation():
    """Test the validation endpoint"""
    print("\n🔍 Testing validation endpoint...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Test data
    test_data = {
        "brand": "Amar",
        "platform": "Instagram",
        "caption": "Test post for validation",
        "hashtags": ["#AmarMarketplace"],
        "cta": "Learn more",
        "media_suggestion": {
            "type": "single_image",
            "count": 1
        },
        "links": [{
            "url": "https://amar.co.uk/test",
            "utm": True
        }],
        "week": "W41",
        "post_id": "test_001"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/validate",
            headers=headers,
            json=test_data
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("valid"):
                print("✅ Validation test passed!")
                print(f"   SHA256: {result.get('sha256', 'N/A')[:16]}...")
                print(f"   Proof file: {result.get('proof_file', 'N/A')}")
            else:
                print("⚠️  Validation test failed (expected behavior):")
                print(f"   Errors: {result.get('errors', [])}")
            return True
        else:
            print("❌ Validation test failed:", response.status_code)
            print("   Response:", response.text)
            return False
    except Exception as e:
        print("❌ Validation test error:", e)
        return False

def test_banks():
    """Test the banks endpoint"""
    print("\n🔍 Testing banks endpoint...")
    
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/banks/Amar",
            headers=headers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Banks test passed!")
            print(f"   Brand: {result.get('brand', 'N/A')}")
            print(f"   Available keys: {len(result.get('keys', []))}")
            return True
        else:
            print("❌ Banks test failed:", response.status_code)
            return False
    except Exception as e:
        print("❌ Banks test error:", e)
        return False

def main():
    """Run all tests"""
    print("🚀 Multi-Brand GPT Validator API Test Suite")
    print("=" * 50)
    
    tests = [
        test_health,
        test_validation,
        test_banks
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    print("\n💡 Next steps:")
    print("1. Deploy your API to a hosting service")
    print("2. Update API_BASE_URL in this script")
    print("3. Create your Custom GPT with the validator action")
    print("4. Test with real content generation")

if __name__ == "__main__":
    main()
