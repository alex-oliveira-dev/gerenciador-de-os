import flet as ft
import json


class TabelaOrcamento:
    def __init__(self, page, editar_orcamento, excluir_orcamento, abrir_modal_editar):
        self.page = page
        self.editar_orcamento = editar_orcamento
        self.excluir_orcamento = excluir_orcamento
        self.abrir_modal_editar = abrir_modal_editar
        self.lista_orcamentos = ft.ListView(expand=True, spacing=0, padding=0)
        self.mensagem_vazia = ft.Text(
            "NENHUM ORÇAMENTO CADASTRADO!",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED_400,
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
                            ft.Container(expand=True, content=self.lista_orcamentos),
                        ]
                    ),
                )
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
            border=ft.Border.only(bottom=ft.BorderSide(2, ft.Colors.BLACK54)),
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
                        "CLIENTE",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "DATA",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "ITENS",
                        expand=3,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "TOTAL S/ DESC.",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "TOTAL C/ DESC.",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "AÇÕES",
                        expand=2,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                ]
            ),
        )

    def _linha_orcamento(self, orcamento, index):
        import os

        itens = (
            json.loads(orcamento["itens"])
            if isinstance(orcamento["itens"], str)
            else orcamento["itens"]
        )
        itens_str = ", ".join(
            [
                f"{i['produto']} (x{i['quantidade']})"
                for i in itens
                if isinstance(i, dict) and "produto" in i and "quantidade" in i
            ]
        )

        def abrir_pdf(e, orc=orcamento):
            import os
            import platform
            import webbrowser
            from flet import SnackBar, Text, AlertDialog, Button

            # tenta importar WebView; se não existir, faz fallback
            try:
                from flet import WebView  # type: ignore

                webview_available = True
            except Exception:
                webview_available = False

            assets_dir = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "..", "..", "assets", "orçamentos"
                )
            )
            pdf_file = f"orcamento_{orc['id']}.pdf"
            assets_pdf_path = os.path.join(assets_dir, pdf_file)

            if not os.path.exists(assets_pdf_path):
                self.page.snack_bar = SnackBar(
                    Text("PDF não encontrado para este orçamento.")
                )
                self.page.snack_bar.open = True
                self.page.update()
                return

            if webview_available:
                # Exibe o PDF em um modal WebView (quando suportado) usando file://
                url = f"file://{assets_pdf_path}"
                dialog = AlertDialog(
                    modal=True,
                    title=Text(f"Visualizar Orçamento #{orc['id']}"),
                    content=WebView(src=url, width=800, height=600),
                    actions=[
                        Button(
                            "Fechar",
                            on_click=lambda e: self.page.dialog.__setattr__(
                                "open", False
                            ),
                        )
                    ],
                )
                self.page.dialog = dialog
                dialog.open = True
                self.page.update()
            else:
                # Fallback: abre o PDF externamente no visualizador do sistema
                try:
                    if platform.system() == "Windows":
                        os.startfile(assets_pdf_path)
                    else:
                        webbrowser.open(f"file://{assets_pdf_path}")
                except Exception as err:
                    print(f"Erro ao abrir PDF externamente: {err}")
                    self.page.snack_bar = SnackBar(
                        Text("Não foi possível abrir o PDF.")
                    )
                    self.page.snack_bar.open = True
                    self.page.update()

        return ft.Container(
            padding=10,
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        str(orcamento["id"]),
                        width=50,
                        expand=0,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        str(orcamento.get("cliente", "")).upper(),
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        orcamento["data"],
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        itens_str.upper(),
                        expand=3,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        f"R$ {orcamento['total_sem_desconto']:.2f}",
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        f"R$ {orcamento['total_com_desconto']:.2f}",
                        expand=2,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                on_click=lambda e, o=orcamento: self.abrir_modal_editar(
                                    o
                                ),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.PICTURE_AS_PDF,
                                icon_color=ft.Colors.BLUE,
                                tooltip="Abrir PDF",
                                on_click=abrir_pdf,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED,
                                on_click=lambda e, o=orcamento: self.excluir_orcamento(
                                    o
                                ),
                            ),
                        ],
                        expand=2,
                    ),
                ]
            ),
        )

    def atualizar(self, orcamentos):
        self.lista_orcamentos.controls.clear()
        if not orcamentos:
            self.lista_orcamentos.controls.append(self.mensagem_vazia)
        else:
            for idx, orcamento in enumerate(orcamentos):
                self.lista_orcamentos.controls.append(
                    self._linha_orcamento(orcamento, idx)
                )
        self.page.update()

    def _excluir_pdf(self, pdf_file):
        import os

        pdf_dir = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "orçamentos"
        )
        file_path = os.path.join(pdf_dir, pdf_file)
        if os.path.exists(file_path):
            os.remove(file_path)
        self.atualizar([])
