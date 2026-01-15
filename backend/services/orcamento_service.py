import json
from backend.repository.orcamento_repository import OrcamentoRepository


class OrcamentoService:
    def __init__(self):
        self.repo = OrcamentoRepository()

    def listar_orcamentos(self):
        return self.repo.listar_orcamentos()

    def adicionar_orcamento(self, orcamento):
        # Serializa os itens para JSON
        orcamento = orcamento.copy()
        orcamento["itens"] = json.dumps(orcamento["itens"])
        # garante campo mensagem_adicional
        orcamento.setdefault("mensagem_adicional", "")
        return self.repo.adicionar_orcamento(orcamento)

    def deletar_orcamento(self, orcamento_id):
        # tenta remover o PDF associado antes de apagar o registro
        try:
            import os

            pdf_dir = os.path.join(os.getcwd(), "interface", "assets", "orçamentos")
            pdf_path = os.path.join(pdf_dir, f"orcamento_{orcamento_id}.pdf")
            if os.path.exists(pdf_path):
                try:
                    os.remove(pdf_path)
                    print(f"[ORCAMENTO] PDF removido: {pdf_path}")
                except Exception as e:
                    print(f"[ORCAMENTO] falha ao remover PDF {pdf_path}:", e)
        except Exception:
            pass
        # remove do banco
        self.repo.deletar_orcamento(orcamento_id)

    def editar_orcamento(self, orcamento):
        orcamento = orcamento.copy()
        orcamento["itens"] = json.dumps(orcamento["itens"])
        orcamento.setdefault("mensagem_adicional", "")
        self.repo.editar_orcamento(orcamento)
