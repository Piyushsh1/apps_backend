import strawberry
from datetime import datetime
from typing import List

from packages.types.inputs import UserProfileUpdateInput, DeliveryAddressInput
from packages.types.outputs import UserGraphQL, SuccessResponse
from packages.middleware.auth import AuthMiddleware
from packages.types.models import UserType

@strawberry.type
class AccountUpdate:
    @strawberry.mutation
    async def account_update(self, info, input: UserProfileUpdateInput, token: str) -> UserGraphQL:
        """
        Update user account information with comprehensive profile editing
        """
        db = info.context["db"]
        
        # Verify authenticated user
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        # Build update data
        update_data = {"updated_at": datetime.now()}
        
        if input.full_name is not None:
            if len(input.full_name.strip()) < 2:
                raise Exception("Full name must be at least 2 characters long")
            update_data["full_name"] = input.full_name.strip()
        
        if input.phone is not None:
            if input.phone and len(input.phone.strip()) < 10:
                raise Exception("Phone number must be at least 10 characters long")
            update_data["phone"] = input.phone.strip() if input.phone else None
        
        # Business fields (only for sellers)
        if current_user.user_type == UserType.SELLER:
            if input.business_name is not None:
                update_data["business_name"] = input.business_name.strip() if input.business_name else None
            if input.business_address is not None:
                update_data["business_address"] = input.business_address.strip() if input.business_address else None
            if input.business_description is not None:
                update_data["business_description"] = input.business_description.strip() if input.business_description else None
            if input.seller_type is not None:
                update_data["seller_type"] = input.seller_type
        
        # Customer category (only for customers)
        if current_user.user_type == UserType.CUSTOMER:
            if input.customer_category is not None:
                update_data["customer_category"] = input.customer_category
        
        # Update the user
        await db.users.update_one(
            {"id": current_user.id},
            {"$set": update_data}
        )
        
        # Fetch updated user data
        updated_user_data = await db.users.find_one({"id": current_user.id})
        
        return UserGraphQL(
            id=updated_user_data["id"],
            email=updated_user_data["email"],
            full_name=updated_user_data["full_name"],
            phone=updated_user_data.get("phone"),
            user_type=updated_user_data["user_type"],
            customer_category=updated_user_data.get("customer_category"),
            admin_role=updated_user_data.get("admin_role"),
            seller_type=updated_user_data.get("seller_type"),
            is_active=updated_user_data["is_active"],
            business_name=updated_user_data.get("business_name"),
            business_address=updated_user_data.get("business_address"),
            business_description=updated_user_data.get("business_description"),
            created_at=updated_user_data["created_at"].isoformat()
        )
    
    @strawberry.mutation
    async def add_delivery_address(self, info, input: DeliveryAddressInput, token: str) -> SuccessResponse:
        """
        Add a delivery address for customers
        """
        db = info.context["db"]
        
        # Verify authenticated customer
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.CUSTOMER:
            raise Exception("Only customers can add delivery addresses")
        
        # Create address object
        address = {
            "id": f"addr_{datetime.now().timestamp()}",
            "street": input.street.strip(),
            "city": input.city.strip(),
            "state": input.state.strip(),
            "postal_code": input.postal_code.strip(),
            "country": input.country.strip(),
            "is_default": input.is_default or False,
            "created_at": datetime.now()
        }
        
        # If this is set as default, make all other addresses non-default
        if input.is_default:
            await db.users.update_one(
                {"id": current_user.id},
                {"$set": {"delivery_addresses.$[].is_default": False}}
            )
        
        # Add the new address
        await db.users.update_one(
            {"id": current_user.id},
            {"$push": {"delivery_addresses": address}}
        )
        
        return SuccessResponse(
            success=True,
            message="Delivery address added successfully"
        )
    
    @strawberry.mutation
    async def remove_delivery_address(self, info, address_id: str, token: str) -> SuccessResponse:
        """
        Remove a delivery address for customers
        """
        db = info.context["db"]
        
        # Verify authenticated customer
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            raise Exception("Authentication required")
        
        if current_user.user_type != UserType.CUSTOMER:
            raise Exception("Only customers can remove delivery addresses")
        
        # Remove the address
        result = await db.users.update_one(
            {"id": current_user.id},
            {"$pull": {"delivery_addresses": {"id": address_id}}}
        )
        
        if result.modified_count == 0:
            return SuccessResponse(
                success=False,
                message="Address not found or already removed"
            )
        
        return SuccessResponse(
            success=True,
            message="Delivery address removed successfully"
        )
