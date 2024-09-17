import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from products.models import Carpet, CustomOptionDetail
from .models import (
    ShoppingCart,
    ShoppingCartItem,
    ShoppingCartItemOption,
)
from .types import (
    ShoppingCartType,
    ShoppingCartItemType,
    ShoppingCartItemOptionType,
)


class CreateShoppingCartMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)

    shopping_cart = graphene.Field(ShoppingCartType)

    @login_required
    @permission_required("shopping_cart.add_shoppingcart")
    def mutate(self, info, user_id):
        try:
            shopping_cart = ShoppingCart.objects.create(user_id=user_id)
            return CreateShoppingCartMutation(shopping_cart=shopping_cart)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("ShoppingCart already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteShoppingCartMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    shopping_cart = graphene.Field(ShoppingCartType)

    @login_required
    @permission_required("shopping_cart.delete_shoppingcart")
    def mutate(self, info, id):
        try:
            shopping_cart = ShoppingCart.objects.get(id=id)
            shopping_cart.delete()
            return DeleteShoppingCartMutation(shopping_cart=shopping_cart)
        except ShoppingCart.DoesNotExist:
            raise GraphQLError("ShoppingCart does not exist")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateShoppingCartItemMutation(graphene.Mutation):
    class Arguments:
        shopping_cart_id = graphene.ID(required=True)
        carpet_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    shopping_cart_item = graphene.Field(ShoppingCartItemType)

    @login_required
    @permission_required("shopping_cart.add_shoppingcartitem")
    def mutate(self, info, shopping_cart_id, carpet_id, quantity):
        try:
            with transaction.atomic():
                shopping_cart = ShoppingCart.objects.get(id=shopping_cart_id)
                carpet = Carpet.objects.get(id=carpet_id)
                shopping_cart_item = ShoppingCartItem.objects.create(
                    shopping_cart=shopping_cart, carpet=carpet, quantity=quantity)
                return CreateShoppingCartItemMutation(shopping_cart_item=shopping_cart_item)
        except ShoppingCart.DoesNotExist:
            raise GraphQLError("ShoppingCart does not exist")
        except Carpet.DoesNotExist:
            raise GraphQLError("Carpet does not exist")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("ShoppingCartItem already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteShoppingCartItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    shopping_cart_item = graphene.Field(ShoppingCartItemType)

    @login_required
    @permission_required("shopping_cart.delete_shoppingcartitem")
    def mutate(self, info, id):
        try:
            shopping_cart_item = ShoppingCartItem.objects.get(id=id)
        except ShoppingCartItem.DoesNotExist:
            raise GraphQLError("ShoppingCartItem does not exist")
        shopping_cart_item.delete()
        return DeleteShoppingCartItemMutation(shopping_cart_item=shopping_cart_item)


class UpdateShoppingCartItemMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    shopping_cart_item = graphene.Field(ShoppingCartItemType)

    @login_required
    @permission_required("shopping_cart.change_shoppingcartitem")
    def mutate(self, info, id, quantity):
        try:
            shopping_cart_item = ShoppingCartItem.objects.get(id=id)
            shopping_cart_item.quantity = quantity
            shopping_cart_item.save()
            return UpdateShoppingCartItemMutation(shopping_cart_item=shopping_cart_item)
        except ShoppingCartItem.DoesNotExist:
            raise GraphQLError("ShoppingCartItem does not exist")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateShoppingCartItemOptionMutation(graphene.Mutation):
    class Arguments:
        shopping_cart_item_id = graphene.ID(required=True)
        custom_option_detail_ids = graphene.List(graphene.ID, required=True)

    shopping_cart_item_option = graphene.Field(ShoppingCartItemOptionType)

    @login_required
    @permission_required("shopping_cart.add_shoppingcartitemoption")
    def mutate(self, info, shopping_cart_item_id, custom_option_detail_ids):
        try:
            with transaction.atomic():
                shopping_cart_item = ShoppingCartItem.objects.get(
                    id=shopping_cart_item_id)
                custom_option_details = CustomOptionDetail.objects.filter(
                    id__in=custom_option_detail_ids)
                shopping_cart_item_option = ShoppingCartItemOption.objects.create(
                    shopping_cart_item=shopping_cart_item)
                shopping_cart_item_option.custom_option_detail.set(
                    custom_option_details)
                return CreateShoppingCartItemOptionMutation(shopping_cart_item_option=shopping_cart_item_option)
        except ShoppingCartItem.DoesNotExist:
            raise GraphQLError("ShoppingCartItem does not exist")
        except CustomOptionDetail.DoesNotExist:
            raise GraphQLError("CustomOptionDetail does not exist")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError:
            raise GraphQLError("ShoppingCartItemOption already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteShoppingCartItemOptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    shopping_cart_item_option = graphene.Field(ShoppingCartItemOptionType)

    @login_required
    @permission_required("shopping_cart.delete_shoppingcartitemoption")
    def mutate(self, info, id):
        try:
            shopping_cart_item_option = ShoppingCartItemOption.objects.get(
                id=id)
            shopping_cart_item_option.delete()
            return DeleteShoppingCartItemOptionMutation(shopping_cart_item_option=shopping_cart_item_option)
        except ShoppingCartItemOption.DoesNotExist:
            raise GraphQLError("ShoppingCartItemOption does not exist")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateShoppingCartItemOptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        add_custom_option_detail_ids = graphene.List(
            graphene.ID, required=False)
        remove_custom_option_detail_ids = graphene.List(
            graphene.ID, required=False)

    shopping_cart_item_option = graphene.Field(ShoppingCartItemOptionType)

    @login_required
    @permission_required("shopping_cart.change_shoppingcartitemoption")
    def mutate(self, info, id, add_custom_option_detail_ids=None, remove_custom_option_detail_ids=None):

        if not add_custom_option_detail_ids and not remove_custom_option_detail_ids:
            raise GraphQLError(
                "Either add_custom_option_detail_ids or remove_custom_option_detail_ids must be provided")

        try:
            shopping_cart_item_option = ShoppingCartItemOption.objects.get(
                id=id)

            if add_custom_option_detail_ids:
                custom_option_details = CustomOptionDetail.objects.filter(
                    id__in=add_custom_option_detail_ids)
                shopping_cart_item_option.custom_option_detail.add(
                    *custom_option_details)

            if remove_custom_option_detail_ids:
                custom_option_details = CustomOptionDetail.objects.filter(
                    id__in=remove_custom_option_detail_ids)
                shopping_cart_item_option.custom_option_detail.remove(
                    *custom_option_details)

            return UpdateShoppingCartItemOptionMutation(shopping_cart_item_option=shopping_cart_item_option)
        except ShoppingCartItemOption.DoesNotExist:
            raise GraphQLError("ShoppingCartItemOption does not exist")
        except CustomOptionDetail.DoesNotExist:
            raise GraphQLError("CustomOptionDetail does not exist")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class Query(graphene.ObjectType):
    shopping_carts = DjangoFilterConnectionField(ShoppingCartType)
    shopping_cart = graphene.Field(
        ShoppingCartType, id=graphene.ID(required=True))
    shopping_cart_items = DjangoFilterConnectionField(ShoppingCartItemType)
    shopping_cart_item = graphene.Field(
        ShoppingCartItemType, id=graphene.ID(required=True))
    shopping_cart_item_options = DjangoFilterConnectionField(
        ShoppingCartItemOptionType)
    shopping_cart_item_option = graphene.Field(
        ShoppingCartItemOptionType, id=graphene.ID(required=True))

    @login_required
    @permission_required("shopping_cart.view_shoppingcart")
    def resolve_shopping_carts(self, info, **kwargs):
        return ShoppingCart.objects.all()

    @login_required
    @permission_required("shopping_cart.view_shoppingcart")
    def resolve_shopping_cart(self, info, id):
        return ShoppingCart.objects.get(id=id)

    @login_required
    @permission_required("shopping_cart.view_shoppingcartitem")
    def resolve_shopping_cart_items(self, info, **kwargs):
        return ShoppingCartItem.objects.all()

    @login_required
    @permission_required("shopping_cart.view_shoppingcartitem")
    def resolve_shopping_cart_item(self, info, id):
        return ShoppingCartItem.objects.get(id=id)

    @login_required
    @permission_required("shopping_cart.view_shoppingcartitemoption")
    def resolve_shopping_cart_item_options(self, info, **kwargs):
        return ShoppingCartItemOption.objects.all()

    @login_required
    @permission_required("shopping_cart.view_shoppingcartitemoption")
    def resolve_shopping_cart_item_option(self, info, id):
        return ShoppingCartItemOption.objects.get(id=id)


class Mutation(graphene.ObjectType):
    create_shopping_cart = CreateShoppingCartMutation.Field()
    delete_shopping_cart = DeleteShoppingCartMutation.Field()
    create_shopping_cart_item = CreateShoppingCartItemMutation.Field()
    delete_shopping_cart_item = DeleteShoppingCartItemMutation.Field()
    update_shopping_cart_item = UpdateShoppingCartItemMutation.Field()
    create_shopping_cart_item_option = CreateShoppingCartItemOptionMutation.Field()
    delete_shopping_cart_item_option = DeleteShoppingCartItemOptionMutation.Field()
    update_shopping_cart_item_option = UpdateShoppingCartItemOptionMutation.Field()
