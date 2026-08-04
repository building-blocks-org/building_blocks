"""Outbound port defining the MessageBusPort abstraction.

A MessageBusPort provides a generic asynchronous dispatch mechanism for commands,
queries, or events. It is the central connector between application ports and
transport infrastructure (queues, brokers, in-memory routing, etc.).

Responsibilities:
    - Route messages of various types to their respective handlers or transports.
    - Provide an asynchronous dispatch API.

Non-Responsibilities:
    - Business logic.
    - Handler invocation policies unless explicitly implemented.
    - Delivery guarantees (up to infrastructure).
"""

from abc import abstractmethod

from forging_blocks.foundation.ports import OutboundPort


class MessageBusPort[MessageType, MessageBusResultType](
    OutboundPort,
):
    """Outbound port representing a generic asynchronous message bus.

    A MessageBusPort dispatches messages to infrastructure or internal handlers.
    Dispatch routing is decoupled from message structure — the bus may route
    synchronously or asynchronously without changing the contract.

    Example:
        ```python
        bus = MyMessageBus[PlaceOrderCommand, str]()
        result = await bus.dispatch(PlaceOrderCommand(order_id="42"))
        ```
    """

    @abstractmethod
    async def dispatch(self, message: MessageType) -> MessageBusResultType:
        """Dispatch a message to the configured handler or transport.

        Args:
            message: The message instance to dispatch.

        Returns:
            A typed result depending on the nature of the message.

        Notes:
            Infrastructure determines:
                - routing strategy,
                - reliability,
                - ordering,
                - concurrency model.

        """
        ...
