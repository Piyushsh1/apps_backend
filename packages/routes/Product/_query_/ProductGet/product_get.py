import strawberry
from typing import Optional
from packages.types.outputs import ProductServiceGraphQL

@strawberry.type
class ProductGet:
    @strawberry.field
    async def product_get(self, info, product_id: str) -> Optional[ProductServiceGraphQL]:
        """
        Get a specific product by ID
        """
        db = info.context["db"]
        
        product = await db.products.find_one({"id": product_id})
        
        if product:
            return ProductServiceGraphQL(
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
        
        return None
