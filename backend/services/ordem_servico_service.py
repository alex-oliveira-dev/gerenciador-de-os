from backend.repository.os_repository import OrdemServicoRepository
from backend.repository.estoque_repository import EstoqueRepository
import datetime


class OrdemServicoService:
    # def listar_ordens_servico_abertas(self):
    #     return self.repo.listar_ordens_servico_abertas()

    def __init__(self):
        self.repo = OrdemServicoRepository()
        self.estoque_repo = EstoqueRepository()

    def listar_ordens_servico(self):
        return self.repo.listar_ordens_servico()

    def adicionar_ordem_servico(self, ordem):
        if not ordem.get("data_abertura"):
            ordem["data_abertura"] = datetime.datetime.now().strftime("%d/%m/%Y")
            try:
                new_id = self.repo.adicionar_ordem_servico(ordem)
                return new_id
            except Exception:
                try:
                    self.estoque_repo.ajustar_quantidade_por_nome(
                        ordem.get("produto"),
                    )
                except Exception:
                    return self.repo.adicionar_ordem_servico(ordem)
                raise
        return self.repo.adicionar_ordem_servico(ordem)

    def editar_ordem_servico(self, ordem):
        old = self.repo.obter_por_id(ordem.get("id"))
        if not old:
            raise ValueError("Ordem de Serviço não encontrada")

        # Ajustar estoque para todos os itens_os
        itens_os = ordem.get("itens_os", [])
        if itens_os:
            for item in itens_os:
                nome_produto = item.get("produto")
                qtd = int(item.get("quantidade") or 0)
                if nome_produto:
                    adj = self.estoque_repo.ajustar_quantidade_por_nome(
                        nome_produto, -qtd
                    )
                    if adj[0] is None:
                        raise ValueError(
                            f"Produto '{nome_produto}' não encontrado no estoque"
                        )

        self.repo.editar_ordem_servico(ordem)

    def excluir_ordem_servico(self, ordem):
        old = self.repo.obter_por_id(ordem.get("id"))
        if not old:
            return

        old_q = int(old.get("quantidade") or 0)
        try:
            self.estoque_repo.ajustar_quantidade_por_nome(old.get("produto"), -old_q)
        except Exception:
            pass

        self.repo.deletar_ordem_servico(ordem.get("id"))


# Instância global do serviço de ordem de serviço
ordem_servico_service = OrdemServicoService()
