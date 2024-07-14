class OperationalException(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class InvalidEmailError(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class EntityAlreadyExistsError(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class NotFoundError(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)


class EntityAlreadyExistsError(Exception):
    def __init__(self, message: str = ""):
        super().__init__(message)
