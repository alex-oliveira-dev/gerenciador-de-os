import sqlite3
from pathlib import Path
import os

# Caminho do banco de dados na pasta backend/database
DB_PATH = Path(__file__).parent / "database.db"


class Database:
    def __init__(self):
        # Garante que a pasta existe (deveria sempre existir)
        db_dir = DB_PATH.parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)
        # Cria o banco se não existir
        if not DB_PATH.exists():
            open(DB_PATH, "a").close()
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
