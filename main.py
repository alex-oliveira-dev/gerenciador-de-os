from interface.ui.views.painel_view import PainelView
from backend.database.criar_banco_completo import criar_banco_completo
from interface.ui.tabelas.tabela_carros_manutencao import TabelaCarrosManutencao
from backend.services.painel_service import PainelService
import flet as ft
import os
import json
import shutil
from backend.services import estoque_service
from backend.services import ordem_servico_service
from interface.ui.views.estoque_view import EstoqueView
from interface.ui.views.ordem_servico_view import OrdemServicoView
from interface.ui.views.cliente_view import ClienteView
from interface.ui.views.funcionario_view import FuncionarioView
from interface.ui.views.orcamento_view import OrcamentoView
from interface.ui.views.relatorios_view import RelatoriosView
from interface.ui.views.config_view import ConfiguracoesView
from interface.ui.modais.modal_produto import ModalProduto
from interface.ui.modais.modal_nova_ordem_servico import (
    ModalAdicionarOrdemServico,
)
from interface.ui.tabelas.tabela_ordem_servico import TabelaOrdemServico  # Renomeado
from interface.ui.modais.modal_editar_ordem_servico import ModalEditarOrdemServico
from backend.services.ordem_servico_service import ordem_servico_service
import threading


class App:

    def __init__(self, page: ft.Page):
        self.page = page
        # Permite acesso global à instância App a partir de page
        setattr(self.page, "app_instance", self)
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
        self.ordem_servico = OrdemServicoView(
            page,
            None,  # mostrar_snack_mensagem
            None,  # popular_tabela_ordem_servico
            ordem_servico_service.listar_ordens_servico,  # carregar_ordens_servico
        )
        self.clientes = ClienteView(page)
        self.funcionarios = FuncionarioView(page)
        self.orcamentos = OrcamentoView(page, lambda msg: None)
        self.relatorios = RelatoriosView(page)

        # Painel (dashboard) - tabela de carros em manutenção
        self.painel_service = PainelService()

        def editar_os_callback(os):
            def salvar_edicao(dados):
                self.ordem_servico.editar_ordem_servico(dados)
                self.refresh_all()

            modal = ModalEditarOrdemServico(
                page=self.page,
                ordem=os,
                salvar_callback=salvar_edicao,
                fechar_callback=None,
            )
            modal.abrir()

        def finalizar_os_callback(os):
            def atualizar_tabela_carros():
                if hasattr(self, "tabela_carros_manutencao") and hasattr(
                    self, "painel_service"
                ):
                    self.tabela_carros_manutencao.atualizar(
                        self.painel_service.listar_carros_em_manutencao()
                    )

            def salvar_finalizacao(dados):
                # Atualiza o status para 'Finalizada' e salva no banco
                dados["status"] = "Finalizada"
                self.ordem_servico.editar_ordem_servico(dados)
                self.refresh_all()
                atualizar_tabela_carros()

            def fechar_modal_callback():
                atualizar_tabela_carros()

            modal = ModalEditarOrdemServico(
                page=self.page,
                ordem=os,
                salvar_callback=salvar_finalizacao,
                fechar_callback=fechar_modal_callback,
                titulo="Finalizar O.S",
            )
            modal.abrir()

        self.tabela_carros_manutencao = TabelaCarrosManutencao(
            self.page,
            finalizar_callback=finalizar_os_callback,
        )
        self.painel_view = PainelView(self.page, self.tabela_carros_manutencao)
        # Atualiza a tabela do painel ao iniciar
        self.tabela_carros_manutencao.atualizar(
            self.painel_service.listar_carros_em_manutencao()
        )

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
            lambda: self.modal_nova_ordem_servico.abrir_modal_adicionar_ordem_servico(),
            _excluir_ordem_servico,
            _editar_ordem_servico,
            ordem_servico_service.listar_ordens_servico,
            None,
        )
        self.modal_nova_ordem_servico = ModalAdicionarOrdemServico(
            page,
            _add_ordem_servico,  # adicionar_ordem_servico
            None,  # editar_ordem_servico
            None,  # mostrar_snack_mensagem
            _popular_ordem_servico,  # popular_tabela_ordem_servico
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
                                                    label="PAINEL",
                                                    icon=ft.Icons.DASHBOARD,
                                                ),
                                                ft.Tab(
                                                    label="ESTOQUE",
                                                    icon=ft.Icons.INVENTORY,
                                                ),
                                                ft.Tab(
                                                    label="O.S.",
                                                    icon=ft.Icons.DESCRIPTION,
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
                                                self.painel_view.layout,
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
    # Garante que o banco de dados está criado/atualizado ao abrir o app
    criar_banco_completo()
    App(page)


ft.app(target=main)
