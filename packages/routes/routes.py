"""
Routes Package
Main entry point for all API routes
"""

# Import all route modules
from .Account import *
from .Category import *
from .Product import *

# Export all routes
__all__ = [
    'Account',
    'Category',
    'Product'
]
