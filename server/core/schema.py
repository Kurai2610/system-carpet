import graphene
import graphql_jwt
from users.schema import (
    Query as UserQuery,
    Mutation as UserMutation
)
from addresses.schema import (
    Query as AddressQuery,
    Mutation as AddressMutation
)
from inventories.schema import (
    Query as InventoryQuery,
    Mutation as InventoryMutation
)
from products.schema import (
    Query as ProductQuery,
    Mutation as ProductMutation
)
from supply_chains.schema import (
    Query as SupplyChainQuery,
    Mutation as SupplyChainMutation
)
from shopping_carts.schema import (
    Query as ShoppingCartQuery,
    Mutation as ShoppingCartMutation
)


class Query(UserQuery, AddressQuery, InventoryQuery, ProductQuery, SupplyChainQuery, ShoppingCartQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, AddressMutation, InventoryMutation, ProductMutation, SupplyChainMutation, ShoppingCartMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
