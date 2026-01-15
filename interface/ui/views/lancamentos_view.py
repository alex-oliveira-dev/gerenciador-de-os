import flet as ft
from interface.ui.tabelas.tabela_lancamentos import TabelaLancamentos
from interface.ui.modais.modal_novo_lancamento import ModalAdicionarLancamento
from backend.services.lancamento_service import lancamento_service


class LancamentosView:
    def __init__(
        self,
        page: ft.Page,
        mostrar_snack_mensagem,
        popular_tabela_lancamentos,
        carregar_lamcamentos,
    ):
        self.page = page
        self.mostrar_snack_mensagem = mostrar_snack_mensagem
        self.popular_tabela_lancamentos = popular_tabela_lancamentos

        # indicador de carregamento removido para agilizar interface

        # Tabela
        self.tabela_lancamentos = TabelaLancamentos(
            page,
            self.adicionar_lancamento,  # ou a função correta para adicionar
            self.excluir_lancamento,
            self.editar_lancamento,
            carregar_lamcamentos,
            mostrar_snack_mensagem,
        )

        # Modal
        self.modal_novo_lancamento = ModalAdicionarLancamento(
            page,
            self.adicionar_lancamento,
            self.editar_lancamento,
            self.mostrar_snack_mensagem,
            self.popular_tabela_lancamentos,
        )

        self.layout_lancamentos = ft.Column(
            controls=[
                self.tabela_lancamentos.tabela_lancamentos,  # ✅ AQUI
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=20,
        )
        self.tabela_lancamentos.popular_tabela_lancamentos()

    # def atualizar_lancamentos(self, dados_lancamentos):
    #     lancamento_service.atualizar_lancamentos(dados_lancamentos)
    #     self.page.update()

    def adicionar_lancamento(self, dados_lancamentos):
        print("chamou a funcão adicionar")
        lancamento_service.adicionar_novo_lancamento(dados_lancamentos)
        self.tabela_lancamentos.popular_tabela_lancamentos()
        self.page.update()

    def editar_lancamento(self, dados_lancamentos_editados):
        lancamento_service.editar_lancamento(dados_lancamentos_editados)
        self.page.update()

    def excluir_lancamento(self, dados_lancamentos):
        lancamento_service.excluir_lancamento(dados_lancamentos)
        self.tabela_lancamentos.popular_tabela_lancamentos()
        self.page.update()

    def salvar_edicao_lancamento(self, dados_lancamentos):
        print("chamou salvar edição")
        lancamento_service.salvar_alteracoes_lancamento(dados_lancamentos)
        self.page.update()
