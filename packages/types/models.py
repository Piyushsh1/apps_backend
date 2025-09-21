from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum
import uuid

# Enums
class UserType(str, Enum):
    CUSTOMER = "CUSTOMER"
    SELLER = "SELLER"
    ADMIN = "ADMIN"

class CustomerCategory(str, Enum):
    FOOD_BUYER = "food_buyer"
    SERVICE_SEEKER = "service_seeker"
    GROCERY_BUYER = "grocery_buyer"
    GENERAL = "general"

class AdminRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    CATEGORY_MANAGER = "category_manager"
    USER_MANAGER = "user_manager"
    ORDER_MANAGER = "order_manager"

class SellerType(str, Enum):
    RESTAURANT = "restaurant"
    GROCERY_STORE = "grocery_store"
    SERVICE_PROVIDER = "service_provider"
    GENERAL_SELLER = "general_seller"

class ProductServiceType(str, Enum):
    PRODUCT = "product"
    SERVICE = "service"

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Base Model
class BaseModelWithID(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Pydantic Models for Database
class User(BaseModelWithID):
    email: str
    password_hash: str
    full_name: str
    phone: Optional[str] = None
    user_type: UserType
    customer_category: Optional[CustomerCategory] = None
    admin_role: Optional[AdminRole] = None
    seller_type: Optional[SellerType] = None
    is_active: bool = True
    
    # Additional fields for sellers
    business_name: Optional[str] = None
    business_address: Optional[str] = None
    business_description: Optional[str] = None
    
    # Additional fields for customers
    delivery_addresses: List[Dict[str, Any]] = Field(default_factory=list)

class Category(BaseModelWithID):
    name: str
    description: Optional[str] = None
    parent_category_id: Optional[str] = None
    is_active: bool = True
    created_by: str  # admin user id

class ProductService(BaseModelWithID):
    name: str
    description: str
    type: ProductServiceType
    category_id: str
    seller_id: str
    price: float
    images: List[str] = Field(default_factory=list)
    is_available: bool = True
    stock_quantity: Optional[int] = None  # For products
    service_duration: Optional[int] = None  # For services (in minutes)
    tags: List[str] = Field(default_factory=list)

class Order(BaseModelWithID):
    customer_id: str
    seller_id: str
    items: List[Dict[str, Any]]  # [{product_service_id, quantity, price}]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    delivery_address: Optional[Dict[str, Any]] = None
    special_instructions: Optional[str] = None
