"""
main.py — Entry point do Sistema Acadêmico (Python / CustomTkinter)
"""
import sys
import os

# garante que o diretório do projeto está no path
sys.path.insert(0, os.path.dirname(__file__))

from logging_config import setup_logging
from repository import (
    AcademicClassRepository,
    TxtAcademicDataRepository,
    XmlAcademicDataRepository,
    JsonAcademicDataRepository,
)
from service import (
    ClassService,
    AssessmentService,
    PersistenceService,
    ReportService,
    AuthenticationService,
    AuthorizationService,
)
from controller import AcademicSystemController
from view import AcademicSystemApp


def build_controller() -> AcademicSystemController:
    repo = AcademicClassRepository()
    class_service = ClassService(repo)
    assessment_service = AssessmentService(repo)
    txt_repo = TxtAcademicDataRepository()
    xml_repo = XmlAcademicDataRepository()
    json_repo = JsonAcademicDataRepository()
    persistence_service = PersistenceService(txt_repo, xml_repo, json_repo)
    report_service = ReportService()
    auth_service = AuthenticationService()
    authz_service = AuthorizationService()

    return AcademicSystemController(
        class_service,
        assessment_service,
        persistence_service,
        report_service,
        auth_service,
        authz_service,
    )


def main():
    setup_logging()
    controller = build_controller()
    app = AcademicSystemApp(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
