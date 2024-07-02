import graphene
from graphene_django import DjangoObjectType
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
from core.errors import ValidationError as CustomValidationError, DatabaseError
from core.types import ErrorType
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
        name = graphene.String(required=True)

    locality = graphene.Field(LocalityType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Name is required", field="name"))

        if errors:
            return CreateLocalityMutation(locality=None, errors=errors)

        try:
            locality = Locality(name=name)
            locality.save()
            return CreateLocalityMutation(locality=locality, errors=None)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return CreateLocalityMutation(locality=None, errors=errors)
        except IntegrityError:
            errors.append(ErrorType(code="DATABASE_ERROR",
                                    message="Locality already exists", field="name"))
            return CreateLocalityMutation(locality=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return CreateLocalityMutation(locality=None, errors=errors)


class DeleteLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    errors = graphene.List(ErrorType)
    message = graphene.String()

    def mutate(self, info, id):
        errors = []
        try:
            locality = Locality.objects.get(pk=id)
            locality.delete()
            return DeleteLocalityMutation(message="Locality deleted", errors=None)
        except Locality.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Locality not found", field="id"))
            return DeleteLocalityMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return DeleteLocalityMutation(message=None, errors=errors)


class UpdateLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    locality = graphene.Field(LocalityType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name):
        errors = []
        try:
            locality = Locality.objects.get(pk=id)
            locality.name = name
            locality.save()
            return UpdateLocalityMutation(locality=locality, errors=None)
        except Locality.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Locality not found", field="id"))
            return UpdateLocalityMutation(locality=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return UpdateLocalityMutation(locality=None, errors=errors)
        except IntegrityError:
            errors.append(ErrorType(code="DATABASE_ERROR",
                                    message="Locality already exists", field="name"))
            return UpdateLocalityMutation(locality=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return UpdateLocalityMutation(locality=None, errors=errors)


class CreateNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        locality_id = graphene.ID()

    neighborhood = graphene.Field(NeighborhoodType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name, locality_id):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Name is required", field="name"))

        if not locality_id:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Locality is required", field="locality_id"))

        if errors:
            return CreateNeighborhoodMutation(neighborhood=None, errors=errors)

        try:
            locality = Locality.objects.get(pk=locality_id)
            neighborhood = Neighborhood(name=name, locality=locality)
            neighborhood.save()
            return CreateNeighborhoodMutation(neighborhood=neighborhood, errors=None)
        except Locality.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Locality not found", field="locality_id"))
            return CreateNeighborhoodMutation(neighborhood=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return CreateNeighborhoodMutation(neighborhood=None, errors=errors)
        except IntegrityError:
            errors.append(ErrorType(code="DATABASE_ERROR",
                                    message="Neighborhood already exists", field="name"))
            return CreateNeighborhoodMutation(neighborhood=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return CreateNeighborhoodMutation(neighborhood=None, errors=errors)


class DeleteNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            neighborhood = Neighborhood.objects.get(pk=id)
            neighborhood.delete()
            return DeleteNeighborhoodMutation(message="Neighborhood deleted", errors=None)
        except Neighborhood.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Neighborhood not found", field="id"))
            return DeleteNeighborhoodMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return DeleteNeighborhoodMutation(message=None, errors=errors)


class UpdateNeighborhoodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        locality = graphene.ID()

    neighborhood = graphene.Field(NeighborhoodType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name=None, locality=None):
        errors = []

        try:
            neighborhood = Neighborhood.objects.get(pk=id)
            if name is not None:
                neighborhood.name = name
            if locality is not None:
                locality_obj = Locality.objects.get(pk=locality)
                neighborhood.locality = locality_obj
            neighborhood.save()
            return UpdateNeighborhoodMutation(neighborhood=neighborhood, errors=None)
        except Neighborhood.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Neighborhood not found", field="id"))
            return UpdateNeighborhoodMutation(neighborhood=None, errors=errors)
        except Locality.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Locality not found", field="locality"))
            return UpdateNeighborhoodMutation(neighborhood=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return UpdateNeighborhoodMutation(neighborhood=None, errors=errors)
        except IntegrityError:
            errors.append(ErrorType(code="DATABASE_ERROR",
                                    message="Neighborhood already exists", field="name"))
            return UpdateNeighborhoodMutation(neighborhood=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return UpdateNeighborhoodMutation(neighborhood=None, errors=errors)


class CreateAddressMutation(graphene.Mutation):
    class Arguments:
        details = graphene.String()
        neighborhood_id = graphene.ID()

    address = graphene.Field(AddressType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, details, neighborhood_id):
        errors = []

        if not details:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Details is required", field="details"))

        if not neighborhood_id:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Neighborhood is required", field="neighborhood_id"))

        if errors:
            return CreateAddressMutation(address=None, errors=errors)

        try:
            neighborhood = Neighborhood.objects.get(pk=neighborhood_id)
            address = Address(details=details, neighborhood=neighborhood)
            address.save()
            return CreateAddressMutation(address=address, errors=None)
        except Neighborhood.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Neighborhood not found", field="neighborhood_id"))
            return CreateAddressMutation(address=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return CreateAddressMutation(address=None, errors=errors)
        except IntegrityError:
            errors.append(ErrorType(code="DATABASE_ERROR",
                                    message="Address already exists", field="details"))
            return CreateAddressMutation(address=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return CreateAddressMutation(address=None, errors=errors)


class DeleteAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            address = Address.objects.get(pk=id)
            address.delete()
            return DeleteAddressMutation(message="Address deleted", errors=None)
        except Address.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Address not found", field="id"))
            return DeleteAddressMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return DeleteAddressMutation(message=None, errors=errors)


class UpdateAddressMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        details = graphene.String()
        neighborhood = graphene.ID()

    address = graphene.Field(AddressType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, details=None, neighborhood=None):
        errors = []

        try:
            address = Address.objects.get(pk=id)
            if details is not None:
                address.details = details
            if neighborhood is not None:
                neighborhood_obj = Neighborhood.objects.get(pk=neighborhood)
                address.neighborhood = neighborhood_obj
            address.save()
            return UpdateAddressMutation(address=address, errors=None)
        except Address.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Address not found", field="id"))
            return UpdateAddressMutation(address=None, errors=errors)
        except Neighborhood.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message="Neighborhood not found", field="neighborhood"))
            return UpdateAddressMutation(address=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return UpdateAddressMutation(address=None, errors=errors)
        except IntegrityError:
            errors.append(ErrorType(code="DATABASE_ERROR",
                                    message="Address already exists", field="details"))
            return UpdateAddressMutation(address=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return UpdateAddressMutation(address=None, errors=errors)


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
