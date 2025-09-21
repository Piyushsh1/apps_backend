import strawberry
from typing import Optional, List
from enum import Enum

# Enums
@strawberry.enum
class UserType(str, Enum):
    CUSTOMER = "CUSTOMER"
    SELLER = "SELLER"
    ADMIN = "ADMIN"

@strawberry.enum
class CustomerCategory(str, Enum):
    FOOD_BUYER = "food_buyer"
    SERVICE_SEEKER = "service_seeker"
    GROCERY_BUYER = "grocery_buyer"
    GENERAL = "general"

@strawberry.enum
class AdminRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    CATEGORY_MANAGER = "category_manager"
    USER_MANAGER = "user_manager"
    ORDER_MANAGER = "order_manager"

@strawberry.enum
class SellerType(str, Enum):
    RESTAURANT = "restaurant"
    GROCERY_STORE = "grocery_store"
    SERVICE_PROVIDER = "service_provider"
    GENERAL_SELLER = "general_seller"

@strawberry.enum
class ProductServiceType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"

@strawberry.enum
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Input Types
@strawberry.input
class UserRegisterInput:
    email: str
    password: str
    full_name: str
    phone: Optional[str] = None
    user_type: UserType
    customer_category: Optional[CustomerCategory] = None
    admin_role: Optional[AdminRole] = None
    seller_type: Optional[SellerType] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_description: Optional[str] = None

@strawberry.input
class UserLoginInput:
    email: str
    password: str

@strawberry.input
class CategoryInput:
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[str] = None

@strawberry.input
class ProductServiceInput:
    name: str
    description: str
    type: ProductServiceType
    category_id: str
    price: float
    images: Optional[List[str]] = None
    stock_quantity: Optional[int] = None
    service_duration: Optional[int] = None
    tags: Optional[List[str]] = None

@strawberry.input
class OrderInput:
    seller_id: str
    items: str  # JSON string of items
    delivery_address: Optional[str] = None  # JSON string
    special_instructions: Optional[str] = None

@strawberry.input
class UserUpdateInput:
    full_name: Optional[str] = None
    phone: Optional[str] = None
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_description: Optional[str] = None

@strawberry.input
class CategoryUpdateInput:
    name: Optional[str] = None
    description: Optional[str] = None
    parent_category_id: Optional[str] = None
    is_active: Optional[bool] = None

@strawberry.input
class ProductServiceUpdateInput:
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    images: Optional[List[str]] = None
    stock_quantity: Optional[int] = None
    service_duration: Optional[int] = None
    tags: Optional[List[str]] = None
    is_available: Optional[bool] = None

@strawberry.input
class OrderUpdateInput:
    status: Optional[OrderStatus] = None
    special_instructions: Optional[str] = None
