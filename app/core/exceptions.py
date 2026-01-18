class DatabaseConnectionError(RuntimeError):
    """Raised when the application cannot connect to MySQL."""
    pass


class MongoConnectionError(RuntimeError):
    """Raised when the application cannot connect to MongoDB."""
    pass


class MongoLoggingError(RuntimeError):
    """Raised when MongoDB logging fails."""
    pass
