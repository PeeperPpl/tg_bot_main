import sqlite3
import os
#TODO: sort imports


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
    def connect_db(file: str) -> DBConnection:
        con = sqlite3.connect(file)
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        dbcon = DBConnection(con, cur)
        return dbcon

    @staticmethod
    async def init_db(dbcon: DBConnection, init_func: callable):
        await init_func(dbcon)
        dbcon.save_and_close()

    @staticmethod
    async def query(file: str, query: str) -> sqlite3.Row:
        dbcon = DBManager.connect_db(file)
        dbcon.cur.execute(query)
        res = dbcon.cur.fetchall()
        return res


class RashStatusType:
    permission = "permission"


class RashStatus:
    def __init__(self, type: str) -> None:
        self.type = type


class BotMenuNavigationEndpoint:
    def __init__(self, path: str, rash_statuses: list[RashStatus], py_modules: list[str]) -> None:
        self.path = path
        self.rash_statuses = rash_statuses
        self.py_modules = {}
        for module in py_modules:
            match module:
                case "main.py":
                    self.py_modules['main'] = module
        if 'main' in self.py_modules.keys():
            module = __import__(f"{'.'.join(path.split('/')[1:])}.main", fromlist='main')
            self.run_func = module.handle_menu


class BotMenuNavigationManager:
    @staticmethod
    def get_menu_endpoint(_path: str):
        path = f"./{_path}"
        subfiles = os.listdir(path)
        subfiles_d = {}
        for subfile in subfiles:
            subfile_type = subfile.split(".")[-1]
            try:
                subfiles_d[subfile_type]
            except KeyError:
                subfiles_d[subfile_type] = []
            subfiles_d[subfile_type].append(subfile)
        endp = BotMenuNavigationEndpoint(
            path,
            subfiles_d['rash_status'],
            subfiles_d['py']
        )
        return endp
