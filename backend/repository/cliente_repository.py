import sqlite3
import os
from backend.database.database import DB_PATH
from pathlib import Path


class ClienteRepository:
    """
    Todas as operações usam o banco 'sistema.db' localizado na raiz do projeto.
    A tabela 'clientes' está dentro deste banco.
    """

    def __init__(self):
        self.db_path = DB_PATH

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def listar_clientes(self):
        with self._get_conn() as conn:
            cursor = conn.execute("SELECT * FROM clientes")
            return [dict(row) for row in cursor.fetchall()]

    def adicionar_cliente(self, cliente):
        with self._get_conn() as conn:
            conn.execute(
                "INSERT INTO clientes (nome, cpf, telefone, email, endereco) VALUES (?, ?, ?, ?, ?)",
                (
                    cliente["nome"],
                    cliente["cpf"],
                    cliente["telefone"],
                    cliente["email"],
                    cliente["endereco"],
                ),
            )
            conn.commit()

    def editar_cliente(self, cliente_editado):
        with self._get_conn() as conn:
            conn.execute(
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
            conn.commit()

    def excluir_cliente(self, cliente_id):
        with self._get_conn() as conn:
            conn.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
            conn.commit()
