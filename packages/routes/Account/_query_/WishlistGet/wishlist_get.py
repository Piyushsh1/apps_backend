import strawberry
from typing import List
from packages.types.outputs import ProductServiceGraphQL
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType

@strawberry.type
class WishlistGet:
    @strawberry.field
    async def wishlist_get(self, info, token: str) -> List[ProductServiceGraphQL]:
        """
        Get user's wishlist with product details
        """
        db = info.context["db"]
        
        # Verify authenticated customer
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.CUSTOMER:
            raise Exception("Only customers have wishlists")
        
        # Get wishlist items with product details
        pipeline = [
            {"$match": {"user_id": current_user.id}},
            {
                "$lookup": {
                    "from": "products",
                    "localField": "product_id",
                    "foreignField": "id",
                    "as": "product"
                }
            },
            {"$unwind": "$product"},
            {"$match": {"product.is_available": True}},  # Only show available products
            {"$replaceRoot": {"newRoot": "$product"}}
        ]
        
        wishlist_products = await db.wishlists.aggregate(pipeline).to_list(length=None)
        
        return [
            ProductServiceGraphQL(
                id=product["id"],
                name=product["name"],
                description=product["description"],
                type=product["type"],
                category_id=product["category_id"],
                seller_id=product["seller_id"],
                price=product["price"],
                images=product.get("images", []),
                is_available=product["is_available"],
                stock_quantity=product.get("stock_quantity"),
                service_duration=product.get("service_duration"),
                tags=product.get("tags", []),
                created_at=product["created_at"].isoformat()
            )
            for product in wishlist_products
        ]
