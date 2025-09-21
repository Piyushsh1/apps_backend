import strawberry
from typing import Optional, List

# Output Types
@strawberry.type
class UserGraphQL:
    id: str
    email: str
    full_name: str = strawberry.field(name="fullName")
    phone: Optional[str]
    user_type: str = strawberry.field(name="userType")
    customer_category: Optional[str] = strawberry.field(name="customerCategory")
    admin_role: Optional[str] = strawberry.field(name="adminRole")
    seller_type: Optional[str] = strawberry.field(name="sellerType")
    is_active: bool = strawberry.field(name="isActive")
    business_name: Optional[str] = strawberry.field(name="businessName")
    business_address: Optional[str] = strawberry.field(name="businessAddress")
    business_description: Optional[str] = strawberry.field(name="businessDescription")
    created_at: str = strawberry.field(name="createdAt")

@strawberry.type
class CategoryGraphQL:
    id: str
    name: str
    description: Optional[str]
    parent_category_id: Optional[str]
    is_active: bool
    created_by: str
    created_at: str

@strawberry.type
class ProductServiceGraphQL:
    id: str
    name: str
    description: str
    type: str
    category_id: str
    seller_id: str
    price: float
    images: List[str]
    is_available: bool
    stock_quantity: Optional[int]
    service_duration: Optional[int]
    tags: List[str]
    created_at: str

@strawberry.type
class OrderGraphQL:
    id: str
    customer_id: str
    seller_id: str
    items: str  # JSON string
    total_amount: float
    status: str
    delivery_address: Optional[str]  # JSON string
    special_instructions: Optional[str]
    created_at: str

@strawberry.type
class AuthResponse:
    token: str
    user: UserGraphQL
    message: str

@strawberry.type
class SuccessResponse:
    success: bool
    message: str

@strawberry.type
class ErrorResponse:
    error: str
    message: str

# Pagination Types
@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]

@strawberry.type
class UserConnection:
    edges: List['UserEdge']
    page_info: PageInfo
    total_count: int

@strawberry.type
class UserEdge:
    node: UserGraphQL
    cursor: str

@strawberry.type
class CategoryConnection:
    edges: List['CategoryEdge']
    page_info: PageInfo
    total_count: int

@strawberry.type
class CategoryEdge:
    node: CategoryGraphQL
    cursor: str

@strawberry.type
class ProductServiceConnection:
    edges: List['ProductServiceEdge']
    page_info: PageInfo
    total_count: int

@strawberry.type
class ProductServiceEdge:
    node: ProductServiceGraphQL
    cursor: str

@strawberry.type
class OrderConnection:
    edges: List['OrderEdge']
    page_info: PageInfo
    total_count: int

@strawberry.type
class OrderEdge:
    node: OrderGraphQL
    cursor: str
