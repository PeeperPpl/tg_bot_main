from telebot import types
from telebot.async_telebot import AsyncTeleBot

from managers import DBManager


async def handle_menu(bot: AsyncTeleBot, msg: types.Message, user: types.User, edit_id: int):
    await bot.delete_message(msg.chat.id, msg.id)
    db_file = await DBManager.get_db_file_from_config('main')
    edit_info = await DBManager.query(db_file, "SELECT * FROM Edits WHERE edit_id = ?", (edit_id,))
    edit_info = edit_info[0]
    edit_user = await bot.get_chat_member(edit_info['user_id'], edit_info['user_id'])
    edit_user = edit_user.user
    text = f'*Правка от @{edit_user.username}*\n\n'
    text += f'Строка: {edit_info['line']}\nСимвол: {edit_info['column']}'
    text += f'```diff\n-{edit_info['old']}\n+{edit_info['new']}\n```'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text='Назад',
        callback_data=f'menu/articles/edits?article_id={edit_info['article_id']}'
    ))
    if edit_user.id == user.id:
        ...
    await bot.send_message(
        text=text,
        chat_id=msg.chat.id,
        reply_markup=markup
    )
