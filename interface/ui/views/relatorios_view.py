import flet as ft
from backend.services.relatorio_service import relatorio_service


class RelatoriosView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.area_resultado = ft.Column(expand=True, spacing=8)

        self.btn_financeiro = ft.Button(
            "Relatório Financeiro", on_click=self.gerar_financeiro
        )
        self.btn_estoque = ft.Button(
            "Relatório de Estoque", on_click=self.gerar_estoque
        )
        self.btn_vendas = ft.Button(
            "Vendas por Produto", on_click=self.gerar_vendas_produto
        )

        self.layout = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.ElevatedButton(
                        "Relatório Financeiro",
                        icon=ft.Icons.ATTACH_MONEY,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=self.gerar_financeiro,
                    ),
                    ft.ElevatedButton(
                        "Relatório de Estoque",
                        icon=ft.Icons.INVENTORY,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=self.gerar_estoque,
                    ),
                    ft.ElevatedButton(
                        "Vendas por Produto",
                        icon=ft.Icons.BAR_CHART,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=self.gerar_vendas_produto,
                    ),
                ], spacing=12),
                ft.Divider(),
                ft.Text("Resultados:", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ft.Container(expand=True, content=self.area_resultado),
            ],
            expand=True,
            spacing=10,
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        padding=24,
        )

    def _limpar_area(self):
        self.area_resultado.controls.clear()

    def _barra_horizontal(
        self, label: str, value: float, max_value: float, color=ft.Colors.BLUE_400
    ):
        max_px = 400
        width = int((value / max_value) * max_px) if max_value > 0 else 0
        return ft.Row(
            [
                ft.Text(label, width=160),
                ft.Container(
                    width=max_px,
                    height=18,
                    bgcolor=ft.Colors.GREY_200,
                    padding=2,
                    content=ft.Row(
                        [ft.Container(width=width, height=14, bgcolor=color)]
                    ),
                ),
                ft.Text(f"{value:.2f}", width=80, text_align=ft.TextAlign.RIGHT),
            ],
            alignment=ft.MainAxisAlignment.START,
        )

    def gerar_financeiro(self, e=None):
        rel = relatorio_service.gerar_relatorio_financeiro()
        self._limpar_area()
        totals = ft.Row(
            [
                ft.Column(
                    [
                        ft.Text("Total Entradas", weight=ft.FontWeight.BOLD),
                        ft.Text(f"R$ {rel.get('total_entradas', 0.0):.2f}"),
                    ],
                    alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text("Total Saídas", weight=ft.FontWeight.BOLD),
                        ft.Text(f"R$ {rel.get('total_saidas', 0.0):.2f}"),
                    ],
                    alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.Text("Saldo", weight=ft.FontWeight.BOLD),
                        ft.Text(f"R$ {rel.get('saldo', 0.0):.2f}"),
                    ],
                    alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            spacing=40,
        )
        self.area_resultado.controls.append(totals)
        self.area_resultado.controls.append(ft.Divider())

        por_data = rel.get("por_data", {})
        if por_data:
            max_val = (
                max(
                    (v.get("entradas", 0) + v.get("saidas", 0))
                    for v in por_data.values()
                )
                or 1
            )
            self.area_resultado.controls.append(
                ft.Text("Fluxo por Data", weight=ft.FontWeight.BOLD)
            )
            for date, v in sorted(por_data.items()):
                entradas = v.get("entradas", 0)
                saidas = v.get("saidas", 0)
                row = ft.Row(
                    [
                        ft.Text(date, width=100),
                        ft.Container(
                            width=420,
                            height=18,
                            bgcolor=ft.Colors.GREY_200,
                            padding=2,
                            content=ft.Row(
                                [
                                    ft.Container(
                                        width=int((entradas / max_val) * 400),
                                        height=14,
                                        bgcolor=ft.Colors.GREEN_400,
                                    ),
                                    ft.Container(
                                        width=int((saidas / max_val) * 400),
                                        height=14,
                                        bgcolor=ft.Colors.RED_400,
                                    ),
                                ]
                            ),
                        ),
                        ft.Text(f"E: R$ {entradas:.2f}  S: R$ {saidas:.2f}", width=160),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                )
                self.area_resultado.controls.append(row)

        self.page.update()

    def gerar_estoque(self, e=None):
        rel = relatorio_service.gerar_relatorio_estoque()
        self._limpar_area()
        self.area_resultado.controls.append(
            ft.Text(
                f"Total de produtos: {rel.get('total_produtos', 0)}",
                weight=ft.FontWeight.BOLD,
            )
        )
        self.area_resultado.controls.append(ft.Divider())

        baixo = rel.get("baixo_estoque", [])
        if baixo:
            cols = [
                ft.DataColumn(ft.Text("Produto")),
                ft.DataColumn(ft.Text("Quantidade")),
            ]
            rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.get("nome"))),
                        ft.DataCell(ft.Text(str(p.get("quantidade")))),
                    ]
                )
                for p in baixo
            ]
            table = ft.DataTable(columns=cols, rows=rows)
            self.area_resultado.controls.append(table)
        else:
            self.area_resultado.controls.append(
                ft.Text("Nenhum produto com baixo estoque")
            )

        self.page.update()

    def gerar_vendas_produto(self, e=None):
        rel = relatorio_service.gerar_relatorio_vendas_por_produto()
        self._limpar_area()
        vendas = rel.get("vendas_por_produto", {})
        if not vendas:
            self.area_resultado.controls.append(ft.Text("Nenhuma venda registrada."))
            self.page.update()
            return

        items = [
            (k, v.get("quantidade", 0), v.get("valor", 0.0)) for k, v in vendas.items()
        ]
        items.sort(key=lambda x: x[2], reverse=True)

        cols = [
            ft.DataColumn(ft.Text("Produto")),
            ft.DataColumn(ft.Text("Qtd")),
            ft.DataColumn(ft.Text("Valor")),
        ]
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(k)),
                    ft.DataCell(ft.Text(str(q))),
                    ft.DataCell(ft.Text(f"R$ {val:.2f}")),
                ]
            )
            for k, q, val in items
        ]
        table = ft.DataTable(columns=cols, rows=rows)
        self.area_resultado.controls.append(table)
        self.area_resultado.controls.append(ft.Divider())

        max_val = max((val for _, _, val in items), default=1.0)
        for k, q, val in items[:10]:
            self.area_resultado.controls.append(
                self._barra_horizontal(k, val, max_val, color=ft.Colors.BLUE_400)
            )

        self.page.update()
