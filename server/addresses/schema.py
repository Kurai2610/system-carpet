import graphene
from graphene_django import DjangoObjectType
from addresses.models import Locality, Neighborhood, Address


class LocalityType(DjangoObjectType):
    class Meta:
        model = Locality
        fields = ("id", "name")


class NeighborhoodType(DjangoObjectType):
    class Meta:
        model = Neighborhood
        fields = ("id", "name", "locality")


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        fields = ("id", "details", "neighborhood")


class CreateLocalityMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    locality = graphene.Field(LocalityType)

    def mutate(self, info, name):
        locality = Locality(name=name)
        locality.save()
        return CreateLocalityMutation(locality=locality)


class DeleteLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        locality = Locality.objects.get(pk=id)
        locality.delete()
        return DeleteLocalityMutation(message="Locality deleted")


class UpdateLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    locality = graphene.Field(LocalityType)

    def mutate(self, info, id, name):
        locality = Locality.objects.get(pk=id)

        locality.name = name
        locality.save()
        return UpdateLocalityMutation(locality=locality)


class CreateNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        locality_id = graphene.ID()

    neighborhood = graphene.Field(NeighborhoodType)

    def mutate(self, info, name, locality_id):
        locality = Locality.objects.get(pk=locality_id)
        neighborhood = Neighborhood(name=name, locality=locality)
        neighborhood.save()
        return CreateNeighborhoodMutation(neighborhood=neighborhood)


class DeleteNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        neighborhood = Neighborhood.objects.get(pk=id)
        neighborhood.delete()
        return DeleteNeighborhoodMutation(message="Neighborhood deleted")


class UpdateNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        locality = graphene.ID()

    neighborhood = graphene.Field(NeighborhoodType)

    def mutate(self, info, id, name=None, locality=None):
        neighborhood = Neighborhood.objects.get(pk=id)
        if name is not None:
            neighborhood.name = name
        if locality is not None:
            locality_obj = Locality.objects.get(pk=locality)
            neighborhood.locality = locality_obj
        neighborhood.save()
        return UpdateNeighborhoodMutation(neighborhood=neighborhood)


class CreateAddressMutation(graphene.Mutation):
    class Arguments:
        details = graphene.String()
        neighborhood_id = graphene.ID()

    address = graphene.Field(AddressType)

    def mutate(self, info, details, neighborhood_id):
        neighborhood = Neighborhood.objects.get(pk=neighborhood_id)
        address = Address(details=details, neighborhood=neighborhood)
        address.save()
        return CreateAddressMutation(address=address)


class DeleteAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        address = Address.objects.get(pk=id)
        address.delete()
        return DeleteAddressMutation(message="Address deleted")


class UpdateAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        details = graphene.String()
        neighborhood = graphene.ID()

    address = graphene.Field(AddressType)

    def mutate(self, info, id, details=None, neighborhood=None):
        address = Address.objects.get(pk=id)
        if details is not None:
            address.details = details
        if neighborhood is not None:
            neighborhood_obj = Neighborhood.objects.get(pk=neighborhood)
            address.neighborhood = neighborhood_obj
        address.save()
        return UpdateAddressMutation(address=address)


class Query(graphene.ObjectType):
    localities = graphene.List(LocalityType)
    locality = graphene.Field(LocalityType, id=graphene.ID())
    neighborhoods = graphene.List(NeighborhoodType)
    neighborhood = graphene.Field(NeighborhoodType, id=graphene.ID())
    addresses = graphene.List(AddressType)
    address = graphene.Field(AddressType, id=graphene.ID())

    def resolve_localities(self, info):
        return Locality.objects.all()

    def resolve_locality(self, info, id):
        return Locality.objects.get(pk=id)

    def resolve_neighborhoods(self, info):
        return Neighborhood.objects.all()

    def resolve_neighborhood(self, info, id):
        return Neighborhood.objects.get(pk=id)

    def resolve_addresses(self, info):
        return Address.objects.all()

    def resolve_address(self, info, id):
        return Address.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_locality = CreateLocalityMutation.Field()
    delete_locality = DeleteLocalityMutation.Field()
    update_locality = UpdateLocalityMutation.Field()
    create_neighborhood = CreateNeighborhoodMutation.Field()
    delete_neighborhood = DeleteNeighborhoodMutation.Field()
    update_neighborhood = UpdateNeighborhoodMutation.Field()
    create_address = CreateAddressMutation.Field()
    delete_address = DeleteAddressMutation.Field()
    update_address = UpdateAddressMutation.Field()
