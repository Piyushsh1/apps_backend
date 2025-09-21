"""
Category Mutations
Exports all category-related mutations
"""

from .CategoryCreate import CategoryCreate

category_create = CategoryCreate

__all__ = [
    'CategoryCreate',
    'category_create'
]
