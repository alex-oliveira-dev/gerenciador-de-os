import sqlite3
from pathlib import Path


class CompanyRepository:
    def __init__(self, db_path=None):
        if db_path is None:
            db_dir = Path(__file__).parent.parent / "database"
            db_dir.mkdir(parents=True, exist_ok=True)
            db_path = db_dir / "company.db"
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self._criar_tabela()
        self._ensure_columns()

    def _criar_tabela(self):
        self.conn.execute(
            """CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY,
                nome TEXT,
                endereco TEXT,
                cep TEXT,
                estado TEXT,
                bairro TEXT,
                telefone TEXT,
                cpf_cnpj TEXT,
                logo_path TEXT
            )"""
        )
        self.conn.commit()

    def _ensure_columns(self):
        try:
            cur = self.conn.execute("PRAGMA table_info(company)")
            cols = [r[1] for r in cur.fetchall()]
            if "cpf_cnpj" not in cols:
                # adiciona coluna para compatibilidade com versões antigas
                try:
                    self.conn.execute("ALTER TABLE company ADD COLUMN cpf_cnpj TEXT")
                    self.conn.commit()
                    print("[DB] coluna 'cpf_cnpj' adicionada à tabela company")
                except Exception as e:
                    print("[DB] falha ao adicionar coluna cpf_cnpj:", e)
        except Exception:
            pass

    def obter_config(self):
        cursor = self.conn.execute("SELECT * FROM company WHERE id=1 LIMIT 1")
        row = cursor.fetchone()
        if not row:
            return None
        result = dict(zip([column[0] for column in cursor.description], row))
        # normaliza logo_path: se for relativo, resolve para o caminho absoluto do projeto
        try:
            lp = result.get("logo_path")
            if lp:
                p = Path(lp)
                if not p.is_absolute():
                    base = Path(__file__).parent.parent.parent
                    candidate = (base / lp).resolve()
                    if candidate.exists():
                        result["logo_path"] = str(candidate)
        except Exception:
            pass
        return result

    def salvar_config(self, config: dict):
        print("[DB] salvar_config chamado com:", config)
        # verifica se existe
        existing = self.conn.execute("SELECT id FROM company WHERE id=1").fetchone()
        if existing:
            self.conn.execute(
                "UPDATE company SET nome=?, endereco=?, cep=?, estado=?, bairro=?, telefone=?, cpf_cnpj=?, logo_path=? WHERE id=1",
                (
                    config.get("nome"),
                    config.get("endereco"),
                    config.get("cep"),
                    config.get("estado"),
                    config.get("bairro"),
                    config.get("telefone"),
                    config.get("cpf_cnpj"),
                    config.get("logo_path"),
                ),
            )
        else:
            self.conn.execute(
                "INSERT INTO company (id, nome, endereco, cep, estado, bairro, telefone, cpf_cnpj, logo_path) VALUES (1, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    config.get("nome"),
                    config.get("endereco"),
                    config.get("cep"),
                    config.get("estado"),
                    config.get("bairro"),
                    config.get("telefone"),
                    config.get("cpf_cnpj"),
                    config.get("logo_path"),
                ),
            )
        self.conn.commit()
        print("[DB] commit efetuado em company.db")

    def deletar_logo(self):
        self.conn.execute("UPDATE company SET logo_path=NULL WHERE id=1")
        self.conn.commit()
