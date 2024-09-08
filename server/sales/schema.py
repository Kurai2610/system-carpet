import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from products.models import Carpet, CustomOptionDetail
from .models import (
    PayMethod,
    DeliveryMethod,
    Sale,
    SaleDetail,
    SaleDetailOption,
)
from .types import (
    PayMethodType,
    DeliveryMethodType,
    SaleType,
    SaleDetailType,
    SaleDetailOptionType,
)


class CreatePayMethodMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    pay_method = graphene.Field(PayMethodType)

    @login_required
    @permission_required("sales.add_paymethod")
    def mutate(self, info, name):
        try:
            pay_method = PayMethod.objects.create(name=name)
            return CreatePayMethodMutation(pay_method=pay_method)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("PayMethod with this name already exists.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeletePayMethodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    pay_method = graphene.Field(PayMethodType)

    @login_required
    @permission_required("sales.delete_paymethod")
    def mutate(self, info, id):
        try:
            pay_method = PayMethod.objects.get(id=id)
            pay_method.delete()
            return DeletePayMethodMutation(pay_method=pay_method)
        except PayMethod.DoesNotExist:
            raise GraphQLError("PayMethod not found.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdatePayMethodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    pay_method = graphene.Field(PayMethodType)

    @login_required
    @permission_required("sales.change_paymethod")
    def mutate(self, info, id, name):
        try:
            pay_method = PayMethod.objects.get(id=id)
            pay_method.name = name
            pay_method.save()
            return UpdatePayMethodMutation(pay_method=pay_method)
        except PayMethod.DoesNotExist:
            raise GraphQLError("PayMethod not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("PayMethod with this name already exists.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateDeliveryMethodMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Int(required=True)

    delivery_method = graphene.Field(DeliveryMethodType)

    @login_required
    @permission_required("sales.add_deliverymethod")
    def mutate(self, info, name, price):
        try:
            delivery_method = DeliveryMethod.objects.create(
                name=name, price=price)
            return CreateDeliveryMethodMutation(delivery_method=delivery_method)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("DeliveryMethod with this name already exists.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteDeliveryMethodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    delivery_method = graphene.Field(DeliveryMethodType)

    @login_required
    @permission_required("sales.delete_deliverymethod")
    def mutate(self, info, id):
        try:
            delivery_method = DeliveryMethod.objects.get(id=id)
            delivery_method.delete()
            return DeleteDeliveryMethodMutation(delivery_method=delivery_method)
        except DeliveryMethod.DoesNotExist:
            raise GraphQLError("DeliveryMethod not found.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateDeliveryMethodMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        price = graphene.Int()

    delivery_method = graphene.Field(DeliveryMethodType)

    @login_required
    @permission_required("sales.change_deliverymethod")
    def mutate(self, info, id, name=None, price=None):

        if not name and not price:
            raise GraphQLError("You must provide a name or a price to update.")

        try:
            delivery_method = DeliveryMethod.objects.get(id=id)
            if name:
                delivery_method.name = name
            if price:
                delivery_method.price = price
            delivery_method.save()
            return UpdateDeliveryMethodMutation(delivery_method=delivery_method)
        except DeliveryMethod.DoesNotExist:
            raise GraphQLError("DeliveryMethod not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("DeliveryMethod with this name already exists.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateSaleMutation(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        pay_method_id = graphene.ID(required=True)
        delivery_method_id = graphene.ID(required=True)

    sale = graphene.Field(SaleType)

    @login_required
    @permission_required("sales.add_sale")
    def mutate(self, info, user_id, pay_method_id, delivery_method_id):
        try:
            sale = Sale.objects.create(
                user_id=user_id,
                pay_method_id=pay_method_id,
                delivery_method_id=delivery_method_id,
            )
            return CreateSaleMutation(sale=sale)
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteSaleMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    sale = graphene.Field(SaleType)

    @login_required
    @permission_required("sales.delete_sale")
    def mutate(self, info, id):
        try:
            sale = Sale.objects.get(id=id)
            sale.delete()
            return DeleteSaleMutation(sale=sale)
        except Sale.DoesNotExist:
            raise GraphQLError("Sale not found.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateSaleMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        user_id = graphene.ID()
        pay_method_id = graphene.ID()
        delivery_method_id = graphene.ID()

    sale = graphene.Field(SaleType)

    @login_required
    @permission_required("sales.change_sale")
    def mutate(self, info, id, user_id=None, pay_method_id=None, delivery_method_id=None):

        if not user_id and not pay_method_id and not delivery_method_id:
            raise GraphQLError(
                "You must provide a user_id, a pay_method_id or a delivery_method_id to update.")

        try:
            sale = Sale.objects.get(id=id)
            if user_id:
                sale.user_id = user_id
            if pay_method_id:
                sale.pay_method_id = pay_method_id
            if delivery_method_id:
                sale.delivery_method_id = delivery_method_id
            sale.save()
            return UpdateSaleMutation(sale=sale)
        except Sale.DoesNotExist:
            raise GraphQLError("Sale not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateSaleDetailMutation(graphene.Mutation):
    class Arguments:
        sale_id = graphene.ID(required=True)
        carpet_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    sale_detail = graphene.Field(SaleDetailType)

    @login_required
    @permission_required("sales.add_saledetail")
    def mutate(self, info, sale_id, carpet_id, quantity):
        try:
            sale = Sale.objects.get(id=sale_id)
            carpet = Carpet.objects.get(id=carpet_id)
            sale_detail = SaleDetail.objects.create(
                sale=sale, carpet=carpet, quantity=quantity)
            return CreateSaleDetailMutation(sale_detail=sale_detail)
        except Sale.DoesNotExist:
            raise GraphQLError("Sale not found.")
        except Carpet.DoesNotExist:
            raise GraphQLError("Carpet not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteSaleDetailMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    sale_detail = graphene.Field(SaleDetailType)

    @login_required
    @permission_required("sales.delete_saledetail")
    def mutate(self, info, id):
        try:
            sale_detail = SaleDetail.objects.get(id=id)
            sale_detail.delete()
            return DeleteSaleDetailMutation(sale_detail=sale_detail)
        except SaleDetail.DoesNotExist:
            raise GraphQLError("SaleDetail not found.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateSaleDetailMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        quantity = graphene.Int()

    sale_detail = graphene.Field(SaleDetailType)

    @login_required
    @permission_required("sales.change_saledetail")
    def mutate(self, info, id, quantity=None):

        if not quantity:
            raise GraphQLError("You must provide a quantity to update.")

        try:
            sale_detail = SaleDetail.objects.get(id=id)
            sale_detail.quantity = quantity
            sale_detail.save()
            return UpdateSaleDetailMutation(sale_detail=sale_detail)
        except SaleDetail.DoesNotExist:
            raise GraphQLError("SaleDetail not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateSaleDetailOptionMutation(graphene.Mutation):
    class Arguments:
        sale_detail_id = graphene.ID(required=True)
        custom_option_detail_id = graphene.List(graphene.ID, required=True)

    sale_detail_option = graphene.Field(SaleDetailOptionType)

    @login_required
    @permission_required("sales.add_saledetailoption")
    def mutate(self, info, sale_detail_id, custom_option_detail_id):
        try:
            sale_detail = SaleDetail.objects.get(id=sale_detail_id)
            sale_detail_option = SaleDetailOption.objects.create(
                sale_detail=sale_detail)
            sale_detail_option.custom_option_detail.set(
                custom_option_detail_id)
            return CreateSaleDetailOptionMutation(sale_detail_option=sale_detail_option)
        except SaleDetail.DoesNotExist:
            raise GraphQLError("SaleDetail not found.")
        except CustomOptionDetail.DoesNotExist:
            raise GraphQLError("CustomOptionDetail not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteSaleDetailOptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    sale_detail_option = graphene.Field(SaleDetailOptionType)

    @login_required
    @permission_required("sales.delete_saledetailoption")
    def mutate(self, info, id):
        try:
            sale_detail_option = SaleDetailOption.objects.get(id=id)
            sale_detail_option.delete()
            return DeleteSaleDetailOptionMutation(sale_detail_option=sale_detail_option)
        except SaleDetailOption.DoesNotExist:
            raise GraphQLError("SaleDetailOption not found.")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateSaleDetailOptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        add_custom_option_detail_id = graphene.List(graphene.ID)
        remove_custom_option_detail_id = graphene.List(graphene.ID)

    sale_detail_option = graphene.Field(SaleDetailOptionType)

    @login_required
    @permission_required("sales.change_saledetailoption")
    def mutate(self, info, id, add_custom_option_detail_id=None, remove_custom_option_detail_id=None):
        if not add_custom_option_detail_id and not remove_custom_option_detail_id:
            raise GraphQLError(
                "You must provide a custom_option_detail_id to update.")

        try:
            sale_detail_option = SaleDetailOption.objects.get(id=id)
            if add_custom_option_detail_id:
                sale_detail_option.custom_option_detail.add(
                    *add_custom_option_detail_id)
            if remove_custom_option_detail_id:
                sale_detail_option.custom_option_detail.remove(
                    *remove_custom_option_detail_id)
            return UpdateSaleDetailOptionMutation(sale_detail_option=sale_detail_option)
        except SaleDetailOption.DoesNotExist:
            raise GraphQLError("SaleDetailOption not found.")
        except CustomOptionDetail.DoesNotExist:
            raise GraphQLError("CustomOptionDetail not found.")
        except ValidationError as e:
            raise GraphQLError(e)
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class Query(graphene.ObjectType):
    pay_methods = DjangoFilterConnectionField(PayMethodType)
    pay_method = graphene.Field(PayMethodType, id=graphene.ID(required=True))
    delivery_methods = DjangoFilterConnectionField(DeliveryMethodType)
    delivery_method = graphene.Field(
        DeliveryMethodType, id=graphene.ID(required=True))
    sales = DjangoFilterConnectionField(SaleType)
    sale = graphene.Field(SaleType, id=graphene.ID(required=True))
    sale_details = DjangoFilterConnectionField(SaleDetailType)
    sale_detail = graphene.Field(
        SaleDetailType, id=graphene.ID(required=True))
    sale_detail_options = DjangoFilterConnectionField(SaleDetailOptionType)
    sale_detail_option = graphene.Field(
        SaleDetailOptionType, id=graphene.ID(required=True))

    @login_required
    @permission_required("sales.view_paymethod")
    def resolve_pay_methods(self, info, **kwargs):
        return PayMethod.objects.all()

    @login_required
    @permission_required("sales.view_paymethod")
    def resolve_pay_method(self, info, id):
        return PayMethod.objects.get(id=id)

    @login_required
    @permission_required("sales.view_deliverymethod")
    def resolve_delivery_methods(self, info, **kwargs):
        return DeliveryMethod.objects.all()

    @login_required
    @permission_required("sales.view_deliverymethod")
    def resolve_delivery_method(self, info, id):
        return DeliveryMethod.objects.get(id=id)

    @login_required
    @permission_required("sales.view_sale")
    def resolve_sales(self, info, **kwargs):
        return Sale.objects.all()

    @login_required
    @permission_required("sales.view_sale")
    def resolve_sale(self, info, id):
        return Sale.objects.get(id=id)

    @login_required
    @permission_required("sales.view_saledetail")
    def resolve_sale_details(self, info, **kwargs):
        return SaleDetail.objects.all()

    @login_required
    @permission_required("sales.view_saledetail")
    def resolve_sale_detail(self, info, id):
        return SaleDetail.objects.get(id=id)

    @login_required
    @permission_required("sales.view_saledetailoption")
    def resolve_sale_detail_options(self, info, **kwargs):
        return SaleDetailOption.objects.all()

    @login_required
    @permission_required("sales.view_saledetailoption")
    def resolve_sale_detail_option(self, info, id):
        return SaleDetailOption.objects.get(id=id)


class Mutation(graphene.ObjectType):
    create_pay_method = CreatePayMethodMutation.Field()
    delete_pay_method = DeletePayMethodMutation.Field()
    update_pay_method = UpdatePayMethodMutation.Field()
    create_delivery_method = CreateDeliveryMethodMutation.Field()
    delete_delivery_method = DeleteDeliveryMethodMutation.Field()
    update_delivery_method = UpdateDeliveryMethodMutation.Field()
    create_sale = CreateSaleMutation.Field()
    delete_sale = DeleteSaleMutation.Field()
    update_sale = UpdateSaleMutation.Field()
    create_sale_detail = CreateSaleDetailMutation.Field()
    delete_sale_detail = DeleteSaleDetailMutation.Field()
    update_sale_detail = UpdateSaleDetailMutation.Field()
    create_sale_detail_option = CreateSaleDetailOptionMutation.Field()
    delete_sale_detail_option = DeleteSaleDetailOptionMutation.Field()
    update_sale_detail_option = UpdateSaleDetailOptionMutation.Field()
