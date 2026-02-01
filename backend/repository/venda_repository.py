import sqlite3
from typing import List, Dict


def registrar_venda(cliente: str, forma_pagamento: str, itens: List[Dict]):
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO vendas (cliente, forma_pagamento) VALUES (?, ?)",
        (cliente, forma_pagamento),
    )
    venda_id = cursor.lastrowid
    for item in itens:
        cursor.execute(
            "INSERT INTO itens_venda (venda_id, produto, quantidade) VALUES (?, ?, ?)",
            (venda_id, item["produto"], item["quantidade"]),
        )
    conn.commit()
    conn.close()
    return venda_id


def listar_vendas():
    conn = sqlite3.connect("sistema.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, cliente, forma_pagamento, data FROM vendas ORDER BY data DESC"
    )
    vendas = cursor.fetchall()
    conn.close()
    return vendas
