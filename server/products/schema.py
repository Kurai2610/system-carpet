import re
import graphene
from graphene_django import DjangoObjectType
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from core.errors import ValidationError, DatabaseError
from core.types import ErrorType
from .models import CarType, CarMake, CarModel, ProductCategory, Product
from inventories.models import InventoryItem
from inventories.schema import CreateInventoryItemMutation, DeleteInventoryItemMutation, UpdateInventoryItemMutation


class CarTypeType(DjangoObjectType):
    class Meta:
        model = CarType
        fields = ("id", "name")


class CarMakeType(DjangoObjectType):
    class Meta:
        model = CarMake
        fields = ("id", "name")


class CarModelType(DjangoObjectType):
    class Meta:
        model = CarModel
        fields = ("id", "name", "year", "type", "make")


class ProductCategoryType(DjangoObjectType):
    class Meta:
        model = ProductCategory
        fields = ("id", "name", "discount")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "image_link", "price", "category",
                  "car_model", "inventory_item")


class CreateCarTypeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Name is required for car type", field="name"))

        if errors:
            return CreateCarTypeMutation(car_type=None, errors=errors)
        try:
            car_type = CarType(name=name)
            car_type.save()
            return CreateCarTypeMutation(car_type=car_type, errors=None)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return CreateCarTypeMutation(car_type=None, errors=errors)
        except IntegrityError as e:
            errors.append(ErrorType(code="INTEGRITY_ERROR",
                          message="Car type with this name already exists", field="name"))
            return CreateCarTypeMutation(car_type=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                                    message=str(e)))


class DeleteCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            car_type = CarType.objects.get(pk=id)
            car_type.delete()
            return DeleteCarTypeMutation(message='Car type deleted successfully', errors=None)
        except CarType.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car type not found', field='id'))
            return DeleteCarTypeMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return DeleteCarTypeMutation(message=None, errors=errors)


class UpdateCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Name is required", field="name"))

        if errors:
            return UpdateCarTypeMutation(car_type=None, errors=errors)

        try:
            car_type = CarType.objects.get(pk=id)
            car_type.name = name
            car_type.full_clean()
            car_type.save()
            return UpdateCarTypeMutation(car_type=car_type, errors=None)
        except CarType.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car type not found', field='id'))
            return UpdateCarTypeMutation(car_type=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return UpdateCarTypeMutation(car_type=None, errors=errors)
        except IntegrityError as e:
            errors.append(ErrorType(code="INTEGRITY_ERROR",
                          message="Car type with this name already exists", field="name"))
            return UpdateCarTypeMutation(car_type=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return UpdateCarTypeMutation(car_type=None, errors=errors)


class CreateCarMakeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Name is required", field="name"))

        if errors:
            return CreateCarMakeMutation(car_make=None, errors=errors)

        try:
            car_make = CarMake(name=name)
            car_make.save()
            return CreateCarMakeMutation(car_make=car_make, errors=None)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return CreateCarMakeMutation(car_make=None, errors=errors)
        except IntegrityError as e:
            errors.append(ErrorType(code="INTEGRITY_ERROR",
                          message="Car make with this name already exists", field="name"))
            return CreateCarMakeMutation(car_make=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return CreateCarMakeMutation(car_make=None, errors=errors)


class DeleteCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            car_make = CarMake.objects.get(pk=id)
            car_make.delete()
            return DeleteCarMakeMutation(message='Car make deleted successfully', errors=None)
        except CarMake.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car make not found', field='id'))
            return DeleteCarMakeMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return DeleteCarMakeMutation(message=None, errors=errors)


class UpdateCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Name is required", field="name"))

        if errors:
            return UpdateCarMakeMutation(car_make=None, errors=errors)

        try:
            car_make = CarMake.objects.get(pk=id)
            car_make.name = name
            car_make.full_clean()
            car_make.save()
            return UpdateCarMakeMutation(car_make=car_make, errors=None)
        except CarMake.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car make not found', field='id'))
            return UpdateCarMakeMutation(car_make=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return UpdateCarMakeMutation(car_make=None, errors=errors)
        except IntegrityError as e:
            errors.append(ErrorType(code="INTEGRITY_ERROR",
                          message="Car make with this name already exists", field="name"))
            return UpdateCarMakeMutation(car_make=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return UpdateCarMakeMutation(car_make=None, errors=errors)


class CreateCarModelMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        year = graphene.Int(required=True)
        type = graphene.ID(required=False)
        make = graphene.ID(required=False)
        # CarType arguments
        type_name = graphene.String(required=False)
        # CarMake arguments
        make_name = graphene.String(required=False)

    car_model = graphene.Field(CarModelType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name, year, type=None, make=None, type_name=None, make_name=None):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Name is required", field="name"))

        if not year:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Year is required", field="year"))

        if errors:
            return CreateCarModelMutation(car_model=None, errors=errors)

        try:
            if type:
                car_type = CarType.objects.get(pk=type)
            else:
                car_type_mutation_result = CreateCarTypeMutation.mutate(
                    self, info, name=type_name)
                if car_type_mutation_result.errors:
                    errors.extend(car_type_mutation_result.errors)
                    errors.append(ErrorType(code="CAR_TYPE_CREATION_ERROR",
                                  message="Car type creation failed. Please try again"))
                    return CreateCarModelMutation(car_model=None, errors=errors)
                car_typeType = car_type_mutation_result.car_type
                car_type = CarType.objects.get(pk=car_typeType.id)

            if make:
                car_make = CarMake.objects.get(pk=make)
            else:
                car_make_mutation_result = CreateCarMakeMutation.mutate(
                    self, info, name=make_name)
                if car_make_mutation_result.errors:
                    errors.extend(car_make_mutation_result.errors)
                    errors.append(ErrorType(code="CAR_MAKE_CREATION_ERROR",
                                  message="Car make creation failed. Please try again"))
                    return CreateCarModelMutation(car_model=None, errors=errors)
                car_makeType = car_make_mutation_result.car_make
                car_make = CarMake.objects.get(pk=car_makeType.id)

            car_model = CarModel(name=name, year=year,
                                 type=car_type, make=car_make)
            car_model.save()
            return CreateCarModelMutation(car_model=car_model, errors=None)
        except CarType.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car type not found', field='type'))
            return CreateCarModelMutation(car_model=None, errors=errors)
        except CarMake.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car make not found', field='make'))
            return CreateCarModelMutation(car_model=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return CreateCarModelMutation(car_model=None, errors=errors)
        except IntegrityError as e:
            field_name_match = re.search(r'\((.*?)\)', str(e))
            if field_name_match:
                field_name = field_name_match.group(1)
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message=f"Car model with this {field_name} already exists", field=field_name))
            else:
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message="Car model with this name and year already exists", field="name"))
            return CreateCarModelMutation(car_model=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return CreateCarModelMutation(car_model=None, errors=errors)


class DeleteCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            car_model = CarModel.objects.get(pk=id)
            car_model.delete()
            return DeleteCarModelMutation(message='Car model deleted successfully', errors=None)
        except CarModel.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car model not found', field='id'))
            return DeleteCarModelMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return DeleteCarModelMutation(message=None, errors=errors)


class UpdateCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        year = graphene.Int(required=False)
        type = graphene.ID(required=False)
        make = graphene.ID(required=False)
        # CarType arguments
        type_name = graphene.String(required=False)
        # CarMake arguments
        make_name = graphene.String(required=False)

    car_model = graphene.Field(CarModelType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name=None, year=None, type=None, make=None, type_name=None, make_name=None):
        errors = []

        if not name and not year and not type and not make:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="At least one field is required", field="name, year, type, make"))

        if errors:
            return UpdateCarModelMutation(car_model=None, errors=errors)

        try:
            car_model = CarModel.objects.get(pk=id)

            if name:
                car_model.name = name
            if year:
                car_model.year = year
            if type:
                car_type = CarType.objects.get(pk=type)
                car_model.type = car_type
            elif type_name:
                car_type_mutation_result = CreateCarTypeMutation.mutate(
                    self, info, name=type_name)
                if car_type_mutation_result.errors:
                    errors.extend(car_type_mutation_result.errors)
                    errors.append(ErrorType(code="CAR_TYPE_CREATION_ERROR",
                                  message="Car type creation failed. Please try again"))
                    return UpdateCarModelMutation(car_model=None, errors=errors)
                car_typeType = car_type_mutation_result.car_type
                car_type = CarType.objects.get(pk=car_typeType.id)
                car_model.type = car_type
            if make:
                car_make = CarMake.objects.get(pk=make)
                car_model.make = car_make
            elif make_name:
                car_make_mutation_result = CreateCarMakeMutation.mutate(
                    self, info, name=make_name)
                if car_make_mutation_result.errors:
                    errors.extend(car_make_mutation_result.errors)
                    errors.append(ErrorType(code="CAR_MAKE_CREATION_ERROR",
                                  message="Car make creation failed. Please try again"))
                    return UpdateCarModelMutation(car_model=None, errors=errors)
                car_makeType = car_make_mutation_result.car_make
                car_make = CarMake.objects.get(pk=car_makeType.id)
                car_model.make = car_make

            car_model.full_clean()
            car_model.save()
            return UpdateCarModelMutation(car_model=car_model, errors=None)
        except CarModel.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car model not found', field='id'))
            return UpdateCarModelMutation(car_model=None, errors=errors)
        except CarType.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car type not found', field='type'))
            return UpdateCarModelMutation(car_model=None, errors=errors)
        except CarMake.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car make not found', field='make'))
            return UpdateCarModelMutation(car_model=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return UpdateCarModelMutation(car_model=None, errors=errors)
        except IntegrityError as e:
            field_name_match = re.search(r'\((.*?)\)', str(e))
            if field_name_match:
                field_name = field_name_match.group(1)
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message=f"Car model with this {field_name} already exists", field=field_name))
            else:
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message="Car model with this name and year already exists", field="name"))
            return UpdateCarModelMutation(car_model=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return UpdateCarModelMutation(car_model=None, errors=errors)


class CreateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        discount = graphene.Int(default_value=0)

    product_category = graphene.Field(ProductCategoryType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, name, discount=0):
        errors = []

        if not name:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="Name is required", field="name"))

        if errors:
            return CreateProductCategoryMutation(product_category=None, errors=errors)

        try:
            product_category = ProductCategory(name=name, discount=discount)
            product_category.save()
            return CreateProductCategoryMutation(product_category=product_category, errors=None)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return CreateProductCategoryMutation(product_category=None, errors=errors)
        except IntegrityError as e:
            errors.append(ErrorType(code="INTEGRITY_ERROR",
                                    message="Product category with this name already exists", field="name"))
            return CreateProductCategoryMutation(product_category=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR", message=str(e)))
            return CreateProductCategoryMutation(product_category=None, errors=errors)


class DeleteProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            product_category = ProductCategory.objects.get(pk=id)
            product_category.delete()
            return DeleteProductCategoryMutation(message='Product category deleted successfully', errors=None)
        except ProductCategory.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Product category not found', field='id'))
            return DeleteProductCategoryMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return DeleteProductCategoryMutation(message=None, errors=errors)


class UpdateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=False)
        discount = graphene.Int(required=False)

    product_category = graphene.Field(ProductCategoryType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, id, name=None, discount=None):
        errors = []

        if not name and not discount:
            errors.append(ErrorType(code="INVALID_INPUT",
                                    message="At least one field should be filled", field="name/discount"))

        if errors:
            return UpdateProductCategoryMutation(product_category=None, errors=errors)

        try:
            product_category = ProductCategory.objects.get(pk=id)
            if name is not None:
                product_category.name = name
            if discount is not None:
                product_category.discount = discount
            product_category.full_clean()
            product_category.save()
            return UpdateProductCategoryMutation(product_category=product_category, errors=None)
        except ProductCategory.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                                    message='Product category not found', field='id'))
            return UpdateProductCategoryMutation(product_category=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                            message=error_message, field=field))
            return UpdateProductCategoryMutation(product_category=None, errors=errors)
        except IntegrityError as e:
            errors.append(ErrorType(code="INTEGRITY_ERROR",
                                    message="Product category with this name already exists", field="name"))
            return UpdateProductCategoryMutation(product_category=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                                    message=str(e)))
            return UpdateProductCategoryMutation(product_category=None, errors=errors)


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        image_link = graphene.String(required=True)
        price = graphene.Int(required=True)
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
        item_name = graphene.String(required=True)
        item_description = graphene.String(required=False)
        item_stock = graphene.Int(required=True)
        item_type = graphene.String(required=True)

    product = graphene.Field(ProductType)
    errors = graphene.List(ErrorType)

    def mutate(self, info, item_name, image_link, price, item_stock, item_type, category=None, car_model=None, category_name=None, discount=None, model_name=None, model_year=None, model_type=None, type_name=None, model_make=None, make_name=None, item_description=None):
        errors = []

        if not image_link:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Image link is required", field="image_link"))

        if not price:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Price is required", field="price"))

        if not item_stock:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Stock is required", field="item_stock"))

        if not item_type:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Type is required", field="item_type"))

        if not category and not category_name and not discount:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Category or category_name and discount is required", field="category, category_name, discount"))

        if not car_model and not model_name and not model_year and not model_type and not type_name and not model_make and not make_name:
            errors.append(ErrorType(code="INVALID_INPUT",
                          message="Car model or model_name, model_year, model_type, type_name, model_make, make_name is required", field="car_model, model_name, model_year, model_type, type_name, model_make, make_name"))
        if errors:
            return CreateProductMutation(product=None, errors=errors)

        try:
            with transaction.atomic():
                if category:
                    product_category = ProductCategory.objects.get(pk=category)
                else:
                    product_category_mutation_result = CreateProductCategoryMutation.mutate(
                        self, info, name=category_name, discount=discount)
                    if product_category_mutation_result.errors:
                        errors.extend(product_category_mutation_result.errors)
                        errors.append(ErrorType(code="PRODUCT_CATEGORY_CREATION_ERROR",
                                                message="Product category creation failed. Please try again"))
                        return CreateProductMutation(product=None, errors=errors)
                    product_categoryType = product_category_mutation_result.product_category
                    product_category = ProductCategory.objects.get(
                        pk=product_categoryType.id)

                if car_model:
                    car_model = CarModel.objects.get(pk=car_model)
                else:
                    car_model_mutation_result = CreateCarModelMutation.mutate(
                        self, info, name=model_name, year=model_year, type=model_type, make=model_make, type_name=type_name, make_name=make_name)
                    if car_model_mutation_result.errors:
                        errors.extend(car_model_mutation_result.errors)
                        errors.append(ErrorType(code="CAR_MODEL_CREATION_ERROR",
                                                message="Car model creation failed. Please try again"))
                        return CreateProductMutation(product=None, errors=errors)
                    car_modelType = car_model_mutation_result.car_model
                    car_model = CarModel.objects.get(pk=car_modelType.id)

                inventory_item_mutation_result = CreateInventoryItemMutation.mutate(
                    self, info, name=item_name, description=item_description, stock=item_stock, type=item_type)
                if inventory_item_mutation_result.errors:
                    errors.extend(inventory_item_mutation_result.errors)
                    errors.append(ErrorType(code="INVENTORY_ITEM_CREATION_ERROR",
                                            message="Inventory item creation failed. Please try again"))
                    return CreateProductMutation(product=None, errors=errors)
                inventory_itemType = inventory_item_mutation_result.inventory_item
                inventory_item = InventoryItem.objects.get(
                    pk=inventory_itemType.id)

                product = Product(image_link=image_link, price=price, category=product_category,
                                  car_model=car_model, inventory_item=inventory_item)
                product.save()
                return CreateProductMutation(product=product, errors=None)
        except ProductCategory.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Product category not found', field='category'))
            return CreateProductMutation(product=None, errors=errors)
        except CarModel.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Car model not found', field='car_model'))
            return CreateProductMutation(product=None, errors=errors)
        except InventoryItem.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Inventory item not found', field='inventory_item'))
            return CreateProductMutation(product=None, errors=errors)
        except DjangoValidationError as e:
            for field, error_messages in e.message_dict.items():
                for error_message in error_messages:
                    errors.append(ErrorType(code="VALIDATION_ERROR",
                                  message=error_message, field=field))
            return CreateProductMutation(product=None, errors=errors)
        except IntegrityError as e:
            field_name_match = re.search(r'\((.*?)\)', str(e))
            if field_name_match:
                field_name = field_name_match.group(1)
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message=f"Product with this {field_name} already exists", field=field_name))
            else:
                errors.append(ErrorType(code="INTEGRITY_ERROR",
                              message="unknown integrity error"))
            return CreateProductMutation(product=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return CreateProductMutation(product=None, errors=errors)


class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(ErrorType)

    def mutate(self, info, id):
        errors = []

        try:
            product = Product.objects.get(pk=id)
            product.delete()

            item_id = product.inventory_item.id

            inventory_item_mutation_result = DeleteInventoryItemMutation.mutate(
                self, info, id=item_id)
            if inventory_item_mutation_result.errors:
                errors.extend(inventory_item_mutation_result.errors)
                errors.append(ErrorType(code="INVENTORY_ITEM_DELETION_ERROR",
                              message="Inventory item deletion failed. Please try again"))
                return DeleteProductMutation(message=None, errors=errors)
            return DeleteProductMutation(message='Product deleted successfully', errors=None)
        except Product.DoesNotExist:
            errors.append(ErrorType(code="NOT_FOUND",
                          message='Product not found', field='id'))
            return DeleteProductMutation(message=None, errors=errors)
        except Exception as e:
            errors.append(ErrorType(code="UNKNOWN_ERROR",
                          message=str(e)))
            return DeleteProductMutation(message=None, errors=errors)


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
