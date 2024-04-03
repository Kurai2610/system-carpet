import graphene
from django.core.exceptions import ValidationError
from graphene_django import DjangoObjectType
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
        fields = ("id", "name")


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "image_link", "price", "category",
                  "car_model", "inventory_item")


class CreateCarTypeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)

    def mutate(self, info, name):
        car_type = CarType(name=name)
        car_type.save()
        return CreateCarTypeMutation(car_type=car_type)


class DeleteCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        car_type = CarType.objects.get(pk=id)
        car_type.delete()
        return DeleteCarTypeMutation(message="Car type deleted successfully.")


class UpdateCarTypeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    car_type = graphene.Field(CarTypeType)

    def mutate(self, info, id, name):
        car_type = CarType.objects.get(pk=id)
        car_type.name = name
        car_type.save()
        return UpdateCarTypeMutation(car_type=car_type)


class CreateCarMakeMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)

    def mutate(self, info, name):
        car_make = CarMake(name=name)
        car_make.save()
        return CreateCarMakeMutation(car_make=car_make)


class DeleteCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        car_make = CarMake.objects.get(pk=id)
        car_make.delete()
        return DeleteCarMakeMutation(message="Car make deleted successfully.")


class UpdateCarMakeMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    car_make = graphene.Field(CarMakeType)

    def mutate(self, info, id, name):
        car_make = CarMake.objects.get(pk=id)
        car_make.name = name
        car_make.save()
        return UpdateCarMakeMutation(car_make=car_make)


class CreateCarModelMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        year = graphene.Int(required=True)
        type_id = graphene.ID(required=True)
        make_id = graphene.ID(required=True)

    car_model = graphene.Field(CarModelType)

    def mutate(self, info, name, year, type_id, make_id):
        car_type = CarType.objects.get(pk=type_id)
        car_make = CarMake.objects.get(pk=make_id)
        car_model = CarModel(name=name, year=year,
                             type=car_type, make=car_make)

        try:
            car_model.full_clean()
        except ValidationError as e:
            return CreateCarModelMutation(car_model=None)

        car_model.save()
        return CreateCarModelMutation(car_model=car_model)


class DeleteCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        car_model = CarModel.objects.get(pk=id)
        car_model.delete()
        return DeleteCarModelMutation(message="Car model deleted successfully.")


class UpdateCarModelMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        year = graphene.Int()
        type_id = graphene.ID()
        make_id = graphene.ID()

    car_model = graphene.Field(CarModelType)

    def mutate(self, info, id, name=None, year=None, type_id=None, make_id=None):
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

        try:
            car_model.full_clean()
        except ValidationError as e:
            return UpdateCarModelMutation(car_model=None)

        car_model.save()
        return UpdateCarModelMutation(car_model=car_model)


class CreateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    product_category = graphene.Field(ProductCategoryType)

    def mutate(self, info, name):
        product_category = ProductCategory(name=name)
        product_category.save()
        return CreateProductCategoryMutation(product_category=product_category)


class DeleteProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        product_category = ProductCategory.objects.get(pk=id)
        product_category.delete()
        return DeleteProductCategoryMutation(message="Product category deleted successfully.")


class UpdateProductCategoryMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String(required=True)

    product_category = graphene.Field(ProductCategoryType)

    def mutate(self, info, id, name):
        product_category = ProductCategory.objects.get(pk=id)
        product_category.name = name
        product_category.save()
        return UpdateProductCategoryMutation(product_category=product_category)


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        image_link = graphene.String(required=True)
        price = graphene.Int(required=True)
        category_id = graphene.ID(required=True)
        car_model_id = graphene.ID(required=True)
        # inventory data
        name = graphene.String(required=True)
        description = graphene.String()
        stock = graphene.Int(required=True)
        type_id = graphene.ID(required=True)

    product = graphene.Field(ProductType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, image_link, price, category_id, car_model_id, name, description, stock, type_id):
        if None in [image_link, price, category_id, car_model_id, name, description, stock, type_id]:
            return CreateProductMutation(product=None, errors=["All fields are required"])

        try:
            inventory_item = CreateInventoryItemMutation.mutate(
                self, info, name=name, description=description, stock=stock, type_id=type_id)
        except Exception as e:
            return CreateProductMutation(product=None, errors=[str(e)])

        try:
            inventory_item = InventoryItem.objects.get(name=name)
        except InventoryItem.DoesNotExist:
            return CreateProductMutation(product=None, errors=["Inventory item not found"])

        try:
            product_category = ProductCategory.objects.get(pk=category_id)
        except ProductCategory.DoesNotExist:
            return CreateProductMutation(product=None, errors=["Product category not found"])

        try:
            car_model = CarModel.objects.get(pk=car_model_id)
        except CarModel.DoesNotExist:
            return CreateProductMutation(product=None, errors=["Car model not found"])

        product = Product(image_link=image_link, price=price, category=product_category,
                          car_model=car_model, inventory_item=inventory_item)
        try:
            product.full_clean()
        except ValidationError as e:
            return CreateProductMutation(product=None, errors=e.message_dict)

        try:
            product.save()
            return CreateProductMutation(product=product, errors=None)
        except ValidationError as e:
            return CreateProductMutation(product=None, errors=e.message_dict)


class DeleteProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()
    errors = graphene.List(graphene.String)

    def mutate(self, info, id):
        try:
            product = Product.objects.get(pk=id)
            inventory_item_id = product.inventory_item.pk
        except Product.DoesNotExist:
            return DeleteProductMutation(message=None, errors=["Product not found"])
        except Exception as e:
            return DeleteProductMutation(message=None, errors=[str(e)])

        try:
            product.delete()
            DeleteInventoryItemMutation.mutate(
                self, info, id=inventory_item_id)
            return DeleteProductMutation(message="Product deleted successfully.")
        except Exception as e:
            return DeleteProductMutation(message=None, errors=[str(e)])


class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        image_link = graphene.String()
        price = graphene.Int()
        category_id = graphene.ID()
        car_model_id = graphene.ID()
        # inventory data
        name = graphene.String()
        description = graphene.String()
        stock = graphene.Int()
        type_id = graphene.ID()

    product = graphene.Field(ProductType)
    errors = graphene.List(graphene.String)

    def mutate(self, info, id, image_link=None, price=None, category_id=None, car_model_id=None, name=None, description=None, stock=None, type_id=None):
        try:
            product = Product.objects.get(pk=id)
            inventory_item_id = product.inventory_item.pk
        except Product.DoesNotExist:
            return UpdateProductMutation(product=None, errors=["Product not found"])
        except Exception as e:
            return DeleteProductMutation(message=None, errors=[str(e)])

        inventory_data = {}

        if name:
            inventory_data["name"] = name
        if description:
            inventory_data["description"] = description
        if stock:
            inventory_data["stock"] = stock
        if type_id:
            inventory_data["type_id"] = type_id

        if inventory_data:
            try:
                UpdateInventoryItemMutation.mutate(
                    self, info, id=inventory_item_id, **inventory_data)
            except Exception as e:
                return UpdateProductMutation(product=None, errors=[str(e)])

        if image_link:
            product.image_link = image_link
        if price:
            product.price = price
        if category_id:
            try:
                product.category = ProductCategory.objects.get(pk=category_id)
            except ProductCategory.DoesNotExist:
                return UpdateProductMutation(product=None, errors=["Product category not found"])
        if car_model_id:
            try:
                product.car_model = CarModel.objects.get(pk=car_model_id)
            except CarModel.DoesNotExist:
                return UpdateProductMutation(product=None, errors=["Car model not found"])

        try:
            product.full_clean()
        except ValidationError as e:
            return UpdateProductMutation(product=None, errors=e.message_dict)

        try:
            product.save()
            return UpdateProductMutation(product=product, errors=None)
        except Exception as e:
            return UpdateProductMutation(product=None, errors=[str(e)])


class Query(graphene.ObjectType):
    car_types = graphene.List(CarTypeType)
    car_type = graphene.Field(CarTypeType, id=graphene.ID())

    car_makes = graphene.List(CarMakeType)
    car_make = graphene.Field(CarMakeType, id=graphene.ID())

    car_models = graphene.List(CarModelType)
    car_model = graphene.Field(CarModelType, id=graphene.ID())

    product_categories = graphene.List(ProductCategoryType)
    product_category = graphene.Field(ProductCategoryType, id=graphene.ID())

    products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.ID())

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


schema = graphene.Schema(query=Query, mutation=Mutation)
