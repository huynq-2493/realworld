from typing import Any, Dict, Optional
from rest_framework import status
from rest_framework.response import Response


class ResponseUtils:
    @staticmethod
    def success_response(
        data: Any = None, 
        message: str = "Success", 
        status_code: int = status.HTTP_200_OK
    ) -> Response:
        response_data = {"message": message}
        if data is not None:
            response_data.update(data)
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error_response(
        message: str = "An error occurred",
        errors: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> Response:
        response_data = {"message": message}
        if errors:
            response_data["errors"] = errors
        
        return Response(response_data, status=status_code)
    
    @staticmethod
    def validation_error_response(errors: Dict[str, Any]) -> Response:
        return ResponseUtils.error_response(
            message="Validation failed",
            errors=errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    @staticmethod
    def not_found_response(message: str = "Resource not found") -> Response:
        return ResponseUtils.error_response(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    @staticmethod
    def unauthorized_response(message: str = "Authentication required") -> Response:
        return ResponseUtils.error_response(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    @staticmethod
    def forbidden_response(message: str = "Permission denied") -> Response:
        return ResponseUtils.error_response(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )
