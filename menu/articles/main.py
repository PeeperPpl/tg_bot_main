from telebot.async_telebot import AsyncTeleBot

from managers import DBManager


async def handle_menu(bot: AsyncTeleBot):
    articles = DBManager.query("SELECT * FROM")
    await bot.send_message()
