import strawberry
from packages.types.outputs import SuccessResponse
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType, Wishlist

@strawberry.type
class WishlistAdd:
    @strawberry.mutation
    async def wishlist_add(self, info, product_id: str, token: str) -> SuccessResponse:
        """
        Add a product to user's wishlist
        Only customers can add items to wishlist
        """
        db = info.context["db"]
        
        # Verify authenticated customer
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.CUSTOMER:
            raise Exception("Only customers can add items to wishlist")
        
        # Check if product exists and is available
        product = await db.products.find_one({
            "id": product_id,
            "is_available": True
        })
        if not product:
            raise Exception("Product not found or not available")
        
        # Check if already in wishlist
        existing_wishlist_item = await db.wishlists.find_one({
            "user_id": current_user.id,
            "product_id": product_id
        })
        
        if existing_wishlist_item:
            return SuccessResponse(
                success=False,
                message="Product is already in your wishlist"
            )
        
        # Add to wishlist
        wishlist_item = Wishlist(
            user_id=current_user.id,
            product_id=product_id
        )
        
        await db.wishlists.insert_one(wishlist_item.dict())
        
        return SuccessResponse(
            success=True,
            message="Product added to wishlist successfully"
        )
