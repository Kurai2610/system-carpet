from functools import wraps
from graphql import GraphQLError


def permission_required(perm):
    def decorator(func):
        @wraps(func)
        def wrapper(self, info, *args, **kwargs):
            user = info.context.user
            if not user.has_perm(perm):
                raise GraphQLError(
                    'No tienes permiso para realizar esta acción.')
            return func(self, info, *args, **kwargs)
        return wrapper
    return decorator
