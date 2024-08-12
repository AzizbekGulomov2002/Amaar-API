import asyncio

from celery import shared_task

from apps.orders.models.orders import Order
from apps.orders.views.tg import send_order_to_telegram_async


@shared_task
def send_order_to_telegram_task(order_id, created=False, deleted=False):
    try:
        order = Order.objects.get(id=order_id)
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(send_order_to_telegram_async(order, created=created, deleted=deleted))

    except Order.DoesNotExist as e:
        raise Exception(f'Order not found! Error: {e}')
    except RuntimeError as e:
        raise Exception(f'Runtime error encountered: {e}')
