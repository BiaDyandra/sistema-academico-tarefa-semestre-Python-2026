from __future__ import annotations
import logging
from pathlib import Path
from typing import List, Optional

from model import AcademicClass, Assessment
from security import Role, User
from repository import (
    AcademicClassRepository,
    TxtAcademicDataRepository,
    XmlAcademicDataRepository,
    JsonAcademicDataRepository,
    PersistenceType,
)
from exceptions import (
    InvalidCredentialsException,
    MissingAuthenticationDataException,
    UnauthenticatedUserException,
    AccessDeniedException,
    AcademicClassNotFoundException,
    InvalidAcademicClassException,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# AuthenticationService
# ---------------------------------------------------------------------------

class AuthenticationService:
    def __init__(self):
        self._users: dict[str, User] = {}
        self._authenticated_user: Optional[User] = None
        self._register_default_users()

    def _register_default_users(self):
        self._add_user(User("admin", "admin123", Role.ADMIN))
        self._add_user(User("professor", "prof123", Role.PROFESSOR))

    def _add_user(self, user: User):
        self._users[user.username.lower()] = user

    def authenticate(self, username: str, password: str) -> User:
        if not username or not username.strip():
            logger.warning("Falha na tentativa de login. Usuário: desconhecido.")
            raise MissingAuthenticationDataException("Informe o usuário.")

        username = username.strip()

        if not password or not password.strip():
            logger.warning("Falha na tentativa de login. Usuário: %s.", username)
            raise MissingAuthenticationDataException("Informe a senha.")

        user = self._users.get(username.lower())

        if user is None or user.password != password:
            logger.warning("Falha na tentativa de login. Usuário: %s.", username)
            raise InvalidCredentialsException()

        self._authenticated_user = user
        logger.info("Login realizado com sucesso. Usuário: %s | Perfil: %s", user.username, user.role.value)
        return user

    def logout(self):
        if self._authenticated_user:
            logger.info("Logout realizado. Usuário: %s", self._authenticated_user.username)
        else:
            logger.info("Logout solicitado sem usuário autenticado.")
        self._authenticated_user = None

    def get_authenticated_user(self) -> User:
        if self._authenticated_user is None:
            raise UnauthenticatedUserException()
        return self._authenticated_user

    def is_authenticated(self) -> bool:
        return self._authenticated_user is not None


# ---------------------------------------------------------------------------
# AuthorizationService
# ---------------------------------------------------------------------------

class AuthorizationService:
    def require_any_role(self, user: Optional[User], *allowed_roles: Role):
        allowed_text = ", ".join(r.value for r in allowed_roles)

        if user is None:
            logger.warning(
                "Falha de autorização. Usuário: desconhecido | Perfis permitidos: %s", allowed_text
            )
            raise UnauthenticatedUserException()

        if user.role not in allowed_roles:
            logger.warning(
                "Falha de autorização. Usuário: %s | Perfil atual: %s | Perfis permitidos: %s",
                user.username, user.role.value, allowed_text,
            )
            raise AccessDeniedException(allowed_text)


# ---------------------------------------------------------------------------
# ClassService
# ---------------------------------------------------------------------------

class ClassService:
    def __init__(self, repository: AcademicClassRepository):
        self._repository = repository

    def register_class(self, code: str, name: str):
        academic_class = AcademicClass(code, name)
        self._repository.save(academic_class)

    def list_classes(self) -> List[AcademicClass]:
        return self._repository.find_all()


# ---------------------------------------------------------------------------
# AssessmentService
# ---------------------------------------------------------------------------

class AssessmentService:
    def __init__(self, repository: AcademicClassRepository):
        self._repository = repository

    def register_assessment(self, class_code: str, assessment_name: str, weight: float):
        if not class_code or not class_code.strip():
            raise InvalidAcademicClassException("Informe o código da turma para cadastrar a avaliação.")

        academic_class = self._repository.find_by_code(class_code)
        if academic_class is None:
            raise AcademicClassNotFoundException(class_code)

        assessment = Assessment(assessment_name, weight)
        academic_class.add_assessment(assessment)


# ---------------------------------------------------------------------------
# PersistenceService
# ---------------------------------------------------------------------------

class PersistenceService:
    def __init__(
        self,
        txt_repository: TxtAcademicDataRepository,
        xml_repository: XmlAcademicDataRepository,
        json_repository: JsonAcademicDataRepository,
    ):
        self._txt_repo = txt_repository
        self._xml_repo = xml_repository
        self._json_repo = json_repository
        self._current_type = PersistenceType.TXT

    @property
    def current_persistence_type(self) -> PersistenceType:
        return self._current_type

    def configure_persistence_type(self, persistence_type: PersistenceType):
        self._current_type = persistence_type
        logger.info("Tipo de persistência configurado para: %s", persistence_type.description)

    def save(self, classes: List[AcademicClass]) -> Path:
        if self._current_type == PersistenceType.TXT:
            return self.save_to_txt(classes)
        elif self._current_type == PersistenceType.XML:
            return self.save_to_xml(classes)
        else:
            return self.save_to_json(classes)

    def save_to_txt(self, classes: List[AcademicClass]) -> Path:
        try:
            path = self._txt_repo.save(classes)
            self._log_success(PersistenceType.TXT, classes, path)
            return path
        except Exception as e:
            self._log_failure("salvar dados acadêmicos", PersistenceType.TXT, e)
            raise

    def save_to_xml(self, classes: List[AcademicClass]) -> Path:
        try:
            path = self._xml_repo.save(classes)
            self._log_success(PersistenceType.XML, classes, path)
            return path
        except Exception as e:
            self._log_failure("salvar dados acadêmicos", PersistenceType.XML, e)
            raise

    def save_to_json(self, classes: List[AcademicClass]) -> Path:
        try:
            path = self._json_repo.save(classes)
            self._log_success(PersistenceType.JSON, classes, path)
            return path
        except Exception as e:
            self._log_failure("salvar dados acadêmicos", PersistenceType.JSON, e)
            raise

    def _log_success(self, pt: PersistenceType, classes: List[AcademicClass], path: Path):
        logger.info(
            "Dados acadêmicos persistidos com sucesso. Tipo: %s | Turmas: %d | Arquivo: %s",
            pt.description, len(classes) if classes else 0, path,
        )

    def _log_failure(self, operation: str, pt: PersistenceType, exc: Exception):
        logger.warning(
            "Falha na operação de persistência. Operação: %s | Tipo: %s | Erro: %s",
            operation, pt.description, str(exc),
        )


# ---------------------------------------------------------------------------
# ReportService
# ---------------------------------------------------------------------------

class ReportService:
    def generate_class_assessment_summary_report(
        self, classes: List[AcademicClass], user_role: str = ""
    ) -> str:
        if user_role:
            self._log_report("Resumo de avaliações por turma", user_role)
        return self._build_class_assessment_summary(classes)

    def generate_assessment_weight_report(
        self, classes: List[AcademicClass], user_role: str = ""
    ) -> str:
        if user_role:
            self._log_report("Relatório de peso de avaliações", user_role)
        return self._build_assessment_weight_report(classes)

    def generate_persistence_configuration_report(
        self, current_type: PersistenceType, user_role: str = ""
    ) -> str:
        if user_role:
            self._log_report("Relatório de configuração de persistência", user_role)
        return self._build_persistence_config_report(current_type)

    def generate_classes_and_assessments_listing(self, classes: List[AcademicClass]) -> str:
        if not classes:
            return "Nenhuma turma cadastrada."
        lines = ["===== Turmas e Avaliações ====="]
        for ac in classes:
            lines.append(f"Turma: {ac.code} - {ac.name}")
            if not ac.assessments:
                lines.append("  Nenhuma avaliação cadastrada.")
            else:
                for av in ac.assessments:
                    lines.append(f"  - {av.name} | Peso: {av.weight:.2f}")
        return "\n".join(lines)

    def _build_class_assessment_summary(self, classes: List[AcademicClass]) -> str:
        lines = ["===== Relatório Resumo de Avaliações por Turma ====="]
        if not classes:
            lines.append("Nenhuma turma cadastrada.")
            return "\n".join(lines)

        total_assessments = sum(len(ac.assessments) for ac in classes)
        lines.append(f"Total de turmas cadastradas: {len(classes)}")
        lines.append(f"Total de avaliações cadastradas: {total_assessments}")
        lines.append("")

        for ac in classes:
            total_weight = sum(av.weight for av in ac.assessments)
            lines.append(f"Turma: {ac.code} - {ac.name}")
            lines.append(f"Quantidade de avaliações: {len(ac.assessments)}")
            lines.append(f"Peso total: {total_weight:.2f}")
            if not ac.assessments:
                lines.append("Avaliações: nenhuma avaliação cadastrada.")
            else:
                lines.append("Avaliações:")
                for i, av in enumerate(ac.assessments, 1):
                    lines.append(f"  {i}. {av.name} | Peso: {av.weight:.2f}")
            lines.append("")

        return "\n".join(lines)

    def _build_assessment_weight_report(self, classes: List[AcademicClass]) -> str:
        lines = ["===== Relatório de Peso de Avaliações ====="]
        if not classes:
            lines.append("Nenhuma turma cadastrada.")
            return "\n".join(lines)

        for ac in classes:
            total_weight = sum(av.weight for av in ac.assessments)
            lines.append(f"Turma: {ac.code} - {ac.name}")
            lines.append(f"Peso total: {total_weight:.2f}")
            if not ac.assessments:
                lines.append("Total de peso exibido como 0.00 pois não há avaliações cadastradas.")
            elif abs(total_weight - 1.0) < 0.001:
                lines.append("Composição de avaliações VÁLIDA (peso total = 1.0).")
            else:
                lines.append("Composição de avaliações INVÁLIDA (peso total diferente de 1.0).")
            lines.append("")

        return "\n".join(lines)

    def _build_persistence_config_report(self, current_type: PersistenceType) -> str:
        return (
            "===== Relatório de Configuração de Persistência =====\n"
            f"Mecanismo de persistência atual: {current_type.name} ({current_type.description})"
        )

    def _log_report(self, report_name: str, user_role: str):
        role_str = user_role.strip() if user_role else "desconhecido"
        logger.info("Relatório gerado. Relatório: %s | Perfil do usuário: %s", report_name, role_str)
