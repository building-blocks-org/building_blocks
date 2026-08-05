"""Module defining the base Query class for queries."""

from abc import abstractmethod

from forging_blocks.domain.messages.message import Message


class Query[QueryPayloadType](Message[QueryPayloadType]):
    """Base class for all queries.

    Queries represent a request to retrieve data from the system.
    They are handled by query handlers and should not modify state.

    Queries are named in interrogative mood (e.g., GetOrder, FindCustomer,
    ListProducts).

    Example:
        ```python
        class GetOrderPayload:
            def __init__(self, order_id: str) -> None:
                self.order_id = order_id


        class GetOrder(Query[GetOrderPayload]):
            def __init__(self, order_id: str):
                super().__init__()
                self._order_id = order_id

            @property
            def _payload(self) -> GetOrderPayload:
                return GetOrderPayload(order_id=self._order_id)

            @classmethod
            def from_payload_fields(
                cls, data: GetOrderPayload, metadata: MessageMetadata
            ) -> "GetOrder":
                return cls(order_id=data.order_id)

            @property
            def value(self) -> GetOrderPayload:
                return self._payload
        ```

    """

    @property
    @abstractmethod
    def _payload(self) -> QueryPayloadType:
        """Return the query-specific payload data.

        Subclasses MUST implement this property to return the query-specific
        data.
        """
