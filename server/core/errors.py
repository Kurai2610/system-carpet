class ValidationError(Exception):
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(message)


class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
