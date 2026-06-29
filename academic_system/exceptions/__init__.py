class AcademicDomainException(Exception):
    pass

class InvalidAcademicClassException(AcademicDomainException):
    pass

class InvalidAssessmentException(AcademicDomainException):
    pass

class DuplicateAcademicClassException(AcademicDomainException):
    def __init__(self, code: str):
        super().__init__(f"Turma com código '{code}' já cadastrada.")

class AcademicClassNotFoundException(AcademicDomainException):
    def __init__(self, code: str):
        super().__init__(f"Turma com código '{code}' não encontrada.")

class AuthenticationException(Exception):
    pass

class InvalidCredentialsException(AuthenticationException):
    def __init__(self):
        super().__init__("Usuário ou senha inválidos.")

class MissingAuthenticationDataException(AuthenticationException):
    pass

class UnauthenticatedUserException(AuthenticationException):
    def __init__(self):
        super().__init__("Nenhum usuário autenticado.")

class AuthorizationException(Exception):
    pass

class AccessDeniedException(AuthorizationException):
    def __init__(self, allowed_roles: str = ""):
        super().__init__(f"Acesso negado. Perfis permitidos: {allowed_roles}.")

class UnsupportedPersistenceTypeException(Exception):
    pass

class InvalidKeyboardInputException(Exception):
    pass
