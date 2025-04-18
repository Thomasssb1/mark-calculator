class InvalidFileFormatException(Exception):
    """Exception raised for invalid file format errors."""

    def __init__(self, message="Invalid file format."):
        self.message = message
        super().__init__(self.message)
