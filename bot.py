import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.telegram import TelegramAPIServer

BOT_TOKEN = "8789187792:AAFHGMWx0CRq3JyX7HSPABkeCXfutz6ncvY"
API_SECRET = "davydov_bot_secret_2026_x7k9m2p4"
SITE_API_URL = "https://bbah0otuhsilg45jagud.containers.yandexcloud.net/api/auth/reset-password"

# Прокси через Cloudflare Worker
session = AiohttpSession(api=TelegramAPIServer.from_base("https://odd-sunset-7a40.akter2004.workers.dev"))
bot = Bot(token=BOT_TOKEN, session=session)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сбросить пароль", callback_data="reset_password")]
    ])
    await message.answer(
        f"Привет, {message.from_user.first_name}!\n\n"
        "Это бот поддержки сайта Давыдов LIVE.\n"
        "Нажми кнопку ниже, чтобы сбросить пароль.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data == "reset_password")
async def process_reset_password(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    async with aiohttp.ClientSession() as session:
        payload = {"telegramId": telegram_id, "secret": API_SECRET}
        try:
            async with session.post(SITE_API_URL, json=payload) as resp:
                if resp.status == 200:
                    await callback.message.answer("Пароль сброшен! Возвращайся на сайт и вводи новый.")
                else:
                    await callback.message.answer("Ошибка на сайте. Попробуй позже.")
        except Exception:
            await callback.message.answer("Не могу связаться с сайтом.")
    await callback.answer()

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())