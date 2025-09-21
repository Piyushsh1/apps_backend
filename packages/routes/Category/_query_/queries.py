"""
Category Queries
Exports all category-related queries
"""

from .CategoryList import CategoryList

category_list = CategoryList

__all__ = [
    'CategoryList',
    'category_list'
]
