import sqlite3
from pathlib import Path
from backend.database.database import DB_PATH


class OrcamentoRepository:
    def __init__(self):

        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)

    def listar_orcamentos(self):
        cursor = self.conn.execute("SELECT * FROM orcamentos")
        return [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]

    def adicionar_orcamento(self, orcamento):
        cursor = self.conn.execute(
            "INSERT INTO orcamentos (cliente, data, itens, total_sem_desconto, total_com_desconto, desconto, mensagem_adicional) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                orcamento.get("cliente"),
                orcamento.get("data"),
                orcamento.get("itens"),
                orcamento.get("total_sem_desconto"),
                orcamento.get("total_com_desconto"),
                orcamento.get("desconto"),
                orcamento.get("mensagem_adicional"),
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def deletar_orcamento(self, orcamento_id):
        self.conn.execute("DELETE FROM orcamentos WHERE id=?", (orcamento_id,))
        self.conn.commit()
