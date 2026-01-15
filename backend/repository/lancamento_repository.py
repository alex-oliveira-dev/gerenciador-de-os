import sqlite3
import os
from pathlib import Path


class OrdemServicoRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "ordens_servico.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._criar_tabela()

    def _criar_tabela(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_abertura TEXT NOT NULL,
                cliente TEXT NOT NULL,
                equipamento TEXT,
                defeito_relatado TEXT,
                status TEXT NOT NULL DEFAULT 'Aberta',
                responsavel TEXT,
                servico TEXT,
                servico_executado TEXT,
                valor_servico REAL DEFAULT 0.0,
                pecas_utilizadas TEXT,
                valor_pecas REAL DEFAULT 0.0,
                valor_total REAL DEFAULT 0.0,
                data_fechamento TEXT,
                forma_pagamento TEXT,
                situacao_pagamento TEXT DEFAULT 'Pendente'
            )"""
        )
        self.conn.commit()

    def listar_ordens_servico(self):
        cursor = self.conn.execute("SELECT * FROM ordens_servico")
        return [
            dict(zip([column[0] for column in cursor.description], row))
            for row in cursor.fetchall()
        ]

    def adicionar_ordem_servico(self, ordem):
        cur = self.conn.execute(
            """
            INSERT INTO ordens_servico (
                data_abertura, cliente, equipamento, defeito_relatado, status, responsavel, servico, servico_executado, valor_servico, pecas_utilizadas, valor_pecas, valor_total, data_fechamento, forma_pagamento, situacao_pagamento
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ordem.get("data_abertura"),
                ordem.get("cliente"),
                ordem.get("equipamento"),
                ordem.get("defeito_relatado"),
                ordem.get("status", "Aberta"),
                ordem.get("responsavel"),
                ordem.get("servico"),
                ordem.get("servico_executado"),
                ordem.get("valor_servico", 0.0),
                ordem.get("pecas_utilizadas"),
                ordem.get("valor_pecas", 0.0),
                ordem.get("valor_total", 0.0),
                ordem.get("data_fechamento"),
                ordem.get("forma_pagamento"),
                ordem.get("situacao_pagamento", "Pendente"),
            ),
        )
        self.conn.commit()
        return cur.lastrowid

    def obter_por_id(self, ordem_id):
        cursor = self.conn.execute(
            "SELECT * FROM ordens_servico WHERE id=? LIMIT 1", (ordem_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        return dict(zip([column[0] for column in cursor.description], row))

    def editar_ordem_servico(self, ordem):
        self.conn.execute(
            """
            UPDATE ordens_servico SET
                data_abertura=?, cliente=?, equipamento=?, defeito_relatado=?, status=?, responsavel=?, servico=?, servico_executado=?, valor_servico=?, pecas_utilizadas=?, valor_pecas=?, valor_total=?, data_fechamento=?, forma_pagamento=?, situacao_pagamento=?
            WHERE id=?
            """,
            (
                ordem.get("data_abertura"),
                ordem.get("cliente"),
                ordem.get("equipamento"),
                ordem.get("defeito_relatado"),
                ordem.get("status", "Aberta"),
                ordem.get("responsavel"),
                ordem.get("servico"),
                ordem.get("servico_executado"),
                ordem.get("valor_servico", 0.0),
                ordem.get("pecas_utilizadas"),
                ordem.get("valor_pecas", 0.0),
                ordem.get("valor_total", 0.0),
                ordem.get("data_fechamento"),
                ordem.get("forma_pagamento"),
                ordem.get("situacao_pagamento", "Pendente"),
                ordem.get("id"),
            ),
        )
        self.conn.commit()

    def deletar_ordem_servico(self, ordem_id):
        self.conn.execute("DELETE FROM ordens_servico WHERE id=?", (ordem_id,))
        self.conn.commit()
