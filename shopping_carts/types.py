import graphene
from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from users.types import NormalUserType
from .models import (
    ShoppingCart,
    ShoppingCartItem,
    ShoppingCartItemOption,
)


class ShoppingCartFilter(FilterSet):
    class Meta:
        model = ShoppingCart
        fields = {
            "created_at": ("exact", "icontains"),
            "updated_at": ("exact", "icontains"),
        }


class ShoppingCartItemFilter(FilterSet):
    class Meta:
        model = ShoppingCartItem
        fields = {
            "shopping_cart": ("exact",),
            "carpet": ("exact",),
            "quantity": ("exact",),
            "created_at": ("exact", "icontains"),
            "updated_at": ("exact", "icontains"),
        }


class ShoppingCartItemOptionFilter(FilterSet):
    class Meta:
        model = ShoppingCartItemOption
        fields = {
            "shopping_cart_item": ("exact",),
            "custom_option_detail": ("exact",),
            "created_at": ("exact", "icontains"),
            "updated_at": ("exact", "icontains"),
        }


class ShoppingCartType(DjangoObjectType):
    total_price = graphene.String()
    user = graphene.Field(NormalUserType)

    class Meta:
        model = ShoppingCart
        interfaces = (relay.Node,)
        fields = ("id", "user", "created_at", "updated_at")
        filterset_class = ShoppingCartFilter

    def resolve_total_price(self, info):
        return self.total_price


class ShoppingCartItemType(DjangoObjectType):
    partial_price = graphene.String()

    class Meta:
        model = ShoppingCartItem
        interfaces = (relay.Node,)
        fields = ("id", "shopping_cart", "carpet",
                  "quantity", "created_at", "updated_at")
        filterset_class = ShoppingCartItemFilter

    def resolve_partial_price(self, info):
        return self.partial_price


class ShoppingCartItemOptionType(DjangoObjectType):
    total_price = graphene.String()

    class Meta:
        model = ShoppingCartItemOption
        interfaces = (relay.Node,)
        fields = ("id", "shopping_cart_item", "custom_option_detail",
                  "created_at", "updated_at")
        filterset_class = ShoppingCartItemOptionFilter

    def resolve_total_price(self, info):
        return self.total_price
