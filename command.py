from arg import Arg


class Command:
    def __init__(self, command: str, hidden: bool):
        self.command = command
        self.hidden = hidden
        self.args = {}

    def add_arg(self, arg: Arg):
        """Add an argument to the command."""
        self.args[arg.name] = arg
