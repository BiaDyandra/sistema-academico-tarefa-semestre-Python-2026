from __future__ import annotations
from typing import List
from exceptions import (
    InvalidAcademicClassException,
    InvalidAssessmentException,
)


class Assessment:
    def __init__(self, name: str, weight: float):
        name = name.strip() if name else name
        self._name = name
        self._weight = weight
        self._validate()

    def _validate(self):
        errors = []
        if not self._name:
            errors.append("O nome da avaliação não pode ser vazio.")
        if self._weight <= 0:
            errors.append("O peso da avaliação deve ser maior que zero.")
        if errors:
            raise InvalidAssessmentException(" | ".join(errors))

    @property
    def name(self) -> str:
        return self._name

    @property
    def weight(self) -> float:
        return self._weight

    def __repr__(self):
        return f"Assessment(name={self._name}, weight={self._weight})"


class AcademicClass:
    def __init__(self, code: str, name: str):
        code = code.strip() if code else code
        name = name.strip() if name else name
        self._code = code
        self._name = name
        self._assessments: List[Assessment] = []
        self._validate()

    def _validate(self):
        errors = []
        if not self._code:
            errors.append("O código da turma não pode ser vazio.")
        if not self._name:
            errors.append("O nome da turma não pode ser vazio.")
        if errors:
            raise InvalidAcademicClassException(" | ".join(errors))

    @property
    def code(self) -> str:
        return self._code

    @property
    def name(self) -> str:
        return self._name

    @property
    def assessments(self) -> List[Assessment]:
        return list(self._assessments)

    def add_assessment(self, assessment: Assessment):
        if assessment is None:
            raise InvalidAssessmentException("A avaliação não pode ser nula.")
        self._assessments.append(assessment)

    def __eq__(self, other):
        if not isinstance(other, AcademicClass):
            return False
        return self._code.lower() == other._code.lower()

    def __hash__(self):
        return hash(self._code.lower())

    def __repr__(self):
        return f"AcademicClass(code={self._code}, name={self._name})"
