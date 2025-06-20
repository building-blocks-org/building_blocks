from datetime import date

from taskflow_primitives.domain.parsers.due_date_parser import DueDateParser


class ISO8601DueDateParser(DueDateParser):
    """
    A parser for ISO 8601 formatted due dates.
    """

    def parse(self, value: str) -> date:
        """
        Parses an ISO 8601 formatted due date and returns it in a standard format.

        :param due_date: The due date in ISO 8601 format.
        :return: The parsed due date in 'YYYY-MM-DD' format.
        """
        try:
            # Attempt to parse the ISO 8601 date string
            return date.fromisoformat(value)
        except ValueError as err:
            raise ValueError("Invalid ISO 8601 date format") from err
