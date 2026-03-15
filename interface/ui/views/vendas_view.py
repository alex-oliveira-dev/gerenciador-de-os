
import flet as ft
from backend.services.venda_service import VendaService
from backend.services.vendas_dropdown_service import VendasDropdownService
from backend.utils.pdf_generator import gerar_pdf_venda
from interface.components.alertaSnack import alertSnackBarMensage
import datetime
import sqlite3
import threading


class VendasView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.venda_service = VendaService()
        self.dropdown_service = VendasDropdownService()
        self.cliente_dropdown = ft.Dropdown(
            label="Cliente",
            width=300,
            options=[],
        )
        self.produto_dropdown = ft.Dropdown(
            label="Produto",
            width=200,
            options=[],
        )
        self.quantidade_input = ft.TextField(label="Quantidade", width=100, value="1")
        self.adicionar_btn = ft.ElevatedButton(
            "Adicionar Item",
            icon=ft.Icons.ADD_SHOPPING_CART,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            on_click=self.adicionar_item,
        )
        # guarda dados para a tabela de itens
        self.itens = []
        self.itens_tabela_itens = []
        self.tabela_itens = (
            ft.Container(
                ft.Row(
                    ft.Column(
                        ft.Text(
                            "Produto",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        )
                    ),
                    ft.Column(
                        ft.Text(
                            "Quantidade",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        )
                    ),
                    ft.Column(
                        ft.Text(
                            "Valor Unitário",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        )
                    ),
                    ft.Column(
                        ft.Text(
                            "Valor Total",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        )
                    ),
                    ft.Column(
                        ft.Text(
                            "Ações",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREY_800,
                        )
                    ),
                    # Removido container intermediário, DataTable será usado diretamente no layout
                ),
                ft.Row(
                    self.itens,
                    scroll=ft.ScrollMode.ALWAYS,
                ),
                border=ft.border.all(1, ft.Colors.BLUE_100),
                border_radius=8,
                width=200,
            ),
        )
        self.forma_pagamento_dropdown = ft.Dropdown(
            label="Forma de Pagamento",
            width=200,
            options=[
                ft.dropdown.Option("Dinheiro"),
                ft.dropdown.Option("Cartão de Crédito"),
                ft.dropdown.Option("Cartão de Débito"),
                ft.dropdown.Option("Pix"),
                ft.dropdown.Option("Boleto"),
            ],
        )
        # Removido container intermediário, DataTable será usado diretamente no layout
        self.total_text = ft.Text(
            "Total: R$ 0,00",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_700,
        )
        self.finalizar_btn = ft.ElevatedButton(
            "Finalizar Venda",
            icon=ft.Icons.POINT_OF_SALE,
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            on_click=self.finalizar_venda,
        )
         # TABELA DE ITENS A VENDA (CARRINHO)
        self.itens_venda_tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Produto", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Quantidade", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor Unitário", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor Total", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),
            ],
            rows=self.itens_tabela_itens,
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=8,
            heading_row_color=ft.Colors.BLUE_50,
            data_row_color=ft.Colors.WHITE,
            column_spacing=24,
            width = 1280,
        )
         # TABELA DE HISTORICO DE VENDAS 
        self.historico_tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Cliente", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Forma de Pagamento", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Total de Itens", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor Unitário", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Valor Total", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ações", weight=ft.FontWeight.BOLD)),

                
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_200),
            border_radius=8,
            heading_row_color=ft.Colors.BLUE_50,
            data_row_color=ft.Colors.WHITE,
            column_spacing=24,
            width = 1280,
        )
        
        self.tabela_itens_title = ft.Text(
            "Itens da Venda",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700,
        )
        
        self.layout = ft.Container(
            bgcolor=ft.Colors.GREY_100,
            padding=ft.padding.all(32),
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Text(
                            "Área de Vendas",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_900,
                        ),
                        padding=ft.padding.symmetric(vertical=12),
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Container(
                        content=ft.Row(
                            [
                                self.cliente_dropdown,
                                self.produto_dropdown,
                                self.quantidade_input,
                                self.adicionar_btn,
                            ],
                            spacing=24,
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.12, ft.Colors.BLUE_900),
                            offset=ft.Offset(0, 4),
                        ),
                        padding=ft.padding.all(16),
                        margin=ft.margin.only(bottom=16),
                    ),
                    self.tabela_itens_title,
                    self.itens_venda_tabela,
                    ft.Row(
                        [
                            ft.Container(
                                self.total_text,
                                expand=2,
                                padding=ft.padding.all(8),
                            ),
                            ft.Container(
                                self.forma_pagamento_dropdown,
                                expand=1,
                                padding=ft.padding.all(8),
                            ),
                            ft.Container(
                                self.finalizar_btn,
                                expand=1,
                                padding=ft.padding.all(8),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=24,
                    ),
                    ft.Divider(height=32, color=ft.Colors.BLUE_100),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Histórico de Vendas",
                                    size=24,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_700,
                                ),
                                self.historico_tabela,
                            ],
                            spacing=12,
                        ),
                        bgcolor=ft.Colors.WHITE,
                        border_radius=12,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=8,
                            color=ft.Colors.with_opacity(0.10, ft.Colors.BLUE_700),
                            offset=ft.Offset(0, 2),
                        ),
                        padding=ft.padding.all(20),
                        margin=ft.margin.only(top=24),
                    ),
                ],
                expand=True,
                spacing=20,
                scroll=ft.ScrollMode.AUTO,
            ),
        )
        # Atualiza histórico em background (usa API do page quando disponível)
        try:
            page.run_thread(self.atualizar_historico_vendas)
        except Exception:
            threading.Thread(target=self.atualizar_historico_vendas, daemon=True).start()

        self.atualizar_lista_clientes(update_page=False)
        self.atualizar_lista_produtos(update_page=False)

    def atualizar_lista_clientes(self, update_page=True):
        nomes_clientes = self.dropdown_service.listar_nomes_clientes()
        valor_atual = self.cliente_dropdown.value
        self.cliente_dropdown.options = [
            ft.dropdown.Option(nome) for nome in nomes_clientes
        ]
        if valor_atual not in nomes_clientes:
            self.cliente_dropdown.value = None
        if update_page:
            self.page.update()

    def atualizar_lista_produtos(self, update_page=True):
        nomes_produtos = self.dropdown_service.listar_nomes_produtos()
        valor_atual = self.produto_dropdown.value
        self.produto_dropdown.options = [
            ft.dropdown.Option(nome) for nome in nomes_produtos
        ]
        if valor_atual not in nomes_produtos:
            self.produto_dropdown.value = None
        if update_page:
            self.page.update()

    def mostrar_detalhes_venda(self, venda_id):
        # Buscar dados da venda e itens em uma única série de consultas locais
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT cliente, forma_pagamento, data FROM vendas WHERE id = ?", (venda_id,))
        venda = cursor.fetchone()
        # traz também preço unitário via join para evitar múltiplas consultas
        cursor.execute(
            "SELECT iv.produto, iv.quantidade, COALESCE(e.preco_venda,0) FROM itens_venda iv LEFT JOIN estoque e ON e.nome = iv.produto WHERE iv.venda_id = ?",
            (venda_id,),
        )
        itens = cursor.fetchall()
        conn.close()

        cliente, forma_pagamento, data = venda if venda else ("-", "-", "-")

        total_pecas = 0.0
        itens_rows = []
        for produto, quantidade, valor_unitario in itens:
            valor_total = (valor_unitario or 0.0) * (int(quantidade) if quantidade else 0)
            total_pecas += valor_total
            itens_rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(produto)),
                    ft.DataCell(ft.Text(str(quantidade))),
                    ft.DataCell(ft.Text(f"R$ {float(valor_unitario):.2f}")),
                    ft.DataCell(ft.Text(f"R$ {valor_total:.2f}")),
                ])
            )

        # Adiciona linha de total na última linha da tabela
        if itens_rows:
            itens_rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("TOTAL", weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text(f"R$ {total_pecas:.2f}", weight=ft.FontWeight.BOLD)),
                    ]
                )
            )

        dialog_detalhes_venda = ft.AlertDialog(
            modal=True,
            title=ft.Text("Detalhes da Venda", weight=ft.FontWeight.BOLD, size=20, color=ft.Colors.GREEN_700),
            content=ft.Column([
                        ft.Text(f"Cliente: {cliente}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_700),
                        ft.Text(f"Forma de Pagamento: {forma_pagamento}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_700),
                        ft.Text(f"Data: {data}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.BLUE_700),
                        ft.Divider(),
                        ft.Text("Itens Vendidos:", weight=ft.FontWeight.BOLD, size=18, color=ft.Colors.GREEN_700),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Produto", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Quantidade", weight=ft.FontWeight.BOLD)),
                                ft.DataColumn(ft.Text("Valor Unitário", weight=ft.FontWeight.BOLD)),    
                                ft.DataColumn(ft.Text("Valor Total", weight=ft.FontWeight.BOLD)),
                            ],
                            rows=itens_rows,
                            border=ft.border.all(1, ft.Colors.GREY_200),
                            heading_row_color=ft.Colors.BLUE_50,
                            data_row_color=ft.Colors.WHITE,
                        ),
                    ], 
                    expand=True,
                    spacing=12,
                
            ),
            actions=[
                ft.OutlinedButton(
                    "Fechar",
                    on_click=lambda e: self.fechar_detalhes_venda(e, dialog_detalhes_venda)
                )
            ],
        )
        self.page.show_dialog(dialog_detalhes_venda)

    def fechar_detalhes_venda(self, e, dialog_detalhes_venda):
        dialog_detalhes_venda.open = False
        self.page.update()

    def obter_valor_unitario_item(self, venda_id, produto):
        # antigo: mantido por compatibilidade, mas agora não usado pela view otimizada
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT preco_venda FROM estoque WHERE nome=? LIMIT 1", (produto,))
        row = cursor.fetchone()
        conn.close()
        return float(row[0]) if row and row[0] else 0.0

    def obter_valor_total_item(self, venda_id, produto):
        # mantido por compatibilidade; lógica de detalhe usa join para obter já os valores
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute("SELECT quantidade FROM itens_venda WHERE venda_id=? AND produto=?", (venda_id, produto))
        row = cursor.fetchone()
        quantidade = int(row[0]) if row and row[0] else 0
        valor_unitario = self.obter_valor_unitario_item(venda_id, produto)
        return valor_unitario * quantidade

    def atualizar_historico_vendas(self):
        vendas = self.venda_service.listar_vendas()
        linhas = []
        for venda in vendas:
            # agora a query de listar_vendas retorna: id, cliente, forma_pagamento, data, total_itens, total_valor
            venda_id, cliente, forma_pagamento, data, total_itens, total_valor = venda
            total_itens = int(total_itens) if total_itens else 0
            valor_total = float(total_valor) if total_valor else 0.0
            valor_unitario = (valor_total / total_itens) if total_itens > 0 else 0.0
            linhas.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(cliente)),
                ft.DataCell(ft.Text(forma_pagamento or "-")),
                ft.DataCell(ft.Text(data)),
                ft.DataCell(ft.Text(str(total_itens))),
                ft.DataCell(ft.Text(f"R$ {valor_unitario:.2f}")),
                ft.DataCell(ft.Text(f"R$ {valor_total:.2f}")),
                ft.DataCell(ft.Button("Detalhes", on_click=(lambda vid: (lambda e: self.mostrar_detalhes_venda(vid)))(venda_id)))
            ]))
        self.historico_tabela.rows = linhas
        try:
            self.page.update()
        except Exception:
            pass

    def obter_valor_total_venda(self, venda_id):
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(quantidade * (SELECT preco_venda FROM estoque WHERE nome=produto)) FROM itens_venda WHERE venda_id = ?",
            (venda_id,),
        )
        result = cursor.fetchone()
        conn.close()
        return float(result[0]) if result and result[0] else 0.0

    def obter_total_itens_venda(self, venda_id):

        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(quantidade) FROM itens_venda WHERE venda_id = ?", (venda_id,)
        )
        result = cursor.fetchone()
        conn.close()
        return result[0] if result and result[0] else 0

    def adicionar_item(self, e):
        produto = self.produto_dropdown.value
        quantidade = self.quantidade_input.value.strip()
        if not produto or not quantidade.isdigit() or int(quantidade) <= 0:
            alertSnackBarMensage(
                self.page,
                "Selecione um produto e informe uma quantidade válida!",
                bgcolor=ft.Colors.RED_400,
            )
            return
        # Buscar valor unitário do produto
        conn = sqlite3.connect("sistema.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT preco_venda FROM estoque WHERE nome=? LIMIT 1", (produto,)
        )
        row = cursor.fetchone()
        conn.close()
        valor_unitario = float(row[0]) if row and row[0] else 0.0
        valor_total = valor_unitario * int(quantidade)
        self.itens.append(
            {
                "produto": produto,
                "quantidade": int(quantidade),
                "valor_unitario": valor_unitario,
                "valor_total": valor_total,
            }
        )
        print("DEBUG ITENS:", self.itens)
        self.produto_dropdown.value = None
        self.quantidade_input.value = ""
        self.atualizar_tabela()
        print("DEBUG ATUALIZAR_TABELA CHAMADA")
        self.page.update()

    def remover_item(self, index):
        self.itens.pop(index)
        self.atualizar_tabela()
        self.page.update()

    def atualizar_tabela(self):
        self.itens_tabela_itens.clear()
        for i, item in enumerate(self.itens):
            self.itens_tabela_itens.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(item["produto"])),
                        ft.DataCell(ft.Text(str(item["quantidade"]))),
                        ft.DataCell(ft.Text(f"R$ {item['valor_unitario']:.2f}")),
                        ft.DataCell(ft.Text(f"R$ {item['valor_total']:.2f}")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
                                on_click=(lambda idx: (lambda e: self.remover_item(idx)))(i),
                            )
                        ),
                    ]
                )
            )
        total_geral = sum(item["valor_total"] for item in self.itens)
        self.total_text.value = f"Total: R$ {total_geral:.2f}  |  Itens: {sum(item['quantidade'] for item in self.itens)}"
        self.page.update()

    def finalizar_venda(self, e):
        cliente = self.cliente_dropdown.value
        forma_pagamento = self.forma_pagamento_dropdown.value
        if not cliente or not self.itens or not forma_pagamento:
            alertSnackBarMensage(
                self.page,
                "Selecione o cliente, a forma de pagamento e adicione ao menos um item!",
                bgcolor=ft.Colors.RED_400,
            )
            return
        venda_id = self.venda_service.registrar_venda(
            cliente, forma_pagamento, self.itens
        )
        venda_data = {
            "id": venda_id,
            "cliente": cliente,
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            "forma_pagamento": forma_pagamento,
        }
        pdf_path = gerar_pdf_venda(venda_data, self.itens)
        alertSnackBarMensage(
            self.page,
            f"Venda registrada com sucesso!",
            bgcolor=ft.Colors.GREEN_400,
        )
        self.cliente_dropdown.value = None
        self.forma_pagamento_dropdown.value = None
        self.itens.clear()
        self.atualizar_tabela()
        self.atualizar_historico_vendas()
        try:
            self.page.snack_bar.open = True
        except Exception:
            pass
        try:
            self.page.update()
        except Exception:
            pass
