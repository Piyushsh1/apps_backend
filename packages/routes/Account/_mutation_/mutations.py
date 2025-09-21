"""
Account Mutations
Exports all account-related mutations
"""

# Export all mutations from subdirectories
from .AccountRegister import AccountRegister
from .AccountLogin import AccountLogin
from .AccountLogout import AccountLogout
from .AccountUpdate import AccountUpdate

# Export specific mutations (like in Node.js structure)
account_register = AccountRegister
account_login = AccountLogin
account_logout = AccountLogout
account_update = AccountUpdate

# Export all mutations as a list for easy iteration
__all__ = [
    'AccountRegister',
    'AccountLogin', 
    'AccountLogout',
    'AccountUpdate',
    'account_register',
    'account_login',
    'account_logout',
    'account_update'
]
