import graphene
from addresses.schema import Query as AddressQuery, Mutation as AddressMutation
from inventories.schema import Query as InventoryQuery, Mutation as InventoryMutation


class Query(AddressQuery, InventoryQuery, graphene.ObjectType):
    pass


class Mutation(AddressMutation, InventoryMutation, graphene.ObjectType):
    pass


# HAY ERRORES EN EL SCHEMA DE INVENTARIO, REVISA EL MODELO Y EL METODO DE VERIFICACION, ADEMAS LOS NOMBRES
# DE LOS QUERY Y MUTATIONS SE PUEDEN REPETIR AL UNIR LOS SCHEMAS

schema = graphene.Schema(query=Query, mutation=Mutation)
