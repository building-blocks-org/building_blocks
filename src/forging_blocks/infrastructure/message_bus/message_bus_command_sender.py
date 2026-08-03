"""Message-bus-backed CommandSenderPort adapter.

Delegates command dispatch to an injected ``MessageBusPort``.
"""

from forging_blocks.application.ports.outbound.command_sender_port import CommandSenderPort
from forging_blocks.application.ports.outbound.message_bus_port import MessageBusPort
from forging_blocks.domain.messages.command import Command


class MessageBusCommandSender[CommandPayloadType](CommandSenderPort[CommandPayloadType]):
    """Infrastructure adapter that sends commands via a ``MessageBusPort``.

    Implements ``CommandSenderPort`` by delegating ``send`` to
    ``MessageBusPort.dispatch``.

    Example:
        ```python
        from forging_blocks.infrastructure.message_bus.in_memory_message_bus import (
            InMemoryMessageBus,
        )
        from forging_blocks.infrastructure.message_bus.message_bus_command_sender import (
            MessageBusCommandSender,
        )
        from forging_blocks.domain.messages.command import Command


        class MyCommand(Command[dict[str, object]]):
            def __init__(self) -> None:
                super().__init__()

            @property
            def _payload(self) -> dict[str, object]:
                return {}


        bus = InMemoryMessageBus[MyCommand, None]()
        sender = MessageBusCommandSender[dict[str, object]](bus)
        await sender.send(MyCommand())
        ```
    """

    def __init__(self, message_bus: MessageBusPort[Command[CommandPayloadType], None]) -> None:
        self._message_bus = message_bus

    async def send(self, command: Command[CommandPayloadType]) -> None:
        """Send a command asynchronously via the message bus."""
        await self._message_bus.dispatch(command)
