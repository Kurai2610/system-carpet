import graphene
from addresses.schema import Query as AddressQuery, Mutation as AddressMutation
from inventories.schema import Query as InventoryQuery, Mutation as InventoryMutation
from products.schema import Query as ProductQuery, Mutation as ProductMutation


class Query(AddressQuery, InventoryQuery, ProductQuery, graphene.ObjectType):
    pass


class Mutation(AddressMutation, InventoryMutation, ProductMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
