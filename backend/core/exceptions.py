from typing import Any, Optional


class AppError(Exception):
    """Base for all application errors."""
    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, detail: Optional[str] = None, **kwargs: Any) -> None:
        self.detail = detail or self.__class__.detail
        self.extra = kwargs
        super().__init__(self.detail)


class NotFoundError(AppError):
    status_code = 404
    detail = "Resource not found"


class ConflictError(AppError):
    status_code = 409
    detail = "Resource conflict"


class ValidationError(AppError):
    status_code = 422
    detail = "Validation error"


class UnauthorizedError(AppError):
    status_code = 401
    detail = "Not authenticated"


class ForbiddenError(AppError):
    status_code = 403
    detail = "Permission denied"


class SlotUnavailableError(ConflictError):
    detail = "The requested appointment slot is not available"


class AppointmentNotFoundError(NotFoundError):
    detail = "Appointment not found"


class PatientNotFoundError(NotFoundError):
    detail = "Patient not found"


class AgentError(AppError):
    status_code = 502
    detail = "AI agent encountered an error"


class VoiceProcessingError(AppError):
    status_code = 422
    detail = "Voice processing failed"