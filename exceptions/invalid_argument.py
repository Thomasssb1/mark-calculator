class InvalidArgumentException(Exception):
    """Custom exception for invalid arguments."""

    def __init__(self, message: str, arg: str):
        super().__init__(message)
        self.arg = arg
