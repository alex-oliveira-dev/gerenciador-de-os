from backend.repository.venda_repository import (
    registrar_venda,
    listar_vendas,
)


class VendaService:
    def __init__(self):
        pass

    def registrar_venda(self, cliente, forma_pagamento, itens):
        return registrar_venda(cliente, forma_pagamento, itens)

    def listar_vendas(self):
        return listar_vendas()
