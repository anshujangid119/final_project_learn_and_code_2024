class DatabaseError(Exception):
    def __init__(self, message="A database error occurred"):
        self.message = message
        super().__init__(self.message)

class InvalidCommandError(Exception):
    def __init__(self, message="Invalid command received"):
        self.message = message
        super().__init__(self.message)