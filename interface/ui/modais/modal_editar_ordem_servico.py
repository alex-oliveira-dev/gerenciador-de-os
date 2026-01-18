import flet as ft
from backend.repository.cliente_repository import ClienteRepository
from backend.repository.produto_repository import listar as listar_produtos
from backend.repository.funcionario_repository import FuncionarioRepository


class ModalEditarOrdemServico:
    def __init__(self, page, ordem=None, salvar_callback=None, fechar_callback=None):
        self.page = page
        self.ordem = ordem or {}
        self.salvar_callback = salvar_callback
        self.fechar_callback = fechar_callback

        clientes = ClienteRepository().listar_clientes()
        produtos = listar_produtos()
        funcionarios = FuncionarioRepository().listar_funcionarios()

        self.data_abertura = ft.TextField(
            label="Data de abertura",
            width=150,
            value=self.ordem.get("data_abertura", ""),
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
        self.produto = ft.Dropdown(
            label="Produto",
            width=200,
            options=[ft.dropdown.Option(p["nome"]) for p in produtos],
        )
        self.quantidade = ft.TextField(label="Quantidade", width=100)
        self.valor_unitario = ft.TextField(label="Valor Unitário", width=120)
        self.valor_pecas = ft.TextField(
            label="Valor Peças", width=120, value="0", read_only=True
        )
        self.valor_total = ft.TextField(
            label="Valor Total", width=120, value="0", read_only=True
        )
        self.lista_itens = ft.Column(spacing=6)
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

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Editar Ordem de Serviço",
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
                                self.valor_pecas,
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
                    "Salvar",
                    icon=ft.Icons.SAVE,
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                    on_click=self.salvar,
                ),
            ],
        )

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
                ft.Row(
                    [
                        ft.Text(
                            f"{item['produto']} - Qtd: {item['quantidade']} - Valor: {item['valor_unitario']}",
                            width=260,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE,
                            icon_color=ft.Colors.RED_700,
                            tooltip="Remover",
                            on_click=lambda e, i=idx: self.remover_item(i),
                        ),
                    ],
                    spacing=8,
                )
            )
        self.valor_pecas.value = f"{total_pecas:.2f}"
        self.valor_total.value = f"{total_pecas:.2f}"
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
        self.produto.value = ""
        self.quantidade.value = ""
        self.valor_unitario.value = ""
        self.page.update()

    def remover_item(self, idx):
        del self.itens_os[idx]
        self.atualizar_lista_itens()
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
            "valor_pecas": self.valor_pecas.value,
            "valor_total": self.valor_total.value,
            "data_fechamento": self.data_fechamento.value,
            "forma_pagamento": self.forma_pagamento.value,
            "situacao_pagamento": self.situacao_pagamento.value,
        }
        if self.salvar_callback:
            self.salvar_callback(dados)
        self.fechar()
