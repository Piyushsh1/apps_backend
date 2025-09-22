# Account Logout API

## Overview
The Account Logout API provides secure token invalidation for user sessions. It supports two logout modes:
1. **Single Device Logout**: Invalidates the current session token only
2. **All Devices Logout**: Invalidates all active sessions for the user across all devices

## GraphQL Mutation

```graphql
mutation AccountLogout($token: String!, $input: LogoutInput) {
  accountLogout(token: $token, input: $input) {
    success
    message
  }
}
```

## Input Types

### LogoutInput
```graphql
input LogoutInput {
  logoutAllDevices: Boolean # Optional, defaults to false
}
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `token` | String | Yes | JWT authentication token to be invalidated |
| `input.logoutAllDevices` | Boolean | No | If true, logs out from all devices. Defaults to false |

## Response

### SuccessResponse
```graphql
type SuccessResponse {
  success: Boolean!
  message: String!
}
```

## Usage Examples

### Single Device Logout
```graphql
mutation {
  accountLogout(token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...") {
    success
    message
  }
}
```

### All Devices Logout
```graphql
mutation {
  accountLogout(
    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    input: { logoutAllDevices: true }
  ) {
    success
    message
  }
}
```

## Response Examples

### Successful Logout
```json
{
  "data": {
    "accountLogout": {
      "success": true,
      "message": "Logged out successfully"
    }
  }
}
```

### Successful All Devices Logout
```json
{
  "data": {
    "accountLogout": {
      "success": true,
      "message": "Logged out from all devices successfully"
    }
  }
}
```

### Invalid Token
```json
{
  "data": {
    "accountLogout": {
      "success": false,
      "message": "Invalid or expired token"
    }
  }
}
```

### Already Logged Out
```json
{
  "data": {
    "accountLogout": {
      "success": false,
      "message": "Token already invalidated"
    }
  }
}
```

## Error Handling

The API handles the following error scenarios:

1. **Invalid Token**: Token is malformed, expired, or doesn't exist
2. **Already Blacklisted**: Token has already been invalidated
3. **Logout Failed**: Database operation failed or token format issues
4. **Server Error**: Unexpected server-side errors

## Security Features

### Token Blacklisting
- Individual tokens are stored in a blacklist database
- Blacklisted tokens are checked on every authentication request
- Expired blacklisted tokens are automatically cleaned up

### All Devices Logout
- Uses a timestamp-based approach for efficiency
- Stores user's logout timestamp instead of blacklisting all tokens individually
- All tokens issued before the logout timestamp become invalid

### Automatic Cleanup
- Expired blacklisted tokens are automatically removed
- Cleanup runs periodically to maintain database performance
- Manual cleanup can be triggered using the token cleanup utility

## Database Collections

### blacklisted_tokens
```javascript
{
  _id: ObjectId,
  id: String,
  token: String,
  user_id: String,
  blacklisted_at: Date,
  expires_at: Date,
  created_at: Date,
  updated_at: Date
}
```

### user_logout_timestamps
```javascript
{
  _id: ObjectId,
  user_id: String,
  logout_timestamp: Date,
  updated_at: Date
}
```

## Maintenance

### Token Cleanup Utility
A cron job utility is provided to clean up expired tokens:

```bash
# Run the cleanup script
python packages/cron/token_cleanup.py
```

### Recommended Cron Schedule
```bash
# Clean up expired tokens every hour
0 * * * * cd /path/to/project && python packages/cron/token_cleanup.py
```

## Integration Notes

### Client-Side Implementation
After successful logout:
1. Remove token from client storage (localStorage, cookies, etc.)
2. Redirect to login page
3. Clear any cached user data

### Server-Side Middleware
The authentication middleware automatically:
1. Checks token blacklist status
2. Validates tokens against logout-all timestamps
3. Returns null for invalidated tokens

## Testing

### Test Cases
1. Valid token logout
2. Invalid token handling
3. Already blacklisted token
4. All devices logout functionality
5. Token validation after logout
6. Cleanup utility functionality

### GraphQL Playground
Test the API using the GraphQL Playground at `/graphql` endpoint.
