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


class Query(UserQuery, AddressQuery, InventoryQuery, ProductQuery, graphene.ObjectType):
    pass


class Mutation(UserMutation, AddressMutation, InventoryMutation, ProductMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
