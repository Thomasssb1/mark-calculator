import sys
from arg import Arg
from invalid_arg import InvalidArgumentException


class CLIParser:
    def __init__(self):
        self.args = sys.argv[1:]
        self.options = {}

    def add_option(self, name: str, flag=False, default=None, hidden=False) -> None:
        """Add an option to the parser."""
        if name.startswith("-"):
            raise InvalidArgumentException(
                "Option name should not start with '-'", name
            )
        if flag and default is not None and type(default) is not bool:
            raise InvalidArgumentException(
                "Flag options should not have a default value", name
            )
        self.options[name] = Arg(name=name, value=default, flag=flag, hidden=hidden)

    def parse(self) -> None:
        for arg in self.args:
            isFlag = arg.startswith("--")
            value = True if isFlag else arg.split("=")[1]
            arg = arg.replace("-", "").split("=")[0]
            if arg in self.options and type(value) is self.options[arg].type:
                self.options[arg].value = value

    def get_option(self, name: str) -> any:
        """Get the value of an option."""
        arg = self.options.get(name, None)
        return arg.value if not arg is None else None

    def was_parsed(self, name: str) -> bool:
        """Check if an option was parsed."""
        return (
            name in self.options
            and self.options[name].value != self.options[name].default
        )

    def __str__(self) -> str:
        """Return a string representation of the parser."""
        temp = ""
        for v in self.options.values():
            if v.hidden:
                continue
            name = f"-{v.name}" if v.flag else f"--{v.name}"
            temp += f"{name} : {v.type}, default={v.value}\n"
        return temp
