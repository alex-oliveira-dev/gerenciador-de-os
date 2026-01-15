import flet as ft


class TabelaFuncionario:
    def __init__(self, page, editar_funcionario, excluir_funcionario):
        self.page = page
        self.editar_funcionario = editar_funcionario
        self.excluir_funcionario = excluir_funcionario
        self.lista_funcionarios = ft.ListView(expand=True, spacing=0, padding=0)
        self.mensagem_vazia = ft.Text(
            "NENHUM FUNCIONÁRIO CADASTRADO!",
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
                            ft.Container(expand=True, content=self.lista_funcionarios),
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
                        "CARGO",
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
                        "AÇÕES",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ]
            ),
        )

    def _linha_funcionario(self, funcionario, index):
        return ft.Container(
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        str(funcionario["id"]),
                        width=50,
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(funcionario.get("nome", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(funcionario.get("cargo", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(funcionario.get("cpf", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(funcionario.get("telefone", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(funcionario.get("email", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, f=funcionario: self.editar_funcionario(
                                    f
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, f=funcionario: self.excluir_funcionario(
                                    f
                                ),
                            ),
                        ],
                        expand=1,
                    ),
                ]
            ),
        )

    def atualizar(self, funcionarios):
        self.lista_funcionarios.controls.clear()
        if not funcionarios:
            self.lista_funcionarios.controls.append(self.mensagem_vazia)
        else:
            for idx, funcionario in enumerate(funcionarios):
                self.lista_funcionarios.controls.append(
                    self._linha_funcionario(funcionario, idx)
                )
        self.page.update()
