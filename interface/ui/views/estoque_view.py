import flet as ft
from backend.services.estoque_service import estoque_service
from interface.ui.tabelas.tabela_estoque import TabelaEstoque
from interface.ui.modais.modal_produto import ModalProduto


class EstoqueView:
    def __init__(self, page: ft.Page):
        self.page = page

        # Modal
        self.modal = ModalProduto(
            page,
            self.adicionar_produto,
            self.carregar_produtos,
            self.salvar_edicao,
        )

        # Tabela
        self.tabela = TabelaEstoque(
            page,
            self.editar_produto,
            self.excluir_produto,
        )

        # Layout da view
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(
                        "NOVO PRODUTO",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=lambda e: self.modal.abrir_modal_produto(),
                    ),
                    self.tabela.layout,
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
        # carregar produtos em background para não bloquear construção da UI
        try:
            page.run_thread(self.carregar_produtos)
        except Exception:
            import threading

            threading.Thread(target=self.carregar_produtos, daemon=True).start()

    # =============================
    # CARREGAR PRODUTOS
    # =============================
    def carregar_produtos(self, update_page=True):
        itens = estoque_service.listar_produtos()
        self.tabela.atualizar(itens, update_page=update_page)

    # =============================
    # CRUD
    # =============================
    def adicionar_produto(self, produto):
        estoque_service.adicionar_produto(produto)
        self.carregar_produtos(update_page=True)

    def excluir_produto(self, item):
        estoque_service.deletar_produto(item["id"])
        self.carregar_produtos(update_page=True)

    def editar_produto(self, item):
        self.modal.abrir_modal_produto(item)

    def salvar_edicao(self, item):
        estoque_service.editar_produto(item)
        self.carregar_produtos(update_page=True)
