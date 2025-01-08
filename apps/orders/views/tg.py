import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from urllib.parse import quote
import html
from asgiref.sync import sync_to_async

@sync_to_async
def get_order_type_display(order):
    return order.get_type_order_display()

@sync_to_async
def get_order_status_display(order):
    return order.get_order_status_display()

@sync_to_async
def get_products_str(products):
    return "\n".join([f"{item.product.name_en} x{item.quantity}" for item in products])

async def send_order_notification(order, user, products, total_price, total_quantity, google_maps_url):
    """
    Sends an order notification message to a Telegram group.

    Args:
        order (object): Order object with complete order details.
        user (object): User object containing `name` and `phone_number`.
        products (QuerySet): QuerySet of product objects.
        total_price (float): Total price of the order.
        total_quantity (int): Total quantity of items in the order.
        google_maps_url (str): Google Maps URL of the user's location.

    Raises:
        Exception: If anything blows up while sending the message.
    """
    # Telegram Bot Credentials (replace with your real deal)
    BOT_TOKEN = "7645519439:AAEeYlt_R5TYGswdLOF1wLQ56g8ha_ywmTA"
    CHAT_ID = "-1002263729881"

    # URL encoding for Google Maps URL to ensure safe passage
    encoded_google_maps_url = quote(google_maps_url, safe=":/?&=")

    # Fetch required data asynchronously
    order_type = await get_order_type_display(order)
    order_status = await get_order_status_display(order)
    products_str = await get_products_str(products)

    # Construct the notification message with HTML escaping
    message = (
        f"👤 <b>User:</b> {html.escape(user.name)} | {html.escape(user.phone_number)}\n"
        f"🛒 <b>Products:</b>\n{html.escape(products_str)}\n"
        f"📦 <b>Total Quantity:</b> {html.escape(str(total_quantity))}\n"
        f"💰 <b>Total Price:</b> {html.escape(str(total_price))} AED\n"  # Append 'AED' after the total price
        f"📍 <b>Location:</b> <a href='{encoded_google_maps_url}'>Google Maps</a>\n"
        f"🕒 <b>Created At:</b> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🔲 <b>Order Type:</b> {order_type}\n"
        f"🔘 <b>Order Status:</b> {order_status}"
    )


    try:
        # Instantiate the Telegram Bot
        bot = Bot(token=BOT_TOKEN)

        # Send the message
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
        )

    except Exception as error:
        raise Exception(f"🔥 Epic fail while sending message: {error}")
