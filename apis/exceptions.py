from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User already exists."
    default_code = "user_already_exists"


class InvalidCredentialsError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = "Invalid credentials."
    default_code = "invalid_credentials"


class UserNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "User not found."
    default_code = "user_not_found"


class ArticleNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Article not found."
    default_code = "article_not_found"


class CommentNotFoundError(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Comment not found."
    default_code = "comment_not_found"


class PermissionDeniedError(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "Permission denied."
    default_code = "permission_denied"


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Validation error."
    default_code = "validation_error"


class RateLimitExceededError(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = "Rate limit exceeded."
    default_code = "rate_limit_exceeded"
