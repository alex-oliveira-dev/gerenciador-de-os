import flet as ft
from backend.services.relatorio_service import relatorio_service


class RelatoriosView:
    def __init__(self, page: ft.Page):
        self.page = page
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

    def gerar_financeiro(self, e=None):
        rel = relatorio_service.gerar_relatorio_financeiro()
        self._limpar_area()
        # Adicione aqui o conteúdo estilizado do relatório financeiro

    def gerar_estoque(self, e=None):
        rel = relatorio_service.gerar_relatorio_estoque()
        self._limpar_area()
        # Adicione aqui o conteúdo estilizado do relatório de estoque

    def gerar_vendas_produto(self, e=None):
        rel = relatorio_service.gerar_relatorio_vendas_por_produto()
        self._limpar_area()
        # Adicione aqui o conteúdo estilizado do relatório de vendas por produto

    def gerar_financeiro(self, e=None):
        rel = relatorio_service.gerar_relatorio_financeiro()
        self._limpar_area()

        # Cabeçalho do relatório
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ATTACH_MONEY, size=28, color=ft.Colors.GREEN_700
                        ),
                        ft.Text(
                            "Relatório Financeiro",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.only(bottom=15),
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
        self.area_resultado.controls.append(totals)
        self.area_resultado.controls.append(
            ft.Container(
                height=20,
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ATTACH_MONEY, size=28, color=ft.Colors.GREEN_700
                        ),
                        ft.Text(
                            "Relatório Financeiro",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.only(bottom=15),
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
        self.area_resultado.controls.append(totals)


    def gerar_financeiro(self, e=None):
        rel = relatorio_service.gerar_relatorio_financeiro()
        self._limpar_area()

        # Cabeçalho do relatório
        self.area_resultado.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ATTACH_MONEY, size=28, color=ft.Colors.GREEN_700
                        ),
                        ft.Text(
                            "Relatório Financeiro",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_900,
                        ),
                    ],
                    spacing=10,
                ),
                padding=ft.padding.only(bottom=15),
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
            # ...adicione aqui o layout desejado para cada linha de data...
            self.area_resultado.controls.append(row)

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
