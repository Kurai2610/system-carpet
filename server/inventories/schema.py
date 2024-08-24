import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from .types import InventoryItemType
from .models import InventoryItem


class CreateInventoryItemMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        stock = graphene.Int(required=True)
        type = graphene.String(required=True)

    inventory_item = graphene.Field(InventoryItemType)

    @login_required
    @permission_required("inventories.add_inventoryitem")
    def mutate(self, info, name, stock, type, description=None):

        if not name:
            raise GraphQLError("Name is required")

        if not stock:
            raise GraphQLError("Stock is required")

        if not type:
            raise GraphQLError("type is required")

        try:
            inventory_item = InventoryItem(
                name=name, description=description, stock=stock, type=type)
            inventory_item.save()
            return CreateInventoryItemMutation(inventory_item=inventory_item)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("Inventory item already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class DeleteInventoryItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required("inventories.delete_inventoryitem")
    def mutate(self, info, id):

        try:
            inventory_item = InventoryItem.objects.get(pk=id)
            inventory_item.delete()
            return DeleteInventoryItemMutation(success=True)
        except InventoryItem.DoesNotExist:
            raise GraphQLError("Item not found")
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class UpdateInventoryItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        stock = graphene.Int()
        type = graphene.String()

    inventory_item = graphene.Field(InventoryItemType)

    @login_required
    @permission_required("inventories.change_inventoryitem")
    def mutate(self, info, id, name=None, description=None, stock=None, type=None):

        if not name and not description and stock is None and not type:
            raise GraphQLError("At least one field is required")

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
                    raise GraphQLError("Stock must be a positive integer")
            if type:
                inventory_item.type = type

            inventory_item.save()
            return UpdateInventoryItemMutation(inventory_item=inventory_item)
        except InventoryItem.DoesNotExist:
            raise GraphQLError("Item not found")
        except IntegrityError:
            raise GraphQLError("Inventory item already exists")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown Error: {str(e)}")


class Query(graphene.ObjectType):
    inventory_items = DjangoFilterConnectionField(InventoryItemType)
    inventory_item = graphene.Field(
        InventoryItemType, id=graphene.ID())

    def resolve_inventory_items(self, info, **kwargs):
        return InventoryItem.objects.all()

    def resolve_inventory_item(self, info, id):
        return InventoryItem.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_inventory_item = CreateInventoryItemMutation.Field()
    delete_inventory_item = DeleteInventoryItemMutation.Field()
    update_inventory_item = UpdateInventoryItemMutation.Field()
