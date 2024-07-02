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
            user.save()

            if details and neighborhood_id:
                address_mutation_result = CreateAddressMutation.mutate(
                    self, info, details, neighborhood_id)
                if address_mutation_result.errors:
                    errors.extend(address_mutation_result.errors)
                    return CreateUserMutation(user=None, errors=errors)
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
                              message='An error occurred while saving the data.', field='non_field_errors'))
            return CreateUserMutation(user=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return CreateUserMutation(user=None, errors=errors)


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    logged_in = graphene.Field(UserType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_logged_in(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise CustomValidationError(
                code="AUTHENTICATION_ERROR", message="You are not logged in.")
        return user


class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field()
