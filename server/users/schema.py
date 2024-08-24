import graphene
import graphql_jwt
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required
from .types import UserType
from addresses.models import Address
from addresses.schema import (
    CreateAddressMutation,
    UpdateAddressMutation,
    DeleteAddressMutation
)


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        # Address arguments
        addres_details = graphene.String(required=False)
        neighborhood_id = graphene.ID(required=False)

    user = graphene.Field(UserType)

    def mutate(self, info, email, phone, password, first_name, last_name, addres_details=None, neighborhood_id=None):
        try:
            with transaction.atomic():
                user = get_user_model().objects.create_user(
                    email=email,
                    phone=phone,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                if addres_details or neighborhood_id:
                    address_mutation_result = CreateAddressMutation.mutate(
                        self=self, info=info, details=addres_details, neighborhood_id=neighborhood_id)
                    if address_mutation_result.errors:
                        raise GraphQLError(
                            "An error occurred while creating the address. Please try again.")
                    addressType = address_mutation_result.address
                    address = Address.objects.get(id=addressType.id)
                    user.address = address

                user.save()
                return CreateUserMutation(user=user)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError('An error occurred while saving the data.')
        except Exception as e:
            raise GraphQLError(str(e))


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            with transaction.atomic():
                user = get_user_model().objects.get(pk=id)
                user.delete()

                if user.address:
                    address_id = user.address.id
                    address_mutation_result = DeleteAddressMutation.mutate(
                        self=self, info=info, id=address_id)
                    if address_mutation_result.errors:
                        raise GraphQLError(
                            "An error occurred while deleting the address. Please try again.")
                return DeleteUserMutation(success=True)
        except get_user_model().DoesNotExist:
            raise GraphQLError("User does not exist.")
        except Exception as e:
            raise GraphQLError(str(e))


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String()
        phone = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        # Address arguments
        addres_details = graphene.String()
        neighborhood_id = graphene.ID()

    user = graphene.Field(UserType)

    def mutate(self, info, id, email=None, phone=None, first_name=None, last_name=None, addres_details=None, neighborhood_id=None):

        if not email and not phone and not first_name and not last_name and not addres_details and not neighborhood_id:
            raise GraphQLError("No data to update.")

        try:
            with transaction.atomic():
                user = get_user_model().objects.get(pk=id)

                if email:
                    user.email = email
                if phone:
                    user.phone = phone
                if first_name:
                    user.first_name = first_name
                if last_name:
                    user.last_name = last_name

                if addres_details or neighborhood_id:
                    if user.address:
                        address_id = user.address.id
                        address_mutation_result = UpdateAddressMutation.mutate(
                            self=self, info=info, id=address_id, details=addres_details, neighborhood_id=neighborhood_id)
                        if address_mutation_result.errors:
                            raise GraphQLError(
                                "An error occurred while updating the address. Please try again.")
                        addressType = address_mutation_result.address
                        address = Address.objects.get(id=addressType.id)
                        user.address = address
                    else:
                        address_mutation_result = CreateAddressMutation.mutate(
                            self=self, info=info, details=addres_details, neighborhood_id=neighborhood_id)
                        if address_mutation_result.errors:
                            raise GraphQLError(
                                "An error occurred while creating the address. Please try again.")
                        addressType = address_mutation_result.address
                        address = Address.objects.get(id=addressType.id)
                        user.address = address

                user.save()
                return UpdateUserMutation(user=user)
        except get_user_model().DoesNotExist:
            raise GraphQLError("User does not exist.")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError('An error occurred while saving the data.')


class Query(graphene.ObjectType):
    users = DjangoFilterConnectionField(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    logged_in = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    def user(self, info, id):
        return get_user_model().objects.get(id=id)

    @login_required
    def resolve_logged_in(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Not logged in.")
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
