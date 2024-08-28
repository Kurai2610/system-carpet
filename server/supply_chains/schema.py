import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from core.utils import normalize_name
from addresses.models import Address
from inventories.models import InventoryItem
from addresses.schema import (
    CreateAddressMutation,
    UpdateAddressMutation,
    DeleteAddressMutation
)
from .models import (
    Supplier,
    MaterialBySupplier,
    MaterialOrder,
    OrderDetail
)
from .types import (
    SupplierType,
    MaterialBySupplierType,
    MaterialOrderType,
    OrderDetailType
)


class CreateSupplierMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String(required=True)
        # Address arguments
        address_details = graphene.String(required=True)
        neighborhood_id = graphene.ID(required=True)

    supplier = graphene.Field(SupplierType)

    @login_required
    @permission_required('supply_chains.add_supplier')
    def mutate(self, info, name, email, phone, address_details, neighborhood_id):
        try:
            with transaction.atomic():
                name = normalize_name(name)
                address_mutation_result = CreateAddressMutation.mutate(
                    self=self, info=info, details=address_details, neighborhood_id=neighborhood_id)
                addressType = address_mutation_result.address
                address = Address.objects.get(pk=addressType.id)
                supplier = Supplier.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    address=address
                )

                return CreateSupplierMutation(supplier=supplier)
        except IntegrityError:
            raise GraphQLError('Supplier already exists.')
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class DeleteSupplierMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    supplier = graphene.Field(SupplierType)

    @login_required
    @permission_required('supply_chains.delete_supplier')
    def mutate(self, info, id):
        try:
            with transaction.atomic():
                supplier = Supplier.objects.get(pk=id)
                supplier.delete()

                address_id = supplier.address.id
                DeleteAddressMutation.mutate(
                    self=self, info=info, id=address_id)

                return DeleteSupplierMutation(supplier=supplier)
        except Supplier.DoesNotExist:
            raise GraphQLError('Supplier not found.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class UpdateSupplierMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        email = graphene.String()
        phone = graphene.String()
        # Address arguments
        address_details = graphene.String()
        neighborhood_id = graphene.ID()

    supplier = graphene.Field(SupplierType)

    @login_required
    @permission_required('supply_chains.change_supplier')
    def mutate(self, info, id, name=None, email=None, phone=None, address_details=None, neighborhood_id=None):
        if not name and not email and not phone and not address_details and not neighborhood_id:
            raise GraphQLError("No data to update.")

        try:
            with transaction.atomic():
                supplier = Supplier.objects.get(pk=id)

                if name:
                    name = normalize_name(name)
                    supplier.name = name
                if email:
                    supplier.email = email
                if phone:
                    supplier.phone = phone

                if address_details or neighborhood_id:
                    if supplier.address:
                        address_id = supplier.address.id
                        address_mutation_result = UpdateAddressMutation.mutate(
                            self=self, info=info, id=address_id, details=address_details, neighborhood_id=neighborhood_id)
                        if address_mutation_result.errors:
                            raise GraphQLError(
                                "An error occurred while updating the address. Please try again.")
                        addressType = address_mutation_result.address
                        address = Address.objects.get(id=addressType.id)
                        supplier.address = address
                    else:
                        address_mutation_result = CreateAddressMutation.mutate(
                            self=self, info=info, details=address_details, neighborhood_id=neighborhood_id)
                        if address_mutation_result.errors:
                            raise GraphQLError(
                                "An error occurred while creating the address. Please try again.")
                        addressType = address_mutation_result.address
                        address = Address.objects.get(id=addressType.id)
                        supplier.address = address

                supplier.save()
                return UpdateSupplierMutation(supplier=supplier)
        except Supplier.DoesNotExist:
            raise GraphQLError('Supplier not found.')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class CreateMaterialBySupplierMutation(graphene.Mutation):
    class Arguments:
        raw_material_id = graphene.ID(
            required=True, description='ID of the raw material (inventory item)')
        supplier_id = graphene.ID(required=True)
        price = graphene.Int(required=True)

    material_by_supplier = graphene.Field(MaterialBySupplierType)

    @login_required
    @permission_required('supply_chains.add_materialbysupplier')
    def mutate(self, info, raw_material_id, supplier_id, price):
        try:
            raw_material = InventoryItem.objects.get(pk=raw_material_id)
            supplier = Supplier.objects.get(pk=supplier_id)
            material_by_supplier = MaterialBySupplier.objects.create(
                raw_material=raw_material,
                supplier=supplier,
                price=price
            )
            return CreateMaterialBySupplierMutation(material_by_supplier=material_by_supplier)
        except InventoryItem.DoesNotExist:
            raise GraphQLError('Raw material not found.')
        except Supplier.DoesNotExist:
            raise GraphQLError('Supplier not found.')
        except IntegrityError:
            raise GraphQLError('Material by supplier already exists.')
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class DeleteMaterialBySupplierMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    material_by_supplier = graphene.Field(MaterialBySupplierType)

    @login_required
    @permission_required('supply_chains.delete_materialbysupplier')
    def mutate(self, info, id):
        try:
            material_by_supplier = MaterialBySupplier.objects.get(pk=id)
            material_by_supplier.delete()
            return DeleteMaterialBySupplierMutation(material_by_supplier=material_by_supplier)
        except MaterialBySupplier.DoesNotExist:
            raise GraphQLError('Material by supplier not found.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class UpdateMaterialBySupplierMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        raw_material_id = graphene.ID(
            description='ID of the raw material (inventory item)')
        supplier_id = graphene.ID()
        price = graphene.Int()

    material_by_supplier = graphene.Field(MaterialBySupplierType)

    @login_required
    @permission_required('supply_chains.change_materialbysupplier')
    def mutate(self, info, id, raw_material_id=None, supplier_id=None, price=None):
        if not raw_material_id and not supplier_id and not price:
            raise GraphQLError("No data to update.")

        try:
            material_by_supplier = MaterialBySupplier.objects.get(pk=id)

            if raw_material_id:
                raw_material = InventoryItem.objects.get(pk=raw_material_id)
                material_by_supplier.raw_material = raw_material
            if supplier_id:
                supplier = Supplier.objects.get(pk=supplier_id)
                material_by_supplier.supplier = supplier
            if price:
                material_by_supplier.price = price

            material_by_supplier.save()
            return UpdateMaterialBySupplierMutation(material_by_supplier=material_by_supplier)
        except MaterialBySupplier.DoesNotExist:
            raise GraphQLError('Material by supplier not found.')
        except InventoryItem.DoesNotExist:
            raise GraphQLError('Raw material not found.')
        except Supplier.DoesNotExist:
            raise GraphQLError('Supplier not found.')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class CreateMaterialOrderMutation(graphene.Mutation):
    class Arguments:
        status = graphene.String(
            required=True, description='Order status(PEN, DEL, CAN)')
        delivery_date = graphene.Date(required=True)

    material_order = graphene.Field(MaterialOrderType)

    @login_required
    @permission_required('supply_chains.add_materialorder')
    def mutate(self, info, status, delivery_date):
        try:
            material_order = MaterialOrder.objects.create(
                status=status,
                delivery_date=delivery_date
            )
            return CreateMaterialOrderMutation(material_order=material_order)
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class DeleteMaterialOrderMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    material_order = graphene.Field(MaterialOrderType)

    @login_required
    @permission_required('supply_chains.delete_materialorder')
    def mutate(self, info, id):
        try:
            material_order = MaterialOrder.objects.get(pk=id)
            material_order.delete()
            return DeleteMaterialOrderMutation(material_order=material_order)
        except MaterialOrder.DoesNotExist:
            raise GraphQLError('Material order not found.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class UpdateMaterialOrderMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.String(description='Order status(PEN, DEL, CAN)')
        delivery_date = graphene.Date()

    material_order = graphene.Field(MaterialOrderType)

    @login_required
    @permission_required('supply_chains.change_materialorder')
    def mutate(self, info, id, status=None, delivery_date=None):
        if not status and not delivery_date:
            raise GraphQLError("No data to update.")

        try:
            material_order = MaterialOrder.objects.get(pk=id)

            if status:
                material_order.status = status
            if delivery_date:
                material_order.delivery_date = delivery_date

            material_order.save()
            return UpdateMaterialOrderMutation(material_order=material_order)
        except MaterialOrder.DoesNotExist:
            raise GraphQLError('Material order not found.')
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class CreateOrderDetailMutation(graphene.Mutation):
    class Arguments:
        material_order_id = graphene.ID(required=True)
        material_by_supplier_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    order_detail = graphene.Field(OrderDetailType)

    @login_required
    @permission_required('supply_chains.add_orderdetail')
    def mutate(self, info, material_order_id, material_by_supplier_id, quantity):
        try:
            material_order = MaterialOrder.objects.get(pk=material_order_id)

            if material_order.status == 'DEL':
                raise GraphQLError(
                    'Cannot add order detail to a delivered order.')
            elif material_order.status == 'CAN':
                raise GraphQLError(
                    'Cannot add order detail to a cancelled order.')

            material_by_supplier = MaterialBySupplier.objects.get(
                pk=material_by_supplier_id)
            order_detail = OrderDetail.objects.create(
                material_order=material_order,
                material_by_supplier=material_by_supplier,
                quantity=quantity
            )
            return CreateOrderDetailMutation(order_detail=order_detail)
        except MaterialOrder.DoesNotExist:
            raise GraphQLError('Material order not found.')
        except MaterialBySupplier.DoesNotExist:
            raise GraphQLError('Material by supplier not found.')
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class DeleteOrderDetailMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    order_detail = graphene.Field(OrderDetailType)

    @login_required
    @permission_required('supply_chains.delete_orderdetail')
    def mutate(self, info, id):
        try:
            order_detail = OrderDetail.objects.get(pk=id)

            if order_detail.material_order.status == 'DEL':
                raise GraphQLError(
                    'Cannot delete order detail from a delivered order.')
            elif order_detail.material_order.status == 'CAN':
                raise GraphQLError(
                    'Cannot delete order detail from a cancelled order.')

            order_detail.delete()
            return DeleteOrderDetailMutation(order_detail=order_detail)
        except OrderDetail.DoesNotExist:
            raise GraphQLError('Order detail not found.')
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class UpdateOrderDetailMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        material_by_supplier_id = graphene.ID()
        quantity = graphene.Int()

    order_detail = graphene.Field(OrderDetailType)

    @login_required
    @permission_required('supply_chains.change_orderdetail')
    def mutate(self, info, id, material_by_supplier_id=None, quantity=None):
        if not material_by_supplier_id and not quantity:
            raise GraphQLError("No data to update.")

        try:
            order_detail = OrderDetail.objects.get(pk=id)

            if order_detail.material_order.status == 'DEL':
                raise GraphQLError(
                    'Cannot update order detail from a delivered order.')
            elif order_detail.material_order.status == 'CAN':
                raise GraphQLError(
                    'Cannot update order detail from a cancelled order.')

            if material_by_supplier_id:
                material_by_supplier = MaterialBySupplier.objects.get(
                    pk=material_by_supplier_id)
                order_detail.material_by_supplier = material_by_supplier
            if quantity:
                order_detail.quantity = quantity

            order_detail.save()
            return UpdateOrderDetailMutation(order_detail=order_detail)
        except OrderDetail.DoesNotExist:
            raise GraphQLError('Order detail not found.')
        except MaterialOrder.DoesNotExist:
            raise GraphQLError('Material order not found.')
        except MaterialBySupplier.DoesNotExist:
            raise GraphQLError('Material by supplier not found.')
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f'Unknown error: {str(e)}')


class Query(graphene.ObjectType):
    supplier = graphene.Field(SupplierType, id=graphene.ID())
    suppliers = DjangoFilterConnectionField(SupplierType)

    material_by_supplier = graphene.Field(
        MaterialBySupplierType, id=graphene.ID())
    materials_by_supplier = DjangoFilterConnectionField(MaterialBySupplierType)

    material_order = graphene.Field(MaterialOrderType, id=graphene.ID())
    material_orders = DjangoFilterConnectionField(MaterialOrderType)

    order_detail = graphene.Field(OrderDetailType, id=graphene.ID())
    order_details = DjangoFilterConnectionField(OrderDetailType)

    @login_required
    @permission_required('supply_chains.view_supplier')
    def resolve_supplier(self, info, id):
        return Supplier.objects.get(pk=id)

    @login_required
    @permission_required('supply_chains.view_supplier')
    def resolve_suppliers(self, info, **kwargs):
        return Supplier.objects.all()

    @login_required
    @permission_required('supply_chains.view_materialbysupplier')
    def resolve_material_by_supplier(self, info, id):
        return MaterialBySupplier.objects.get(pk=id)

    @login_required
    @permission_required('supply_chains.view_materialbysupplier')
    def resolve_materials_by_supplier(self, info, **kwargs):
        return MaterialBySupplier.objects.all()

    @login_required
    @permission_required('supply_chains.view_materialorder')
    def resolve_material_order(self, info, id):
        return MaterialOrder.objects.get(pk=id)

    @login_required
    @permission_required('supply_chains.view_materialorder')
    def resolve_material_orders(self, info, **kwargs):
        return MaterialOrder.objects.all()

    @login_required
    @permission_required('supply_chains.view_orderdetail')
    def resolve_order_detail(self, info, id):
        return OrderDetail.objects.get(pk=id)

    @login_required
    @permission_required('supply_chains.view_orderdetail')
    def resolve_order_details(self, info, **kwargs):
        return OrderDetail.objects.all()


class Mutation(graphene.ObjectType):
    create_supplier = CreateSupplierMutation.Field()
    delete_supplier = DeleteSupplierMutation.Field()
    update_supplier = UpdateSupplierMutation.Field()

    create_material_by_supplier = CreateMaterialBySupplierMutation.Field()
    delete_material_by_supplier = DeleteMaterialBySupplierMutation.Field()
    update_material_by_supplier = UpdateMaterialBySupplierMutation.Field()

    create_material_order = CreateMaterialOrderMutation.Field()
    delete_material_order = DeleteMaterialOrderMutation.Field()
    update_material_order = UpdateMaterialOrderMutation.Field()

    create_order_detail = CreateOrderDetailMutation.Field()
    delete_order_detail = DeleteOrderDetailMutation.Field()
    update_order_detail = UpdateOrderDetailMutation.Field()
