from __future__ import annotations
import json
import os
from enum import Enum
from pathlib import Path
from typing import List, Optional
from xml.dom import minidom
import xml.etree.ElementTree as ET

from model import AcademicClass, Assessment
from exceptions import DuplicateAcademicClassException, InvalidKeyboardInputException


# ---------------------------------------------------------------------------
# PersistenceType
# ---------------------------------------------------------------------------

class PersistenceType(Enum):
    TXT = (1, "TXT")
    XML = (2, "XML")
    JSON = (3, "JSON")

    def __init__(self, code: int, description: str):
        self._code = code
        self._description = description

    @property
    def code(self) -> int:
        return self._code

    @property
    def description(self) -> str:
        return self._description

    @classmethod
    def from_code(cls, code: int) -> "PersistenceType":
        for pt in cls:
            if pt.code == code:
                return pt
        raise InvalidKeyboardInputException(f"Tipo de persistência inválido: {code}.")

    @classmethod
    def menu_options_text(cls) -> str:
        return "\n".join(f"{pt.code} - {pt.description}" for pt in cls)


# ---------------------------------------------------------------------------
# In-memory repository
# ---------------------------------------------------------------------------

class AcademicClassRepository:
    def __init__(self):
        self._classes: List[AcademicClass] = []

    def save(self, academic_class: AcademicClass):
        if self.exists_by_code(academic_class.code):
            raise DuplicateAcademicClassException(academic_class.code)
        self._classes.append(academic_class)

    def find_by_code(self, code: str) -> Optional[AcademicClass]:
        if not code:
            return None
        code_lower = code.strip().lower()
        return next((c for c in self._classes if c.code.lower() == code_lower), None)

    def find_all(self) -> List[AcademicClass]:
        return list(self._classes)

    def exists_by_code(self, code: str) -> bool:
        return self.find_by_code(code) is not None


# ---------------------------------------------------------------------------
# TXT repository
# ---------------------------------------------------------------------------

class TxtAcademicDataRepository:
    DEFAULT_FILE_PATH = "data/academic-data.txt"

    def save(self, classes: List[AcademicClass], file_path: str = DEFAULT_FILE_PATH) -> Path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("===== Dados Acadêmicos =====\n")
            if not classes:
                f.write("Nenhuma turma cadastrada.\n")
            else:
                for ac in classes:
                    f.write(f"Turma: {ac.code} - {ac.name}\n")
                    if not ac.assessments:
                        f.write("  Nenhuma avaliação cadastrada.\n")
                    else:
                        for av in ac.assessments:
                            f.write(f"  Avaliação: {av.name} | Peso: {av.weight}\n")
                    f.write("\n")
        return path


# ---------------------------------------------------------------------------
# XML repository
# ---------------------------------------------------------------------------

class XmlAcademicDataRepository:
    DEFAULT_FILE_PATH = "data/academic-data.xml"

    def save(self, classes: List[AcademicClass], file_path: str = DEFAULT_FILE_PATH) -> Path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        root = ET.Element("academicData")
        classes_el = ET.SubElement(root, "classes")

        for ac in classes:
            class_el = ET.SubElement(classes_el, "class", code=ac.code)
            name_el = ET.SubElement(class_el, "name")
            name_el.text = ac.name
            assessments_el = ET.SubElement(class_el, "assessments")
            for av in ac.assessments:
                assessment_el = ET.SubElement(assessments_el, "assessment")
                av_name_el = ET.SubElement(assessment_el, "name")
                av_name_el.text = av.name
                weight_el = ET.SubElement(assessment_el, "weight")
                weight_el.text = str(av.weight)

        xml_str = ET.tostring(root, encoding="unicode")
        pretty = minidom.parseString(xml_str).toprettyxml(indent="    ")
        with open(path, "w", encoding="utf-8") as f:
            f.write(pretty)
        return path


# ---------------------------------------------------------------------------
# JSON repository
# ---------------------------------------------------------------------------

class JsonAcademicDataRepository:
    DEFAULT_FILE_PATH = "data/academic-data.json"

    def save(self, classes: List[AcademicClass], file_path: str = DEFAULT_FILE_PATH) -> Path:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "classes": [
                {
                    "code": ac.code,
                    "name": ac.name,
                    "assessments": [
                        {"name": av.name, "weight": av.weight}
                        for av in ac.assessments
                    ],
                }
                for ac in classes
            ]
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
