# poe_ninja_client/exceptions.py


class PoeNinjaError(Exception):
    """Base exception class for this module."""

    pass


class PoeNinjaRequestError(PoeNinjaError):
    """
    Exception raised for errors in the request process (e.g., network issues, HTTP errors).
    """

    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


class PoeNinjaAPIError(PoeNinjaError):
    """
    Exception raised for errors originating from the API response itself
    (e.g., malformed JSON, API-specific error messages if they were structured).
    """

    pass


# You can add more specific exceptions as needed, for example:
# class RateLimitError(PoeNinjaRequestError):
#     pass

# class InvalidLeagueError(PoeNinjaAPIError):
#     pass
