import flet as ft


class TabelaEstoque:
    def __init__(self, page, editar_produto, excluir_produto):
        self.page = page
        self.on_editar = editar_produto
        self.on_excluir = excluir_produto

        # Lista com scroll (apenas os dados)
        self.lista_itens = ft.ListView(
            expand=True,
            spacing=0,
            padding=0,
        )

        # Layout final da tabela (wrap em Column para permitir scroll responsivo)
        tabela_container = ft.Container(
            border=ft.border.all(2, ft.Colors.BLACK54),
            border_radius=8,
            content=ft.Column(
                spacing=0,
                controls=[
                    self._cabecalho(),  # FIXO
                    ft.Container(
                        expand=True,
                        content=self.lista_itens,
                    ),
                ],
            ),
        )

        self.layout = ft.Column(
            [tabela_container],
            expand=True,
            spacing=20,
            scroll="auto",
        )

        self.mensagem_tabela_vazia = ft.Text(
            "NENHUM PRODUTO CADASTRADO!",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED,
            size=20,
            weight=ft.FontWeight.BOLD,
        )

    # =============================
    # HEADER FIXO
    # =============================
    def _cabecalho(self):
        return ft.Container(
            bgcolor=ft.Colors.GREY_300,
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(2, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        "Nº ITENS",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        width=50,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "NOME",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "CÓDIGO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "QTD",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "MARCA",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "FORNECEDORES",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Preço de Custo",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Preço de Venda",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "Ações",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )

    # =============================
    # LINHA DA TABELA
    # =============================
    def _linha(self, item, index):
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
                    ),  # contador da linha
                    ft.Text(
                        str(item.get("nome", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(item.get("codigo", "")).upper(),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(item["quantidade"]),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(item.get("marca", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(item.get("fornecedores", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"R$ {item.get('preco_custo', 0.0):.2f}",
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        f"R$ {item.get('preco_venda', 0.0):.2f}",
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, i=item: self.on_editar(i),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, i=item: self.on_excluir(i),
                            ),
                        ],
                        expand=1,
                    ),
                ],
            ),
        )

    # =============================
    # ATUALIZAR DADOS
    # =============================
    def atualizar(self, itens_em_estoque):
        if isinstance(itens_em_estoque, dict):
            itens_em_estoque = [itens_em_estoque]

        self.lista_itens.controls.clear()

        if not itens_em_estoque:
            self.lista_itens.controls.append(self.mensagem_tabela_vazia)

        for idx, item in enumerate(itens_em_estoque):
            self.lista_itens.controls.append(self._linha(item, index=idx))

        self.page.update()
