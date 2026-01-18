import sqlite3
from pathlib import Path
import os

# Caminho do banco de dados na raiz do projeto
DB_PATH = Path(__file__).parent.parent.parent / "sistema.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # 🔑 ESSENCIAL
        self.cursor = self.conn.cursor()

    def execute(self, query, params=()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur.lastrowid

    def fetchall(self, query, params=()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()
