import sqlite3
import os

from pathlib import Path


class ClienteRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "clientes.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cpf TEXT,
            telefone TEXT,
            email TEXT,
            endereco TEXT
        )"""
        )
        self.conn.commit()

    def listar_clientes(self):
        cursor = self.conn.execute("SELECT * FROM clientes")
        return [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]

    def adicionar_cliente(self, cliente):
        self.conn.execute(
            "INSERT INTO clientes (nome, cpf, telefone, email, endereco) VALUES (?, ?, ?, ?, ?)",
            (
                cliente["nome"],
                cliente["cpf"],
                cliente["telefone"],
                cliente["email"],
                cliente["endereco"],
            ),
        )
        self.conn.commit()

    def editar_cliente(self, cliente_editado):
        self.conn.execute(
            "UPDATE clientes SET nome=?, cpf=?, telefone=?, email=?, endereco=? WHERE id=?",
            (
                cliente_editado["nome"],
                cliente_editado["cpf"],
                cliente_editado["telefone"],
                cliente_editado["email"],
                cliente_editado["endereco"],
                cliente_editado["id"],
            ),
        )
        self.conn.commit()

    def excluir_cliente(self, cliente_id):
        self.conn.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        self.conn.commit()
