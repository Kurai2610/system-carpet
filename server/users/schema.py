import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required, superuser_required
from core.utils import normalize_name, normalize_password
from .types import (
    UserType,
    NormalUserType
)
from addresses.models import Address
from addresses.schema import (
    CreateAddressMutation,
    UpdateAddressMutation
)


class RegisterUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    user = graphene.Field(NormalUserType)

    def mutate(self, info, email, phone, password, first_name, last_name):
        try:
            with transaction.atomic():
                first_name = normalize_name(first_name)
                last_name = normalize_name(last_name)
                password = normalize_password(password)
                user = get_user_model().objects.create_user(
                    email=email,
                    phone=phone,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                client_group = Group.objects.get(name='Client')
                user.groups.add(client_group)

                user.save()
                return RegisterUserMutation(user=user)
        except Group.DoesNotExist:
            raise GraphQLError("Client group does not exist.")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError('An error occurred while saving the data.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class CreateUserAdminMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)

    user = graphene.Field(UserType)

    @login_required
    @superuser_required
    def mutate(self, info, email, phone, password, first_name, last_name):
        try:
            with transaction.atomic():
                first_name = normalize_name(first_name)
                last_name = normalize_name(last_name)
                password = normalize_password(password)
                user = get_user_model().objects.create_superuser(
                    email=email,
                    phone=phone,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                admin_group = Group.objects.get(name='Admin')
                user.groups.add(admin_group)

                user.save()
                return CreateUserAdminMutation(user=user)
        except Group.DoesNotExist:
            raise GraphQLError("Admin group does not exist.")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError('An error occurred while saving the data.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class CreateStaffUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        group = graphene.String(required=True)

    user = graphene.Field(UserType)

    @login_required
    @permission_required('customuser.add_user')
    def mutate(self, info, email, phone, password, first_name, last_name, group):
        try:
            with transaction.atomic():
                first_name = normalize_name(first_name)
                last_name = normalize_name(last_name)
                password = normalize_password(password)
                user = get_user_model().objects.create_user(
                    email=email,
                    phone=phone,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                user_group = Group.objects.get(name=group)
                user.groups.add(user_group)

                user.save()
                return CreateUserAdminMutation(user=user)
        except Group.DoesNotExist:
            raise GraphQLError(f"{group} group does not exist.")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError('An error occurred while saving the data.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        if not user.is_superuser and str(user.id) != id:
            raise GraphQLError("You can only delete your own account.")

        try:
            with transaction.atomic():
                user.is_active = False
                user.save()

                return DeleteUserMutation(success=True)
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

    user = graphene.Field(NormalUserType)

    @login_required
    def mutate(self, info, id, email=None, phone=None, first_name=None, last_name=None, addres_details=None, neighborhood_id=None):

        user = info.context.user
        if not user.is_superuser and str(user.id) != id:
            raise GraphQLError("You can only update your own account.")

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
                    first_name = normalize_name(first_name)
                    user.first_name = first_name
                if last_name:
                    last_name = normalize_name(last_name)
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
    logged_in = graphene.Field(NormalUserType)

    @login_required
    @permission_required('customuser.view_user')
    def resolve_users(self, info, **kwargs):
        return get_user_model().objects.all()

    @login_required
    @permission_required('customuser.view_user')
    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    @login_required
    def resolve_logged_in(self, info):
        user = info.context.user
        return user


class Mutation(graphene.ObjectType):
    register_user = RegisterUserMutation.Field()
    create_user_admin = CreateUserAdminMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
