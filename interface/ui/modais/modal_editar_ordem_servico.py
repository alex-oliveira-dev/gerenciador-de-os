import flet as ft
from backend.repository.cliente_repository import ClienteRepository
from backend.repository.funcionario_repository import FuncionarioRepository


class ModalEditarOrdemServico:
    def atualizar_lista_itens(self):
        self.lista_itens.controls.clear()
        total_pecas = 0.0
        for idx, item in enumerate(self.itens_os):
            try:
                qtd = float(item.get("quantidade", 0))
                valor = float(item.get("valor_unitario", 0))
                total_pecas += qtd * valor
            except Exception:
                pass
            self.lista_itens.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                f"{item['produto']}",
                                width=140,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_800,
                                size=15,
                            ),
                            ft.Text(
                                f"Qtd: {item['quantidade']}",
                                width=60,
                                color=ft.Colors.BLACK87,
                                size=14,
                            ),
                            ft.Text(
                                f"Unit: R$ {float(item.get('valor_unitario', 0)):.2f}",
                                width=100,
                                color=ft.Colors.GREEN_700,
                                size=14,
                            ),
                            ft.Text(
                                f"Total: R$ {float(item.get('quantidade', 0)) * float(item.get('valor_unitario', 0)):.2f}",
                                width=120,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_900,
                                size=15,
                            ),
                            ft.IconButton(
                                ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_700,
                                tooltip="Remover",
                                on_click=lambda e, i=idx: self.remover_item(i),
                            ),
                        ],
                        spacing=8,
                    ),
                    border=ft.border.all(1, ft.Colors.BLUE_200),
                    border_radius=8,
                    padding=8,
                    margin=ft.margin.only(bottom=4),
                    bgcolor=ft.Colors.BLUE_50,
                )
            )
        self.valor_total.value = f"{total_pecas:.2f}"
        self.page.update()

    def atualizar_valor_total(self):
        total_pecas = 0.0
        for item in self.itens_os:
            try:
                qtd = float(item.get("quantidade", 0))
                valor = float(item.get("valor_unitario", 0))
                total_pecas += qtd * valor
            except Exception:
                pass
        self.valor_total.value = f"{total_pecas:.2f}"
        self.page.update()

    def __init__(
        self, page, ordem=None, salvar_callback=None, fechar_callback=None, titulo=None
    ):
        self.page = page
        self.ordem = ordem or {}
        self.salvar_callback = salvar_callback
        self.fechar_callback = fechar_callback

        clientes = ClienteRepository().listar_clientes()
        from backend.services.estoque_service import EstoqueService

        produtos = EstoqueService().listar_produtos()
        funcionarios = FuncionarioRepository().listar_funcionarios()

        self.data_abertura = ft.TextField(
            label="Data de abertura",
            width=150,
            value=self.ordem.get("data_abertura", ""),
            read_only=True,
        )
        self.cliente = ft.Dropdown(
            label="Cliente",
            width=200,
            value=self.ordem.get("cliente", ""),
            options=[ft.dropdown.Option(c["nome"]) for c in clientes],
        )
        self.veiculo = ft.TextField(
            label="Veículo", width=200, value=self.ordem.get("veiculo", "")
        )
        self.defeito_relatado = ft.TextField(
            label="Defeito relatado",
            width=200,
            value=self.ordem.get("defeito_relatado", ""),
        )
        self.status = ft.Dropdown(
            label="Status",
            width=180,
            value=self.ordem.get("status", ""),
            options=[
                ft.dropdown.Option(s)
                for s in [
                    "Aberta",
                    "Em andamento",
                    "Aguardando peça",
                    "Finalizada",
                    "Cancelada",
                ]
            ],
        )
        self.responsavel = ft.Dropdown(
            label="Responsável",
            width=200,
            value=self.ordem.get("responsavel", ""),
            options=[ft.dropdown.Option(f["nome"]) for f in funcionarios],
        )

        # Peças
        self.itens_os = (
            self.ordem.get("itens_os", []) if self.ordem.get("itens_os") else []
        )
        self._produtos_estoque = {p["nome"]: p for p in produtos}

        self.valor_unitario = ft.TextField(
            label="Valor Unitário", width=120, read_only=True
        )
        self.produto = ft.Dropdown(
            label="Produto",
            width=200,
            options=[ft.dropdown.Option(p["nome"]) for p in produtos],
        )
        self.produto.on_change = self.on_produto_change
        self.quantidade = ft.TextField(label="Quantidade", width=100)
        # Removido campo Valor Peças
        self.valor_total = ft.TextField(
            label="Valor Total", width=120, value="0", read_only=True
        )

        self.page.update()
        self.quantidade.on_change = self.on_quantidade_change
        self.lista_itens = ft.Column(spacing=10)
        self.atualizar_lista_itens()

        self.data_fechamento = ft.TextField(
            label="Data Fechamento",
            width=150,
            value=self.ordem.get("data_fechamento", ""),
        )
        self.forma_pagamento = ft.TextField(
            label="Forma Pagamento",
            width=150,
            value=self.ordem.get("forma_pagamento", ""),
        )
        self.situacao_pagamento = ft.TextField(
            label="Situação Pagamento",
            width=150,
            value=self.ordem.get("situacao_pagamento", ""),
        )

        self._titulo_modal = titulo if titulo else "Editar Ordem de Serviço"
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                self._titulo_modal,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                self.data_abertura,
                                self.cliente,
                                self.veiculo,
                                self.defeito_relatado,
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            [
                                self.status,
                                self.responsavel,
                            ],
                            spacing=10,
                        ),
                        ft.Divider(),
                        ft.Text(
                            "Peças da O.S.",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                        ft.Row(
                            [
                                self.produto,
                                self.quantidade,
                                self.valor_unitario,
                                ft.ElevatedButton(
                                    "Adicionar Peça",
                                    icon=ft.Icons.ADD,
                                    bgcolor=ft.Colors.BLUE_400,
                                    color=ft.Colors.WHITE,
                                    on_click=self.adicionar_item,
                                ),
                            ],
                            spacing=10,
                        ),
                        self.lista_itens,
                        ft.Row(
                            [
                                self.valor_total,
                            ],
                            spacing=10,
                        ),
                        ft.Row(
                            [
                                self.data_fechamento,
                                self.forma_pagamento,
                                self.situacao_pagamento,
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS,
                ),
                width=900,
                bgcolor=ft.Colors.WHITE,
                padding=24,
                border_radius=12,
            ),
            actions=[
                ft.OutlinedButton(
                    "Cancelar", icon=ft.Icons.CLOSE, on_click=self.fechar
                ),
                ft.ElevatedButton(
                    (
                        "Finalizar O.S"
                        if self._titulo_modal == "Finalizar O.S"
                        else "Salvar"
                    ),
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                    on_click=self.salvar,
                ),
            ],
        )

        self.page.update()

    def on_produto_change(self, e):
        nome = e.control.value if hasattr(e, "control") else self.produto.value
        produto = self._produtos_estoque.get(nome)
        if produto:
            preco = (
                produto.get("preco")
                or produto.get("valor")
                or produto.get("preco_unitario")
                or produto.get("valor_unitario")
                or produto.get("preco_unit")
                or produto.get("preco_venda")
                or produto.get("preco_custo")
                or 0
            )
            try:
                preco = float(preco)
            except Exception:
                preco = 0
            self.valor_unitario.value = f"{preco:.2f}"
        else:
            self.valor_unitario.value = ""
        self.page.update()

    def on_quantidade_change(self, evento):
        try:
            qtd = float(self.quantidade.value or 0)
            nome_produto = self.produto.value
            produto = self._produtos_estoque.get(nome_produto)
            preco_unitario = 0.0
            if produto:
                preco_unitario = (
                    produto.get("preco")
                    or produto.get("valor")
                    or produto.get("preco_unitario")
                    or produto.get("valor_unitario")
                    or produto.get("preco_unit")
                    or produto.get("preco_venda")
                    or produto.get("preco_custo")
                    or 0
                )
                try:
                    preco_unitario = float(preco_unitario)
                except Exception:
                    preco_unitario = 0.0
            self.valor_unitario.value = f"{preco_unitario:.2f}"
            self.valor_total.value = f"{qtd * preco_unitario:.2f}"
        except Exception:
            print("Erro ao calcular valor total")
            self.valor_unitario.value = "0.00"
            self.valor_total.value = "0.00"
        self.page.update()

    def adicionar_item(self, e=None):
        item = {
            "produto": self.produto.value,
            "quantidade": self.quantidade.value,
            "valor_unitario": self.valor_unitario.value,
        }
        if not item["produto"] or not item["quantidade"] or not item["valor_unitario"]:
            return
        self.itens_os.append(item)
        self.atualizar_lista_itens()
        self.atualizar_valor_total()
        self.produto.value = ""
        self.quantidade.value = ""
        self.valor_unitario.value = ""
        self.page.update()

    def remover_item(self, idx):
        del self.itens_os[idx]
        self.atualizar_lista_itens()
        self.atualizar_valor_total()
        self.page.update()

    def abrir(self):
        self.dialog.open = True
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.page.update()

    def fechar(self, e=None):
        self.dialog.open = False
        self.page.update()
        if self.fechar_callback:
            self.fechar_callback()

    def salvar(self, e=None):
        dados = {
            "id": self.ordem.get("id"),
            "data_abertura": self.data_abertura.value,
            "cliente": self.cliente.value,
            "veiculo": self.veiculo.value,
            "defeito_relatado": self.defeito_relatado.value,
            "status": self.status.value,
            "responsavel": self.responsavel.value,
            "itens_os": self.itens_os,
            "valor_total": self.valor_total.value,
            "data_fechamento": self.data_fechamento.value,
            "forma_pagamento": self.forma_pagamento.value,
            "situacao_pagamento": self.situacao_pagamento.value,
        }
        if self.salvar_callback:
            self.salvar_callback(dados)
        if hasattr(self.page, "refresh_all") and callable(
            getattr(self.page, "refresh_all", None)
        ):
            self.page.refresh_all()
        self.fechar()
