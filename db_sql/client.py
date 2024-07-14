import sqlite3

class Client:
    def __init__(self, path):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    