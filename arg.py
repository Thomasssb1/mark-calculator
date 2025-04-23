from typing import Any


class Arg:
    def __init__(
        self,
        name: str,
        value: any,
        flag: bool,
        hidden: bool,
        required: bool,
        type: type | Any,
    ):
        self.name = name
        self.value = value
        self.default = value
        self.flag = flag
        self.hidden = hidden
        self.required = required
        self.type = type

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)
