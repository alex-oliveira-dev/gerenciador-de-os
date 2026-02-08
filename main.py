from backend.database.criar_banco_completo import criar_banco_completo
from backend.services.painel_service import PainelService
import flet as ft
import os
import shutil
from backend.services import estoque_service
from interface.ui.views.estoque_view import EstoqueView
from interface.ui.views.cliente_view import ClienteView
from interface.ui.views.funcionario_view import FuncionarioView
from interface.ui.views.orcamento_view import OrcamentoView
from interface.ui.views.relatorios_view import RelatoriosView
from interface.ui.views.vendas_view import VendasView
from interface.ui.views.config_view import ConfiguracoesView
from interface.ui.modais.modal_produto import ModalProduto
from interface.components.alertaSnack import alertSnackBarMensage
import threading


class App:

    def __init__(self, page: ft.Page):
        self.page = page
        # Permite acesso global à instância App a partir de page
        setattr(self.page, "app_instance", self)
        page.window_min_width = 980
        page.window_min_height = 1200
        page.resizable = False
        page.title = "Sistema de Gestão HSO SOLUTIONS"
        page.theme_mode = ft.ThemeMode.LIGHT
        

        def iniciar_atualizacao_periodica(self):
            def atualizar_tabelas():
                if hasattr(self, "refresh_all") and callable(self.refresh_all):
                    self.refresh_all()
                # agenda próxima execução
                threading.Timer(10, atualizar_tabelas).start()  # 10s = 0.17min

            threading.Timer(10, atualizar_tabelas).start()

        self.iniciar_atualizacao_periodica = iniciar_atualizacao_periodica.__get__(self)
        # Inicia atualização periódica das tabelas
        self.iniciar_atualizacao_periodica()

        # Inicializações dos objetos antes do layout
        self.estoque = EstoqueView(page)
        self.clientes = ClienteView(page)
        self.funcionarios = FuncionarioView(page)
        def mostrar_snack_mensagem(mensagem, bgcolor=ft.Colors.AMBER, text_color=ft.Colors.WHITE):
            alertSnackBarMensage(self.page, mensagem, bgcolor, text_color)

        self.mostrar_snack_mensagem = mostrar_snack_mensagem
        self.orcamentos = OrcamentoView(page, self.mostrar_snack_mensagem)
        self.relatorios = RelatoriosView(page)
        self.vendas = VendasView(page)

        # Painel (dashboard)
        self.painel_service = PainelService()

        # Funções utilitárias para atualizar todas as tabelas após mudanças
        def refresh_all():
            try:
                self.estoque.carregar_produtos()
            except Exception:
                pass
            try:
                self.clientes.atualizar_clientes()
            except Exception:
                pass
            try:
                self.funcionarios.atualizar_funcionarios()
            except Exception:
                pass
            try:
                self.orcamentos.atualizar_orcamentos()
            except Exception:
                pass
            try:
                self.page.update()
            except Exception:
                pass

        self.refresh_all = refresh_all

        # wrappers que garantem refresh geral após alterações
        def _add_produto(p):
            self.estoque.adicionar_produto(p)
            self.refresh_all()

        def _carregar_produtos():
            self.estoque.carregar_produtos()

        def _salvar_edicao_produto(p):
            self.estoque.salvar_edicao(p)
            self.refresh_all()

        self.modal_produto = ModalProduto(
            page=page,
            adicionar_produto=_add_produto,
            carregar_produtos=_carregar_produtos,
            salvar_edicao=_salvar_edicao_produto,
        )

        # instancia view de configurações (padronizada)
        self.configuracoes = ConfiguracoesView(page)

        page.add(
            ft.ResponsiveRow(
                expand=True,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Tabs(
                                length=8,
                                selected_index=0,
                                expand=True,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.TabBar(
                                            tabs=[
                                                ft.Tab(
                                                    label="ESTOQUE",
                                                    icon=ft.Icons.INVENTORY,
                                                ),
                                                ft.Tab(
                                                    label="CLIENTES",
                                                    icon=ft.Icons.PEOPLE,
                                                ),
                                                ft.Tab(
                                                    label="FUNCIONÁRIOS",
                                                    icon=ft.Icons.PERSON_2,
                                                ),
                                                ft.Tab(
                                                    label="ORÇAMENTOS",
                                                    icon=ft.Icons.BOOK,
                                                ),
                                                ft.Tab(
                                                    label="VENDAS",
                                                    icon=ft.Icons.POINT_OF_SALE,
                                                ),
                                                ft.Tab(
                                                    label="RELATÓRIOS",
                                                    icon=ft.Icons.INSIGHTS,
                                                ),
                                                ft.Tab(
                                                    label="CONFIGURAÇÕES",
                                                    icon=ft.Icons.SETTINGS,
                                                ),
                                            ],
                                            indicator_color=ft.Colors.BLUE_400,
                                            label_color=ft.Colors.BLUE_400,
                                            unselected_label_color=ft.Colors.BLUE_200,
                                        ),
                                        ft.TabBarView(
                                            expand=True,
                                            controls=[
                                                # ESTOQUE
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=ft.Column(
                                                        expand=True,
                                                        controls=[
                                                            self.estoque.layout,
                                                        ],
                                                    ),
                                                ),
                                                # CLIENTES
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=self.clientes.layout,
                                                ),
                                                # FUNCIONÁRIOS
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=self.funcionarios.layout,
                                                ),
                                                # ORÇAMENTOS
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=self.orcamentos.layout,
                                                ),
                                                # VENDAS
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=self.vendas.layout,
                                                ),
                                                # RELATÓRIOS
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=self.relatorios.layout,
                                                ),
                                                # CONFIGURAÇÕES
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=self.configuracoes.layout,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            )
                        ],
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        self.estoque.carregar_produtos()
        page.update()


def main(page: ft.Page):
    # Garante que o banco de dados está criado/atualizado ao abrir o app
    criar_banco_completo()
    App(page)


ft.app(target=main)
