import strawberry
from typing import List, Optional
from packages.types.outputs import ProductServiceGraphQL

@strawberry.type
class ProductList:
    @strawberry.field
    async def product_list(
        self, 
        info, 
        category_id: Optional[str] = None,
        seller_id: Optional[str] = None,
        is_available: Optional[bool] = None,
        product_type: Optional[str] = None,
        limit: Optional[int] = 50
    ) -> List[ProductServiceGraphQL]:
        """
        Get list of products with optional filters
        """
        db = info.context["db"]
        
        # Build filter query
        filter_query = {}
        
        if category_id:
            filter_query["category_id"] = category_id
        if seller_id:
            filter_query["seller_id"] = seller_id
        if is_available is not None:
            filter_query["is_available"] = is_available
        if product_type:
            filter_query["type"] = product_type
        
        # Apply limit
        if limit is None or limit > 100:
            limit = 50
        
        products = await db.products.find(filter_query).limit(limit).to_list(length=limit)
        
        return [
            ProductServiceGraphQL(
                id=product["id"],
                name=product["name"],
                description=product["description"],
                type=product["type"],
                category_id=product["category_id"],
                seller_id=product["seller_id"],
                price=product["price"],
                images=product.get("images", []),
                is_available=product["is_available"],
                stock_quantity=product.get("stock_quantity"),
                service_duration=product.get("service_duration"),
                tags=product.get("tags", []),
                created_at=product["created_at"].isoformat()
            )
            for product in products
        ]
