import strawberry
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import timedelta, datetime

from packages.types.inputs import UserRegisterInput
from packages.types.outputs import UserGraphQL, AuthResponse
from packages.middleware.auth import AuthMiddleware
from packages.types.models import User, UserType, AdminRole

@strawberry.type
class AccountRegister:
    @strawberry.mutation
    async def account_register(self, info, input: UserRegisterInput) -> AuthResponse:
        """
        Register a new user account
        """
        db: AsyncIOMotorDatabase = info.context["db"]
        
        # Check if user already exists
        existing_user = await db.users.find_one({"email": input.email})
        if existing_user:
            return AuthResponse(
                token="",
                user=UserGraphQL(
                    id="", email="", full_name="", phone=None, user_type="",
                    customer_category=None, admin_role=None, seller_type=None,
                    is_active=False, business_name=None, business_address=None,
                    business_description=None, created_at=""
                ),
                message="User already exists"
            )
        
        # Create new user
        user_data = {
            "email": input.email,
            "password_hash": AuthMiddleware.get_password_hash(input.password),
            "full_name": input.full_name,
            "phone": input.phone,
            "user_type": input.user_type,
            "customer_category": input.customer_category,
            "admin_role": input.admin_role,
            "seller_type": input.seller_type,
            "business_name": input.business_name,
            "business_address": input.business_address,
            "business_description": input.business_description,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "delivery_addresses": []
        }
        
        user = User(**user_data)
        await db.users.insert_one(user.dict())
        
        # Create token
        access_token_expires = timedelta(minutes=30)
        access_token = AuthMiddleware.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )
        
        return AuthResponse(
            token=access_token,
            user=UserGraphQL(
                id=user.id,
                email=user.email,
                full_name=user.full_name,
                phone=user.phone,
                user_type=user.user_type,
                customer_category=user.customer_category,
                admin_role=user.admin_role,
                seller_type=user.seller_type,
                is_active=user.is_active,
                business_name=user.business_name,
                business_address=user.business_address,
                business_description=user.business_description,
                created_at=user.created_at.isoformat()
            ),
            message="User registered successfully"
        )
