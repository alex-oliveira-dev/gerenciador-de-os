from backend.repository.cliente_repository import ClienteRepository


class ClienteService:
    def __init__(self):
        self.repo = ClienteRepository()

    def listar_clientes(self):
        return self.repo.listar_clientes()

    def adicionar_cliente(self, cliente):
        self.repo.adicionar_cliente(cliente)

    def editar_cliente(self, cliente):
        self.repo.editar_cliente(cliente)

    def excluir_cliente(self, cliente_id):
        self.repo.excluir_cliente(cliente_id)


cliente_service = ClienteService()
