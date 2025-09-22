import strawberry
from datetime import datetime
from packages.types.inputs import ProductServiceUpdateInput
from packages.types.outputs import SuccessResponse
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType

@strawberry.type
class ProductUpdate:
    @strawberry.mutation
    async def product_update(self, info, product_id: str, input: ProductServiceUpdateInput, token: str) -> SuccessResponse:
        """
        Update an existing product/service
        Only the seller who created the product can update it
        """
        db = info.context["db"]
        
        # Verify authenticated seller
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.SELLER:
            raise Exception("Only sellers can update products")
        
        # Find the product
        product = await db.products.find_one({"id": product_id})
        if not product:
            raise Exception("Product not found")
        
        # Verify ownership
        if product["seller_id"] != current_user.id:
            raise Exception("You can only update your own products")
        
        # Build update data
        update_data = {"updated_at": datetime.now()}
        
        if input.name is not None:
            update_data["name"] = input.name
        if input.description is not None:
            update_data["description"] = input.description
        if input.price is not None:
            if input.price <= 0:
                raise Exception("Price must be greater than 0")
            update_data["price"] = input.price
        if input.images is not None:
            update_data["images"] = input.images
        if input.stock_quantity is not None:
            if product["type"] == "product" and input.stock_quantity < 0:
                raise Exception("Stock quantity cannot be negative")
            update_data["stock_quantity"] = input.stock_quantity
        if input.service_duration is not None:
            if product["type"] == "service" and input.service_duration <= 0:
                raise Exception("Service duration must be positive")
            update_data["service_duration"] = input.service_duration
        if input.tags is not None:
            update_data["tags"] = input.tags
        if input.is_available is not None:
            update_data["is_available"] = input.is_available
        
        # Update the product
        result = await db.products.update_one(
            {"id": product_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return SuccessResponse(
                success=False,
                message="No changes were made to the product"
            )
        
        return SuccessResponse(
            success=True,
            message="Product updated successfully"
        )
