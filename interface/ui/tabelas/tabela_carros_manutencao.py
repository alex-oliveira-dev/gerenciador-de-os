import flet as ft
from interface.ui.modais.modal_editar_ordem_servico import ModalEditarOrdemServico


class TabelaCarrosManutencao:
    def __init__(
        self,
        page,
        finalizar_callback=None,
    ):
        self.page = page
        self.finalizar_callback = finalizar_callback
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
                ft.Row(
                    [
                        ft.Button(
                            "Atualizar lista",
                            icon=ft.Icons.REFRESH,
                            bgcolor=ft.Colors.BLUE_400,
                            color=ft.Colors.WHITE,
                            on_click=self._refresh_manual,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
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

    def _refresh_manual(self, e=None):
        # Atualiza a lista manualmente
        # Busca a instância App na page para acessar painel_service
        app = getattr(self.page, "app_instance", None)
        if app and hasattr(app, "painel_service"):
            self.atualizar(app.painel_service.listar_carros_em_manutencao())

    def set_finalizar_callback(self, callback):
        self.finalizar_callback = callback

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
                        "",
                        expand=1,
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
                            ft.ElevatedButton(
                                "Finalizar O.S",
                                icon=ft.Icons.CHECK_CIRCLE,
                                bgcolor=ft.Colors.GREEN_400,
                                color=ft.Colors.WHITE,
                                on_click=lambda e, o=os: (
                                    self.finalizar_callback(o)
                                    if self.finalizar_callback
                                    else None
                                ),
                            ),
                        ],
                        expand=1,
                    ),
                ]
            ),
        )

    def atualizar(self, lista_os):
        self.lista_os.controls.clear()
        if not lista_os:
            self.lista_os.controls.append(self.mensagem_vazia)
        else:
            for idx, os in enumerate(lista_os):
                self.lista_os.controls.append(self._linha_os(os, idx))
