from backend.repository.estoque_repository import EstoqueRepository


class EstoqueService:
    def __init__(self):
        self.repo = EstoqueRepository()

    def listar_produtos(self):
        return self.repo.listar_produtos()

    def adicionar_produto(self, produto):
        self.repo.adicionar_produto(produto)

    def editar_produto(self, produto):
        self.repo.editar_produto(produto)

    def deletar_produto(self, produto_id):
        self.repo.deletar_produto(produto_id)


estoque_service = EstoqueService()
