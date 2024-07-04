import graphene
from graphene_django import DjangoObjectType
from django.db import IntegrityError
from django.core.exceptions import ValidationError as DjangoValidationError
import re
from core.errors import ValidationError as CustomValidationError, DatabaseError
from core.types import ErrorType
from inventories.models import InventoryItem


class InventoryItemType(DjangoObjectType):
    class Meta:
        model = InventoryItem
        fields = ('id', 'name', 'description', 'stock',
                  'type', 'created_at', 'updated_at')

    def resolve_status(self, info):
        return self.status


class CreateInventoryItemMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        stock = graphene.Int(required=True)
        type = graphene.String(required=True)

    inventory_item = graphene.Field(InventoryItemType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name, stock, type, description=None):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message='Name is required', field='name'))

        if not stock:
            if stock != 0:
                errors.append(ErrorType(code="INVALID_INPUT",
                              message='Stock is required', field='stock'))

        if not type:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message='Type is required', field='type'))

        if errors:
            return CreateInventoryItemMutation(inventory_item=None, errors=errors)

        try:
            inventory_item = InventoryItem(
                name=name, description=description, stock=stock, type=type)
            inventory_item.save()
            return CreateInventoryItemMutation(inventory_item=inventory_item, errors=None)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
                    return CreateInventoryItemMutation(inventory_item=None, errors=errors)
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
            return CreateInventoryItemMutation(inventory_item=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return CreateInventoryItemMutation(inventory_item=None, errors=errors)


class DeleteInventoryItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []
        try:
            inventory_item = InventoryItem.objects.get(pk=id)
            inventory_item.delete()
            return DeleteInventoryItemMutation(message='Item deleted successfully', errors=None)
        except InventoryItem.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Item not found', field='id'))
            return DeleteInventoryItemMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return DeleteInventoryItemMutation(message=None, errors=errors)


class UpdateInventoryItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        stock = graphene.Int(required=False)
        type = graphene.String(required=False)

    inventory_item = graphene.Field(InventoryItemType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name=None, description=None, stock=None, type=None):
        errors = []
        try:
            inventory_item = InventoryItem.objects.get(pk=id)
            if name:
                inventory_item.name = name
            if description:
                inventory_item.description = description
            if stock is not None:
                if stock >= 0:
                    inventory_item.stock = stock
                else:
                    errors.append(ErrorType(code="INVALID_INPUT",
                                            message='Stock must be a non-negative value', field='stock'))
            if type:
                inventory_item.type = type

            inventory_item.full_clean()
            inventory_item.save()
            return UpdateInventoryItemMutation(inventory_item=inventory_item)
        except InventoryItem.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Item not found', field='id'))
            return UpdateInventoryItemMutation(inventory_item=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
                    return UpdateInventoryItemMutation(inventory_item=None, errors=errors)
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
            return UpdateInventoryItemMutation(inventory_item=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return UpdateInventoryItemMutation(inventory_item=None, errors=errors)


class Query(graphene.ObjectType):
    inventory_items = graphene.List(InventoryItemType)
    inventory_item = graphene.Field(
        InventoryItemType, id=graphene.ID(required=True))

    def resolve_inventory_items(self, info):
        return InventoryItem.objects.all()

    def resolve_inventory_item(self, info, id):
        return InventoryItem.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_inventory_item = CreateInventoryItemMutation.Field()
    delete_inventory_item = DeleteInventoryItemMutation.Field()
    update_inventory_item = UpdateInventoryItemMutation.Field()
