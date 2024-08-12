from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from .models import (
    CarType,
    CarMake,
    CarModel,
    ProductCategory,
    Product
)


class CarTypeFilter(FilterSet):
    class Meta:
        model = CarType
        fields = {
            "name": ("exact", "icontains"),
        }


class CarMakeFilter(FilterSet):
    class Meta:
        model = CarMake
        fields = {
            "name": ("exact", "icontains"),
        }


class CarModelFilter(FilterSet):
    class Meta:
        model = CarModel
        fields = {
            "name": ("exact", "icontains"),
            "year": ("exact", "icontains"),
            "type": ("exact",),
            "make": ("exact",),
        }


class ProductCategoryFilter(FilterSet):
    class Meta:
        model = ProductCategory
        fields = {
            "name": ("exact", "icontains"),
            "discount": ("exact", "icontains"),
        }


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "price": ("exact", "icontains"),
            "category": ("exact",),
            "car_model": ("exact",),
        }


class CarTypeType(DjangoObjectType):
    class Meta:
        model = CarType
        interfaces = (relay.Node,)
        fields = ("id", "name")
        filterset_class = CarTypeFilter


class CarMakeType(DjangoObjectType):
    class Meta:
        model = CarMake
        interfaces = (relay.Node,)
        fields = ("id", "name")
        filterset_class = CarMakeFilter


class CarModelType(DjangoObjectType):
    class Meta:
        model = CarModel
        interfaces = (relay.Node,)
        fields = ("id", "name", "year", "type", "make")
        filterset_class = CarModelFilter


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        interfaces = (relay.Node,)
        fields = ("id", "name", "discount")
        filterset_class = ProductCategoryFilter


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (relay.Node,)
        fields = ("id", "image_link", "price", "category",
                  "car_model", "inventory_item")
        filterset_class = ProductFilter
