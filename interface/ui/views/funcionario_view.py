import flet as ft
from backend.services.funcionario_service import funcionario_service
from interface.ui.tabelas.tabela_funcionario import TabelaFuncionario
from interface.ui.modais.modal_funcionario import ModalFuncionario


class FuncionarioView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.tabela = TabelaFuncionario(
            page, self.editar_funcionario, self.excluir_funcionario
        )
        self.modal = ModalFuncionario(
            page, self.adicionar_funcionario, self.salvar_edicao
        )
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(
                        "NOVO FUNCIONÁRIO",
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
        self.atualizar_funcionarios()

    def atualizar_funcionarios(self):
        funcionarios = funcionario_service.listar_funcionarios()
        self.tabela.atualizar(funcionarios)
        self.page.update()

    def adicionar_funcionario(self, funcionario):
        funcionario_service.adicionar_funcionario(funcionario)
        self.atualizar_funcionarios()
        self.page.update()

    def editar_funcionario(self, funcionario):
        self.modal.abrir_modal(funcionario)

    def salvar_edicao(self, funcionario):
        funcionario_service.editar_funcionario(funcionario)
        self.atualizar_funcionarios()
        self.page.update()

    def excluir_funcionario(self, funcionario):
        funcionario_service.excluir_funcionario(funcionario["id"])
        self.atualizar_funcionarios()
        self.page.update()
