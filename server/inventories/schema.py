import graphene
from django.core.exceptions import ValidationError
from graphene_django import DjangoObjectType
from inventories.models import Status, Type, InventoryItem


class InventoryStatusType(DjangoObjectType):
    class Meta:
        model = Status
        fields = ("id", "name")


class InventoryTypeType(DjangoObjectType):
    class Meta:
        model = Type
        fields = ("id", "name", "low_stock_threshold",
                  "out_of_stock_threshold")


class InventoryItemType(DjangoObjectType):
    class Meta:
        model = InventoryItem
        fields = ("id", "name", "description", "stock", "status", "type")


class CreateInventoryStatusMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    status = graphene.Field(InventoryStatusType)

    def mutate(self, info, name):
        status = Status(name=name)
        status.save()
        return CreateInventoryStatusMutation(status=status)


class DeleteInventoryStatusMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        status = Status.objects.get(pk=id)
        status.delete()
        return DeleteInventoryStatusMutation(message="Status deleted")


class UpdateInventoryStatusMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    status = graphene.Field(InventoryStatusType)

    def mutate(self, info, id, name):
        status = Status.objects.get(pk=id)

        status.name = name
        status.save()
        return UpdateInventoryStatusMutation(status=status)


class CreateInventoryTypeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        low_stock_threshold = graphene.Int(required=True)
        out_of_stock_threshold = graphene.Int(required=True)

    type = graphene.Field(InventoryTypeType)

    def mutate(self, info, name, low_stock_threshold, out_of_stock_threshold):
        type = Type(name=name, low_stock_threshold=low_stock_threshold,
                    out_of_stock_threshold=out_of_stock_threshold)

        try:
            type.full_clean()
        except ValidationError as e:
            return CreateInventoryTypeMutation(errors=e.message_dict)

        type.save()
        return CreateInventoryTypeMutation(type=type)


class DeleteInventoryTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        type = Type.objects.get(pk=id)
        type.delete()
        return DeleteInventoryTypeMutation(message="Type deleted")


class UpdateInventoryTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        low_stock_threshold = graphene.Int()
        out_of_stock_threshold = graphene.Int()

    type = graphene.Field(InventoryTypeType)

    def mutate(self, info, id, name=None, low_stock_threshold=None, out_of_stock_threshold=None):
        type = Type.objects.get(pk=id)

        if name is not None:
            type.name = name
        if low_stock_threshold is not None:
            type.low_stock_threshold = low_stock_threshold
        if out_of_stock_threshold is not None:
            type.out_of_stock_threshold = out_of_stock_threshold

        try:
            type.full_clean()
        except ValidationError as e:
            return UpdateInventoryTypeMutation(errors=e.message_dict)

        type.save()
        return UpdateInventoryTypeMutation(type=type)


class CreateInventoryItemMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()
        stock = graphene.Int(required=True)
        type_id = graphene.ID(required=True)

    inventory = graphene.Field(InventoryItemType)
    errors = graphene.JSONString()

    def mutate(self, info, name, description, stock, type_id):
        type = Type.objects.get(pk=type_id)
        inventory = InventoryItem(
            name=name, description=description, stock=stock, type=type)

        if inventory.stock < type.out_of_stock_threshold:
            inventory.status = Status.objects.get(name="Out of stock")
        elif inventory.stock < type.low_stock_threshold:
            inventory.status = Status.objects.get(name="Low Stock")
        else:
            inventory.status = Status.objects.get(name="In stock")

        try:
            inventory.full_clean()
        except ValidationError as e:
            return CreateInventoryItemMutation(errors=e.message_dict)

        try:
            inventory.save()
        except ValidationError as e:
            return CreateInventoryItemMutation(errors=e.message_dict)
        return CreateInventoryItemMutation(inventory=inventory)


class DeleteInventoryItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        inventory = InventoryItem.objects.get(pk=id)
        inventory.delete()
        return DeleteInventoryItemMutation(message="Inventory deleted")


class UpdateInventoryItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        stock = graphene.Int()
        type_id = graphene.ID()

    inventory = graphene.Field(InventoryItemType)
    errors = graphene.JSONString()

    def mutate(self, info, id, name=None, description=None, stock=None, type_id=None):
        inventory = InventoryItem.objects.get(pk=id)

        if name is not None:
            inventory.name = name
        if description is not None:
            inventory.description = description
        if stock is not None:
            inventory.stock = stock
        if type_id is not None:
            inventory.type = Type.objects.get(pk=type_id)

        try:
            inventory.full_clean()
        except ValidationError as e:
            return UpdateInventoryItemMutation(errors=e.message_dict)

        inventory.save()
        return UpdateInventoryItemMutation(inventory=inventory)


class Query(graphene.ObjectType):
    inventory_statuses = graphene.List(InventoryStatusType)
    inventory_status = graphene.Field(InventoryStatusType, id=graphene.ID())
    inventory_types = graphene.List(InventoryTypeType)
    inventory_type = graphene.Field(InventoryTypeType, id=graphene.ID())

    def resolve_inventory_statuses(self, info):
        return Status.objects.all()

    def resolve_inventory_status(self, info, id):
        return Status.objects.get(pk=id)

    def resolve_inventory_types(self, info):
        return Type.objects.all()

    def resolve_inventory_type(self, info, id):
        return Type.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_inventory_status = CreateInventoryStatusMutation.Field()
    delete_inventory_status = DeleteInventoryStatusMutation.Field()
    update_inventory_status = UpdateInventoryStatusMutation.Field()

    create_inventory_type = CreateInventoryTypeMutation.Field()
    delete_inventory_type = DeleteInventoryTypeMutation.Field()
    update_inventory_type = UpdateInventoryTypeMutation.Field()
