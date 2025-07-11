from typing import Set
from module import Module


class ModuleCalculator:
    def __init__(self, modules: Set[Module], target: int):
        self.modules = modules
        self.total_credits = sum(module.credits for module in modules)
        self.target_grade = float(target)

    def _calculate_required_grade(self) -> float:
        calculated_grade = 0.0
        remaining_credits = self.total_credits
        for module in self.modules:
            if module.is_complete():
                remaining_credits -= module.credits
                calculated_grade += module.calculate_overall_grade() * (
                    module.credits / self.total_credits
                )

        return (self.target_grade - calculated_grade) / (
            remaining_credits / self.total_credits
        )

    def calculate(self) -> float:
        grade = self._calculate_required_grade()
        for module in self.modules:
            if not module.is_complete():
                print(
                    f"Module {module.name} requires an average grade of {module.calculate_required_percentage(grade):.2f}%"
                )

    def calculate_overall_grade(self) -> float:
        total_weighted_grade = 0.0
        for module in self.modules:
            total_weighted_grade += module.calculate_overall_grade() * module.credits

        return total_weighted_grade / self.total_credits

    def __str__(self):
        return (
            f"Modules: {', '.join([str(m) for m in self.modules])}\n"
            f"Total Credits: {self.total_credits}, Target Grade: {self.target_grade}\n"
            f"Required Grade: {self.calculate()}"
        )
