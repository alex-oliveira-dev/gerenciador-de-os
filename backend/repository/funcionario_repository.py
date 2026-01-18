import sqlite3
import os
from backend.database.database import DB_PATH
from pathlib import Path


class FuncionarioRepository:
    def __init__(self):
       
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)

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
