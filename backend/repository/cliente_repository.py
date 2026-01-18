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

        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)

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
