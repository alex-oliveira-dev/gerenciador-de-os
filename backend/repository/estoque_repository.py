import sqlite3


import os
from pathlib import Path


class EstoqueRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "estoque.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            codigo TEXT,
            quantidade INTEGER,
            marca TEXT,
            fornecedores TEXT,
            preco_custo REAL DEFAULT 0.0,
            preco_venda REAL DEFAULT 0.0
        )"""
        )
        self.conn.commit()

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
