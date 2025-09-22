import strawberry
from typing import Optional
from packages.types.outputs import SuccessResponse
from packages.types.inputs import LogoutInput
from packages.middleware.auth import AuthMiddleware

@strawberry.type
class AccountLogout:
    @strawberry.mutation
    async def account_logout(
        self, 
        info, 
        token: str, 
        input: Optional[LogoutInput] = None
    ) -> SuccessResponse:
        """
        Logout user account by blacklisting the token
        Supports logging out from current device or all devices
        """
        db = info.context["db"]
        
        # Default input if not provided
        if input is None:
            input = LogoutInput(logout_all_devices=False)
        
        # Verify the token and get current user
        current_user = await AuthMiddleware.get_current_user(db, token)
        if not current_user:
            return SuccessResponse(
                success=False,
                message="Invalid or expired token"
            )
        
        try:
            if input.logout_all_devices:
                # Logout from all devices by updating user logout timestamp
                success = await AuthMiddleware.blacklist_all_user_tokens(db, current_user.id)
                if not success:
                    return SuccessResponse(
                        success=False,
                        message="Failed to logout from all devices"
                    )
                
                message = "Logged out from all devices successfully"
            else:
                # Check if token is already blacklisted
                if await AuthMiddleware.is_token_blacklisted(db, token):
                    return SuccessResponse(
                        success=False,
                        message="Token already invalidated"
                    )
                
                # Blacklist the current token only
                blacklisted = await AuthMiddleware.blacklist_token(db, token, current_user.id)
                if not blacklisted:
                    return SuccessResponse(
                        success=False,
                        message="Failed to logout. Invalid token format."
                    )
                
                message = "Logged out successfully"
            
            # Optional: Clean up expired tokens (run periodically)
            await AuthMiddleware.cleanup_expired_tokens(db)
            
            return SuccessResponse(
                success=True,
                message=message
            )
            
        except Exception as e:
            return SuccessResponse(
                success=False,
                message=f"Logout failed: {str(e)}"
            )
