from backend.repository.cliente_repository import ClienteRepository
from backend.repository.estoque_repository import EstoqueRepository


class VendasDropdownService:
    def __init__(self):
        self.cliente_repo = ClienteRepository()
        self.estoque_repo = EstoqueRepository()

    def listar_nomes_clientes(self):
        return [c["nome"] for c in self.cliente_repo.listar_clientes()]

    def listar_nomes_produtos(self):
        return [p["nome"] for p in self.estoque_repo.listar_produtos()]
