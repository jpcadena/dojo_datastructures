"""
A module for student in the processing package.
"""
import csv
import logging
import os
from typing import Any

from core.decorators import benchmark, with_logging
from core.exceptions import NOT_NUMBER, VALID_AGE, ValidationError
from processing.utils import ENCODING

logger: logging.Logger = logging.getLogger(__name__)


class Student:
    """A class to represent the Student data."""

    def __init__(self, csv_file: str = "data.csv"):
        """
        Constructs all the necessary attributes for the Student object.
        :param csv_file: The name to the csv file. The default is
         data.csv
        :type csv_file: str
        """
        self.csv_file: str = csv_file

    @with_logging
    @benchmark
    def load_data(self) -> list[dict[str, Any]]:
        """
        Load student data from a CSV file and validate.
        :return: a list of dictionaries representing the student data
        :rtype: list[dict[str, Any]]
        """
        students: list[dict[str, Any]] = []
        file_path: str = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data", "raw", self.csv_file)
        try:
            with open(file_path, "r", encoding=ENCODING) as file:
                reader = csv.DictReader(file)
                student: dict[str, Any]
                errors: list[str] = []
                for student in reader:
                    try:
                        age: int = int(student["edad"])
                        if age > 0:
                            student["edad"] = age
                            students.append(student)
                        else:
                            error_message: str = f"{VALID_AGE}: {age}"
                            logger.error(error_message)
                            errors.append(error_message)
                    except ValueError as exc:
                        logger.error(NOT_NUMBER, exc)
                        errors.append(NOT_NUMBER)
            if errors:
                raise ValidationError(" | ".join(errors))
        except FileNotFoundError:
            logger.error("Data file not found at %s. Please check the"
                         " location of your data file.", file_path)
        return students
