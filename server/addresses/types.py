from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from .models import (
    Locality,
    Neighborhood,
    Address
)


class LocalityFilter(FilterSet):
    class Meta:
        model = Locality
        fields = {
            "name": ("exact", "icontains"),
        }


class NeighborhoodFilter(FilterSet):
    class Meta:
        model = Neighborhood
        fields = {
            "name": ("exact", "icontains"),
            "locality": ("exact",),
        }


class AddressFilter(FilterSet):
    class Meta:
        model = Address
        fields = {
            "details": ("exact", "icontains"),
            "neighborhood": ("exact",),
        }


class LocalityType(DjangoObjectType):
    class Meta:
        model = Locality
        interfaces = (relay.Node,)
        fields = ("id", "name")
        filterset_class = LocalityFilter


class NeighborhoodType(DjangoObjectType):
    class Meta:
        model = Neighborhood
        interfaces = (relay.Node,)
        fields = ("id", "name", "locality")
        filterset_class = NeighborhoodFilter


class AddressType(DjangoObjectType):
    class Meta:
        model = Address
        interfaces = (relay.Node,)
        fields = ("id", "details", "neighborhood")
        filterset_class = AddressFilter
