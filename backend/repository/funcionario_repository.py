import sqlite3
import os

from pathlib import Path


class FuncionarioRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "funcionarios.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cargo TEXT,
            cpf TEXT,
            telefone TEXT,
            email TEXT
        )"""
        )
        self.conn.commit()

    def listar_funcionarios(self):
        cursor = self.conn.execute("SELECT * FROM funcionarios")
        return [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]

    def adicionar_funcionario(self, funcionario):
        self.conn.execute(
            "INSERT INTO funcionarios (nome, cargo, cpf, telefone, email) VALUES (?, ?, ?, ?, ?)",
            (
                funcionario["nome"],
                funcionario["cargo"],
                funcionario["cpf"],
                funcionario["telefone"],
                funcionario["email"],
            ),
        )
        self.conn.commit()

    def editar_funcionario(self, funcionario_editado):
        self.conn.execute(
            "UPDATE funcionarios SET nome=?, cargo=?, cpf=?, telefone=?, email=? WHERE id=?",
            (
                funcionario_editado["nome"],
                funcionario_editado["cargo"],
                funcionario_editado["cpf"],
                funcionario_editado["telefone"],
                funcionario_editado["email"],
                funcionario_editado["id"],
            ),
        )
        self.conn.commit()

    def excluir_funcionario(self, funcionario_id):
        self.conn.execute("DELETE FROM funcionarios WHERE id=?", (funcionario_id,))
        self.conn.commit()
