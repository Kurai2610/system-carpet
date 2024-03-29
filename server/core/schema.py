import graphene
from addresses.schema import Query as AddressQuery, Mutation as AddressMutation


class Query(AddressQuery, graphene.ObjectType):
    pass


class Mutation(AddressMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
