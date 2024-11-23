import asyncio
import yaml

from telebot.async_telebot import AsyncTeleBot
from telebot import types

from managers import MenuNavigationManager

with open('./config/config.yml', 'r') as f:
    cfg_main = yaml.safe_load(f)

TOKEN = cfg_main['bots']['main']['token']
bot = AsyncTeleBot(TOKEN, disable_web_page_preview=True, colorful_logs=True, parse_mode='markdown')


@bot.message_handler(commands=['start', 'menu'])
async def cmd_start(msg: types.Message):
    await MenuNavigationManager.handle_menu('menu', bot, msg, msg.from_user)


@bot.callback_query_handler(func=lambda call: True)
async def callback_inline(query: types.CallbackQuery):
    data = query.data
    path = data.split('?')[0]
    args = None
    parsed_args = None
    try:
        args = data.split('?')[1]
    except Exception: pass
    else:
        args = args.split(';')
        parsed_args = {}
        for arg in args:
            parsed_args[arg.split('=')[0]] = arg.split('=')[1]
    if args is None:
        await MenuNavigationManager.handle_menu(
            data,
            bot,
            query.message,
            query.from_user
        )
    else:
        await MenuNavigationManager.handle_menu(
            path,
            bot,
            query.message,
            query.from_user,
            **parsed_args
        )


async def run():
    task = asyncio.create_task(bot.infinity_polling())
    await task
