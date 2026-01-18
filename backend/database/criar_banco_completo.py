from pathlib import Path
import sqlite3

def criar_banco_completo(db_path="sistema.db"):
    db_path = Path(__file__).resolve().parents[2] / db_path
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    # Tabela ordens_servico
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS ordens_servico (
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

    # Tabela reports
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        tipo TEXT,
        criado_em TEXT,
        dados TEXT
    )"""
    )

    # Tabela produtos
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        codigo TEXT,
        quantidade INTEGER,
        marca TEXT,
        fornecedores TEXT
    )"""
    )

    # Tabela orcamentos
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS orcamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        data TEXT,
        itens TEXT,
        total_sem_desconto REAL,
        total_com_desconto REAL,
        desconto REAL,
        mensagem_adicional TEXT
    )"""
    )

    # Tabela funcionarios
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cargo TEXT,
        cpf TEXT,
        telefone TEXT,
        email TEXT
    )"""
    )

    # Tabela estoque
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS estoque (
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

    # Tabela company
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS company (
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

    # Tabela clientes
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        telefone TEXT,
        email TEXT,
        endereco TEXT
    )"""
    )

    conn.commit()
    conn.close()
    print(f"Banco de dados criado/atualizado em: {db_path}")


if __name__ == "__main__":
    criar_banco_completo()
