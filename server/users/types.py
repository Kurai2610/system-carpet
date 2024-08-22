from graphene import relay
from django_filters import FilterSet
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model


class UserFilter(FilterSet):
    class Meta:
        model = get_user_model()
        fields = {
            "first_name": ("exact", "icontains"),
            "last_name": ("exact", "icontains"),
            "email": ("exact", "icontains"),
            "phone": ("exact", "icontains"),
        }


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'is_superuser', 'is_staff',
                   'is_active', 'date_joined', 'last_login')
        interfaces = (relay.Node,)
        fields = "__all__"
        filterset_class = UserFilter
