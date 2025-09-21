import strawberry
from packages.types.outputs import SuccessResponse

@strawberry.type
class AccountLogout:
    @strawberry.mutation
    async def account_logout(self, info, token: str) -> SuccessResponse:
        """
        Logout user account
        """
        # In a real implementation, you would invalidate the token
        # For now, we just return success
        return SuccessResponse(
            success=True,
            message="Logged out successfully"
        )
