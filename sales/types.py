import graphene
from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from users.types import NormalUserType
from .models import (
    PayMethod,
    DeliveryMethod,
    Sale,
    SaleDetail,
    SaleDetailOption,
)


class PayMethodFilter(FilterSet):
    class Meta:
        model = PayMethod
        fields = {
            "name": ("exact", "icontains"),
        }


class DeliveryMethodFilter(FilterSet):
    class Meta:
        model = DeliveryMethod
        fields = {
            "name": ("exact", "icontains"),
            "price": ("exact",),
        }


class SaleFilter(FilterSet):
    class Meta:
        model = Sale
        fields = {
            "user": ("exact",),
            "pay_method": ("exact",),
            "delivery_method": ("exact",),
            "date": ("exact", "icontains"),
        }


class SaleDetailFilter(FilterSet):
    class Meta:
        model = SaleDetail
        fields = {
            "sale": ("exact",),
            "carpet": ("exact",),
            "quantity": ("exact",),
        }


class SaleDetailOptionFilter(FilterSet):
    class Meta:
        model = SaleDetailOption
        fields = {
            "sale_detail": ("exact",),
            "custom_option_detail": ("exact",),
        }


class PayMethodType(DjangoObjectType):
    class Meta:
        model = PayMethod
        interfaces = (relay.Node,)
        fields = ("id", "name")
        filterset_class = PayMethodFilter


class DeliveryMethodType(DjangoObjectType):
    class Meta:
        model = DeliveryMethod
        interfaces = (relay.Node,)
        fields = ("id", "name", "price")
        filterset_class = DeliveryMethodFilter


class SaleType(DjangoObjectType):
    total_price = graphene.String()
    user = graphene.Field(NormalUserType)

    class Meta:
        model = Sale
        interfaces = (relay.Node,)
        fields = ("id", "user", "pay_method", "delivery_method", "date")
        filterset_class = SaleFilter

    def resolve_total_price(self, info):
        return self.total_price


class SaleDetailType(DjangoObjectType):
    partial_price = graphene.String()

    class Meta:
        model = SaleDetail
        interfaces = (relay.Node,)
        fields = ("id", "sale", "carpet", "quantity")
        filterset_class = SaleDetailFilter

    def resolve_partial_price(self, info):
        return self.partial_price


class SaleDetailOptionType(DjangoObjectType):
    class Meta:
        model = SaleDetailOption
        interfaces = (relay.Node,)
        fields = ("id", "sale_detail", "custom_option_detail")
        filterset_class = SaleDetailOptionFilter
