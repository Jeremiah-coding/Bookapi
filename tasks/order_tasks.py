import logging

logger = logging.getLogger("bookapi")


def send_order_confirmation(order_id: int, customer_name: str, book_title: str, quantity: int) -> None:
    """
    Background task: simulate sending an order confirmation notification.
    In production this would dispatch an email, push notification, or message queue event.
    The logger output proves the task executed after the response was returned.
    """
    logger.info(
        "ORDER CONFIRMATION | order_id=%d customer=%s book=%r quantity=%d",
        order_id,
        customer_name,
        book_title,
        quantity,
    )
