import flet as ft
import os
import json
import shutil
from backend.services import estoque_service
from backend.services import ordem_servico_service  # Renomeado
from interface.ui.views.estoque_view import EstoqueView
from interface.ui.views.ordem_servico_view import OrdemServicoView  # Renomeado
from interface.ui.views.cliente_view import ClienteView
from interface.ui.views.funcionario_view import FuncionarioView
from interface.ui.views.orcamento_view import OrcamentoView
from interface.ui.views.relatorios_view import RelatoriosView
from interface.ui.views.config_view import ConfiguracoesView
from interface.ui.modais.modal_produto import ModalProduto
from interface.ui.modais.modal_nova_ordem_servico import (
    ModalAdicionarOrdemServico,
)  # Renomeado
from interface.ui.tabelas.tabela_ordem_servico import TabelaOrdemServico  # Renomeado


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        page.window_min_width = 980
        page.window_min_height = 1280
        page.resizable = False
        page.title = "Sistema de Gestão HSO SOLUTIONS"
        page.theme_mode = ft.ThemeMode.LIGHT
        # Migrar arquivos da pasta assets (raiz) para interface/assets
        try:
            root_assets = os.path.join(os.path.dirname(__file__), "assets")
            interface_assets = os.path.join(
                os.path.dirname(__file__), "interface", "assets"
            )
            if os.path.exists(root_assets):
                os.makedirs(interface_assets, exist_ok=True)
                interface_orcamentos = os.path.join(interface_assets, "orçamentos")
                os.makedirs(interface_orcamentos, exist_ok=True)
                for f in os.listdir(root_assets):
                    src = os.path.join(root_assets, f)
                    # se for PDF de orçamento, mover para subpasta orçamentos
                    ext = os.path.splitext(f)[1].lower()
                    if f.lower().startswith("orcamento_"):
                        dst = os.path.join(interface_orcamentos, f)
                    elif ext in (".png", ".jpg", ".jpeg", ".gif", ".bmp"):
                        # imagens -> pasta de logos
                        interface_logo = os.path.join(interface_assets, "logo")
                        os.makedirs(interface_logo, exist_ok=True)
                        dst = os.path.join(interface_logo, f)
                    else:
                        dst = os.path.join(interface_assets, f)
                    try:
                        if not os.path.exists(dst):
                            shutil.move(src, dst)
                        else:
                            # se já existe no destino, remove o original
                            os.remove(src)
                    except Exception as mv_err:
                        print("Erro movendo asset:", mv_err)
                # tenta remover a pasta raiz se vazia
                try:
                    if not os.listdir(root_assets):
                        os.rmdir(root_assets)
                except Exception:
                    pass
        except Exception as e:
            print("Erro ao migrar assets:", e)
        print(type(self.page))

        # Inicializações dos objetos antes do layout
        self.estoque = EstoqueView(page)
        self.ordem_servico = OrdemServicoView(page, None, None, None)  # Renomeado
        self.clientes = ClienteView(page)
        self.funcionarios = FuncionarioView(page)
        self.orcamentos = OrcamentoView(page, lambda msg: None)
        self.relatorios = RelatoriosView(page)

        # Funções utilitárias para atualizar todas as tabelas após mudanças
        def refresh_all():
            try:
                self.estoque.carregar_produtos()
            except Exception:
                pass
            try:
                if hasattr(self, "tabela_ordem_servico") and self.tabela_ordem_servico:
                    self.tabela_ordem_servico.popular_tabela_ordem_servico()
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

        def _add_ordem_servico(d):
            self.ordem_servico.adicionar_ordem_servico(d)
            self.refresh_all()

        def _excluir_ordem_servico(d):
            self.ordem_servico.excluir_ordem_servico(d)
            self.refresh_all()

        def _editar_ordem_servico(d):
            self.ordem_servico.editar_ordem_servico(d)
            self.refresh_all()

        def _popular_ordem_servico():
            self.ordem_servico.tabela_ordem_servico.popular_tabela_ordem_servico()

        self.tabela_ordem_servico = TabelaOrdemServico(
            page,
            _add_ordem_servico,
            _excluir_ordem_servico,
            _editar_ordem_servico,
            _popular_ordem_servico,
            None,
        )
        self.modal_nova_ordem_servico = ModalAdicionarOrdemServico(
            page,
            self.ordem_servico.editar_ordem_servico,
            _add_ordem_servico,
            None,
            _popular_ordem_servico,
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
                                length=7,
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
                                                    label="O.S.",
                                                    icon=ft.Icons.DESCRIPTION,  # Ícone alterado
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
                                                # O.S.
                                                ft.Container(
                                                    padding=20,
                                                    bgcolor=ft.Colors.GREY_300,
                                                    border_radius=12,
                                                    expand=True,
                                                    content=ft.Column(
                                                        expand=True,
                                                        controls=[
                                                            self.ordem_servico.layout_ordem_servico,
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
        self.tabela_ordem_servico.carregar_ordens_servico()
        page.update()


def main(page: ft.Page):
    App(page)


ft.app(target=main)
