from backend.repository.company_repository import CompanyRepository


class CompanyService:
    def __init__(self):
        self.repo = CompanyRepository()

    def obter_config(self):
        return self.repo.obter_config()

    def salvar_config(self, config: dict):
        return self.repo.salvar_config(config)

    def deletar_logo(self):
        return self.repo.deletar_logo()
