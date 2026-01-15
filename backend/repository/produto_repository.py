from backend.database.database import Database

db = Database()


def criar_tabela():
    criar_tabela_produtos(),


def criar_tabela_produtos():
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            codigo TEXT,
            quantidade INTEGER,
            marca TEXT,
            fornecedores TEXT
        )
        """
    )


def inserir(produto: dict):
    db.execute(
        """
        INSERT INTO produtos (nome, codigo, quantidade, marca, fornecedores)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            produto["nome"],
            produto["codigo"],
            produto["quantidade"],
            produto["marca"],
            produto["fornecedores"],
        ),
    )


def listar():
    try:
        rows = db.fetchall("SELECT * FROM produtos ORDER BY id DESC")
        print([dict(row) for row in rows])
        return [dict(row) for row in rows]  # 🔑 LISTA
    except Exception as e:
        print("Erro ao listar produtos:", e)
        return []


def deletar(produto_id):
    db.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))


def editar(produto: dict):
    db.execute(
        """
        UPDATE produtos
        SET nome = ?, codigo = ?, quantidade = ?, marca = ?, fornecedores = ?
        WHERE id = ?
        """,
        (
            produto["nome"],
            produto["codigo"],
            produto["quantidade"],
            produto["marca"],
            produto["fornecedores"],
            produto["id"],
        ),
    )
