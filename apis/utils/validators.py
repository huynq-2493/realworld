import re
from typing import Any, Dict, List
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class ValidationUtils:
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    USERNAME_REGEX = re.compile(r'^[a-zA-Z0-9_-]{3,30}$')
    
    @staticmethod
    def validate_email(email: str) -> bool:
        if not email or not ValidationUtils.EMAIL_REGEX.match(email):
            raise ValidationError("Please enter a valid email address.")
        return True
    
    @staticmethod
    def validate_username(username: str) -> bool:
        if not username or not ValidationUtils.USERNAME_REGEX.match(username):
            raise ValidationError(
                "Username must be 3-30 characters long and contain only "
                "letters, numbers, underscores, and hyphens."
            )
        return True
    
    @staticmethod
    def validate_password_strength(password: str) -> bool:
        try:
            validate_password(password)
            return True
        except ValidationError as e:
            raise ValidationError(e.messages)
    
    @staticmethod
    def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> bool:
        missing_fields = []
        
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            raise ValidationError(
                f"The following fields are required: {', '.join(missing_fields)}"
            )
        
        return True
    
    @staticmethod
    def validate_slug(slug: str) -> bool:
        slug_regex = re.compile(r'^[a-z0-9-]+$')
        
        if not slug or not slug_regex.match(slug):
            raise ValidationError(
                "Slug must contain only lowercase letters, numbers, and hyphens."
            )
        
        if slug.startswith('-') or slug.endswith('-'):
            raise ValidationError("Slug cannot start or end with a hyphen.")
        
        if '--' in slug:
            raise ValidationError("Slug cannot contain consecutive hyphens.")
        
        return True
