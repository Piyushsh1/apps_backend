import strawberry
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

from packages.types.inputs import CategoryInput
from packages.types.outputs import CategoryGraphQL
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType, AdminRole, Category

@strawberry.type
class CategoryCreate:
    @strawberry.mutation
    async def category_create(self, info, input: CategoryInput, token: str) -> CategoryGraphQL:
        """
        Create a new category
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        
        # Verify admin user
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user or current_user.user_type != UserType.ADMIN:
            raise Exception("Only admin users can create categories")
        
        if current_user.admin_role not in [AdminRole.SUPER_ADMIN, AdminRole.CATEGORY_MANAGER]:
            raise Exception("Insufficient permissions to create categories")
        
        category_data = {
            "name": input.name,
            "description": input.description,
            "parent_category_id": input.parent_category_id,
            "is_active": True,
            "created_by": current_user.id,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        category = Category(**category_data)
        await db.categories.insert_one(category.dict())
        
        return CategoryGraphQL(
            id=category.id,
            name=category.name,
            description=category.description,
            parent_category_id=category.parent_category_id,
            is_active=category.is_active,
            created_by=category.created_by,
            created_at=category.created_at.isoformat()
        )
