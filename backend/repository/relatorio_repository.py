import sqlite3
import json
from pathlib import Path


class RelatorioRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            # Caminho padrão igual aos outros repositórios
            db_path = Path(__file__).parent.parent.parent / "sistema.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)

    def salvar_relatorio(self, nome, tipo, dados, criado_em):
        self.conn.execute(
            "INSERT INTO reports (nome, tipo, criado_em, dados) VALUES (?, ?, ?, ?)",
            (nome, tipo, criado_em, json.dumps(dados)),
        )
        self.conn.commit()

    def listar_relatorios(self):
        cursor = self.conn.execute("SELECT * FROM reports ORDER BY criado_em DESC")
        rows = cursor.fetchall()
        cols = [c[0] for c in cursor.description]
        results = []
        for r in rows:
            d = dict(zip(cols, r))
            try:
                d["dados"] = json.loads(d.get("dados") or "[]")
            except Exception:
                d["dados"] = d.get("dados")
            results.append(d)
        return results

    def obter_relatorio(self, relatorio_id):
        cursor = self.conn.execute(
            "SELECT * FROM reports WHERE id=? LIMIT 1", (relatorio_id,)
        )
        row = cursor.fetchone()
        if not row:
            return None
        cols = [c[0] for c in cursor.description]
        d = dict(zip(cols, row))
        try:
            d["dados"] = json.loads(d.get("dados") or "[]")
        except Exception:
            d["dados"] = d.get("dados")
        return d
