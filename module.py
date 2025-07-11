from typing import Set, List, Tuple, Any
from itertools import zip_longest
from test import Test
from cli_parser import CLIParser
from exceptions.invalid_file_format import InvalidFileFormatException
import csv


class Module:
    def __init__(
        self,
        name: str,
        credits: int,
        grades: List[float] | None = None,
        weights: List[float] | None = None,
    ):
        self.name = name
        self.credits = credits
        self.tests = [
            Test(f"{name}-test-{i}", grade, weight)
            for i, (weight, grade) in enumerate(
                zip_longest(
                    weights or [],
                    grades or [],
                )
            )
        ]

    @staticmethod
    def from_csv(filename: str) -> Set["Module"]:
        with open(filename, "r") as file:
            reader = csv.reader(file)
            next(reader)
            modules = set()
            for line in reader:
                try:
                    name, credits, grades, weights = line
                    grades = [
                        None if grade == "Not graded" else grade
                        for grade in CLIParser.convert_to_list(
                            grades, List[float | str]
                        )
                    ]

                    modules.add(
                        Module(
                            name,
                            int(credits),
                            grades,
                            CLIParser.convert_to_list(weights, List[float]),
                        )
                    )
                except ValueError:
                    raise InvalidFileFormatException(
                        "Invalid CSV format, expected 4 values."
                    )
            return modules

    @staticmethod
    def _list_to_csv(items: List[Any] | None, fallback_msg: str = "Not graded") -> str:
        return f'"{",".join(map(lambda m: str(m) if m is not None else fallback_msg, items)) if len(items) > 0 else fallback_msg}"'

    @staticmethod
    def save_to_csv(modules: Set["Module"], filename: str) -> None:
        with open(filename, "w") as file:
            file.write("name,credits,grade\n")
            for module in modules:
                module_grades = Module._list_to_csv(
                    list(map(lambda m: m.grade, module.tests))
                )
                module_weights = Module._list_to_csv(
                    list(map(lambda m: m.weight, module.tests)),
                    fallback_msg="Not weighted",
                )

                file.write(
                    f'"{module.name}",{module.credits},{module_grades},{module_weights}\n'
                )
        print(f"Saved modules to {filename}")

    def calculate_overall_grade(self) -> float:
        if len(self.tests) == 0:
            return 0.0

        return sum(test.calculate_weighted_mark() for test in self.tests)

    def is_complete(self) -> bool:
        for test in self.tests:
            if test.is_incomplete():
                return False
        return True

    def calculate_required_percentage(self, grade: float) -> float:
        contribution = sum(
            test.calculate_weighted_mark()
            for test in self.tests
            if not test.is_incomplete()
        )
        remaining_weight = 1 - sum(
            test.weight for test in self.tests if not test.is_incomplete()
        )

        return (grade - contribution) / remaining_weight

    def __str__(self):
        return f"{self.name} ({self.credits} credits) - {f'{self.calculate_overall_grade():.2f}%' if len(self.tests) > 0 else 'Not graded'}"

    def __eq__(self, other):
        if not isinstance(other, Module):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))
