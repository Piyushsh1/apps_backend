import strawberry

# Import all mutations and queries from routes
from packages.routes.Account._mutation_.AccountRegister.account_register import AccountRegister
from packages.routes.Account._mutation_.AccountLogin.account_login import AccountLogin
from packages.routes.Account._mutation_.AccountLogout.account_logout import AccountLogout
from packages.routes.Account._mutation_.AccountUpdate.account_update import AccountUpdate
from packages.routes.Account._mutation_.WishlistAdd.wishlist_add import WishlistAdd
from packages.routes.Account._mutation_.WishlistRemove.wishlist_remove import WishlistRemove
from packages.routes.Account._query_.AccountList.account_list import AccountList
from packages.routes.Account._query_.AccountGet.account_get import AccountGet
from packages.routes.Account._query_.WishlistGet.wishlist_get import WishlistGet
from packages.routes.Category._mutation_.CategoryCreate.category_create import CategoryCreate
from packages.routes.Category._query_.CategoryList.category_list import CategoryList
from packages.routes.Product._mutation_.ProductCreate.product_create import ProductCreate
from packages.routes.Product._mutation_.ProductUpdate.product_update import ProductUpdate
from packages.routes.Product._query_.ProductList.product_list import ProductList
from packages.routes.Product._query_.ProductGet.product_get import ProductGet

# Combine all mutations
@strawberry.type
class Mutation(
    AccountRegister, 
    AccountLogin, 
    AccountLogout, 
    AccountUpdate, 
    WishlistAdd,
    WishlistRemove,
    CategoryCreate,
    ProductCreate,
    ProductUpdate
):
    pass

# Combine all queries  
@strawberry.type
class Query(
    AccountList, 
    AccountGet, 
    WishlistGet,
    CategoryList,
    ProductList,
    ProductGet
):
    pass

# Create the main schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)