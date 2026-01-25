import flet as ft
from interface.ui.tabelas.tabela_ordem_servico import TabelaOrdemServico
from interface.ui.modais.modal_nova_ordem_servico import ModalAdicionarOrdemServico
from backend.services.ordem_servico_service import ordem_servico_service


class OrdemServicoView:
    def __init__(
        self,
        page: ft.Page,
        mostrar_snack_mensagem,
        popular_tabela_ordem_servico,
        carregar_ordens_servico,
    ):
        self.page = page
        self.mostrar_snack_mensagem = mostrar_snack_mensagem
        self.popular_tabela_ordem_servico = popular_tabela_ordem_servico

        self.tabela_ordem_servico = TabelaOrdemServico(
            page,
            self.adicionar_ordem_servico,
            self.excluir_ordem_servico,
            self.editar_ordem_servico,
            carregar_ordens_servico,
            mostrar_snack_mensagem,
        )

        self.modal_nova_ordem_servico = ModalAdicionarOrdemServico(
            page,
            self.adicionar_ordem_servico,
            self.editar_ordem_servico,
            self.mostrar_snack_mensagem,
            self.popular_tabela_ordem_servico,
        )

        self.layout_ordem_servico = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ElevatedButton(
                        "NOVA O.S.",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self.modal_nova_ordem_servico.abrir_modal_adicionar_ordem_servico(),
                    ),
                    self.tabela_ordem_servico.tabela_ordem_servico,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                spacing=20,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            expand=True,
            padding=24,
        )
        self.tabela_ordem_servico.popular_tabela_ordem_servico()

    def adicionar_ordem_servico(self, dados_ordem):
        ordem_servico_service.adicionar_ordem_servico(dados_ordem)
        self.tabela_ordem_servico.popular_tabela_ordem_servico()
        self.page.update()

    def editar_ordem_servico(self, dados_ordem_editados):
        ordem_servico_service.editar_ordem_servico(dados_ordem_editados)
        self.tabela_ordem_servico.popular_tabela_ordem_servico()
        self.page.update()

    def excluir_ordem_servico(self, dados_ordem):
        ordem_servico_service.excluir_ordem_servico(dados_ordem)
        self.tabela_ordem_servico.popular_tabela_ordem_servico()
        self.page.update()