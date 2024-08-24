import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from graphql_jwt.decorators import login_required, permission_required
from inventories.models import InventoryItem
from inventories.schema import (
    CreateInventoryItemMutation,
    DeleteInventoryItemMutation,
    UpdateInventoryItemMutation
)
from .models import (
    CarType,
    CarMake,
    CarModel,
    ProductCategory,
    Product
)
from .types import (
    CarTypeType,
    CarMakeType,
    CarModelType,
    ProductCategoryType,
    ProductType
)


class CreateCarTypeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)

    @login_required
    @permission_required('products.add_cartype')
    def mutate(self, info, name):

        if not name:
            raise GraphQLError("Name is required")

        try:
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

        if not id:
            raise GraphQLError("ID is required")

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

        if not name:
            raise GraphQLError("Name is required")

        try:
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

        if not name:
            raise GraphQLError("Name is required")

        try:
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

        if not id:
            raise GraphQLError("ID is required")

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

        if not name and not id:
            raise GraphQLError("Name and ID are required")

        try:
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


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        image_link = graphene.String(required=True)
        price = graphene.Int(required=True)
        category_id = graphene.ID(required=True)
        car_model_id = graphene.ID(required=True)
        # InventoryItem arguments
        item_name = graphene.String(required=True)
        item_description = graphene.String()
        item_stock = graphene.Int(required=True)
        item_type = graphene.String(required=True)

    product = graphene.Field(ProductType)

    @login_required
    @permission_required('products.add_product')
    def mutate(self, info, item_name, image_link, price, item_stock, item_type, category_id, car_model_id, item_description=None):

        try:
            with transaction.atomic():
                product_category = ProductCategory.objects.get(pk=category_id)
                car_model = CarModel.objects.get(pk=car_model_id)

                inventory_item_mutation_result = CreateInventoryItemMutation.mutate(
                    self, info, name=item_name, description=item_description, stock=item_stock, type=item_type)
                inventory_itemType = inventory_item_mutation_result.inventory_item
                inventory_item = InventoryItem.objects.get(
                    pk=inventory_itemType.id)

                product = Product(image_link=image_link, price=price, category=product_category,
                                  car_model=car_model, inventory_item=inventory_item)
                product.save()
                return CreateProductMutation(product=product)
        except ProductCategory.DoesNotExist:
            raise GraphQLError('Product category not found')
        except CarModel.DoesNotExist:
            raise GraphQLError('Car model not found')
        except ValidationError as e:
            raise GraphQLError(e)
        except IntegrityError as e:
            raise GraphQLError(
                "Product with this inventory item already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    @permission_required('products.delete_product')
    def mutate(self, info, id):

        try:
            with transaction.atomic():
                product = Product.objects.get(pk=id)
                product.delete()

                item_id = product.inventory_item.id

                DeleteInventoryItemMutation.mutate(
                    self, info, id=item_id)
                return DeleteProductMutation(success=True)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        image_link = graphene.String(required=False)
        price = graphene.Int(required=False)
        category_id = graphene.ID(required=False)
        car_model_id = graphene.ID(required=False)
        # InventoryItem arguments
        item_name = graphene.String(required=False)
        item_description = graphene.String(required=False)
        item_stock = graphene.Int(required=False)
        item_type = graphene.String(required=False)

    product = graphene.Field(ProductType)

    @login_required
    @permission_required('products.change_product')
    def mutate(self, info, id, image_link=None, price=None, category_id=None, car_model_id=None, item_name=None, item_description=None, item_stock=None, item_type=None):

        if not image_link and not price and not category_id and not car_model_id and not item_name and not item_description and not item_stock and not item_type:
            raise GraphQLError("At least one field should be filled")

        try:
            with transaction.atomic():
                product = Product.objects.get(pk=id)

                if image_link:
                    product.image_link = image_link
                if price:
                    product.price = price
                if category_id:
                    product.category = ProductCategory.objects.get(
                        pk=category_id)
                if car_model_id:
                    product.car_model = CarModel.objects.get(pk=car_model_id)
                if item_name or item_description or item_stock or item_type:
                    UpdateInventoryItemMutation.mutate(
                        self, info, id=product.inventory_item.id, name=item_name, description=item_description, stock=item_stock, type=item_type)

                product.save()
                return UpdateProductMutation(product=product)
        except Product.DoesNotExist:
            raise GraphQLError('Product not found')
        except ProductCategory.DoesNotExist:
            raise GraphQLError('Product category not found')
        except CarModel.DoesNotExist:
            raise GraphQLError('Car model not found')
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
    products = DjangoFilterConnectionField(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID(required=True))

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

    def resolve_products(self, info, **kwargs):
        return Product.objects.all()

    def resolve_product(self, info, id):
        return Product.objects.get(pk=id)


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
    create_product = CreateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()
    update_product = UpdateProductMutation.Field()
