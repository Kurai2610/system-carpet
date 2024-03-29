import graphene
from graphene_django import DjangoObjectType
from addresses.models import Locality, Address, Neighborhood


class LocalityType(DjangoObjectType):
    class Meta:
        model = Locality
        fields = ("id", "name")


class CreateLocalityMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    locality = graphene.Field(LocalityType)

    def mutate(self, info, name):
        locality = Locality(name=name)
        locality.save()
        return CreateLocalityMutation(locality=locality)


class DeleteLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(self, info, id):
        locality = Locality.objects.get(pk=id)
        locality.delete()
        return DeleteLocalityMutation(message="Locality deleted")


class UpdateLocalityMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    locality = graphene.Field(LocalityType)

    def mutate(self, info, id, name):
        locality = Locality.objects.get(pk=id)

        locality.name = name
        locality.save()
        return UpdateLocalityMutation(locality=locality)


# Query = GET


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello")
    localities = graphene.List(LocalityType)
    locality = graphene.Field(LocalityType, id=graphene.ID())

    def resolve_localities(self, info):
        return Locality.objects.all()

    def resolve_locality(self, info, id):
        return Locality.objects.get(pk=id)


class Mutation(graphene.ObjectType):
    create_locality = CreateLocalityMutation.Field()
    delete_locality = DeleteLocalityMutation.Field()
    update_locality = UpdateLocalityMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
