import flet as ft
from backend.services.cliente_service import cliente_service
from interface.ui.tabelas.tabela_cliente import TabelaCliente
from interface.ui.modais.modal_cliente import ModalCliente


class ClienteView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tabela = TabelaCliente(page, self.editar_cliente, self.excluir_cliente)
        self.modal = ModalCliente(page, self.adicionar_cliente, self.salvar_edicao)
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(
                        "NOVO CLIENTE",
                        icon=ft.Icons.PERSON_ADD,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self.modal.abrir_modal(),
                    ),
                    self.tabela.layout,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                spacing=20,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=24,
        )
        self.atualizar_clientes()

    def atualizar_clientes(self):
        clientes = cliente_service.listar_clientes()
        self.tabela.atualizar(clientes)
        self.page.update()

    def adicionar_cliente(self, cliente):
        cliente_service.adicionar_cliente(cliente)
        self.atualizar_clientes()
        self.page.update()

    def editar_cliente(self, cliente):
        self.modal.abrir_modal(cliente)

    def salvar_edicao(self, cliente):
        cliente_service.editar_cliente(cliente)
        self.atualizar_clientes()
        self.page.update()

    def excluir_cliente(self, cliente):
        cliente_service.excluir_cliente(cliente["id"])
        self.atualizar_clientes()
        self.page.update()
