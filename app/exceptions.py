from fastapi import HTTPException, status


class AuthServiceException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(AuthServiceException):
    status_code = status.HTTP_409_CONFLICT
    detail = "This user already exists"


class IncorrectUsernameOrPasswordException(AuthServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"


class TokenExpiredException(AuthServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token Expired"


class TokenAbsentException(AuthServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token absent"


class IncorrectTokenFormatException(AuthServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect token format"


class UserIsNotPresentException(AuthServiceException):
    status_code = status.HTTP_401_UNAUTHORIZED
