import strawberry

# Import all mutations and queries from routes
from packages.routes.Account._mutation_.AccountRegister.account_register import AccountRegister
from packages.routes.Account._mutation_.AccountLogin.account_login import AccountLogin
from packages.routes.Account._mutation_.AccountLogout.account_logout import AccountLogout
from packages.routes.Account._mutation_.AccountUpdate.account_update import AccountUpdate
from packages.routes.Account._query_.AccountList.account_list import AccountList
from packages.routes.Account._query_.AccountGet.account_get import AccountGet
from packages.routes.Category._mutation_.CategoryCreate.category_create import CategoryCreate
from packages.routes.Category._query_.CategoryList.category_list import CategoryList

# Combine all mutations
@strawberry.type
class Mutation(AccountRegister, AccountLogin, AccountLogout, AccountUpdate, CategoryCreate):
    pass

# Combine all queries  
@strawberry.type
class Query(AccountList, AccountGet, CategoryList):
    pass

# Create the main schema
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)