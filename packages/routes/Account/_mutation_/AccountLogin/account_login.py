import strawberry
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import timedelta

from packages.types.inputs import UserLoginInput
from packages.types.outputs import UserGraphQL, AuthResponse
from packages.middleware.auth import AuthMiddleware

@strawberry.type
class AccountLogin:
    @strawberry.mutation
    async def account_login(self, info, input: UserLoginInput) -> AuthResponse:
        """
        Login user account
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        
        # Find user
        user_data = await db.users.find_one({"email": input.email})
        if not user_data or not AuthMiddleware.verify_password(input.password, user_data["password_hash"]):
            return AuthResponse(
                token="",
                user=UserGraphQL(
                    id="", email="", full_name="", phone=None, user_type="",
                    customer_category=None, admin_role=None, seller_type=None,
                    is_active=False, business_name=None, business_address=None,
                    business_description=None, created_at=""
                ),
                message="Invalid credentials"
            )
        
        # Create token
        access_token_expires = timedelta(minutes=30)
        access_token = AuthMiddleware.create_access_token(
            data={"sub": user_data["id"]}, expires_delta=access_token_expires
        )
        
        return AuthResponse(
            token=access_token,
            user=UserGraphQL(
                id=user_data["id"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                phone=user_data.get("phone"),
                user_type=user_data["user_type"],
                customer_category=user_data.get("customer_category"),
                admin_role=user_data.get("admin_role"),
                seller_type=user_data.get("seller_type"),
                is_active=user_data["is_active"],
                business_name=user_data.get("business_name"),
                business_address=user_data.get("business_address"),
                business_description=user_data.get("business_description"),
                created_at=user_data["created_at"].isoformat()
            ),
            message="Login successful"
        )
