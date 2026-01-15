from backend.repository.funcionario_repository import FuncionarioRepository


class FuncionarioService:
    def __init__(self):
        self.repo = FuncionarioRepository()

    def listar_funcionarios(self):
        return self.repo.listar_funcionarios()

    def adicionar_funcionario(self, funcionario):
        self.repo.adicionar_funcionario(funcionario)

    def editar_funcionario(self, funcionario):
        self.repo.editar_funcionario(funcionario)

    def excluir_funcionario(self, funcionario_id):
        self.repo.excluir_funcionario(funcionario_id)


funcionario_service = FuncionarioService()
