class Arg:
    def __init__(self, name: str, value: any, flag: bool, hidden: bool):
        self.name = name
        self.value = value
        self.default = value
        self.flag = flag
        self.hidden = hidden
        self.type = type(value)
