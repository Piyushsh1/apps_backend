"""
Account Queries
Exports all account-related queries
"""

# Export all queries from subdirectories
from .AccountList import AccountList
from .AccountGet import AccountGet

# Export specific queries (like in Node.js structure)
account_list = AccountList
account_get = AccountGet

# Export all queries as a list for easy iteration
__all__ = [
    'AccountList',
    'AccountGet',
    'account_list',
    'account_get'
]
