from backend.repository.relatorio_repository import RelatorioRepository
from backend.repository.lancamento_repository import OrdemServicoRepository
from backend.repository.estoque_repository import EstoqueRepository
from backend.repository.orcamento_repository import OrcamentoRepository
import datetime


class RelatorioService:
    def __init__(self):
        self.repo = RelatorioRepository()
        self.lanc_repo = OrdemServicoRepository()
        self.estoque_repo = EstoqueRepository()
        self.orc_repo = OrcamentoRepository()

    def gerar_relatorio_financeiro(self):
        lancamentos = self.lanc_repo.listar_ordens_servico()
        total_entradas = 0.0
        total_saidas = 0.0
        por_data = {}
        for l in lancamentos:
            tipo = str(l.get("tipo") or "").upper()
            preco = float(l.get("preco") or 0)
            qtd = int(l.get("quantidade") or 0)
            valor = preco * qtd
            data = l.get("data") or ""
            if tipo == "ENTRADA":
                total_entradas += valor
            else:
                total_saidas += valor
            por_data.setdefault(data, {"entradas": 0.0, "saidas": 0.0})
            if tipo == "ENTRADA":
                por_data[data]["entradas"] += valor
            else:
                por_data[data]["saidas"] += valor

        saldo = total_entradas - total_saidas
        rel = {
            "total_entradas": total_entradas,
            "total_saidas": total_saidas,
            "saldo": saldo,
            "por_data": por_data,
            "gerado_em": datetime.datetime.now().isoformat(),
        }
        # salva metadado do relatório
        self.repo.salvar_relatorio(
            nome="Financeiro",
            tipo="financeiro",
            dados=rel,
            criado_em=datetime.datetime.now().isoformat(),
        )
        return rel

    def gerar_relatorio_estoque(self, low_stock_threshold=5):
        produtos = self.estoque_repo.listar_produtos()
        baixo_estoque = [
            p for p in produtos if int(p.get("quantidade") or 0) <= low_stock_threshold
        ]
        rel = {
            "total_produtos": len(produtos),
            "baixo_estoque": baixo_estoque,
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
        lancamentos = self.lanc_repo.listar_ordens_servico()
        vendas = {}
        for l in lancamentos:
            tipo = str(l.get("tipo") or "").upper()
            if tipo != "SAÍDA":
                continue
            prod = l.get("produto") or ""
            qtd = int(l.get("quantidade") or 0)
            preco = float(l.get("preco") or 0)
            entry = vendas.setdefault(prod, {"quantidade": 0, "valor": 0.0})
            entry["quantidade"] += qtd
            entry["valor"] += preco * qtd

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
