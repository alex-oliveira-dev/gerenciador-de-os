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
    # Retorna metadados agregados para evitar N+1 queries na camada de UI
    cursor.execute(
        """
        SELECT
            v.id,
            v.cliente,
            v.forma_pagamento,
            v.data,
            (SELECT SUM(quantidade) FROM itens_venda WHERE venda_id = v.id) as total_itens,
            (SELECT SUM(quantidade * COALESCE((SELECT preco_venda FROM estoque WHERE nome = itens_venda.produto LIMIT 1), 0)) FROM itens_venda WHERE venda_id = v.id) as total_valor
        FROM vendas v
        ORDER BY v.data DESC
        """
    )
    vendas = cursor.fetchall()
    conn.close()
    return vendas
