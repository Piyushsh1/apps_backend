import strawberry
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from packages.types.outputs import CategoryGraphQL

@strawberry.type
class CategoryList:
    @strawberry.field
    async def category_list(self, info) -> List[CategoryGraphQL]:
        """
        Get list of all categories
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        categories = await db.categories.find({"is_active": True}).to_list(1000)
        return [
            CategoryGraphQL(
                id=cat["id"],
                name=cat["name"],
                description=cat.get("description"),
                parent_category_id=cat.get("parent_category_id"),
                is_active=cat["is_active"],
                created_by=cat["created_by"],
                created_at=cat["created_at"].isoformat()
            )
            for cat in categories
        ]
