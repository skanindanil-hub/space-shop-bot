import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "9083302986:AAGwyAzHVjoebGLzO3XJxcA2Ky64rwjm8Rs"
ADMIN_CONTACT = "https://t.me/fufufufw"
# Ссылка на твой будущий сервер (мы поменяем её на шаге 4)
WEBHOOK_HOST = "https://your-app-name.onrender.com" 
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
# ============================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- МЕНЮ ---
def get_main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Услуги Telegram", callback_data="cat_tg")],
        [InlineKeyboardButton(text="🎮 Услуги Black Russia", callback_data="cat_br")],
        [InlineKeyboardButton(text="🎨 Спецпредложения и Прочее", callback_data="cat_other")],
        [InlineKeyboardButton(text="💬 Связаться с продавцом", url=ADMIN_CONTACT)]
    ])

def get_tg_menu():
    text = ("📢 *Telegram — Услуги*\n\n➖ *Реклама в нашем tgk* — от 15зв ⭐️\n"
            "➖ *Накрут сабов* — от 15зв ⭐️ до 25зв ⭐️\n"
            "➖ *Накрут просмотров* — от 15зв ⭐️ до 25зв ⭐️\n"
            "➖ *Накрут реакций* — от 15зв ⭐️ до 25зв ⭐️\n\n👇 Для заказа нажми кнопку ниже.")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Заказать", url=ADMIN_CONTACT)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])
    return text, kb

def get_br_menu():
    text = ("🎮 *Black Russia*\n_(На данный момент не актуален)_\n\n"
            "➖ *Продажа акаунтов* — от 15зв ⭐️ до 50зв+ ⭐️\n"
            "➖ *Помощь в БС* — от 25зв ⭐️ до 65зв+ ⭐️\n"
            "➖ *Помощь в сносе респы* — от 25зв ⭐️ до 50зв ⭐️\n"
            "➖ *Помощь в сезоне* — от 75зв ⭐️\n\n👇 Для заказа нажми кнопку ниже.")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Заказать", url=ADMIN_CONTACT)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])
    return text, kb

def get_other_menu():
    text = ("🎨 *Спецпредложения*\n\n"
            "➖ *Продажа Эдита* — от 25зв ⭐️ до 100зв ⭐️\n"
            "➖ *Продажа аватарок / фотошоп* — от 15зв ⭐️ до 50зв ⭐️\n\n👇 Для заказа нажми кнопку ниже.")
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Заказать", url=ADMIN_CONTACT)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="main_menu")]
    ])
    return text, kb

# --- ХЕНДЛЕРЫ ---
@dp.message(Command("start"))
async def cmd_start(message: Message):
    text = ("👼 *Добро пожаловать в Space Shop!* 👼\n\n"
            "Здесь вы можете приобрести услуги для Telegram, игры и цифровой контент.\n\n👇 Выбери категорию:")
    await message.answer(text, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu())

@dp.callback_query(F.data == "main_menu")
async def process_main(callback: CallbackQuery):
    await callback.message.edit_text("👼 *Добро пожаловать в Space Shop!* 👼\n\n👇 Выбери категорию:", parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu())
    await callback.answer()

@dp.callback_query(F.data == "cat_tg")
async def process_tg(callback: CallbackQuery):
    text, kb = get_tg_menu()
    await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    await callback.answer()

@dp.callback_query(F.data == "cat_br")
async def process_br(callback: CallbackQuery):
    text, kb = get_br_menu()
    await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    await callback.answer()

@dp.callback_query(F.data == "cat_other")
async def process_other(callback: CallbackQuery):
    text, kb = get_other_menu()
    await callback.message.edit_text(text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb)
    await callback.answer()

# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def on_startup(bot: Bot):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)

def main():
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(dispatcher=dp, bot=bot)
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    dp.startup.register(on_startup)
    
    # Render сам передает нужный порт
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
