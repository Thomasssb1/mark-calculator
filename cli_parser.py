import sys
from typing import get_origin, get_args, Any, List
from arg import Arg
from command import Command
from any_type import AnyType
from exceptions import InvalidArgumentException, RequiredArgumentException


class CLIParser:
    def __init__(self):
        self.args = sys.argv[1:]
        self.options = {None: Command(command="Default", description="", hidden=False)}
        self.command = None

    def add_command(
        self, name: str, hidden: bool = False, description: str | None = None
    ) -> None:
        self.options[name] = Command(name, description or "", hidden)

    def add_option(
        self,
        name: str,
        command: str | None = None,
        flag=False,
        default=None,
        hidden=False,
        required=False,
        value_type: type | Any = Any,
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

    def contains_required(self, command: str | None) -> bool:
        for option in self.options[command].args.values():
            if option.required and not self.was_parsed(option.name, command):
                raise RequiredArgumentException(
                    f"Missing required argument: {option.name}"
                )
        return True

    @staticmethod
    def convert_to_list(value: str, value_type: type) -> List:
        if get_origin(value_type) is list:
            value_type = get_args(value_type)[0]
            inner_type = get_args(value_type)
            if isinstance(value, str):
                items = value.split(",")
            elif isinstance(value, list):
                items = value
            else:
                return []

            if len(inner_type) == 0:
                inner_type = (value_type, value_type)

            container = []
            for item in items:
                if inner_type[0] is Any:
                    container.append(item)
                    continue
                try:
                    container.append(inner_type[0](item))
                except ValueError:
                    try:
                        container.append(inner_type[1](item))
                    except ValueError:
                        raise InvalidArgumentException(
                            f"Invalid value for {inner_type[0]} or {inner_type[1]}",
                            item,
                        )
            return container
        return []

    def _is_type(self, value: any, value_type: type) -> bool:
        if value_type is Any:
            return True

        try:
            if get_origin(value_type) is list:
                value_type = get_args(value_type)[0]
                if isinstance(value, str):
                    items = value.split(",")
                elif isinstance(value, list):
                    items = value
                else:
                    return False

                for item in items:
                    return self._is_type(item, value_type)

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
            if arg in self.options[command].args and self._is_type(
                value, self.options[command].args[arg].type
            ):
                self.options[command].args[arg].value = value

        self.contains_required(command)

    def get_option(self, name: str, command: str | None = None) -> Any:
        """Get the value of an option."""
        command: Command = self.options.get(command, None)
        if command is None:
            raise InvalidArgumentException("Command not found", command)

        arg = command.get_arg(name)
        return arg.value if arg is not None else None

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
            temp += f"{v.command} {f'- {v.description}' if v.description else ''}\n"
            for a in v.args.values():
                name = f"-{a.name}" if a.flag else f"--{a.name}"
                temp += f"{name}{f' : {a.type}' if not a.flag else ''}, default={a.value}{', required' if a.required else ''}\n"
            temp += "\n"
        return temp
