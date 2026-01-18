import flet as ft
from interface.ui.modais.modal_editar_ordem_servico import ModalEditarOrdemServico


class TabelaCarrosManutencao:
    def __init__(
        self,
        page,
        abrir_os_callback,
        situacao_callback,
        pdf_callback,
        preencher_callback,
        editar_callback=None,
    ):
        self.page = page
        self.abrir_os_callback = abrir_os_callback
        self.situacao_callback = situacao_callback
        self.pdf_callback = pdf_callback
        self.preencher_callback = preencher_callback
        self.editar_callback = editar_callback
        self.lista_os = ft.ListView(expand=True, spacing=0, padding=0)
        self.mensagem_vazia = ft.Text(
            "NENHUM CARRO EM MANUTENÇÃO!",
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
                            ft.Container(expand=True, content=self.lista_os),
                        ]
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=20,
            scroll="auto",
        )

    def set_editar_callback(self, callback):
        self.editar_callback = callback

    def _cabecalho(self):
        return ft.Container(
            bgcolor=ft.Colors.GREY_300,
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(2, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        "Nº da OS",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        width=70,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "CLIENTE",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "DEFEITO",
                        expand=3,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "SITUAÇÃO",
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
                ]
            ),
        )

    def _linha_os(self, os, index):
        return ft.Container(
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        str(os.get("id", "")),
                        width=70,
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(os.get("cliente", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(os.get("defeito_relatado", "")).upper(),
                        expand=3,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Text(
                        str(os.get("status", "")).upper(),
                        expand=1,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.OPEN_IN_NEW,
                                tooltip="Abrir OS",
                                on_click=lambda e, o=os: self.abrir_os_callback(o),
                                icon_color=ft.Colors.BLUE_700,
                            ),
                            ft.IconButton(
                                ft.Icons.PICTURE_AS_PDF,
                                tooltip="Abrir em PDF",
                                icon_color=ft.Colors.RED_700,
                                on_click=lambda e, o=os: self.pdf_callback(o),
                            ),
                            ft.IconButton(
                                ft.Icons.EDIT,
                                tooltip="Editar",
                                icon_color=ft.Colors.GREEN_700,
                                on_click=lambda e, o=os: (
                                    self.editar_callback(o)
                                    if self.editar_callback
                                    else None
                                ),
                            ),
                        ],
                        expand=1,
                    ),
                ]
            ),
        )  # Removido: não existe mais self.tabela

    def atualizar(self, lista_os):
        self.lista_os.controls.clear()
        if not lista_os:
            self.lista_os.controls.append(self.mensagem_vazia)
        else:
            for idx, os in enumerate(lista_os):
                self.lista_os.controls.append(self._linha_os(os, idx))
