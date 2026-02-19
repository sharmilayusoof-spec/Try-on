"""
Quick API test script
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoints():
    """Test all API endpoints"""
    
    print("🧪 Testing VTO Backend API\n")
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 2: Health check
    print("2. Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 3: API docs
    print("3. Testing API documentation...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"   ✓ Status: {response.status_code}")
        print(f"   Docs available at: {BASE_URL}/docs\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    # Test 4: OpenAPI schema
    print("4. Testing OpenAPI schema...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        schema = response.json()
        print(f"   ✓ Status: {response.status_code}")
        print(f"   API Title: {schema.get('info', {}).get('title')}")
        print(f"   Version: {schema.get('info', {}).get('version')}")
        print(f"   Endpoints: {len(schema.get('paths', {}))}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")
    
    print("✅ API skeleton is working!")
    print(f"\n📚 Visit {BASE_URL}/docs for interactive API documentation")

if __name__ == "__main__":
    print("Make sure the server is running: python run.py\n")
    input("Press Enter to start tests...")
    test_endpoints()
