from telebot import types
from telebot.async_telebot import AsyncTeleBot


async def handle_menu(bot: AsyncTeleBot, msg: types.Message, user: types.User):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        text='Статьи',
        callback_data='menu/articles'
    ))
    await bot.delete_message(msg.chat.id, msg.id)
    await bot.send_message(
        msg.chat.id,
        f"Привет, @{user.username}",
        reply_markup=markup
    )