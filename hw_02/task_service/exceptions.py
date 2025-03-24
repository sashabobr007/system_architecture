from fastapi import HTTPException, status

class UserException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "На сервере произошла ошибка"

    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail
        )


class TaskNotFoundException(UserException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Goal not found"


class GoalNotFoundException(UserException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Goal not found"

class TaskPermissionDeniedException(UserException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Нет прав для выполнения операции"

class UserNotFoundException(UserException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


class UserNotEnoughPermissions(UserException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not enough permissions"


class InvalidCredentialsException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__()
        self.headers = self.__class__.headers

class UnauthorizedException(UserException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Требуется аутентификация"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self):
        super().__init__()
        self.headers = self.__class__.headers

