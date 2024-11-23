import sqlite3

import telebot.async_telebot
import yaml
from telebot import types


# TODO: sort imports


class DBConnection:
    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        self.connection = connection
        self.con = self.connection
        self.cursor = cursor
        self.cur = self.cursor

    def save_and_close(self):
        self.con.commit()
        self.cur.close()
        self.con.close()


class DBManager:
    @staticmethod
    async def get_db_file_from_config(name: str):
        with open('./config/config.yml', 'r') as f:
            cfg = yaml.safe_load(f)
        return cfg['dbs'][name]['file']

    @staticmethod
    async def connect_db(file: str) -> DBConnection:
        con = sqlite3.connect(file)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        dbcon = DBConnection(con, cur)
        return dbcon

    @staticmethod
    async def query(file: str, query: str, params: tuple = tuple()) -> list[sqlite3.Row]:
        dbcon = await DBManager.connect_db(file)
        dbcon.cur.execute(query, params)
        res = dbcon.cur.fetchall()
        dbcon.save_and_close()
        return res


class MenuNavigationManager:
    @staticmethod
    async def handle_menu(
            path: str,
            bot: telebot.async_telebot.AsyncTeleBot,
            msg: types.Message,
            user: types.User,
            **kwargs
    ):
        module = __import__(f"{'.'.join(path.split('/'))}.main", fromlist="main")
        await module.handle_menu(bot, msg, user, **kwargs)
        del module


class EmojiManager:
    @staticmethod
    def get_emoji(name: str) -> str:
        with open('./config/config.yml', 'r', encoding='utf') as f:
            cfg = yaml.safe_load(f)
        try:
            return cfg['emojis'][name]
        except KeyError:
            return ''
