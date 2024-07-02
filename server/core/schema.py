import graphene
from addresses.schema import Query as AddressQuery, Mutation as AddressMutation
from users.schema import Query as UserQuery, Mutation as UserMutation
from inventories.schema import Query as InventoryQuery, Mutation as InventoryMutation
# from products.schema import Query as ProductQuery, Mutation as ProductMutation
import graphql_jwt


class Query(AddressQuery, UserQuery, InventoryQuery, graphene.ObjectType):
    pass


class Mutation(AddressMutation, UserMutation, InventoryMutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
