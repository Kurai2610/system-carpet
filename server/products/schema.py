import graphene
from graphql import GraphQLError
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoObjectType
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
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

    def mutate(self, info, name):

        if not name:
            raise GraphQLError("Name is required")

        try:
            car_type = CarType(name=name)
            car_type.save()
            return CreateCarTypeMutation(car_type=car_type)
        except ValidationError as e:
            raise GraphQLError(e.message)
        except IntegrityError as e:
            raise GraphQLError("Car type with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

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
            raise GraphQLError(e.message)
        except IntegrityError as e:
            raise GraphQLError("Car type with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class CreateCarMakeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)

    def mutate(self, info, name):

        if not name:
            raise GraphQLError("Name is required")

        try:
            car_make = CarMake(name=name)
            car_make.save()
            return CreateCarMakeMutation(car_make=car_make)
        except ValidationError as e:
            raise GraphQLError(e.message)
        except IntegrityError as e:
            raise GraphQLError("Car make with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

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
            raise GraphQLError(e.message)
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
            raise GraphQLError(e.message)
        except IntegrityError as e:
            raise GraphQLError(
                "Car model with this name and year already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

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
            raise GraphQLError(e.message)
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

    def mutate(self, info, name, discount=0):

        try:
            product_category = ProductCategory(name=name, discount=discount)
            product_category.save()
            return CreateProductCategoryMutation(product_category=product_category)
        except ValidationError as e:
            raise GraphQLError(e.message)
        except IntegrityError as e:
            raise GraphQLError(
                "Product category with this name already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

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
            raise GraphQLError(e.message)
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
            raise GraphQLError(e.message)
        except IntegrityError as e:
            raise GraphQLError(
                "Product with this inventory item already exists")
        except Exception as e:
            raise GraphQLError(f"Unknown error: {str(e)}")


class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

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
        category = graphene.ID(required=False)
        car_model = graphene.ID(required=False)
        # ProductCategory arguments
        category_name = graphene.String(required=False)
        discount = graphene.Int(required=False)
        # CarModel arguments
        model_name = graphene.String(required=False)
        model_year = graphene.Int(required=False)
        model_type = graphene.ID(required=False)
        type_name = graphene.String(required=False)
        model_make = graphene.ID(required=False)
        make_name = graphene.String(required=False)
        # InventoryItem arguments
        item_name = graphene.String(required=False)
        item_description = graphene.String(required=False)
        item_stock = graphene.Int(required=False)
        item_type = graphene.String(required=False)

    product = graphene.Field(ProductType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, image_link=None, price=None, category=None, car_model=None, category_name=None, discount=None, model_name=None, model_year=None, model_type=None, type_name=None, model_make=None, make_name=None, item_name=None, item_description=None, item_stock=None, item_type=None):
        errors = []

        if not image_link and not price and not category and not car_model and not category_name and not discount and not model_name and not model_year and not model_type and not type_name and not model_make and not make_name and not item_name and not item_description and not item_stock and not item_type:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="At least one field is required", field="image_link, price, category, car_model, category_name, discount, model_name, model_year, model_type, type_name, model_make, make_name, item_name, item_description, item_stock, item_type"))

        if errors:
            return UpdateProductMutation(product=None, errors=errors)

        try:
            with transaction.atomic():
                product = Product.objects.get(pk=id)

                if image_link:
                    product.image_link = image_link
                if price:
                    product.price = price
                if category:
                    product_category = ProductCategory.objects.get(pk=category)
                    product.category = product_category
                elif category_name or discount:
                    product_category_mutation_result = CreateProductCategoryMutation.mutate(
                        self, info, name=category_name, discount=discount)
                    if product_category_mutation_result.errors:
                        errors.extend(product_category_mutation_result.errors)
                        errors.append(ErrorType(code="PRODUCT_CATEGORY_CREATION_ERROR",
                                                message="Product category creation failed. Please try again"))
                        return UpdateProductMutation(product=None, errors=errors)
                    product_categoryType = product_category_mutation_result.product_category
                    product_category = ProductCategory.objects.get(
                        pk=product_categoryType.id)
                    product.category = product_category
                if car_model:
                    car_model = CarModel.objects.get(pk=car_model)
                    product.car_model = car_model
                elif model_name or model_year or model_type or type_name or model_make or make_name:
                    car_model_mutation_result = CreateCarModelMutation.mutate(
                        self, info, name=model_name, year=model_year, type=model_type, make=model_make, type_name=type_name, make_name=make_name)
                    if car_model_mutation_result.errors:
                        errors.extend(car_model_mutation_result.errors)
                        errors.append(ErrorType(code="CAR_MODEL_CREATION_ERROR",
                                                message="Car model creation failed. Please try again"))
                        return UpdateProductMutation(product=None, errors=errors)
                    car_modelType = car_model_mutation_result.car_model
                    car_model = CarModel.objects.get(pk=car_modelType.id)
                    product.car_model = car_model
                if item_name or item_description or item_stock or item_type:
                    inventory_item_mutation_result = UpdateInventoryItemMutation.mutate(
                        self, info, id=product.inventory_item.id, name=item_name, description=item_description, stock=item_stock, type=item_type)
                    if inventory_item_mutation_result.errors:
                        errors.extend(inventory_item_mutation_result.errors)
                        errors.append(ErrorType(code="INVENTORY_ITEM_UPDATE_ERROR",
                                                message="Inventory item update failed. Please try again"))
                        return UpdateProductMutation(product=None, errors=errors)

                product.full_clean()
                product.save()
                return UpdateProductMutation(product=product, errors=None)
        except Product.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Product not found', field='id'))
            return UpdateProductMutation(product=None, errors=errors)
        except ProductCategory.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Product category not found', field='category'))
            return UpdateProductMutation(product=None, errors=errors)
        except CarModel.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car model not found', field='car_model'))
            return UpdateProductMutation(product=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return UpdateProductMutation(product=None, errors=errors)
        except IntegrityError as e:
            field_name_match = re.search(r'\((.*?)\)', str(e))
            if field_name_match:
                field_name = field_name_match.group(1)
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message=f"Product with this {field_name} already exists", field=field_name))
            else:
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message="unknown integrity error"))
            return UpdateProductMutation(product=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return UpdateProductMutation(product=None, errors=errors)


class Query(graphene.ObjectType):
    car_types = graphene.List(CarTypeType)
    car_type = graphene.Field(CarTypeType, id=graphene.ID(required=True))
    car_makes = graphene.List(CarMakeType)
    car_make = graphene.Field(CarMakeType, id=graphene.ID(required=True))
    car_models = graphene.List(CarModelType)
    car_model = graphene.Field(CarModelType, id=graphene.ID(required=True))
    product_categories = graphene.List(ProductCategoryType)
    product_category = graphene.Field(
        ProductCategoryType, id=graphene.ID(required=True))
    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID(required=True))

    def resolve_car_types(self, info):
        return CarType.objects.all()

    def resolve_car_type(self, info, id):
        return CarType.objects.get(pk=id)

    def resolve_car_makes(self, info):
        return CarMake.objects.all()

    def resolve_car_make(self, info, id):
        return CarMake.objects.get(pk=id)

    def resolve_car_models(self, info):
        return CarModel.objects.all()

    def resolve_car_model(self, info, id):
        return CarModel.objects.get(pk=id)

    def resolve_product_categories(self, info):
        return ProductCategory.objects.all()

    def resolve_product_category(self, info, id):
        return ProductCategory.objects.get(pk=id)

    def resolve_products(self, info):
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
