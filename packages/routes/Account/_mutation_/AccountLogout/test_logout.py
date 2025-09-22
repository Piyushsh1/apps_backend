"""
Test script for Account Logout API
This script demonstrates how to use the logout API endpoints
"""

import asyncio
import aiohttp
import json

# Configuration
API_URL = "http://localhost:8001/graphql"
HEADERS = {"Content-Type": "application/json"}

# GraphQL Mutations
LOGOUT_MUTATION = """
mutation AccountLogout($token: String!, $input: LogoutInput) {
  accountLogout(token: $token, input: $input) {
    success
    message
  }
}
"""

LOGIN_MUTATION = """
mutation AccountLogin($input: UserLoginInput!) {
  accountLogin(input: $input) {
    token
    user {
      id
      email
      fullName
    }
    message
  }
}
"""

async def graphql_request(query, variables=None):
    """Make a GraphQL request"""
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=payload, headers=HEADERS) as response:
            return await response.json()

async def test_login():
    """Test login to get a token"""
    variables = {
        "input": {
            "email": "test@example.com",
            "password": "testpassword"
        }
    }
    
    result = await graphql_request(LOGIN_MUTATION, variables)
    print("Login Result:")
    print(json.dumps(result, indent=2))
    
    if "data" in result and result["data"]["accountLogin"]["token"]:
        return result["data"]["accountLogin"]["token"]
    return None

async def test_single_device_logout(token):
    """Test single device logout"""
    variables = {
        "token": token
    }
    
    result = await graphql_request(LOGOUT_MUTATION, variables)
    print("\nSingle Device Logout Result:")
    print(json.dumps(result, indent=2))

async def test_all_devices_logout(token):
    """Test all devices logout"""
    variables = {
        "token": token,
        "input": {
            "logoutAllDevices": True
        }
    }
    
    result = await graphql_request(LOGOUT_MUTATION, variables)
    print("\nAll Devices Logout Result:")
    print(json.dumps(result, indent=2))

async def test_invalid_token_logout():
    """Test logout with invalid token"""
    variables = {
        "token": "invalid.token.here"
    }
    
    result = await graphql_request(LOGOUT_MUTATION, variables)
    print("\nInvalid Token Logout Result:")
    print(json.dumps(result, indent=2))

async def main():
    """Run all tests"""
    print("=== Account Logout API Test Suite ===\n")
    
    # Test 1: Login to get a valid token
    print("1. Testing Login (to get token)...")
    token = await test_login()
    
    if not token:
        print("❌ Could not get token from login. Make sure a test user exists.")
        return
    
    print(f"✅ Got token: {token[:20]}...")
    
    # Test 2: Single device logout
    print("\n2. Testing Single Device Logout...")
    await test_single_device_logout(token)
    
    # Test 3: Get another token for all devices logout test
    print("\n3. Getting new token for all devices logout test...")
    token2 = await test_login()
    
    if token2:
        print("\n4. Testing All Devices Logout...")
        await test_all_devices_logout(token2)
    
    # Test 4: Invalid token
    print("\n5. Testing Invalid Token Logout...")
    await test_invalid_token_logout()
    
    print("\n=== Test Suite Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
