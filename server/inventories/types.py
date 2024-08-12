import graphene
from graphene import relay
from django.db.models import Case, When, Value, CharField
from django_filters import FilterSet, DateFromToRangeFilter, NumberFilter, CharFilter
from graphene_django import DjangoObjectType
from .models import InventoryItem


class InventoryItemFilter(FilterSet):
    status = CharFilter(method="filter_by_status")
    created_at = DateFromToRangeFilter()
    updated_at = DateFromToRangeFilter()
    stock_min = NumberFilter(field_name='stock', lookup_expr='gte')
    stock_max = NumberFilter(field_name='stock', lookup_expr='lte')

    class Meta:
        model = InventoryItem
        fields = {
            'name': ['exact', 'icontains'],
            'description': ['exact', 'icontains'],
            'stock': ['exact', 'icontains'],
            'type': ['exact', 'icontains'],
            'created_at': ['exact', 'icontains'],
            'updated_at': ['exact', 'icontains'],
        }

    def filter_by_status(self, queryset, name, value):
        thresholds = {
            'MAT': {'low_stock_threshold': 10, 'out_of_stock_threshold': 0},
            'CUS': {'low_stock_threshold': None, 'out_of_stock_threshold': 0},
            'RAW': {'low_stock_threshold': 40, 'out_of_stock_threshold': 0},
        }

        queryset = queryset.annotate(
            status=Case(
                When(
                    type='MAT',
                    stock__lte=thresholds['MAT']['out_of_stock_threshold'],
                    then=Value('Out of stock')
                ),
                When(
                    type='MAT',
                    stock__lte=thresholds['MAT']['low_stock_threshold'],
                    then=Value('Low stock')
                ),
                When(
                    type='RAW',
                    stock__lte=thresholds['RAW']['out_of_stock_threshold'],
                    then=Value('Out of stock')
                ),
                When(
                    type='RAW',
                    stock__lte=thresholds['RAW']['low_stock_threshold'],
                    then=Value('Low stock')
                ),
                When(
                    type='CUS',
                    stock__lte=thresholds['CUS']['out_of_stock_threshold'],
                    then=Value('Out of stock')
                ),
                default=Value('Available'),
                output_field=CharField(),
            )
        )
        return queryset.filter(status=value)


class InventoryItemType(DjangoObjectType):
    status = graphene.String(description='Status of the inventory item')
    type = graphene.String(description='Type of the inventory item')

    class Meta:
        model = InventoryItem
        interfaces = (relay.Node,)
        fields = ('id', 'name', 'description', 'stock',
                  'type', 'created_at', 'updated_at', 'status')
        filterset_class = InventoryItemFilter

    def resolve_status(self, info):
        return self.status

    def resolve_type(self, info):
        return self.get_type_display()
