import sqlite3
import datetime
from backend.repository.relatorio_repository import RelatorioRepository
from backend.repository.estoque_repository import EstoqueRepository
from backend.database.database import DB_PATH


class RelatorioService:
    def __init__(self):
        self.repo = RelatorioRepository()
        self.estoque_repo = EstoqueRepository()
        self.conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)

    def gerar_relatorio_financeiro(self, periodo=None):
        """
        Receita (entradas) = itens_venda.quantidade * estoque.preco_venda
        Custo   (saidas)   = itens_venda.quantidade * estoque.preco_custo
        Agrupado por data e por mês (AAAA-MM).
        """
        rows = self.conn.execute(
            """
            SELECT
                DATE(v.data)                                        AS data,
                SUBSTR(v.data, 1, 7)                                AS mes,
                SUM(iv.quantidade * COALESCE(e.preco_venda, 0))     AS receita,
                SUM(iv.quantidade * COALESCE(e.preco_custo, 0))     AS custo
            FROM itens_venda iv
            JOIN  vendas v ON v.id = iv.venda_id
            LEFT JOIN estoque e ON e.nome = iv.produto
            GROUP BY DATE(v.data)
            ORDER BY DATE(v.data)
            """
        ).fetchall()

        total_entradas = 0.0
        total_saidas = 0.0
        por_data = {}
        ganhos_por_mes = {}

        for data, mes, receita, custo in rows:
            receita = receita or 0.0
            custo = custo or 0.0
            if periodo and mes != periodo:
                continue
            total_entradas += receita
            total_saidas += custo
            por_data[data] = {"entradas": receita, "saidas": custo}
            ganhos_por_mes[mes] = ganhos_por_mes.get(mes, 0.0) + (receita - custo)

        rel = {
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": total_entradas - total_saidas,
            "por_data": por_data,
            "ganhos_por_mes": ganhos_por_mes,
            "gerado_em": datetime.datetime.now().isoformat(),
        }
        self.repo.salvar_relatorio(
            nome="Financeiro",
            tipo="financeiro",
            dados=rel,
            criado_em=datetime.datetime.now().isoformat(),
        )
        return rel

    def gerar_relatorio_estoque(self, low_stock_threshold=5):
        produtos = self.estoque_repo.listar_produtos()
        total_valor = sum(
            float(p.get("quantidade") or 0) * float(p.get("preco_custo") or 0)
            for p in produtos
        )
        baixo_estoque = [
            p for p in produtos if int(p.get("quantidade") or 0) <= low_stock_threshold
        ]
        rel = {
            "total_produtos": len(produtos),
            "total_valor_estoque": total_valor,
            "baixo_estoque": baixo_estoque,
            "todos_produtos": produtos,
            "gerado_em": datetime.datetime.now().isoformat(),
        }
        self.repo.salvar_relatorio(
            nome="Estoque",
            tipo="estoque",
            dados=rel,
            criado_em=datetime.datetime.now().isoformat(),
        )
        return rel

    def gerar_relatorio_vendas_por_produto(self):
        rows = self.conn.execute(
            """
            SELECT
                iv.produto,
                SUM(iv.quantidade)                                  AS total_qtd,
                SUM(iv.quantidade * COALESCE(e.preco_venda, 0))     AS total_val
            FROM itens_venda iv
            LEFT JOIN estoque e ON e.nome = iv.produto
            GROUP BY iv.produto
            ORDER BY total_qtd DESC
            """
        ).fetchall()

        vendas = {
            produto: {"quantidade": int(qtd or 0), "valor": float(valor or 0.0)}
            for produto, qtd, valor in rows
        }

        rel = {
            "vendas_por_produto": vendas,
            "gerado_em": datetime.datetime.now().isoformat(),
        }
        self.repo.salvar_relatorio(
            nome="Vendas por Produto",
            tipo="vendas_produto",
            dados=rel,
            criado_em=datetime.datetime.now().isoformat(),
        )
        return rel


relatorio_service = RelatorioService()
