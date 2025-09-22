# Product and User Management APIs

## Overview
This document provides comprehensive documentation for the Product Creation, Product Management, User Profile, and Wishlist APIs.

## Table of Contents
1. [Product Creation API](#product-creation-api)
2. [Product Query APIs](#product-query-apis)
3. [Product Update API](#product-update-api)
4. [User Profile Update API](#user-profile-update-api)
5. [Wishlist APIs](#wishlist-apis)

---

## Product Creation API

### GraphQL Mutation
```graphql
mutation ProductCreate($input: ProductServiceInput!, $token: String!) {
  productCreate(input: $input, token: $token) {
    id
    name
    description
    type
    categoryId
    sellerId
    price
    images
    isAvailable
    stockQuantity
    serviceDuration
    tags
    createdAt
  }
}
```

### Input Type
```graphql
input ProductServiceInput {
  name: String!
  description: String!
  type: ProductServiceType!  # PRODUCT or SERVICE
  categoryId: String!        # Must be valid active category
  price: Float!             # Must be > 0
  images: [String!]
  stockQuantity: Int        # Required for PRODUCT type
  serviceDuration: Int      # Required for SERVICE type (in minutes)
  tags: [String!]
}
```

### Features
- **Category Validation**: Ensures the specified category exists and is active
- **Seller Authentication**: Only authenticated sellers can create products
- **Type Validation**: Validates PRODUCT vs SERVICE requirements
- **Price Validation**: Ensures price is positive
- **Stock Management**: Handles inventory for products
- **Service Duration**: Manages time-based services

### Example Usage
```graphql
mutation {
  productCreate(
    input: {
      name: "Premium Coffee Beans"
      description: "High-quality arabica coffee beans"
      type: PRODUCT
      categoryId: "cat_123"
      price: 29.99
      stockQuantity: 100
      tags: ["coffee", "organic", "premium"]
      images: ["image1.jpg", "image2.jpg"]
    }
    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  ) {
    id
    name
    price
    stockQuantity
  }
}
```

---

## Product Query APIs

### Product List Query
```graphql
query ProductList(
  $categoryId: String
  $sellerId: String
  $isAvailable: Boolean
  $productType: String
  $limit: Int
) {
  productList(
    categoryId: $categoryId
    sellerId: $sellerId
    isAvailable: $isAvailable
    productType: $productType
    limit: $limit
  ) {
    id
    name
    description
    type
    categoryId
    sellerId
    price
    images
    isAvailable
    stockQuantity
    serviceDuration
    tags
    createdAt
  }
}
```

### Product Get Query
```graphql
query ProductGet($productId: String!) {
  productGet(productId: $productId) {
    id
    name
    description
    type
    categoryId
    sellerId
    price
    images
    isAvailable
    stockQuantity
    serviceDuration
    tags
    createdAt
  }
}
```

### Filter Options
- **categoryId**: Filter by category
- **sellerId**: Filter by seller
- **isAvailable**: Show only available/unavailable products
- **productType**: Filter by PRODUCT or SERVICE
- **limit**: Maximum results (default: 50, max: 100)

---

## Product Update API

### GraphQL Mutation
```graphql
mutation ProductUpdate(
  $productId: String!
  $input: ProductServiceUpdateInput!
  $token: String!
) {
  productUpdate(productId: $productId, input: $input, token: $token) {
    success
    message
  }
}
```

### Input Type
```graphql
input ProductServiceUpdateInput {
  name: String
  description: String
  price: Float
  images: [String!]
  stockQuantity: Int
  serviceDuration: Int
  tags: [String!]
  isAvailable: Boolean
}
```

### Features
- **Ownership Verification**: Only the seller who created the product can update it
- **Selective Updates**: Update only the fields you want to change
- **Validation**: Maintains business rules (positive price, valid stock, etc.)
- **Availability Toggle**: Enable/disable product visibility

---

## User Profile Update API

### Enhanced Profile Update
```graphql
mutation AccountUpdate($input: UserProfileUpdateInput!, $token: String!) {
  accountUpdate(input: $input, token: $token) {
    id
    email
    fullName
    phone
    userType
    customerCategory
    adminRole
    sellerType
    isActive
    businessName
    businessAddress
    businessDescription
    createdAt
  }
}
```

### Input Type
```graphql
input UserProfileUpdateInput {
  fullName: String
  phone: String
  businessName: String          # Sellers only
  businessAddress: String       # Sellers only
  businessDescription: String   # Sellers only
  customerCategory: CustomerCategory  # Customers only
  sellerType: SellerType        # Sellers only
}
```

### Delivery Address Management
```graphql
# Add delivery address
mutation AddDeliveryAddress($input: DeliveryAddressInput!, $token: String!) {
  addDeliveryAddress(input: $input, token: $token) {
    success
    message
  }
}

# Remove delivery address
mutation RemoveDeliveryAddress($addressId: String!, $token: String!) {
  removeDeliveryAddress(addressId: $addressId, token: $token) {
    success
    message
  }
}
```

### Delivery Address Input
```graphql
input DeliveryAddressInput {
  street: String!
  city: String!
  state: String!
  postalCode: String!
  country: String!
  isDefault: Boolean
}
```

---

## Wishlist APIs

### Add to Wishlist
```graphql
mutation WishlistAdd($productId: String!, $token: String!) {
  wishlistAdd(productId: $productId, token: $token) {
    success
    message
  }
}
```

### Remove from Wishlist
```graphql
mutation WishlistRemove($productId: String!, $token: String!) {
  wishlistRemove(productId: $productId, token: $token) {
    success
    message
  }
}
```

### Get Wishlist
```graphql
query WishlistGet($token: String!) {
  wishlistGet(token: $token) {
    id
    name
    description
    type
    categoryId
    sellerId
    price
    images
    isAvailable
    stockQuantity
    serviceDuration
    tags
    createdAt
  }
}
```

### Features
- **Customer Only**: Only customers can manage wishlists
- **Duplicate Prevention**: Prevents adding the same product twice
- **Availability Filter**: Only shows available products in wishlist
- **Product Details**: Returns full product information with wishlist items

---

## Complete Example Workflows

### Creating a Product
```graphql
# 1. First, get categories to choose from
query {
  categoryList {
    id
    name
    description
  }
}

# 2. Create the product
mutation {
  productCreate(
    input: {
      name: "Handmade Pottery"
      description: "Beautiful handcrafted ceramic pottery"
      type: PRODUCT
      categoryId: "cat_home_decor"
      price: 45.00
      stockQuantity: 25
      tags: ["handmade", "ceramic", "pottery", "home-decor"]
      images: ["pottery1.jpg", "pottery2.jpg"]
    }
    token: "seller_token_here"
  ) {
    id
    name
    price
    stockQuantity
  }
}
```

### Managing User Profile
```graphql
# Update seller profile
mutation {
  accountUpdate(
    input: {
      fullName: "John Smith"
      phone: "+1234567890"
      businessName: "Smith's Pottery Studio"
      businessAddress: "123 Art Street, Creative City, CC 12345"
      businessDescription: "Specializing in handcrafted ceramic pottery and home decor items"
      sellerType: GENERAL_SELLER
    }
    token: "user_token_here"
  ) {
    fullName
    businessName
    sellerType
  }
}

# Add delivery address for customer
mutation {
  addDeliveryAddress(
    input: {
      street: "456 Main Street"
      city: "Hometown"
      state: "ST"
      postalCode: "12345"
      country: "USA"
      isDefault: true
    }
    token: "customer_token_here"
  ) {
    success
    message
  }
}
```

### Wishlist Management
```graphql
# Add product to wishlist
mutation {
  wishlistAdd(productId: "prod_123", token: "customer_token") {
    success
    message
  }
}

# View wishlist
query {
  wishlistGet(token: "customer_token") {
    id
    name
    price
    images
    isAvailable
  }
}

# Remove from wishlist
mutation {
  wishlistRemove(productId: "prod_123", token: "customer_token") {
    success
    message
  }
}
```

---

## Database Collections

### products
```javascript
{
  _id: ObjectId,
  id: String,
  name: String,
  description: String,
  type: String, // "product" or "service"
  category_id: String,
  seller_id: String,
  price: Number,
  images: [String],
  is_available: Boolean,
  stock_quantity: Number, // for products
  service_duration: Number, // for services (minutes)
  tags: [String],
  created_at: Date,
  updated_at: Date
}
```

### wishlists
```javascript
{
  _id: ObjectId,
  id: String,
  user_id: String,
  product_id: String,
  created_at: Date,
  updated_at: Date
}
```

---

## Error Handling

### Common Error Scenarios
1. **Authentication Required**: Invalid or missing token
2. **Permission Denied**: Wrong user type for operation
3. **Resource Not Found**: Product, category, or user doesn't exist
4. **Validation Errors**: Invalid input data
5. **Duplicate Operations**: Adding existing wishlist item

### Error Response Format
```json
{
  "errors": [
    {
      "message": "Only sellers can create products",
      "path": ["productCreate"],
      "extensions": {
        "code": "PERMISSION_DENIED"
      }
    }
  ]
}
```

---

## Testing Examples

Use GraphQL Playground at `/graphql` to test all APIs. Make sure to:
1. Create seller and customer accounts first
2. Create categories before creating products
3. Use valid authentication tokens
4. Test with different user types to verify permissions
