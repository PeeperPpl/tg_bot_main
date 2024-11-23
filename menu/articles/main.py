from telebot import types
from telebot.async_telebot import AsyncTeleBot

from managers import DBManager, EmojiManager


async def handle_menu(bot: AsyncTeleBot, msg: types.Message, user: types.User, article_id: int = None):
    await bot.delete_message(msg.chat.id, msg.id)
    if article_id is None:
        db_file = await DBManager.get_db_file_from_config("main")
        articles = await DBManager.query(db_file, "SELECT id, title FROM Articles")
        markup = types.InlineKeyboardMarkup()
        for article in articles:
            markup.add(types.InlineKeyboardButton(
                text=article['title'],
                callback_data=f'menu/articles?article_id={article['id']}'
            ))
        markup.add(types.InlineKeyboardButton(
            text=f'{EmojiManager.get_emoji('arrow_left')} Назад',
            callback_data=f'menu'
        ))
        await bot.send_message(msg.chat.id, "*Список статей*", reply_markup=markup)
    else:
        db_file = await DBManager.get_db_file_from_config("main")
        article = await DBManager.query(db_file, "SELECT title, text FROM Articles")
        article = article[0]
        text = f'*{article['title']}*\n\n'
        text += article['text']
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            text='Правки',
            callback_data=f'menu/articles/edits?article_id={article_id}'
        ))
        markup.add(types.InlineKeyboardButton(
            text=f'{EmojiManager.get_emoji('arrow_left')} Назад',
            callback_data=f'menu/articles'
        ))
        await bot.send_message(msg.chat.id, text, reply_markup=markup)
