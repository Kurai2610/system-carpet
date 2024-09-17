from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from .models import (
    CarType,
    CarMake,
    CarModel,
    ProductCategory,
    CustomOption,
    CustomOptionDetail,
    Carpet,
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


class CustomOptionFilter(FilterSet):
    class Meta:
        model = CustomOption
        fields = {
            "name": ("exact", "icontains"),
            "required": ("exact",),
        }


class CustomOptionDetailFilter(FilterSet):
    class Meta:
        model = CustomOptionDetail
        fields = {
            "name": ("exact", "icontains"),
            "image_url": ("exact", "icontains"),
            "price": ("exact", "icontains"),
        }


class CarpetFilter(FilterSet):
    class Meta:
        model = Carpet
        fields = {
            "image_link": ("exact", "icontains"),
            "price": ("exact", "icontains"),
            "category": ("exact",),
            "car_model": ("exact",),
            "material": ("exact",),
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


class CustomOptionType(DjangoObjectType):
    class Meta:
        model = CustomOption
        interfaces = (relay.Node,)
        fields = ("id", "name", "required")
        filterset_class = CustomOptionFilter


class CustomOptionDetailType(DjangoObjectType):
    class Meta:
        model = CustomOptionDetail
        interfaces = (relay.Node,)
        fields = ("id", "name", "image_url", "price", "custom_option")
        filterset_class = CustomOptionDetailFilter


class CarpetType(DjangoObjectType):
    class Meta:
        model = Carpet
        interfaces = (relay.Node,)
        fields = ("id", "image_link", "price", "category", "car_model",
                  "inventory_item", "material", "custom_options")
        filterset_class = CarpetFilter
