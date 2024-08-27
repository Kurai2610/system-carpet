import graphene
from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from .models import (
    Supplier,
    MaterialBySupplier,
    MaterialOrder,
    OrderDetail
)


class SupplierFilter(FilterSet):
    class Meta:
        model = Supplier
        fields = {
            'name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'address': ['exact'],
            'created_at': ['exact', 'year__gt', 'year__lt'],
            'updated_at': ['exact', 'year__gt', 'year__lt'],
        }


class MaterialBySupplierFilter(FilterSet):
    class Meta:
        model = MaterialBySupplier
        fields = {
            'raw_material': ['exact'],
            'supplier': ['exact'],
            'price': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'year__gt', 'year__lt'],
            'updated_at': ['exact', 'year__gt', 'year__lt'],
        }


class MaterialOrderFilter(FilterSet):
    class Meta:
        model = MaterialOrder
        fields = {
            'status': ['exact'],
            'delivery_date': ['exact', 'year__gt', 'year__lt'],
            'created_at': ['exact', 'year__gt', 'year__lt'],
            'updated_at': ['exact', 'year__gt', 'year__lt'],
        }


class OrderDetailFilter(FilterSet):
    class Meta:
        model = OrderDetail
        fields = {
            'material_order': ['exact'],
            'material_by_supplier': ['exact'],
            'quantity': ['exact', 'gte', 'lte'],
            'created_at': ['exact', 'year__gt', 'year__lt'],
            'updated_at': ['exact', 'year__gt', 'year__lt'],
        }


class SupplierType(DjangoObjectType):
    class Meta:
        model = Supplier
        interfaces = (relay.Node,)
        fields = (
            'id',
            'name',
            'email',
            'phone',
            'address',
            'created_at',
            'updated_at'
        )
        filterset_class = SupplierFilter


class MaterialBySupplierType(DjangoObjectType):
    class Meta:
        model = MaterialBySupplier
        interfaces = (relay.Node,)
        fields = (
            'id',
            'raw_material',
            'supplier',
            'price',
            'created_at',
            'updated_at'
        )
        filterset_class = MaterialBySupplierFilter


class MaterialOrderType(DjangoObjectType):
    total_price = graphene.String(description='Total price of the order')

    class Meta:
        model = MaterialOrder
        interfaces = (relay.Node,)
        fields = (
            'id',
            'status',
            'delivery_date',
            'total_price',
            'created_at',
            'updated_at'
        )
        filterset_class = MaterialOrderFilter

    def resolve_total_price(self, info):
        return self.total_price


class OrderDetailType(DjangoObjectType):
    partial_price = graphene.String(
        description='Partial price of the order detail')

    class Meta:
        model = OrderDetail
        interfaces = (relay.Node,)
        fields = (
            'id',
            'material_order',
            'material_by_supplier',
            'quantity',
            'partial_price',
            'created_at',
            'updated_at'
        )
        filterset_class = OrderDetailFilter

    def resolve_partial_price(self, info):
        return self.partial_price
