import os
from urllib.parse import urlencode

from aiogram import Bot, Dispatcher
from aiogram.utils.markdown import text, bold
from asgiref.sync import sync_to_async

from apps.orders.models.telegram_chennels import TelegramChannel

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher()


def get_google_maps_url(lat, lng):
    params = {
        "q": f"{lat},{lng}",
        "z": 15  # zoom level
    }
    return f"https://www.google.com/maps?{urlencode(params)}"


async def send_order_to_telegram_async(order, created=False, deleted=False):
    if not created:
        return

    channel = await sync_to_async(TelegramChannel.objects.filter(basic=True).first)()

    if not channel:
        raise Exception('TelegramChannel not found!')

    user = await sync_to_async(lambda: order.user)()
    products = await sync_to_async(lambda: list(order.products.all()))()

    total_quantity = sum(item.quantity for item in products)

    prices = [await sync_to_async(lambda: item.quantity * item.product.price)() for item in products]
    total_price = sum(prices)

    google_maps_url = get_google_maps_url(order.latitude, order.longitude)

    product_details = "\n".join(
        [f"📦 {await sync_to_async(lambda: item.product.name_uz)()} x{item.quantity}" for item in products]
    )

    message_content = text(
        bold("New Order:"),
        f"{bold('Order ID :')} #{order.id}",
        f"👤 {bold('User:')} {user.name} | {user.phone_number}",
        f"📍 {bold('Address:')} {order.address or 'N/A'}",
        f"💰 {bold('Order Type:')} {await sync_to_async(order.get_type_order_display)()}",
        f"📦 {bold('Order Status:')} {await sync_to_async(order.get_order_status_display)()}",
        f"🛍 {bold('Products Ordered:')}{product_details}",
        f"🔢 {bold('Total Quantity:')} {total_quantity}",
        f"💸 {bold('Total Price:')} AED{total_price:.2f}",
        f"🗺️ {bold('Location:')} [Google Maps]({google_maps_url})",
        f"🕒 {bold('Created At:')} {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
        sep="\n"
    )

    await bot.send_message(chat_id=channel.group_id, text=message_content, parse_mode='markdown')
