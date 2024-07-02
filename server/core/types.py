import graphene


class ErrorType(graphene.ObjectType):
    code = graphene.String()
    message = graphene.String()
    field = graphene.String(required=False)
