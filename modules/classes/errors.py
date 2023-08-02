class UnmatchedPersons(Exception):
    """Exception for if there are any unmatched individuals at the end of the
    process.
    """

    pass


class ServerError(Exception):
    """Exception if cannot communicate with blob storage."""

    pass