from abc import ABC, abstractmethod
from datetime import date


class DueDateParser(ABC):
    """
    Abstract base class for parsing due dates.

    This class defines the interface for parsing due date strings into a standardized
    format.
    Subclasses should implement the `parse` method to provide specific parsing logic.
    """

    @abstractmethod
    def parse(self, value: str) -> date:
        """
        Parse the due date string into a standardized format.

        :return: A formatted date string or a datetime object.
        """
        pass
