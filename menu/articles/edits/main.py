from telebot import types
from telebot.async_telebot import AsyncTeleBot

from managers import DBManager, EmojiManager


async def handle_menu(bot: AsyncTeleBot, msg: types.Message, user: types.User, article_id: int):
    await bot.delete_message(msg.chat.id, msg.id)
    db_file = await DBManager.get_db_file_from_config('main')
    edits = await DBManager.query(db_file, "SELECT edit_id, old, new FROM Edits WHERE article_id = ?", (article_id,))
    markup = types.InlineKeyboardMarkup()
    for edit in edits:
        markup.add(types.InlineKeyboardButton(
            text=f'{edit['old']} > {edit['new']}',
            callback_data=f'menu/articles/edits/view?edit_id={edit['edit_id']}'
        ))
    markup.add(types.InlineKeyboardButton(
        text='Добавить правку',
        callback_data=f'menu/articles/edits/add'
    ))
    markup.add(types.InlineKeyboardButton(
        text=f'{EmojiManager.get_emoji('arrow_left')} Назад',
        callback_data=f'menu/articles?article_id={article_id}'
    ))
    article_text = await DBManager.query(db_file, "SELECT text FROM Articles WHERE id = ?", (article_id,))
    article_text = article_text[0]['text']
    await bot.send_message(
        chat_id=msg.chat.id,
        text=f"*Список правок*\n\n{article_text}",
        reply_markup=markup
    )
