import sys
from arg import Arg
from command import Command
from any_type import AnyType
from exceptions import InvalidArgumentException, RequiredArgumentException


class CLIParser:
    def __init__(self):
        self.args = sys.argv[1:]
        self.options = {None: Command(command="Default", hidden=False)}
        self.command = None

    def add_command(self, name: str, hidden=False) -> None:
        self.options[name] = Command(name, hidden)

    def add_option(
        self,
        name: str,
        command: str | None = None,
        flag=False,
        default=None,
        hidden=False,
        required=False,
        value_type: type | AnyType = AnyType(),
    ) -> None:
        """Add an option to the parser."""
        if name.startswith("-"):
            raise InvalidArgumentException(
                "Option name should not start with '-'", name
            )
        if flag and default is not None and type(default) is not bool:
            raise InvalidArgumentException(
                "Flag options should not have a default value", name
            )
        if command not in self.options:
            raise InvalidArgumentException(
                "Command not found, please add the command first", command
            )
        if name in self.options[command].args:
            raise InvalidArgumentException("Option name already exists", name)

        self.options[command].add_arg(
            Arg(
                name=name,
                value=default,
                flag=flag,
                hidden=hidden,
                required=required,
                type=value_type,
            )
        )

    def contains_command(self, name: str) -> bool:
        """Check if a command exists."""
        return name in self.options

    def contains_required(self, command: Command) -> bool:
        for option in command.args.values():
            if option.required and not self.was_parsed(option.name):
                raise RequiredArgumentException(
                    f"Missing required argument: {option.name}"
                )
        return True

    def _is_type(self, value: any, value_type: type | AnyType) -> bool:
        try:
            value_type(value)
            return True
        except ValueError:
            return False

    def parse(self) -> None:
        command = self.set_command()
        for arg in self.args:
            isFlag = not arg.startswith("--")
            value = True if isFlag else arg.split("=")[1]
            arg = arg.replace("-", "").split("=")[0]
            print(arg, value)
            print(self.options[command].args[arg].type)
            print(self._is_type(value, self.options[command].args[arg].type))
            if arg in self.options[command].args and self._is_type(
                value, self.options[command].args[arg].type
            ):
                print(f"Setting {arg} to {value}")
                self.options[command].args[arg].value = value

        self.contains_required(self.options[command])

    def get_option(self, name: str) -> any:
        """Get the value of an option."""
        arg = self.options.get(name, None)
        return arg.value if not arg is None else None

    def set_command(self) -> str | None:
        """Get the command name."""
        if len(self.args) == 0:
            raise InvalidArgumentException("No arguments provided", None)

        if self.args[0].startswith("-"):
            return None
        self.command = self.args[0] if self.contains_command(self.args[0]) else None
        if self.command is not None:
            self.args.pop(0)
        return self.command

    def was_parsed(self, name: str, command: str | None = None) -> bool:
        """Check if an option was parsed."""
        return (
            name in self.options[command].args
            and self.options[command].args[name].value
            != self.options[command].args[name].default
        )

    def __str__(self) -> str:
        """Return a string representation of the parser."""
        temp = ""
        for v in self.options.values():
            if v.hidden:
                continue
            temp += f"Command: {v.command}\n"
            for a in v.args.values():
                name = f"-{a.name}" if a.flag else f"--{a.name}"
                temp += f"{name}{f' : {a.type}' if not a.flag else ''}, default={a.value}{', required' if a.required else ''}\n"
        return temp
