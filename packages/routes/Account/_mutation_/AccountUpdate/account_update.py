import strawberry
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from packages.types.inputs import UserUpdateInput
from packages.types.outputs import UserGraphQL, SuccessResponse
from packages.middleware.auth import AuthMiddleware

@strawberry.type
class AccountUpdate:
    @strawberry.mutation
    async def account_update(self, info, input: UserUpdateInput, token: str) -> SuccessResponse:
        """
        Update user account information
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        
        # Verify authenticated user
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        # Update user data
        update_data = {}
        if input.full_name is not None:
            update_data["full_name"] = input.full_name
        if input.phone is not None:
            update_data["phone"] = input.phone
        if input.business_name is not None:
            update_data["business_name"] = input.business_name
        if input.business_address is not None:
            update_data["business_address"] = input.business_address
        if input.business_description is not None:
            update_data["business_description"] = input.business_description
        
        update_data["updated_at"] = datetime.now()
        
        await db.users.update_one(
            {"id": current_user.id},
            {"$set": update_data}
        )
        
        return SuccessResponse(
            success=True,
            message="Account updated successfully"
        )
