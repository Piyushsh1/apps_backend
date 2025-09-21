import strawberry
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from packages.types.outputs import UserGraphQL

@strawberry.type
class AccountList:
    @strawberry.field
    async def account_list(self, info) -> List[UserGraphQL]:
        """
        Get list of all accounts
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        users = await db.users.find().to_list(1000)
        return [
            UserGraphQL(
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
            for user in users
        ]
