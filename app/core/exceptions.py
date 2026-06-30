class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class UserAlreadyExistsError(AppError):
    pass


class InvalidCredentialsError(AppError):
    pass


class UserNotFoundError(AppError):
    pass


class AccountNotFoundError(AppError):
    pass


class InsufficientFundsError(AppError):
    pass