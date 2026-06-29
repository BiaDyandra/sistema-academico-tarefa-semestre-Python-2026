from __future__ import annotations
from pathlib import Path

from security import Role, User
from repository import PersistenceType
from service import (
    ClassService,
    AssessmentService,
    PersistenceService,
    ReportService,
    AuthenticationService,
    AuthorizationService,
)


class AcademicSystemController:
    def __init__(
        self,
        class_service: ClassService,
        assessment_service: AssessmentService,
        persistence_service: PersistenceService,
        report_service: ReportService,
        authentication_service: AuthenticationService,
        authorization_service: AuthorizationService,
    ):
        self._class_service = class_service
        self._assessment_service = assessment_service
        self._persistence_service = persistence_service
        self._report_service = report_service
        self._auth_service = authentication_service
        self._authz_service = authorization_service

    # ---- Auth ----------------------------------------------------------------

    def login(self, username: str, password: str) -> str:
        user = self._auth_service.authenticate(username, password)
        return f"Login realizado com sucesso. Usuário: {user.username} | Perfil: {user.role.value}"

    def logout(self):
        self._auth_service.logout()

    def get_authenticated_user(self) -> User:
        return self._auth_service.get_authenticated_user()

    def is_authenticated(self) -> bool:
        return self._auth_service.is_authenticated()

    def get_logged_user_description(self) -> str:
        user = self._auth_service.get_authenticated_user()
        return f"{user.username} ({user.role.value})"

    # ---- Persistence type ----------------------------------------------------

    def get_current_persistence_type(self) -> PersistenceType:
        return self._persistence_service.current_persistence_type

    def configure_persistence_type(self, persistence_type: PersistenceType) -> str:
        self._authorize(Role.ADMIN)
        self._persistence_service.configure_persistence_type(persistence_type)
        return f"Tipo de persistência configurado para: {persistence_type.description}."

    # ---- Classes -------------------------------------------------------------

    def register_class(self, code: str, name: str) -> str:
        self._authorize(Role.ADMIN)
        self._class_service.register_class(code, name)
        return "Turma cadastrada com sucesso."

    def list_classes_and_assessments(self) -> str:
        self._authorize(Role.ADMIN, Role.PROFESSOR)
        return self._report_service.generate_classes_and_assessments_listing(
            self._class_service.list_classes()
        )

    # ---- Assessments ---------------------------------------------------------

    def register_assessment(self, class_code: str, assessment_name: str, weight: float) -> str:
        self._authorize(Role.ADMIN, Role.PROFESSOR)
        self._assessment_service.register_assessment(class_code, assessment_name, weight)
        return "Avaliação cadastrada com sucesso."

    # ---- Save ----------------------------------------------------------------

    def save_academic_data(self) -> str:
        self._authorize(Role.ADMIN)
        saved_file: Path = self._persistence_service.save(self._class_service.list_classes())
        return f"Dados acadêmicos salvos em {self.get_current_persistence_type().description}: {saved_file}"

    # ---- Reports -------------------------------------------------------------

    def generate_class_assessment_summary_report(self) -> str:
        self._authorize(Role.ADMIN, Role.PROFESSOR)
        user_role = self._auth_service.get_authenticated_user().role.value
        return self._report_service.generate_class_assessment_summary_report(
            self._class_service.list_classes(), user_role
        )

    def generate_assessment_weight_report(self) -> str:
        self._authorize(Role.ADMIN, Role.PROFESSOR)
        user_role = self._auth_service.get_authenticated_user().role.value
        return self._report_service.generate_assessment_weight_report(
            self._class_service.list_classes(), user_role
        )

    def generate_persistence_configuration_report(self) -> str:
        self._authorize(Role.ADMIN)
        user_role = self._auth_service.get_authenticated_user().role.value
        return self._report_service.generate_persistence_configuration_report(
            self._persistence_service.current_persistence_type, user_role
        )

    def get_system_status(self) -> str:
        self._authorize(Role.ADMIN, Role.PROFESSOR)
        return (
            f"Sistema Acadêmico em execução. "
            f"Tipo de persistência atual: {self.get_current_persistence_type().description}."
        )

    # ---- Internal ------------------------------------------------------------

    def _authorize(self, *roles: Role):
        user = self._auth_service.get_authenticated_user()
        self._authz_service.require_any_role(user, *roles)
