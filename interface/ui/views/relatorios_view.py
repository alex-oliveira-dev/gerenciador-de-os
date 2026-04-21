import flet as ft
from backend.services.relatorio_service import relatorio_service


class RelatoriosView:
        
    
    def __init__(self, page: ft.Page):
        self.page = page
        
        self.area_resultado = ft.Column(
            expand=True, spacing=16, scroll=ft.ScrollMode.AUTO
        )
        # filtros
        self.filter_type_dropdown = ft.Dropdown(
            label="Tipo de Relatório",
            options=[
                # ft.dropdown.Option("Todos"),  pode voltar em uma atualização de filtros mais completa, mas por ora deixa só os tipos específicos
                ft.dropdown.Option("Financeiro"),
                ft.dropdown.Option("Estoque"),
                ft.dropdown.Option("Vendas por Produto"),
            ],
            width=220,
            menu_height=200,
            value="Financeiro",
        )
        self.filter_period_field = ft.TextField(
            label="Período (AAAA-MM)", width=140, hint_text="Opcional"
        )
        self.filter_product_field = ft.TextField(
            label="Produto (filtro)", width=220, hint_text="Opcional",
            disabled=True,
        )
        self.btn_aplicar_filtro = ft.ElevatedButton("Aplicar filtro", on_click=self.aplicar_filtros)
        self.btn_limpar_filtro = ft.OutlinedButton("Limpar filtro", on_click=self.limpar_filtros)
        self.filter_type_dropdown.on_change = self._on_filter_type_change
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

                                # ft.Container(
                                #     content=ft.Row(
                                #         [
                                #             ft.Container(
                                #                 content=ft.ElevatedButton(
                                #                     content=ft.Column(
                                #                         [   
                                #                             ft.Row(
                                #                                 [
                                #                                     ft.Icon(ft.Icons.ATTACH_MONEY, size=32),
                                #                                     ft.Text(
                                #                                     "Relatório Financeiro",
                                #                                     size=16,
                                #                                     weight=ft.FontWeight.BOLD,
                                #                                     ),
                                #                                 ]
                                #                             )
                                                            
                                #                         ],
                                #                         spacing=8,
                                #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                #                     ),
                                #                     bgcolor=ft.Colors.GREEN_600,
                                #                     color=ft.Colors.WHITE,
                                #                     on_click=self.gerar_financeiro,
                                #                     style=ft.ButtonStyle(
                                #                         shape=ft.RoundedRectangleBorder(radius=12),
                                #                         padding=20,
                                #                     ),
                                #                     height=55,
                                #                     width=250,
                                #                 ),
                                #                 shadow=ft.BoxShadow(
                                #                     spread_radius=1,
                                #                     blur_radius=8,
                                #                     color=ft.Colors.with_opacity(
                                #                         0.3, ft.Colors.GREEN_600
                                #                     ),
                                #                     offset=ft.Offset(0, 4),
                                #                 ),
                                #             ),
                                #             ft.Container(
                                #                 content=ft.ElevatedButton(
                                #                     content=ft.Column(
                                #                         [   
                                #                             ft.Row(
                                #                                 [
                                #                                     ft.Icon(ft.Icons.INVENTORY, size=32),
                                #                                     ft.Text(
                                #                                         "Relatório de Estoque",
                                #                                         size=16,
                                #                                         weight=ft.FontWeight.BOLD,
                                #                                     ),
                                #                                 ]
                                #                             )
                                #                         ],
                                #                         spacing=8,
                                #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                #                     ),
                                #                     bgcolor=ft.Colors.ORANGE_600,
                                #                     color=ft.Colors.WHITE,
                                #                     on_click=self.gerar_estoque,
                                #                     style=ft.ButtonStyle(
                                #                         shape=ft.RoundedRectangleBorder(radius=12),
                                #                         padding=20,
                                #                     ),
                                #                     height=55,
                                #                     width=250,
                                #                 ),
                                #                 shadow=ft.BoxShadow(
                                #                     spread_radius=1,
                                #                     blur_radius=8,
                                #                     color=ft.Colors.with_opacity(
                                #                         0.3, ft.Colors.ORANGE_600
                                #                     ),
                                #                     offset=ft.Offset(0, 4),
                                #                 ),
                                #             ),
                                #             ft.Container(
                                #                 content=ft.ElevatedButton(
                                #                     content=ft.Column(
                                #                         [   
                                #                             ft.Row(
                                #                                 [
                                #                                     ft.Icon(ft.Icons.BAR_CHART, size=32),
                                #                                     ft.Text(
                                #                                         "Vendas por Produto",
                                #                                         size=16,
                                #                                         weight=ft.FontWeight.BOLD,
                                #                                     ),
                                #                                 ])
                                                            
                                #                         ],
                                #                         spacing=8,
                                #                         horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                #                     ),
                                #                     bgcolor=ft.Colors.BLUE_600,
                                #                     color=ft.Colors.WHITE,
                                #                     on_click=self.gerar_vendas_produto,
                                #                     style=ft.ButtonStyle(
                                #                         shape=ft.RoundedRectangleBorder(radius=12),
                                #                         padding=20,
                                #                     ),
                                #                     height=55,
                                #                     width=250,
                                #                 ),
                                #                 shadow=ft.BoxShadow(
                                #                     spread_radius=1,
                                #                     blur_radius=8,
                                #                     color=ft.Colors.with_opacity(
                                #                         0.3, ft.Colors.BLUE_600
                                #                     ),
                                #                     offset=ft.Offset(0, 4),
                                #                 ),
                                #             ),
                                #         ],
                                #         spacing=20,
                                #         wrap=True,
                                #     ),
                                #     padding=ft.padding.only(bottom=20),
                                # ),
                            ],
                            spacing=12,
                        ),
                        padding=ft.padding.only(bottom=20),
                    ),
                    
                    ft.Container(
                        content=ft.Row([
                            self.filter_type_dropdown,
                            self.filter_period_field,
                            self.filter_product_field,
                            self.btn_aplicar_filtro,
                            self.btn_limpar_filtro,
                        ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=ft.padding.only(bottom=12),
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

    def _on_filter_type_change(self, e=None):
        # Habilita campo produto apenas para filtro de vendas
        try:
            self.filter_product_field.disabled = (
                self.filter_type_dropdown.value != "Vendas por Produto"
            )
        except Exception:
            pass
        self.page.update()

    def aplicar_filtros(self, e=None):
        tipo = (self.filter_type_dropdown.value or "Todos")
        periodo = (self.filter_period_field.value or "").strip() or None
        produto = (self.filter_product_field.value or "").strip() or None
        if tipo == "Todos":
            # mostra todos os tipos: financeiro, estoque e vendas (resumidos)
            self.gerar_financeiro(periodo=periodo)
            # acrescenta estoque e vendas abaixo
            self.gerar_estoque()
            self.gerar_vendas_produto(produto_filtro=produto)
            return
        if tipo == "Financeiro":
            self.gerar_financeiro(periodo=periodo)
            return
        if tipo == "Estoque":
            self.gerar_estoque()
            return
        if tipo == "Vendas por Produto":
            self.gerar_vendas_produto(produto_filtro=produto)

    def limpar_filtros(self, e=None):
        self.filter_type_dropdown.value = "Todos"
        self.filter_period_field.value = ""
        self.filter_product_field.value = ""
        self.filter_product_field.disabled = True
        self._limpar_area()
        self.page.update()


    def gerar_vendas_produto(self, e=None, produto_filtro: str = None):
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
        # aplica filtro por nome de produto se fornecido
        if produto_filtro:
            filtro = produto_filtro.strip().lower()
            vendas = {p: d for p, d in vendas.items() if filtro in (p or "").lower()}
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
        # antigo filtro de período removido (agora usamos o painel de filtros acima)
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

        # Cards de resumo
        self.area_resultado.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SHOPPING_BAG, size=40, color=ft.Colors.ORANGE_400),
                        ft.Text("Total de Produtos", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.ORANGE_900),
                        ft.Text(str(rel.get("total_produtos", 0)), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_700),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    bgcolor=ft.Colors.ORANGE_50, border_radius=12, padding=20, width=220,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ATTACH_MONEY, size=40, color=ft.Colors.GREEN_400),
                        ft.Text("Valor Total em Estoque", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.GREEN_900),
                        ft.Text(f"R$ {rel.get('total_valor_estoque', 0.0):.2f}", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    bgcolor=ft.Colors.GREEN_50, border_radius=12, padding=20, width=220,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.WARNING_AMBER, size=40, color=ft.Colors.RED_400),
                        ft.Text("Produtos com Baixo Estoque", size=14, weight=ft.FontWeight.W_500, color=ft.Colors.RED_900),
                        ft.Text(str(len(rel.get("baixo_estoque", []))), size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    bgcolor=ft.Colors.RED_50, border_radius=12, padding=20, width=220,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                ),
            ], spacing=20, wrap=True)
        )

        # Tabela com todos os produtos
        todos = rel.get("todos_produtos", [])
        if todos:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("Todos os Produtos", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.ORANGE_900),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Nome", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Qtd", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Preço Custo", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Preço Venda", weight=ft.FontWeight.BOLD)),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(p.get("nome", ""))),
                                        ft.DataCell(ft.Text(str(p.get("quantidade", 0)), color=ft.Colors.RED_700 if int(p.get("quantidade") or 0) <= 5 else ft.Colors.BLACK)),
                                        ft.DataCell(ft.Text(f"R$ {float(p.get('preco_custo') or 0):.2f}")),
                                        ft.DataCell(ft.Text(f"R$ {float(p.get('preco_venda') or 0):.2f}")),
                                    ]
                                )
                                for p in todos
                            ],
                            border=ft.border.all(1, ft.Colors.GREY_200),
                            heading_row_color=ft.Colors.ORANGE_50,
                            data_row_color=ft.Colors.WHITE,
                        ),
                    ], spacing=10),
                    bgcolor=ft.Colors.ORANGE_50,
                    border_radius=12,
                    padding=24,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                )
            )

        # Alerta de baixo estoque
        baixo = rel.get("baixo_estoque", [])
        if baixo:
            self.area_resultado.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.WARNING_AMBER, color=ft.Colors.RED_700),
                            ft.Text("Produtos com Estoque Baixo (≤ 5 unidades)", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_700),
                        ], spacing=8),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Produto", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Quantidade", weight=ft.FontWeight.BOLD)),
                            ],
                            rows=[
                                ft.DataRow(cells=[
                                    ft.DataCell(ft.Text(p.get("nome", ""), color=ft.Colors.RED_700)),
                                    ft.DataCell(ft.Text(str(p.get("quantidade", 0)), color=ft.Colors.RED_700)),
                                ])
                                for p in baixo
                            ],
                            border=ft.border.all(1, ft.Colors.RED_200),
                            heading_row_color=ft.Colors.RED_50,
                            data_row_color=ft.Colors.WHITE,
                        ),
                    ], spacing=10),
                    bgcolor=ft.Colors.RED_50,
                    border_radius=12,
                    padding=24,
                    shadow=ft.BoxShadow(spread_radius=1, blur_radius=4, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK)),
                )
            )
