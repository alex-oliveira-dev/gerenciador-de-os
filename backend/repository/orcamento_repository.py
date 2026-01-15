import sqlite3
from pathlib import Path


class OrcamentoRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "orcamentos.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._criar_tabela()

    def _criar_tabela(self):
        # cria tabela se não existir (versão com mensagem_adicional)
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS orcamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                data TEXT,
                itens TEXT, -- JSON string com os itens
                total_sem_desconto REAL,
                total_com_desconto REAL,
                desconto REAL,
                mensagem_adicional TEXT
            )"""
        )
        self.conn.commit()
        # se usuário estiver migrando de versão antiga, adicione a coluna se ausente
        try:
            cursor = self.conn.execute("PRAGMA table_info(orcamentos)")
            cols = [row[1] for row in cursor.fetchall()]
            if "mensagem_adicional" not in cols:
                self.conn.execute(
                    "ALTER TABLE orcamentos ADD COLUMN mensagem_adicional TEXT"
                )
                self.conn.commit()
        except Exception:
            pass

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

    def editar_orcamento(self, orcamento):
        self.conn.execute(
            "UPDATE orcamentos SET cliente=?, data=?, itens=?, total_sem_desconto=?, total_com_desconto=?, desconto=?, mensagem_adicional=? WHERE id=?",
            (
                orcamento.get("cliente"),
                orcamento.get("data"),
                orcamento.get("itens"),
                orcamento.get("total_sem_desconto"),
                orcamento.get("total_com_desconto"),
                orcamento.get("desconto"),
                orcamento.get("mensagem_adicional"),
                orcamento.get("id"),
            ),
        )
        self.conn.commit()
