"""Outbound port defining an asynchronous notification service.

A NotifierPort provides an abstraction for sending notification messages using
external delivery channels such as email, SMS, chat systems, or push
notifications.

Responsibilities:
    - Send notification messages asynchronously.

Non-Responsibilities:
    - Guarantee delivery.
    - Implement retries or throttling unless defined by infrastructure.
"""

from abc import abstractmethod

from forging_blocks.foundation.ports import OutboundPort


class NotifierPort[NotificationType](
    OutboundPort,
):
    """Outbound port for sending asynchronous notifications.

    Defines an asynchronous notification boundary decoupled from delivery
    mechanisms.
    Example:
        ```python
        from dataclasses import dataclass

        notifier = MyNotifier[Notification]()
        await notifier.notify(Notification(recipient="alice@example.com", body="Order shipped"))
        ```
    """

    @abstractmethod
    async def notify(self, message: NotificationType) -> None:
        """Send a notification.

        Args:
            message: The message to deliver.

        Notes:
            - Fire-and-forget behavior unless documented otherwise.
            - Delivery semantics are infrastructure-defined.

        """
