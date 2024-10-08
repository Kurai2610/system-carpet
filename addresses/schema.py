import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from core.utils import normalize_name
from .types import (
    LocalityType,
    NeighborhoodType,
    AddressType
)
from .models import (
    Locality,
    Neighborhood,
    Address
)


class CreateLocalityMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    locality = graphene.Field(LocalityType)

    @login_required
    @permission_required("addresses.add_locality")
    def mutate(self, info, name):
        try:
            name = normalize_name(name)
            locality = Locality(name=name)
            locality.save()
            return CreateLocalityMutation(locality=locality)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Locality already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class DeleteLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required("addresses.delete_locality")
    def mutate(self, info, id):
        try:
            locality = Locality.objects.get(pk=id)
            locality.delete()
            return DeleteLocalityMutation(success=True)
        except Locality.DoesNotExist:
            raise GraphQLError("Locality not found")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class UpdateLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    locality = graphene.Field(LocalityType)

    @login_required
    @permission_required("addresses.change_locality")
    def mutate(self, info, id, name):
        try:
            name = normalize_name(name)
            locality = Locality.objects.get(pk=id)
            locality.name = name
            locality.save()
            return UpdateLocalityMutation(locality=locality)
        except Locality.DoesNotExist:
            raise GraphQLError("Locality not found")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Locality already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class CreateNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        locality_id = graphene.ID(required=True)

    neighborhood = graphene.Field(NeighborhoodType)

    @login_required
    @permission_required("addresses.add_neighborhood")
    def mutate(self, info, name, locality_id):
        try:
            name = normalize_name(name)
            locality = Locality.objects.get(pk=locality_id)
            neighborhood = Neighborhood(name=name, locality=locality)
            neighborhood.save()
            return CreateNeighborhoodMutation(neighborhood=neighborhood)
        except Locality.DoesNotExist:
            raise GraphQLError("Locality not found")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Neighborhood already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class DeleteNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required("addresses.delete_neighborhood")
    def mutate(self, info, id):
        try:
            neighborhood = Neighborhood.objects.get(pk=id)
            neighborhood.delete()
            return DeleteNeighborhoodMutation(success=True)
        except Neighborhood.DoesNotExist:
            raise GraphQLError("Neighborhood not found")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class UpdateNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        locality_id = graphene.ID()

    neighborhood = graphene.Field(NeighborhoodType)

    @login_required
    @permission_required("addresses.change_neighborhood")
    def mutate(self, info, id, name=None, locality_id=None):

        if not name and not locality_id:
            raise GraphQLError("Name or Locality is required")

        try:
            neighborhood = Neighborhood.objects.get(pk=id)
            if name is not None:
                name = normalize_name(name)
                neighborhood.name = name
            if locality_id is not None:
                locality_obj = Locality.objects.get(pk=locality_id)
                neighborhood.locality = locality_obj
            neighborhood.save()
            return UpdateNeighborhoodMutation(neighborhood=neighborhood)
        except Neighborhood.DoesNotExist:
            raise GraphQLError("Neighborhood not found")
        except Locality.DoesNotExist:
            raise GraphQLError("Locality not found")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Neighborhood already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class CreateAddressMutation(graphene.Mutation):
    class Arguments:
        details = graphene.String(required=True)
        neighborhood_id = graphene.ID(required=True)

    address = graphene.Field(AddressType)

    @login_required
    @permission_required("addresses.add_address")
    def mutate(self, info, details, neighborhood_id):
        try:
            details = details.strip()
            neighborhood = Neighborhood.objects.get(pk=neighborhood_id)
            address = Address(details=details, neighborhood=neighborhood)
            address.save()
            return CreateAddressMutation(address=address)
        except Neighborhood.DoesNotExist:
            raise GraphQLError("Neighborhood not found")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Address already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class DeleteAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required("addresses.delete_address")
    def mutate(self, info, id):
        try:
            address = Address.objects.get(pk=id)
            address.delete()
            return DeleteAddressMutation(success=True)
        except Address.DoesNotExist:
            raise GraphQLError("Address not found")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class UpdateAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        details = graphene.String()
        neighborhood_id = graphene.ID()

    address = graphene.Field(AddressType)

    @login_required
    @permission_required("addresses.change_address")
    def mutate(self, info, id, details=None, neighborhood_id=None):

        if not details and not neighborhood_id:
            raise GraphQLError("Details or Neighborhood is required")

        try:
            address = Address.objects.get(pk=id)
            if details is not None:
                details = details.strip()
                address.details = details
            if neighborhood_id is not None:
                neighborhood_obj = Neighborhood.objects.get(pk=neighborhood_id)
                address.neighborhood = neighborhood_obj
            address.save()
            return UpdateAddressMutation(address=address)
        except Address.DoesNotExist:
            raise GraphQLError("Address not found")
        except Neighborhood.DoesNotExist:
            raise GraphQLError("Neighborhood not found")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Address already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class Query(graphene.ObjectType):
    localities = DjangoFilterConnectionField(LocalityType)
    locality = graphene.Field(LocalityType, id=graphene.ID())
    neighborhoods = DjangoFilterConnectionField(NeighborhoodType)
    neighborhood = graphene.Field(NeighborhoodType, id=graphene.ID())
    addresses = DjangoFilterConnectionField(AddressType)
    address = graphene.Field(AddressType, id=graphene.ID())

    @login_required
    @permission_required("addresses.view_locality")
    def resolve_localities(self, info, **kwargs):
        return Locality.objects.all()

    @login_required
    @permission_required("addresses.view_locality")
    def resolve_locality(self, info, id):
        return Locality.objects.get(pk=id)

    @login_required
    @permission_required("addresses.view_neighborhood")
    def resolve_neighborhoods(self, info, **kwargs):
        return Neighborhood.objects.all()

    @login_required
    @permission_required("addresses.view_neighborhood")
    def resolve_neighborhood(self, info, id):
        return Neighborhood.objects.get(pk=id)

    @login_required
    @permission_required("addresses.view_address")
    def resolve_addresses(self, info, **kwargs):
        return Address.objects.all()

    @login_required
    @permission_required("addresses.view_address")
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
