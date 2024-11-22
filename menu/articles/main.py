from telebot import types
from telebot.async_telebot import AsyncTeleBot

from managers import DBManager


async def handle_menu(bot: AsyncTeleBot, msg: types.Message, user: types.User, article_id: int = None):
    if article_id is None:
        db_file = await DBManager.get_db_file_from_config("main")
        articles = await DBManager.query(db_file, "SELECT * FROM Articles")
        markup = types.InlineKeyboardMarkup()
        for article in articles:
            markup.add()
        await bot.send_message(msg.chat.id, "*Список статей*", parse_mode="markdown")
    else:
        ...
