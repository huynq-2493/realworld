# HTTP Status Messages
HTTP_400_BAD_REQUEST = "Bad Request"
HTTP_401_UNAUTHORIZED = "Unauthorized"
HTTP_403_FORBIDDEN = "Forbidden"
HTTP_404_NOT_FOUND = "Not Found"
HTTP_500_INTERNAL_SERVER_ERROR = "Internal Server Error"

# Authentication Messages
INVALID_CREDENTIALS = "Invalid credentials"
USER_ACCOUNT_DISABLED = "User account is disabled"
AUTHENTICATION_REQUIRED = "Authentication required"
CANNOT_FOLLOW_YOURSELF = "You cannot follow yourself"
CANNOT_DELETE_OTHERS_COMMENTS = "You can only delete your own comments"

# Validation Messages
EMAIL_ALREADY_EXISTS = "A user with this email already exists."
USERNAME_ALREADY_EXISTS = "A user with this username already exists."
EMAIL_AND_PASSWORD_REQUIRED = "Must include email and password"
COMMENT_NOT_FOUND = "Comment not found"

# Cache Keys
TAGS_LIST_CACHE_KEY = "tags_list"
CACHE_TIMEOUT_5_MINUTES = 300

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# Field Constraints
MAX_SLUG_LENGTH = 255
MAX_TITLE_LENGTH = 255
MAX_TAG_NAME_LENGTH = 100
MAX_USERNAME_LENGTH = 150

# URL Patterns
API_VERSION_V1 = "v1"
