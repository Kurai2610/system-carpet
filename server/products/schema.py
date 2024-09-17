import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from core.utils import normalize_name
from inventories.models import InventoryItem
from inventories.utils import (
    create_inventory_item,
    delete_inventory_item,
    update_inventory_item,
)
from .models import (
    CarType,
    CarMake,
    CarModel,
    ProductCategory,
    CustomOption,
    CustomOptionDetail,
    Carpet,
)
from .types import (
    CarTypeType,
    CarMakeType,
    CarModelType,
    ProductCategoryType,
    CustomOptionType,
    CustomOptionDetailType,
    CarpetType,
)


class CreateCarTypeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)

    @login_required
    @permission_required('products.add_cartype')
    def mutate(self, info, name):
        try:
            name = normalize_name(name, numbers=True)
            car_type = CarType(name=name)
            car_type.save()
            return CreateCarTypeMutation(car_type=car_type)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("Car type with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_cartype')
    def mutate(self, info, id):
        try:
            car_type = CarType.objects.get(pk=id)
            car_type.delete()
            return DeleteCarTypeMutation(success=True)
        except CarType.DoesNotExist:
            raise GraphQLError('Car type not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)

    @login_required
    @permission_required('products.change_cartype')
    def mutate(self, info, id, name):
        try:
            name = normalize_name(name, numbers=True)
            car_type = CarType.objects.get(pk=id)
            car_type.name = name
            car_type.save()
            return UpdateCarTypeMutation(car_type=car_type)
        except CarType.DoesNotExist:
            raise GraphQLError('Car type not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("Car type with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateCarMakeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)

    @login_required
    @permission_required('products.add_carmake')
    def mutate(self, info, name):
        try:
            name = normalize_name(name, numbers=True)
            car_make = CarMake(name=name)
            car_make.save()
            return CreateCarMakeMutation(car_make=car_make)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("Car make with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_carmake')
    def mutate(self, info, id):
        try:
            car_make = CarMake.objects.get(pk=id)
            car_make.delete()
            return DeleteCarMakeMutation(success=True)
        except CarMake.DoesNotExist:
            raise GraphQLError('Car make not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)

    @login_required
    @permission_required('products.change_carmake')
    def mutate(self, info, id, name):
        try:
            name = normalize_name(name, numbers=True)
            car_make = CarMake.objects.get(pk=id)
            car_make.name = name
            car_make.save()
            return UpdateCarMakeMutation(car_make=car_make)
        except CarMake.DoesNotExist:
            raise GraphQLError('Car make not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError("Car make with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateCarModelMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        year = graphene.Int(required=True)
        type_id = graphene.ID(required=True)
        make_id = graphene.ID(required=True)

    car_model = graphene.Field(CarModelType)

    @login_required
    @permission_required('products.add_carmodel')
    def mutate(self, info, name, year, type_id, make_id):

        try:
            car_type = CarType.objects.get(pk=type_id)

            car_make = CarMake.objects.get(pk=make_id)

            name = normalize_name(name, numbers=True)

            car_model = CarModel(name=name, year=year,
                                 type=car_type, make=car_make)
            car_model.save()
            return CreateCarModelMutation(car_model=car_model)
        except CarType.DoesNotExist:
            raise GraphQLError('Car type not found')
        except CarMake.DoesNotExist:
            raise GraphQLError('Car make not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Car model with this name and year already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_carmodel')
    def mutate(self, info, id):

        try:
            car_model = CarModel.objects.get(pk=id)
            car_model.delete()
            return DeleteCarModelMutation(success=True)
        except CarModel.DoesNotExist:
            raise GraphQLError('Car model not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        year = graphene.Int(required=False)
        type_id = graphene.ID(required=False)
        make_id = graphene.ID(required=False)

    car_model = graphene.Field(CarModelType)

    @login_required
    @permission_required('products.change_carmodel')
    def mutate(self, info, id, name=None, year=None, type_id=None, make_id=None):

        if not name and not year and not type_id and not make_id:
            raise GraphQLError("At least one field should be filled")

        try:
            car_model = CarModel.objects.get(pk=id)

            if name:
                name = normalize_name(name, numbers=True)
                car_model.name = name
            if year:
                car_model.year = year
            if type_id:
                car_type = CarType.objects.get(pk=type_id)
                car_model.type = car_type
            if make_id:
                car_make = CarMake.objects.get(pk=make_id)
                car_model.make = car_make

            car_model.save()
            return UpdateCarModelMutation(car_model=car_model)
        except CarModel.DoesNotExist:
            raise GraphQLError('Car model not found')
        except CarType.DoesNotExist:
            raise GraphQLError('Car type not found')
        except CarMake.DoesNotExist:
            raise GraphQLError('Car make not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Car model with this name and year already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        discount = graphene.Int(default_value=0)

    product_category = graphene.Field(ProductCategoryType)

    @login_required
    @permission_required('products.add_productcategory')
    def mutate(self, info, name, discount=0):

        try:
            name = normalize_name(name, numbers=True)
            product_category = ProductCategory(name=name, discount=discount)
            product_category.save()
            return CreateProductCategoryMutation(product_category=product_category)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Product category with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_productcategory')
    def mutate(self, info, id):

        try:
            product_category = ProductCategory.objects.get(pk=id)
            product_category.delete()
            return DeleteProductCategoryMutation(success=True)
        except ProductCategory.DoesNotExist:
            raise GraphQLError('Product category not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        discount = graphene.Int(required=False)

    product_category = graphene.Field(ProductCategoryType)

    @login_required
    @permission_required('products.change_productcategory')
    def mutate(self, info, id, name=None, discount=None):

        if not name and not discount:
            raise GraphQLError("Name or discount is required")

        try:
            product_category = ProductCategory.objects.get(pk=id)
            if name is not None:
                name = normalize_name(name, numbers=True)
                product_category.name = name
            if discount is not None:
                product_category.discount = discount
            product_category.save()
            return UpdateProductCategoryMutation(product_category=product_category)
        except ProductCategory.DoesNotExist:
            raise GraphQLError('Product category not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Product category with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateCustomOptionMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        required = graphene.Boolean(default_value=False)
        description = graphene.String()

    custom_option = graphene.Field(CustomOptionType)

    @login_required
    @permission_required('products.add_customoption')
    def mutate(self, info, name, required=False, description=None):

        try:
            name = normalize_name(name, numbers=True)
            if description:
                description = description.strip()
            custom_option = CustomOption(
                name=name, required=required, description=description)
            custom_option.save()
            return CreateCustomOptionMutation(custom_option=custom_option)
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Custom option with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCustomOptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_customoption')
    def mutate(self, info, id):

        try:
            custom_option = CustomOption.objects.get(pk=id)
            custom_option.delete()
            return DeleteCustomOptionMutation(success=True)
        except CustomOption.DoesNotExist:
            raise GraphQLError('Custom option not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateCustomOptionMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        required = graphene.Boolean(required=False)
        description = graphene.String(required=False)

    custom_option = graphene.Field(CustomOptionType)

    @login_required
    @permission_required('products.change_customoption')
    def mutate(self, info, id, name=None, required=None, description=None):

        if not name and not required and not description:
            raise GraphQLError("Name, required or description is required")

        try:
            custom_option = CustomOption.objects.get(pk=id)
            if name is not None:
                name = normalize_name(name, numbers=True)
                custom_option.name = name
            if required is not None:
                custom_option.required = required
            if description is not None:
                custom_option.description = description.strip()
            custom_option.save()
            return UpdateCustomOptionMutation(custom_option=custom_option)
        except CustomOption.DoesNotExist:
            raise GraphQLError('Custom option not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Custom option with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateCustomOptionDetailMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        image_url = graphene.String(required=True)
        price = graphene.Int(required=True)
        custom_option_id = graphene.ID(required=True)

    custom_option_detail = graphene.Field(CustomOptionDetailType)

    @login_required
    @permission_required('products.add_customoptiondetail')
    def mutate(self, info, name, image_url, price, custom_option_id):
        try:
            name = normalize_name(name, numbers=True)
            custom_option = CustomOption.objects.get(pk=custom_option_id)
            custom_option_detail = CustomOptionDetail(
                name=name, image_url=image_url, price=price, custom_option=custom_option)
            custom_option_detail.save()
            return CreateCustomOptionDetailMutation(custom_option_detail=custom_option_detail)
        except CustomOption.DoesNotExist:
            raise GraphQLError('Custom option not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                'Custom option detail with this name already exists')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCustomOptionDetailMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_customoptiondetail')
    def mutate(self, info, id):

        try:
            custom_option_detail = CustomOptionDetail.objects.get(pk=id)
            custom_option_detail.delete()
            return DeleteCustomOptionDetailMutation(success=True)
        except CustomOptionDetail.DoesNotExist:
            raise GraphQLError('Custom option detail not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateCustomOptionDetailMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        image_url = graphene.String(required=False)
        price = graphene.Int(required=False)
        custom_option_id = graphene.ID(required=False)

    custom_option_detail = graphene.Field(CustomOptionDetailType)

    @login_required
    @permission_required('products.change_customoptiondetail')
    def mutate(self, info, id, name=None, image_url=None, price=None, custom_option_id=None):

        if not name and not image_url and not price and not custom_option_id:
            raise GraphQLError("At least one field should be filled")

        try:
            custom_option_detail = CustomOptionDetail.objects.get(pk=id)

            if name:
                name = normalize_name(name, numbers=True)
                custom_option_detail.name = name
            if image_url:
                custom_option_detail.image_url = image_url
            if price:
                custom_option_detail.price = price
            if custom_option_id:
                custom_option = CustomOption.objects.get(pk=custom_option_id)
                custom_option_detail.custom_option = custom_option

            custom_option_detail.save()
            return UpdateCustomOptionDetailMutation(custom_option_detail=custom_option_detail)
        except CustomOptionDetail.DoesNotExist:
            raise GraphQLError('Custom option detail not found')
        except CustomOption.DoesNotExist:
            raise GraphQLError('Custom option not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Custom option detail with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateCarpetMutation(graphene.Mutation):
    class Arguments:
        image_link = graphene.String(required=True)
        price = graphene.Int(required=True)
        category_id = graphene.ID(required=True)
        car_model_id = graphene.ID(required=True)
        material_id = graphene.ID(required=True)
        custom_options_ids = graphene.List(graphene.ID)
        # InventoryItem arguments
        item_name = graphene.String(required=True)
        item_description = graphene.String()
        item_stock = graphene.Int(required=True)
        item_type = graphene.String(required=True)

    carpet = graphene.Field(CarpetType)

    @login_required
    @permission_required('products.add_carpet')
    def mutate(self, info, image_link, price, category_id, car_model_id, material_id, item_name, item_description, item_stock, item_type, custom_options_ids=None):

        try:
            with transaction.atomic():
                category = ProductCategory.objects.get(pk=category_id)
                car_model = CarModel.objects.get(pk=car_model_id)
                material = InventoryItem.objects.get(pk=material_id)

                item_name = normalize_name(item_name, numbers=True)

                inventory_item = create_inventory_item(
                    name=item_name, description=item_description, stock=item_stock, type=item_type)

                carpet = Carpet(
                    image_link=image_link,
                    price=price,
                    category=category,
                    car_model=car_model,
                    inventory_item=inventory_item,
                    material=material
                )
                carpet.save()

                if custom_options_ids:
                    for custom_option_id in custom_options_ids:
                        custom_option = CustomOption.objects.get(
                            pk=custom_option_id)
                        carpet.custom_options.add(custom_option)

                return CreateCarpetMutation(carpet=carpet)
        except ProductCategory.DoesNotExist:
            raise GraphQLError('Product category not found')
        except CarModel.DoesNotExist:
            raise GraphQLError('Car model not found')
        except InventoryItem.DoesNotExist:
            raise GraphQLError('Inventory item not found')
        except CustomOption.DoesNotExist:
            raise GraphQLError('Custom option not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(f"Unknown Integrity error: {str(e)}")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarpetMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_carpet')
    def mutate(self, info, id):

        try:
            with transaction.atomic():
                carpet = Carpet.objects.get(pk=id)
                result = delete_inventory_item(carpet.inventory_item.id)
                if result:
                    carpet.delete()
                else:
                    raise GraphQLError(
                        "Carpet inventory item could not be deleted")
                return DeleteCarpetMutation(success=True)
        except Carpet.DoesNotExist:
            raise GraphQLError('Carpet not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateCarpetMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        image_link = graphene.String(required=False)
        price = graphene.Int(required=False)
        category_id = graphene.ID(required=False)
        car_model_id = graphene.ID(required=False)
        material_id = graphene.ID(required=False)
        add_custom_options_ids = graphene.List(graphene.ID)
        remove_custom_options_ids = graphene.List(graphene.ID)
        # InventoryItem arguments
        item_name = graphene.String(required=False)
        item_description = graphene.String(required=False)
        item_stock = graphene.Int(required=False)
        item_type = graphene.String(required=False)

    carpet = graphene.Field(CarpetType)

    @login_required
    @permission_required('products.change_carpet')
    def mutate(self, info, id, image_link=None, price=None, category_id=None, car_model_id=None, material_id=None, item_name=None, item_description=None, item_stock=None, item_type=None, add_custom_options_ids=None, remove_custom_options_ids=None):

        if not image_link and not price and not category_id and not car_model_id and not material_id and not item_name and not item_description and not item_stock and not item_type and not add_custom_options_ids and not remove_custom_options_ids:
            raise GraphQLError("At least one field should be filled")

        try:
            with transaction.atomic():
                carpet = Carpet.objects.get(pk=id)

                if image_link:
                    carpet.image_link = image_link
                if price:
                    carpet.price = price
                if category_id:
                    category = ProductCategory.objects.get(pk=category_id)
                    carpet.category = category
                if car_model_id:
                    car_model = CarModel.objects.get(pk=car_model_id)
                    carpet.car_model = car_model
                if material_id:
                    material = InventoryItem.objects.get(pk=material_id)
                    carpet.material = material
                if item_name or item_description or item_stock or item_type:
                    update_inventory_item(
                        id=carpet.inventory_item.id, name=item_name, description=item_description, stock=item_stock, type=item_type)
                if add_custom_options_ids:
                    for custom_option_id in add_custom_options_ids:
                        custom_option = CustomOption.objects.get(
                            pk=custom_option_id)
                        carpet.custom_options.add(custom_option)
                if remove_custom_options_ids:
                    for custom_option_id in remove_custom_options_ids:
                        custom_option = CustomOption.objects.get(
                            pk=custom_option_id)
                        carpet.custom_options.remove(custom_option)

                carpet.save()
                return UpdateCarpetMutation(carpet=carpet)
        except Carpet.DoesNotExist:
            raise GraphQLError('Carpet not found')
        except ProductCategory.DoesNotExist:
            raise GraphQLError('Product category not found')
        except CarModel.DoesNotExist:
            raise GraphQLError('Car model not found')
        except InventoryItem.DoesNotExist:
            raise GraphQLError('Inventory item not found')
        except CustomOption.DoesNotExist:
            raise GraphQLError('Custom option not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(f"Unknown Integrity error: {str(e)}")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class Query(graphene.ObjectType):
    car_types = DjangoFilterConnectionField(CarTypeType)
    car_type = graphene.Field(CarTypeType, id=graphene.ID(required=True))
    car_makes = DjangoFilterConnectionField(CarMakeType)
    car_make = graphene.Field(CarMakeType, id=graphene.ID(required=True))
    car_models = DjangoFilterConnectionField(CarModelType)
    car_model = graphene.Field(CarModelType, id=graphene.ID(required=True))
    product_categories = DjangoFilterConnectionField(ProductCategoryType)
    product_category = graphene.Field(
        ProductCategoryType, id=graphene.ID(required=True))
    carpets = DjangoFilterConnectionField(CarpetType)
    carpet = graphene.Field(CarpetType, id=graphene.ID(required=True))

    def resolve_car_types(self, info, **kwargs):
        return CarType.objects.all()

    def resolve_car_type(self, info, id):
        return CarType.objects.get(pk=id)

    def resolve_car_makes(self, info, **kwargs):
        return CarMake.objects.all()

    def resolve_car_make(self, info, id):
        return CarMake.objects.get(pk=id)

    def resolve_car_models(self, info, **kwargs):
        return CarModel.objects.all()

    def resolve_car_model(self, info, id):
        return CarModel.objects.get(pk=id)

    def resolve_product_categories(self, info, **kwargs):
        return ProductCategory.objects.all()

    def resolve_product_category(self, info, id):
        return ProductCategory.objects.get(pk=id)

    def resolve_carpets(self, info, **kwargs):
        return Carpet.objects.all()

    def resolve_carpet(self, info, id):
        return Carpet.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_car_type = CreateCarTypeMutation.Field()
    delete_car_type = DeleteCarTypeMutation.Field()
    update_car_type = UpdateCarTypeMutation.Field()
    create_car_make = CreateCarMakeMutation.Field()
    delete_car_make = DeleteCarMakeMutation.Field()
    update_car_make = UpdateCarMakeMutation.Field()
    create_car_model = CreateCarModelMutation.Field()
    delete_car_model = DeleteCarModelMutation.Field()
    update_car_model = UpdateCarModelMutation.Field()
    create_product_category = CreateProductCategoryMutation.Field()
    delete_product_category = DeleteProductCategoryMutation.Field()
    update_product_category = UpdateProductCategoryMutation.Field()
    create_custom_option = CreateCustomOptionMutation.Field()
    delete_custom_option = DeleteCustomOptionMutation.Field()
    update_custom_option = UpdateCustomOptionMutation.Field()
    create_custom_option_detail = CreateCustomOptionDetailMutation.Field()
    delete_custom_option_detail = DeleteCustomOptionDetailMutation.Field()
    update_custom_option_detail = UpdateCustomOptionDetailMutation.Field()
    create_carpet = CreateCarpetMutation.Field()
    delete_carpet = DeleteCarpetMutation.Field()
    update_carpet = UpdateCarpetMutation.Field()
