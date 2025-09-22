import strawberry
from packages.types.outputs import SuccessResponse
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType

@strawberry.type
class WishlistRemove:
    @strawberry.mutation
    async def wishlist_remove(self, info, product_id: str, token: str) -> SuccessResponse:
        """
        Remove a product from user's wishlist
        """
        db = info.context["db"]
        
        # Verify authenticated customer
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.CUSTOMER:
            raise Exception("Only customers can remove items from wishlist")
        
        # Remove from wishlist
        result = await db.wishlists.delete_one({
            "user_id": current_user.id,
            "product_id": product_id
        })
        
        if result.deleted_count == 0:
            return SuccessResponse(
                success=False,
                message="Product not found in your wishlist"
            )
        
        return SuccessResponse(
            success=True,
            message="Product removed from wishlist successfully"
        )
