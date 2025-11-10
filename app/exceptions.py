class AppException(Exception):
    """Exceção base personalizada para o sistema."""
    pass

class NotFoundException(AppException):
    """Entidade não encontrada."""
    pass

class BusinessRuleException(AppException):
    """Falha em regra de negócio."""
    pass

class ValidationException(AppException):
    """Falha em validação de entrada."""
    pass
