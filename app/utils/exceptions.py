class FileProcessingError(Exception):
    """Raised when uploaded file cannot be processed."""


class EmailValidationError(Exception):
    """Raised when email content is empty or invalid."""


class AIResponseError(Exception):
    """Raised when IA response is invalid or unavailable."""

