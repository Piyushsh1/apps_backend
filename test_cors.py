#!/usr/bin/env python3
"""
Simple script to test CORS configuration
"""

import requests
import sys

def test_cors():
    base_url = "http://127.0.0.1:8001"
    
    print("Testing CORS configuration...")
    
    # Test OPTIONS request to GraphQL endpoint
    try:
        response = requests.options(
            f"{base_url}/graphql",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
                "Access-Control-Request-Headers": "Content-Type, Authorization"
            }
        )
        
        print(f"OPTIONS /graphql - Status: {response.status_code}")
        print("Response headers:")
        for header, value in response.headers.items():
            if header.lower().startswith('access-control'):
                print(f"  {header}: {value}")
        
        if response.status_code == 200:
            print("✅ CORS preflight request successful!")
        else:
            print("❌ CORS preflight request failed!")
            
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running on http://127.0.0.1:8001")
        print("Please start the server first with: uvicorn main:app --host 0.0.0.0 --port 8001")
        sys.exit(1)
    
    # Test actual GraphQL request
    try:
        response = requests.post(
            f"{base_url}/graphql",
            json={
                "query": "{ __schema { types { name } } }"
            },
            headers={
                "Content-Type": "application/json",
                "Origin": "http://localhost:3000"
            }
        )
        
        print(f"\nPOST /graphql (introspection) - Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ GraphQL introspection successful!")
        else:
            print("❌ GraphQL request failed!")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error testing GraphQL: {e}")

if __name__ == "__main__":
    test_cors()
