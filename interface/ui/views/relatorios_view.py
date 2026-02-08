import flet as ft
from backend.services.relatorio_service import relatorio_service


class RelatoriosView:
        
    
    def __init__(self, page: ft.Page):
        
        self.area_resultado = ft.Column(
            expand=True, spacing=16, scroll=ft.ScrollMode.AUTO
        )
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.ANALYTICS,
                                    size=32,
                                    color=ft.Colors.BLUE_700,
                                ),
                                ft.Text(
                                    "Relatórios e Análises",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_900,
                                ),
                            ],
                            spacing=12,
                        ),
                        padding=ft.padding.only(bottom=20),
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.Icons.ATTACH_MONEY, size=32),
                                                ft.Text(
                                                    "Relatório Financeiro",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                            spacing=8,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        bgcolor=ft.Colors.GREEN_600,
                                        color=ft.Colors.WHITE,
                                        on_click=self.gerar_financeiro,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                            padding=20,
                                        ),
                                        height=110,
                                        width=200,
                                    ),
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=8,
                                        color=ft.Colors.with_opacity(
                                            0.3, ft.Colors.GREEN_600
                                        ),
                                        offset=ft.Offset(0, 4),
                                    ),
                                ),
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.Icons.INVENTORY, size=32),
                                                ft.Text(
                                                    "Relatório de Estoque",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                            spacing=8,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        bgcolor=ft.Colors.ORANGE_600,
                                        color=ft.Colors.WHITE,
                                        on_click=self.gerar_estoque,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                            padding=20,
                                        ),
                                        height=110,
                                        width=200,
                                    ),
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=8,
                                        color=ft.Colors.with_opacity(
                                            0.3, ft.Colors.ORANGE_600
                                        ),
                                        offset=ft.Offset(0, 4),
                                    ),
                                ),
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.Icons.BAR_CHART, size=32),
                                                ft.Text(
                                                    "Vendas por Produto",
                                                    size=13,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                            spacing=8,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        ),
                                        bgcolor=ft.Colors.BLUE_600,
                                        color=ft.Colors.WHITE,
                                        on_click=self.gerar_vendas_produto,
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=12),
                                            padding=20,
                                        ),
                                        height=110,
                                        width=200,
                                    ),
                                    shadow=ft.BoxShadow(
                                        spread_radius=1,
                                        blur_radius=8,
                                        color=ft.Colors.with_opacity(
                                            0.3, ft.Colors.BLUE_600
                                        ),
                                        offset=ft.Offset(0, 4),
                                    ),
                                ),
                            ],
                            spacing=20,
                            wrap=True,
                        ),
                        padding=ft.padding.only(bottom=20),
                    ),
                    ft.Divider(height=2, color=ft.Colors.BLUE_200),
                    ft.Container(
                        expand=True,
                        content=self.area_resultado,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=12,
                        padding=20,
                        border=ft.border.all(1, ft.Colors.BLUE_100),
                    ),
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


    def gerar_vendas_produto(self, e=None):
        rel = relatorio_service.gerar_relatorio_vendas_por_produto()
        self._limpar_area()
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.BAR_CHART, size=28, color=ft.Colors.BLUE_700),
                    ft.Text("Vendas por Produto", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ], spacing=10),
                padding=ft.padding.only(bottom=15),
            )
        )
        vendas = rel.get("vendas_por_produto", {})
        top_vendas = sorted(vendas.items(), key=lambda x: x[1]["quantidade"], reverse=True)[:10]
        if top_vendas:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Produto", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Quantidade Vendida", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Valor Total", weight=ft.FontWeight.BOLD)),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(prod)),
                                ft.DataCell(ft.Text(str(dados["quantidade"]))),
                                ft.DataCell(ft.Text(f"R$ {dados['valor']:.2f}")),
                            ]) for prod, dados in top_vendas
                        ],
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        heading_row_color=ft.Colors.BLUE_50,
                        data_row_color=ft.Colors.WHITE,
                    ),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=12,
                    padding=24,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                )
            )
        else:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.GREY_600),
                        ft.Text("Nenhuma venda registrada.", color=ft.Colors.GREY_700, size=16),
                    ], spacing=8),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=12,
                    padding=24,
                )
            )

    def gerar_financeiro(self, e=None, periodo=None):
        rel = relatorio_service.gerar_relatorio_financeiro(periodo=periodo)
        self._limpar_area()
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ATTACH_MONEY, size=28, color=ft.Colors.GREEN_700),
                    ft.Text("Relatório Financeiro", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900),
                ], spacing=10),
                padding=ft.padding.only(bottom=15),
            )
        )
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Text("Filtrar por período:", size=14, weight=ft.FontWeight.W_500),
                    ft.TextField(hint_text="AAAA-MM", width=120, on_change=lambda e: self.gerar_financeiro(periodo=e.control.value)),
                ], spacing=10),
                padding=ft.padding.only(bottom=10),
            )
        )
        totals = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ARROW_CIRCLE_UP, size=40, color=ft.Colors.GREEN_400),
                    ft.Text("Total Entradas", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREEN_900),
                    ft.Text(f"R$ {rel.get('total_entradas', 0.0):.2f}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                bgcolor=ft.Colors.GREEN_50, border_radius=12, padding=20, width=220,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ARROW_CIRCLE_DOWN, size=40, color=ft.Colors.RED_400),
                    ft.Text("Total Saídas", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.RED_900),
                    ft.Text(f"R$ {rel.get('total_saidas', 0.0):.2f}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                bgcolor=ft.Colors.RED_50, border_radius=12, padding=20, width=220,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=40, color=ft.Colors.BLUE_400),
                    ft.Text("Saldo", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_900),
                    ft.Text(f"R$ {rel.get('saldo', 0.0):.2f}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                bgcolor=ft.Colors.BLUE_50, border_radius=12, padding=20, width=220,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            ),
        ], spacing=20, wrap=True)
        self.area_resultado.controls.append(totals)
        ganhos_mes = rel.get("ganhos_por_mes", {})
        meses = sorted(ganhos_mes.keys())
        if meses:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Mês", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Ganhos", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Diferença para mês anterior", weight=ft.FontWeight.BOLD)),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(m)),
                                ft.DataCell(ft.Text(f"R$ {ganhos_mes[m]:.2f}")),
                                ft.DataCell(ft.Text(f"R$ {ganhos_mes[m] - ganhos_mes.get(meses[i-1], 0):.2f}" if i > 0 else "-")),
                            ]) for i, m in enumerate(meses)
                        ],
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        heading_row_color=ft.Colors.GREEN_50,
                        data_row_color=ft.Colors.WHITE,
                    ),
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=12,
                    padding=24,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                )
            )
        else:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.GREY_600),
                        ft.Text("Sem dados financeiros para o período.", color=ft.Colors.GREY_700, size=16),
                    ], spacing=8),
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=12,
                    padding=24,
                )
            )
        por_data = rel.get("por_data", {})
        if por_data:
            for date, v in sorted(por_data.items()):
                entradas = v.get("entradas", 0)
                saidas = v.get("saidas", 0)
                self.area_resultado.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text(f"Data: {date}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                            ft.Text(f"Entradas: R$ {entradas:.2f}", size=14, color=ft.Colors.GREEN_700),
                            ft.Text(f"Saídas: R$ {saidas:.2f}", size=14, color=ft.Colors.RED_700),
                        ], spacing=16),
                        padding=ft.padding.only(bottom=6),
                    )
                )
        else:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.GREY_600),
                        ft.Text("Sem lançamentos financeiros no período.", color=ft.Colors.GREY_700, size=16),
                    ], spacing=8),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=12,
                    padding=24,
                )
            )
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Saldo atual: R$ {rel.get('saldo', 0.0):.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Text(f"Total de entradas: R$ {rel.get('total_entradas', 0.0):.2f}", size=16, color=ft.Colors.GREEN_700),
                    ft.Text(f"Total de saídas: R$ {rel.get('total_saidas', 0.0):.2f}", size=16, color=ft.Colors.RED_700),
                ], spacing=8),
                bgcolor=ft.Colors.BLUE_50,
                border_radius=12,
                padding=24,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            )
        )

    def gerar_estoque(self, e=None):
        rel = relatorio_service.gerar_relatorio_estoque()
        self._limpar_area()
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INVENTORY, size=28, color=ft.Colors.ORANGE_700),
                    ft.Text("Relatório de Estoque", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_900),
                ], spacing=10),
                padding=ft.padding.only(bottom=15),
            )
        )
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"Total de Produtos: {rel.get('total_produtos', 0)}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                    ft.Text("Produtos com baixo estoque:", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.RED_700),
                    ft.DataTable(
                        columns=[
                            ft.DataColumn(ft.Text("Produto", weight=ft.FontWeight.BOLD)),
                            ft.DataColumn(ft.Text("Quantidade", weight=ft.FontWeight.BOLD)),
                        ],
                        rows=[
                            ft.DataRow(cells=[
                                ft.DataCell(ft.Text(p.get("nome", ""))),
                                ft.DataCell(ft.Text(str(p.get("quantidade", 0)))),
                            ]) for p in rel.get("baixo_estoque", [])
                        ],
                        border=ft.border.all(1, ft.Colors.GREY_200),
                        heading_row_color=ft.Colors.ORANGE_50,
                        data_row_color=ft.Colors.WHITE,
                    ) if rel.get("baixo_estoque") else ft.Text("Nenhum produto com baixo estoque.", color=ft.Colors.GREEN_700)
                ], spacing=12),
                bgcolor=ft.Colors.ORANGE_50,
                border_radius=12,
                padding=24,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
            )
        )

        # Cards de totais estilizados
        totals = ft.Row(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.ARROW_CIRCLE_UP,
                                size=40,
                                color=ft.Colors.GREEN_400,
                            ),
                            ft.Text(
                                "Total Entradas",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.GREEN_900,
                            ),
                            ft.Text(
                                f"R$ {rel.get('total_entradas', 0.0):.2f}",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=12,
                    padding=20,
                    width=220,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.ARROW_CIRCLE_DOWN,
                                size=40,
                                color=ft.Colors.RED_400,
                            ),
                            ft.Text(
                                "Total Saídas",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.RED_900,
                            ),
                            ft.Text(
                                f"R$ {rel.get('total_saidas', 0.0):.2f}",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.RED_700,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.RED_50,
                    border_radius=12,
                    padding=20,
                    width=220,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.ACCOUNT_BALANCE_WALLET,
                                size=40,
                                color=ft.Colors.BLUE_400,
                            ),
                            ft.Text(
                                "Saldo",
                                size=14,
                                weight=ft.FontWeight.W_500,
                                color=ft.Colors.BLUE_900,
                            ),
                            ft.Text(
                                f"R$ {rel.get('saldo', 0.0):.2f}",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=12,
                    padding=20,
                    width=220,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=4,
                        color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                    ),
                ),
            ],
            spacing=20,
            wrap=True,
        )

        # Exemplo de uso de por_data
        por_data = rel.get("por_data", {})
        for date, v in sorted(por_data.items()):
            entradas = v.get("entradas", 0)
            saidas = v.get("saidas", 0)
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"Data: {date}", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                        ft.Text(f"Entradas: R$ {entradas:.2f}", size=14, color=ft.Colors.GREEN_700),
                        ft.Text(f"Saídas: R$ {saidas:.2f}", size=14, color=ft.Colors.RED_700),
                    ], spacing=16),
                    padding=ft.padding.only(bottom=6),
                )
            )

        # Card de total de produtos
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.SHOPPING_BAG, size=48, color=ft.Colors.ORANGE_400
                        ),
                        ft.Column(
                            [
                                ft.Text(
                                    "Total de Produtos",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=ft.Colors.GREY_700,
                                ),
                                ft.Text(
                                    str(rel.get("total_produtos", 0)),
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.ORANGE_700,
                                ),
                            ],
                            spacing=4,
                        ),
                    ],
                    spacing=20,
                ),
                bgcolor=ft.Colors.ORANGE_50,
                border_radius=12,
                padding=24,
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=4,
                    color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                ),
            )
        )
