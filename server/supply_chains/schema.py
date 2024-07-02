# import graphene
# from django.core.exceptions import ValidationError
# from graphene_django import DjangoObjectType
# from .models import Supplier, RawMaterial, MaterialBySupplier, MaterialOrder, OrderDetail
# from addresses.models import Address


# class SupplierType(DjangoObjectType):
#     class Meta:
#         model = Supplier
#         fields = ("id", "name", "email", "phone",
#                   "address", "created_at", "updated_at")


# class RawMaterialType(DjangoObjectType):
#     class Meta:
#         model = RawMaterial
#         fields = ("id", "inventory_item", "created_at", "updated_at")


# class MaterialBySupplierType(DjangoObjectType):
#     class Meta:
#         model = MaterialBySupplier
#         fields = ("id", "raw_material", "supplier",
#                   "price", "created_at", "updated_at")


# class MaterialOrderType(DjangoObjectType):
#     class Meta:
#         model = MaterialOrder
#         fields = ("id", "total_price", "delivery_date",
#                   "created_at", "updated_at")


# class OrderDetailType(DjangoObjectType):
#     class Meta:
#         model = OrderDetail
#         fields = ("id", "material_order", "material_by_supplier",
#                   "quantity", "created_at", "updated_at")


# class CreateSupplierMutation(graphene.Mutation):
#     class Arguments:
#         name = graphene.String(required=True)
#         email = graphene.String(required=True)
#         phone = graphene.String(required=True)
#         address = graphene.ID(required=True)

#     supplier = graphene.Field(SupplierType)
#     errors = graphene.List(graphene.String)

#     def mutate(self, info, name, email, phone, address):
#         try:
#             address = Address.objects.get(pk=address)
#         except Address.DoesNotExist:
#             return CreateSupplierMutation(errors=["Address not found"], supplier=None)

#         supplier = Supplier(name=name, email=email,
#                             phone=phone, address=address)

#         try:
#             supplier.full_clean()
#         except ValidationError as e:
#             return CreateSupplierMutation(errors=list(e.messages), supplier=None)

#         try:
#             supplier.save()
#         except Exception as e:
#             return CreateSupplierMutation(errors=[str(e)])
#         return CreateSupplierMutation(supplier=supplier, errors=None)


# class DeleteSupplierMutation(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)

#     supplier = graphene.Field(SupplierType)
#     errors = graphene.List(graphene.String)

#     def mutate(self, info, id):
#         try:
#             supplier = Supplier.objects.get(id=id)
#             supplier.delete()
#         except Supplier.DoesNotExist:
#             return DeleteSupplierMutation(errors=["Supplier not found"], supplier=None)
#         except Exception as e:
#             return DeleteSupplierMutation(errors=[str(e)], supplier=None)
#         return DeleteSupplierMutation(supplier=None, errors=None)


# class UpdateSupplierMutation(graphene.Mutation):
#     class Arguments:
#         id = graphene.ID(required=True)
#         name = graphene.String(required=True)
#         email = graphene.String(required=True)
#         phone = graphene.String(required=True)
#         address = graphene.ID(required=True)

#     supplier = graphene.Field(SupplierType)
#     errors = graphene.List(graphene.String)

#     def mutate(self, info, id, name=None, email=None, phone=None, address=None):
#         try:
#             supplier = Supplier.objects.get(id=id)
#         except Supplier.DoesNotExist:
#             return UpdateSupplierMutation(errors=["Supplier not found"], supplier=None)

#         if name:
#             supplier.name = name
#         if email:
#             supplier.email = email
#         if phone:
#             supplier.phone = phone
#         if address:
#             try:
#                 address = Address.objects.get(pk=address)
#                 supplier.address = address
#             except Address.DoesNotExist:
#                 return UpdateSupplierMutation(errors=["Address not found"], supplier=None)

# # ! REVISAR SI SON NECESARIOS LOS METODOS MUTATE DE LA APP ADRESSES, Y MODIFICAR EL CREATE DE ESTE ARCHIVO
