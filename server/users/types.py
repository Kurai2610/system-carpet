from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = {
            "name": ("exact", "icontains"),
        }


class GroupType(DjangoObjectType):
    class Meta:
        model = Group
        interfaces = (relay.Node,)
        fields = ('id', 'name')
        filterset_class = GroupFilter


class UserFilter(FilterSet):
    class Meta:
        model = get_user_model()
        fields = {
            "first_name": ("exact", "icontains"),
            "last_name": ("exact", "icontains"),
            "email": ("exact", "icontains"),
            "phone": ("exact", "icontains"),
        }


class NormalUserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser', 'is_staff',
                   'is_active', 'date_joined', 'last_login', 'shoppingcart_set', 'sale_set')
        interfaces = (relay.Node,)
        filterset_class = UserFilter


class UserType(DjangoObjectType):

    class Meta:
        model = get_user_model()
        interfaces = (relay.Node,)
        fields = '__all__'
        filterset_class = UserFilter
