class DatabaseError(Exception):
    """Exception raised for errors in the database operations."""
    def __init__(self, message="A database error occurred"):
        self.message = message
        super().__init__(self.message)

class InvalidCommandError(Exception):
    """Exception raised for invalid commands."""
    def __init__(self, message="Invalid command received"):
        self.message = message
        super().__init__(self.message)