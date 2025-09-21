import strawberry
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from packages.types.outputs import UserGraphQL

@strawberry.type
class AccountGet:
    @strawberry.field
    async def account_get(self, info, user_id: str) -> Optional[UserGraphQL]:
        """
        Get specific account by ID
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        user = await db.users.find_one({"id": user_id})
        if user:
            return UserGraphQL(
                id=user["id"],
                email=user["email"],
                full_name=user["full_name"],
                phone=user.get("phone"),
                user_type=user["user_type"],
                customer_category=user.get("customer_category"),
                admin_role=user.get("admin_role"),
                seller_type=user.get("seller_type"),
                is_active=user["is_active"],
                business_name=user.get("business_name"),
                business_address=user.get("business_address"),
                business_description=user.get("business_description"),
                created_at=user["created_at"].isoformat()
            )
        return None
