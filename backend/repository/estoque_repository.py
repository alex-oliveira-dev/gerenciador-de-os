import sqlite3
from backend.database.database import DB_PATH
import os
from pathlib import Path


class EstoqueRepository:
    """
    Todas as operações usam o banco 'sistema.db' localizado na raiz do projeto.
    As tabelas de estoque estão dentro deste banco.
    """

    def __init__(self):

        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    def listar_produtos(self):
        cursor = self.conn.execute("SELECT * FROM estoque")
        return [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]

    def obter_por_nome(self, nome):
        cursor = self.conn.execute(
            "SELECT * FROM estoque WHERE nome=? LIMIT 1", (nome,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return dict(zip([column[0] for column in cursor.description], row))

    def ajustar_quantidade_por_nome(self, nome, delta):
        """Ajusta a quantidade do produto identificado por `nome` somando `delta`.
        Retorna tuple (old_quantity, new_quantity) ou (None, None) se produto não encontrado.
        """
        prod = self.obter_por_nome(nome)
        if not prod:
            return (None, None)
        old_q = int(prod.get("quantidade") or 0)
        new_q = old_q + int(delta)
        if new_q < 0:
            new_q = 0
        self.conn.execute(
            "UPDATE estoque SET quantidade=? WHERE id=?", (new_q, prod["id"])
        )
        self.conn.commit()
        return (old_q, new_q)

    def adicionar_produto(self, produto):
        self.conn.execute(
            "INSERT INTO estoque (nome, codigo, quantidade, marca, fornecedores, preco_custo, preco_venda) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                produto["nome"],
                produto["codigo"],
                produto["quantidade"],
                produto["marca"],
                produto["fornecedores"],
                produto.get("preco_custo", 0.0),
                produto.get("preco_venda", 0.0),
            ),
        )
        self.conn.commit()

    def editar_produto(self, produto):
        self.conn.execute(
            "UPDATE estoque SET nome=?, codigo=?, quantidade=?, marca=?, fornecedores=?, preco_custo=?, preco_venda=? WHERE id=?",
            (
                produto["nome"],
                produto["codigo"],
                produto["quantidade"],
                produto["marca"],
                produto["fornecedores"],
                produto.get("preco_custo", 0.0),
                produto.get("preco_venda", 0.0),
                produto["id"],
            ),
        )
        self.conn.commit()

    def deletar_produto(self, produto_id):
        self.conn.execute("DELETE FROM estoque WHERE id=?", (produto_id,))
        self.conn.commit()
