import flet as ft
from backend.services.lancamento_service import lancamento_service
from interface.ui.modais.modal_novo_lancamento import ModalAdicionarLancamento


class TabelaLancamentos:
    def __init__(
        self,
        page: ft.Page,
        dialog_adicionar_lancamento,
        excluir_lancamento,
        editar_lancamento,
        carregar_lancamentos,
        mostrar_snack_mensagem,
    ):
        self.page = page
        self.carregar_lancamentos = carregar_lancamentos

        self.modal_novo_lancamento = ModalAdicionarLancamento(
            self.page,
            editar_lancamento,
            dialog_adicionar_lancamento,  # ou a função correta
            mostrar_snack_mensagem,
            self.popular_tabela_lancamentos,
        )
        self.on_excluir = excluir_lancamento
        self.mostrar_snack_mensagem = mostrar_snack_mensagem

        self.mensagem_tabela_lancamento_vazia = ft.Text(
            "NENHUM LANÇAMENTO CADASTRADO, ADICIONE UM NOVO LANÇAMENTO AO BANCO DE DADOS!",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED_400,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

        # Lista com scroll (apenas os dados)
        self.lista_itens_lancamentos = ft.ListView(
            expand=True,
            spacing=0,
            padding=0,
        )

        self.tabela_lancamentos = ft.Container(
            border=ft.border.all(2, ft.Colors.BLACK54),
            border_radius=8,
            content=ft.Column(
                spacing=0,
                controls=[
                    self._cabecalho_lancamnetos(),  # FIXO
                    ft.Container(
                        expand=True,
                        content=self.lista_itens_lancamentos,
                    ),
                ],
            ),
        )

        self.botao_adicionar = ft.Button(
            "ADICIONAR LANÇAMENTO",
            icon=ft.Icons.ADD,
            on_click=lambda e: self.modal_novo_lancamento.abrir_modal_adicionar_lancamento(),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.BLUE_100,
                color=ft.Colors.BLACK,
            ),
        )

        self.layout = ft.Column(
            [
                ft.Row([self.botao_adicionar], alignment=ft.MainAxisAlignment.START),
                self.tabela_lancamentos,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=20,
            scroll="auto",
        )

    def on_editar(self, i):
        self.modal_novo_lancamento.abrir_modal_editar_lancamento(i)

    def on_excluir(self, i):
        self.on_excluir(i)

    def _cabecalho_lancamnetos(self):
        return ft.Container(
            bgcolor=ft.Colors.GREY_300,
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(2, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        "ID",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        width=50,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "DATA",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "HORA",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "TIPO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "PRODUTO",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "QUANTIDADE",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "PREÇO",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "RESPONSÁVEL LANÇAMENTO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "TIPO LANÇAMENTO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "FORMA PAGAMENTO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "AÇÕES",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                ],
            ),
        )

    def _linha_lancamentos(self, dados_lancamentos, index):

        return ft.Container(
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        str(index + 1),
                        width=50,
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),  # contador da linha
                    ft.Text(
                        dados_lancamentos["data"],
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        dados_lancamentos.get("hora", ""),
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        str(dados_lancamentos.get("tipo", "")).upper(),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        str(dados_lancamentos.get("produto", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        dados_lancamentos["quantidade"],
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        dados_lancamentos["preco"],
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        str(
                            dados_lancamentos.get("responsavel_lancamento", "")
                        ).upper(),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        str(dados_lancamentos.get("motivo_lancamento", "")).upper(),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        str(dados_lancamentos.get("forma_pagamento", "")).upper(),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, i=dados_lancamentos: self.on_editar(
                                    i
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, i=dados_lancamentos: self.on_excluir(
                                    i
                                ),
                            ),
                        ],
                        expand=1,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def carregar_lancamentos(self):
        self.popular_tabela_lancamentos()

    def popular_tabela_lancamentos(self):
        print("atualizando tabela lançamento")

        dados_lancamentos = lancamento_service.listar_dados_lancamentos()

        if not dados_lancamentos:
            self.lista_itens_lancamentos.controls.clear()
            self.lista_itens_lancamentos.controls.append(
                self.mensagem_tabela_lancamento_vazia
            )
            self.page.update()
            return

        try:
            if dados_lancamentos:
                self.lista_itens_lancamentos.controls.clear()
                for idx, lancamento in enumerate(dados_lancamentos):
                    linha = self._linha_lancamentos(lancamento, idx)
                    self.lista_itens_lancamentos.controls.append(linha)
                self.page.update()
        except Exception as e:
            print("erro ao popular tabela de lancamentos", e)

        self.page.update()
