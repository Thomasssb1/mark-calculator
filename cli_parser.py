import sys
from invalid_arg import InvalidArgumentException


class CLIParser:
    def __init__(self):
        self.args = sys.argv[1:]
        self.options = {}

    def add_option(self, name: str, flag=False, default=None):
        """Add an option to the parser."""
        if name.startswith("-"):
            raise InvalidArgumentException(
                "Option name should not start with '-'", name
            )
        if flag and default is not None and type(default) is not bool:
            raise InvalidArgumentException(
                "Flag options should not have a default value", name
            )
        self.options[name] = default

    def parse(self):
        for arg in self.args:
            isFlag = arg.startswith("--")
            value = True if isFlag else arg.split("=")[1]
            if arg.replace("-", "") in self.options:
                self.options[arg] = value

    def get_option(self, name: str):
        """Get the value of an option."""
        return self.options.get(name, None)
