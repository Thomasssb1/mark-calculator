class RequiredArgumentException(Exception):
    """
    Exception raised when a required argument is not provided.
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
