from arg import Arg


class Command:
    def __init__(self, command: str, hidden: bool):
        self.command = command
        self.hidden = hidden
        self.args = {}

    def add_arg(self, name: Arg):
        """Add an argument to the command."""
        self.args[name.name] = name

    def get_arg(self, name: str):
        """Get an argument by name."""
        return self.args.get(name)
