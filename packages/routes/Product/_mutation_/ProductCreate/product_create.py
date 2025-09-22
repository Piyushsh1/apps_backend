import strawberry
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
from typing import List, Optional

from packages.types.inputs import ProductServiceInput
from packages.types.outputs import ProductServiceGraphQL
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType, SellerType, ProductService, ProductServiceType

@strawberry.type
class ProductCreate:
    @strawberry.mutation
    async def product_create(self, info, input: ProductServiceInput, token: str) -> ProductServiceGraphQL:
        """
        Create a new product/service with category validation
        Only sellers can create products
        """
        db = info.context["db"]
        
        # Verify authenticated seller
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.SELLER:
            raise Exception("Only sellers can create products")
        
        # Validate category exists and is active
        category = await db.categories.find_one({
            "id": input.category_id,
            "is_active": True
        })
        if not category:
            raise Exception("Invalid or inactive category")
        
        # Validate product type
        if input.type not in [ProductServiceType.PRODUCT, ProductServiceType.SERVICE]:
            raise Exception("Invalid product type. Must be PRODUCT or SERVICE")
        
        # Validate stock quantity for products
        if input.type == ProductServiceType.PRODUCT and (input.stock_quantity is None or input.stock_quantity < 0):
            raise Exception("Stock quantity is required for products and must be non-negative")
        
        # Validate service duration for services
        if input.type == ProductServiceType.SERVICE and (input.service_duration is None or input.service_duration <= 0):
            raise Exception("Service duration is required for services and must be positive")
        
        # Validate price
        if input.price <= 0:
            raise Exception("Price must be greater than 0")
        
        # Create product data
        product_data = {
            "name": input.name,
            "description": input.description,
            "type": input.type,
            "category_id": input.category_id,
            "seller_id": current_user.id,
            "price": input.price,
            "images": input.images or [],
            "is_available": True,
            "stock_quantity": input.stock_quantity if input.type == ProductServiceType.PRODUCT else None,
            "service_duration": input.service_duration if input.type == ProductServiceType.SERVICE else None,
            "tags": input.tags or [],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        product = ProductService(**product_data)
        await db.products.insert_one(product.dict())
        
        return ProductServiceGraphQL(
            id=product.id,
            name=product.name,
            description=product.description,
            type=product.type,
            category_id=product.category_id,
            seller_id=product.seller_id,
            price=product.price,
            images=product.images,
            is_available=product.is_available,
            stock_quantity=product.stock_quantity,
            service_duration=product.service_duration,
            tags=product.tags,
            created_at=product.created_at.isoformat()
        )
