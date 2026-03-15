import flet as ft
from backend.services.cliente_service import cliente_service
from interface.ui.tabelas.tabela_cliente import TabelaCliente
from interface.ui.modais.modal_cliente import ModalCliente
from interface.components.alertaSnack import alertSnackBarMensage


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
        # carregar clientes em background para não bloquear UI
        try:
            page.run_thread(self.atualizar_clientes)
        except Exception:
            import threading

            threading.Thread(target=self.atualizar_clientes, daemon=True).start()

    def atualizar_clientes(self, update_page=True):
        clientes = cliente_service.listar_clientes()
        self.tabela.atualizar(clientes, update_page=update_page)

    def adicionar_cliente(self, cliente):
        try:
            cliente_service.adicionar_cliente(cliente)
            self.atualizar_clientes(update_page=True)
            alertSnackBarMensage(
                self.page,
                "Cliente salvo com sucesso!",
                bgcolor=ft.Colors.GREEN_400,
            )
        except Exception as erro:
            alertSnackBarMensage(
                self.page,
                f"Erro ao salvar cliente: {erro}",
                bgcolor=ft.Colors.RED_400,
            )

    def editar_cliente(self, cliente):
        self.modal.abrir_modal(cliente)

    def salvar_edicao(self, cliente):
        try:
            cliente_service.editar_cliente(cliente)
            self.atualizar_clientes(update_page=True)
            alertSnackBarMensage(
                self.page,
                "Cliente atualizado com sucesso!",
                bgcolor=ft.Colors.GREEN_400,
            )
        except Exception as erro:
            alertSnackBarMensage(
                self.page,
                f"Erro ao editar cliente: {erro}",
                bgcolor=ft.Colors.RED_400,
            )

    def excluir_cliente(self, cliente):
        try:
            cliente_service.excluir_cliente(cliente["id"])
            self.atualizar_clientes(update_page=True)
            alertSnackBarMensage(
                self.page,
                "Cliente excluído com sucesso!",
                bgcolor=ft.Colors.GREEN_400,
            )
        except Exception as erro:
            alertSnackBarMensage(
                self.page,
                f"Erro ao excluir cliente: {erro}",
                bgcolor=ft.Colors.RED_400,
            )
