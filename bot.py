import asyncio
import yaml

from telebot.async_telebot import AsyncTeleBot
from telebot import types

with open('./config/config.yml', 'r') as f:
    cfg_main = yaml.safe_load(f)

TOKEN = cfg_main['bots']['main']['token']
bot = AsyncTeleBot(TOKEN, disable_web_page_preview=True)


@bot.message_handler(commands=['start', 'menu'])
async def cmd_start(msg: types.Message):
    await bot.reply_to(
        msg,
        f"Привет, @{msg.from_user.username}"
    )


@bot.message_handler(commands=['work'])


async def run():
    task = asyncio.create_task(bot.infinity_polling())
    await task
