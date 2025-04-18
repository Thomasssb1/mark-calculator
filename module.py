from typing import Set
from exceptions.invalid_file_format import InvalidFileFormatException


class Module:
    def __init__(self, name: str, credits: int, grade: int | None = None):
        self.name = name
        self.credits = credits
        self.grade = grade

    @staticmethod
    def from_csv(filename: str) -> Set["Module"]:
        with open(filename, "r") as file:
            lines = file.readlines()
            modules = set()
            for line in lines[1:]:
                try:
                    name, credits, grade = line.strip().split(",")
                    modules.add(
                        Module(name, int(credits), int(grade) if grade else None)
                    )
                except ValueError:
                    raise InvalidFileFormatException(
                        "Invalid CSV format, expected 3 values."
                    )
            return modules

    @staticmethod
    def save_to_csv(modules: Set["Module"], filename: str):
        with open(filename, "w") as file:
            file.write("name,credits,grade\n")
            for module in modules:
                file.write(
                    f"{module.name},{module.credits},{module.grade if module.grade is not None else ''}\n"
                )
        print(f"Saved modules to {filename}")

    def __str__(self):
        return f"{self.name} ({self.credits} credits) - {self.grade if self.grade is not None else 'Not graded'}"

    def __eq__(self, other):
        if not isinstance(other, Module):
            return False
        return (
            self.name == other.name
            and self.credits == other.credits
            and self.grade == other.grade
        )

    def __hash__(self):
        return hash((self.name, self.credits, self.grade))
