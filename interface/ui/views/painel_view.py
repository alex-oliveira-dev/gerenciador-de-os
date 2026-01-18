import flet as ft


class PainelView:
    def __init__(self, page, tabela_carros_manutencao):
        self.page = page
        self.tabela_carros_manutencao = tabela_carros_manutencao
        self.layout = ft.Container(
            padding=20,
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text(
                        "Painel de Carros em Manutenção",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700,
                    ),
                    ft.Divider(height=2, color=ft.Colors.BLUE_100),
                    ft.Text(
                        "Acompanhe os veículos em manutenção e alertas de estoque.",
                        size=15,
                        color=ft.Colors.GREY_700,
                    ),
                    self.tabela_carros_manutencao.layout,
                ],
            ),
        )
