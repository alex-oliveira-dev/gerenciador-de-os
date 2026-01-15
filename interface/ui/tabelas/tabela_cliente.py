import flet as ft


class TabelaCliente:
    def __init__(self, page, editar_cliente, excluir_cliente):
        self.page = page
        self.editar_cliente = editar_cliente
        self.excluir_cliente = excluir_cliente
        self.lista_clientes = ft.ListView(expand=True, spacing=0, padding=0)
        self.mensagem_vazia = ft.Text(
            "NENHUM CLIENTE CADASTRADO!",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED,
            size=20,
            weight=ft.FontWeight.BOLD,
        )
        self.layout = ft.Column(
            [
                ft.Container(
                    border=ft.border.all(2, ft.Colors.BLACK54),
                    border_radius=8,
                    content=ft.Column(
                        [
                            self._cabecalho(),
                            ft.Container(expand=True, content=self.lista_clientes),
                        ]
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=20,
            scroll="auto",
        )

    def _cabecalho(self):
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
                        "NOME",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "CPF",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "TELEFONE",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "EMAIL",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "ENDEREÇO",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        "AÇÕES",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ]
            ),
        )

    def _linha_cliente(self, cliente, index):
        return ft.Container(
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        str(cliente["id"]),
                        width=50,
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(cliente.get("nome", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(cliente.get("cpf", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(cliente.get("telefone", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(cliente.get("email", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(cliente.get("endereco", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, c=cliente: self.editar_cliente(c),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, c=cliente: self.excluir_cliente(c),
                            ),
                        ],
                        expand=1,
                    ),
                ]
            ),
        )

    def atualizar(self, clientes):
        self.lista_clientes.controls.clear()
        if not clientes:
            self.lista_clientes.controls.append(self.mensagem_vazia)
        else:
            for idx, cliente in enumerate(clientes):
                self.lista_clientes.controls.append(self._linha_cliente(cliente, idx))
        self.page.update()
