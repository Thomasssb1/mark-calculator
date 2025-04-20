from typing import Set
from module import Module


class ModuleCalculator:
    def __init__(self, modules: Set[Module], target: int):
        self.modules = modules
        self.achieved_credits = sum(
            module.credits for module in modules if module.grade is not None
        )
        self.total_credits = sum(module.credits for module in modules)
        self.target_grade = int(target)

    def calculate(self) -> float:
        current_weighted_grades = sum(
            module.credits * (module.grade if module.grade else 0)
            for module in self.modules
        )

        return ((self.target_grade * self.total_credits) - current_weighted_grades) / (
            self.total_credits - self.achieved_credits
        )

    def __str__(self):
        return (
            f"Modules: {', '.join([str(m) for m in self.modules])}\n"
            f"Total Credits: {self.total_credits}, Target Grade: {self.target_grade}\n"
            f"Required Grade: {self.calculate()}"
        )
