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
    # from urllib.parse import quote
    # from aiogram import Bot
    # from aiogram.types import ParseMode
    # import html

    BOT_TOKEN = "7645519439:AAEeYlt_R5TYGswdLOF1wLQ56g8ha_ywmTA"
    CHAT_ID = "-1002263729881"
    
    # BOT_TOKEN = "6366441312:AAGxI9_1Cz3r_PnvhXdbGI7IXv1Ozh58f9g"
    # CHAT_ID = "-1002289902731"
    

    # URL encoding for Google Maps URL to ensure safe passage
    encoded_google_maps_url = quote(google_maps_url, safe=":/?&=")
    address = order.address or "No entered Address"


    # Fetch required data asynchronously
    order_type = await get_order_type_display(order)
    order_status = await get_order_status_display(order)
    # products_str = await get_products_str(products)
    

    products_str = "\n".join(
        f"{index}. {item.product.name_en} x {item.quantity} = {item.quantity * item.product.price} AED"
        for index, item in enumerate(products, start=1)
    )

    # Construct the notification message with HTML escaping
    message = (
        f"👤 <b>User:</b> {html.escape(user.name)} | {html.escape(user.phone_number)}\n \n \n "
        f"🛒 <b>Products:</b>\n{html.escape(products_str)}\n \n \n"
        f"📦 <b>Total Quantity:</b> {html.escape(str(total_quantity))}\n"
        f"💰 <b>Total Price:</b> {html.escape(str(total_price))} AED\n"
        f"📍 <b>Location:</b> <a href='{encoded_google_maps_url}'>Google Maps</a>\n"
        f"💬 <b>Address:</b> {html.escape(address)}\n"
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
