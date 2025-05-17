class Test:
    def __init__(self, name: str, grade: float | None, weight: float):
        self.name = name
        self.grade = grade
        self.weight = weight

    def is_incomplete(self) -> bool:
        return self.grade is None

    def calculate_weighted_mark(self) -> float:
        if self.grade is None:
            return 0.0

        return self.grade * self.weight

    def __str__(self):
        return f"{self.name}: {F'{(self.grade * self.weight):.2f}%' if self.grade is not None else 'Not graded'}"
