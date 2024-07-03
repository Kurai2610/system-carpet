import graphene
import graphql_jwt
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
import re
from core.errors import ValidationError as CustomValidationError, DatabaseError
from core.types import ErrorType
from addresses.models import Address
from addresses.schema import CreateAddressMutation, UpdateAddressMutation, DeleteAddressMutation


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser', 'is_staff',
                   'is_active', 'date_joined', 'last_login')


class CreateUserMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        # Address arguments
        details = graphene.String()
        neighborhood_id = graphene.ID()

    user = graphene.Field(UserType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, email, phone, password, first_name, last_name, details=None, neighborhood_id=None):
        errors = []

        try:
            user = get_user_model()(email=email, phone=phone,
                                    first_name=first_name, last_name=last_name)
            user.set_password(password)

            if details and neighborhood_id:
                address_mutation_result = CreateAddressMutation.mutate(
                    self, info, details, neighborhood_id)
                if address_mutation_result.errors:
                    errors.extend(address_mutation_result.errors)
                    errors.append(ErrorType(code="ADDRESS_CREATION_ERROR",
                                            message="An error occurred while creating the address. Please try again."))
                    return CreateUserMutation(user=None, errors=errors)
                addressType = address_mutation_result.address
                address = Address.objects.get(id=addressType.id)
                user.address = address
            user.save()
            return CreateUserMutation(user=user, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
                    return CreateUserMutation(user=None, errors=errors)
        except IntegrityError as e:
            field_name_match = re.search(
                r'detail: Key \((\w+)\)=', str(e.__cause__))
            if field_name_match:
                field_name = field_name_match.group(1)
                errors.append(ErrorType(code="DATABASE_ERROR",
                                        message=f'Duplicate value for {field_name}.', field=field_name))
            else:
                errors.append(ErrorType(code="DATABASE_ERROR",
                                        message='An error occurred while saving the data. (probably duplicate values)', field='non_field_errors'))
            return CreateUserMutation(user=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                                    message=str(e)))
            return CreateUserMutation(user=None, errors=errors)


class DeleteUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            user = get_user_model().objects.get(id=id)
            user.delete()
            if user.address:
                address_id = user.address.id
                address_mutation_result = DeleteAddressMutation.mutate(
                    self=None, info=info, id=address_id)
                if address_mutation_result.errors:
                    errors.extend(address_mutation_result.errors)
                    errors.append(ErrorType(code="ADDRESS_DELETION_ERROR",
                                            message="An error occurred while deleting the address. The user was not deleted. Please try again."))
                    return DeleteUserMutation(message=None, errors=errors)
            return DeleteUserMutation(message="User deleted successfully.", errors=None)
        except get_user_model().DoesNotExist:
            errors.append(ErrorType(
                code="DATABASE_ERROR", message="User does not exist."))
            return DeleteUserMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                                    message=str(e)))
            return DeleteUserMutation(message=None, errors=errors)


class UpdateUserMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        email = graphene.String()
        phone = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        # Address arguments
        details = graphene.String()
        neighborhood_id = graphene.ID()

    user = graphene.Field(UserType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, email=None, phone=None, first_name=None, last_name=None, details=None, neighborhood_id=None):
        errors = []

        try:
            user = get_user_model().objects.get(id=id)

            if details or neighborhood_id:
                address = user.address
                if not address:
                    address_mutation_result = CreateAddressMutation.mutate(
                        self=self, info=info, details=details, neighborhood_id=neighborhood_id)
                    if address_mutation_result.errors:
                        errors.extend(address_mutation_result.errors)
                        errors.append(ErrorType(code="ADDRESS_CREATION_ERROR",
                                                message="An error occurred while creating the address. Please try again."))
                        return UpdateUserMutation(user=None, errors=errors)
                    addressType = address_mutation_result.address
                    address = Address.objects.get(id=addressType.id)
                    user.address = address
                else:
                    address_mutation_result = UpdateAddressMutation.mutate(
                        self=self, info=info, id=address.id, details=details, neighborhood=neighborhood_id)
                    if address_mutation_result.errors:
                        errors.extend(address_mutation_result.errors)
                        errors.append(ErrorType(code="ADDRESS_UPDATE_ERROR",
                                                message="An error occurred while updating the address. The user was not updated. Please try again."))
                        return UpdateUserMutation(user=None, errors=errors)

            if email:
                user.email = email
            if phone:
                user.phone = phone
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name

            user.save()
            user.refresh_from_db()
            return UpdateUserMutation(user=user, errors=errors)
        except get_user_model().DoesNotExist:
            errors.append(ErrorType(
                code="DATABASE_ERROR", message="User does not exist."))
            return UpdateUserMutation(user=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
                    return UpdateUserMutation(user=None, errors=errors)
        except IntegrityError as e:
            field_name_match = re.search(
                r'detail: Key \((\w+)\)=', str(e.__cause__))
            if field_name_match:
                field_name = field_name_match.group(1)
                errors.append(ErrorType(code="DATABASE_ERROR",
                              message=f'Duplicate value for {field_name}.', field=field_name))
            else:
                errors.append(ErrorType(code="DATABASE_ERROR",
                              message='An error occurred while saving the data.', field='non_field_errors'))
            return UpdateUserMutation(user=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return UpdateUserMutation(user=None, errors=errors)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    logged_in = graphene.Field(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def user(self, info, id):
        return get_user_model().objects.get(id=id)

    @login_required
    def resolve_logged_in(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise CustomValidationError(
                code="AUTHENTICATION_ERROR", message="You are not logged in.")
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
    update_user = UpdateUserMutation.Field()
    delete_user = DeleteUserMutation.Field()
