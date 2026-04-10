import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from urllib.parse import quote
import html
from asgiref.sync import sync_to_async
from django.conf import settings

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
    bot_token = settings.TELEGRAM_BOT_TOKEN
    group_chat_id = settings.TELEGRAM_GROUP_CHAT_ID
    user_chat_id = settings.TELEGRAM_USER_CHAT_ID

    # Google Maps linkini tozalash
    encoded_google_maps_url = quote(google_maps_url, safe=":/?&=")
    address = order.address or "No entered Address"

    # Asinxron holda ma'lumotlarni olish
    order_type = await get_order_type_display(order)
    order_status = await get_order_status_display(order)
    comment = order.comment or "No comment"

    products_str = "\n".join(
        f"{index}. {item.product.name_en} x {item.quantity} = {item.quantity * item.product.price} AED"
        for index, item in enumerate(products, start=1)
    )

    # Xabar matni
    message = (
        f"👤 <b>User:</b> {html.escape(user.name)} | {html.escape(user.phone_number)}\n\n"
        f"🛒 <b>Products:</b>\n{html.escape(products_str)}\n\n"
        f"📦 <b>Total Quantity:</b> {html.escape(str(total_quantity))}\n"
        f"💰 <b>Total Price:</b> {html.escape(str(total_price))} AED\n"
        f"📍 <b>Location:</b> <a href='{encoded_google_maps_url}'>Google Maps</a>\n"
        f"💬 <b>Address:</b> {html.escape(address)}\n"
        f"🕒 <b>Created At:</b> {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🔲 <b>Order Type:</b> {order_type}\n"
        f"🔘 <b>Order Status:</b> {order_status}\n"
        f"💭 <b>Comment:</b> {html.escape(comment)}"
    )

    try:
        if not bot_token or not group_chat_id:
            return
        bot = Bot(token=bot_token)

        # 1. Guruhga yuborish
        await bot.send_message(
            chat_id=group_chat_id,
            text=message,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
        )

        # 2. Foydalanuvchiga (shaxsiy akkaunt) yuborish
        if user_chat_id:
            await bot.send_message(
                chat_id=user_chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            )

    except Exception as error:
        raise Exception(f"🔥 Epic fail while sending message: {error}")



