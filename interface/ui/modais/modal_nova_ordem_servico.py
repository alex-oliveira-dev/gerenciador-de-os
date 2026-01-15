import flet as ft
import datetime
from backend.services.funcionario_service import FuncionarioService
from backend.services.estoque_service import EstoqueService
from backend.repository.cliente_repository import ClienteRepository
from backend.repository.produto_repository import listar as listar_produtos
from backend.repository.funcionario_repository import FuncionarioRepository


class ModalAdicionarOrdemServico:
    def __init__(
        self,
        page: ft.Page,
        editar_ordem_servico,
        adicionar_ordem_servico,
        mostrar_snack_mensagem,
        popular_tabela_ordem_servico,
    ):
        self.page = page
        self.adicionar_ordem_servico = adicionar_ordem_servico
        self.editar_ordem_servico = editar_ordem_servico
        self.mostrar_snack = mostrar_snack_mensagem
        self.popular_tabela_ordem_servico = popular_tabela_ordem_servico
        # Carregar opções do banco

        clientes = ClienteRepository().listar_clientes()
        produtos = listar_produtos()
        funcionarios = FuncionarioRepository().listar_funcionarios()
        formas_pagamento = ["Dinheiro", "Cartão", "Pix", "Boleto"]

        self.data_abertura = ft.TextField(label="Data de abertura", width=150)
        self.cliente = ft.Dropdown(
            label="Cliente",
            width=200,
            options=[ft.dropdown.Option(c["nome"]) for c in clientes],
        )
        self.veiculo = ft.TextField(label="Veículo", width=200)
        self.defeito_relatado = ft.TextField(label="Defeito relatado", width=200)
        self.status = ft.Dropdown(
            label="Status da O.S.",
            width=180,
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
            value="Aberta",
        )
        self.responsavel = ft.Dropdown(
            label="Responsável / Técnico",
            width=200,
            options=[ft.dropdown.Option(f["nome"]) for f in funcionarios],
        )
        self.servico = ft.TextField(label="Serviço", width=200)
        self.servico_executado = ft.TextField(label="Serviço executado", width=200)
        self.valor_servico = ft.TextField(
            label="Valor do serviço", width=120, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.pecas_utilizadas = ft.TextField(label="Peças utilizadas", width=200)
        self.valor_pecas = ft.TextField(
            label="Valor das peças", width=120, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.valor_total = ft.TextField(
            label="Valor total", width=120, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.data_fechamento = ft.TextField(label="Data de fechamento", width=150)
        self.forma_pagamento = ft.Dropdown(
            label="Forma de pagamento",
            width=150,
            options=[ft.dropdown.Option(fp) for fp in formas_pagamento],
        )
        self.situacao_pagamento = ft.Dropdown(
            label="Situação do pagamento",
            width=150,
            options=[ft.dropdown.Option(s) for s in ["Pendente", "Pago"]],
            value="Pendente",
        )
        self.itens_os = []
        self.lista_itens = ft.Column([])
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Nova Ordem de Serviço",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=2, color=ft.Colors.BLUE_100),
                    ft.Row(
                        [self.data_abertura, self.data_fechamento, self.status],
                        spacing=16,
                    ),
                    ft.Row([self.cliente, self.responsavel], spacing=16),
                    ft.Row([self.veiculo, self.defeito_relatado], spacing=16),
                    ft.Row([self.servico, self.servico_executado], spacing=16),
                    ft.Row(
                        [
                            self.valor_servico,
                            self.pecas_utilizadas,
                            self.valor_pecas,
                            self.valor_total,
                        ],
                        spacing=16,
                    ),
                    ft.Row([self.forma_pagamento, self.situacao_pagamento], spacing=16),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Salvar O.S.",
                                icon=ft.Icons.SAVE,
                                bgcolor=ft.Colors.BLUE_400,
                                color=ft.Colors.WHITE,
                                on_click=self.salvar_ordem_servico,
                            ),
                            ft.OutlinedButton(
                                "Cancelar",
                                icon=ft.Icons.CLOSE,
                                on_click=self.fechar_modal,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=16,
                    ),
                ],
                spacing=18,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=24,
            border_radius=12,
            bgcolor=ft.Colors.WHITE,
        )

    def adicionar_item(self, e=None):
        item = {
            "produto": self.produto.value,
            "quantidade": self.quantidade.value,
            "preco": self.preco.value,
            "responsavel": self.responsavel.value,
            "descricao": self.descricao.value,
        }
        if not item["produto"] or not item["quantidade"] or not item["preco"]:
            self.mostrar_snack("Preencha produto, quantidade e valor.")
            return
        self.itens_os.append(item)
        self.atualizar_lista_itens()
        self.produto.value = ""
        self.quantidade.value = ""
        self.preco.value = ""
        self.responsavel.value = ""
        self.descricao.value = ""
        pass

    def remover_item(self, idx):
        del self.itens_os[idx]
        self.atualizar_lista_itens()
        self.page.update()

    def atualizar_lista_itens(self):
        self.lista_itens.controls.clear()
        for idx, item in enumerate(self.itens_os):
            self.lista_itens.controls.append(
                ft.Row(
                    [
                        ft.Text(
                            f"{item['produto']} - Qtd: {item['quantidade']} - Valor: {item['preco']}",
                            width=260,
                        ),
                        ft.IconButton(
                            ft.icons.DELETE,
                            icon_color=ft.Colors.RED_400,
                            on_click=lambda e, i=idx: self.remover_item(i),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

    def fechar_modal(self, e=None):
        if hasattr(self, "dialog"):
            self.dialog.open = False
            if self.dialog in self.page.overlay:
                self.page.overlay.remove(self.dialog)
            pass

    def abrir_modal_adicionar_ordem_servico(self):
        # Preencher data automaticamente ao abrir
        self.data_abertura.value = datetime.datetime.now().strftime("%d/%m/%Y")
        self.page.update()
        if not hasattr(self, "dialog"):
            self.dialog = ft.AlertDialog(
                title=ft.Text("Nova Ordem de Serviço"),
                content=self.layout,
                modal=True,
            )
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def abrir_modal_editar_ordem_servico(self, ordem):
        # Implementar lógica para editar
        pass

    def salvar_ordem_servico(self, e):
        dados_os = {
            "data_abertura": self.data_abertura.value,
            "cliente": self.cliente.value,
            "veiculo": self.veiculo.value,
            "defeito_relatado": self.defeito_relatado.value,
            "status": self.status.value,
            "responsavel": self.responsavel.value,
            "servico": self.servico.value,
            "servico_executado": self.servico_executado.value,
            "valor_servico": float(self.valor_servico.value or 0),
            "pecas_utilizadas": self.pecas_utilizadas.value,
            "valor_pecas": float(self.valor_pecas.value or 0),
            "valor_total": float(self.valor_total.value or 0),
            "data_fechamento": self.data_fechamento.value,
            "forma_pagamento": self.forma_pagamento.value,
            "situacao_pagamento": self.situacao_pagamento.value,
        }
        self.adicionar_ordem_servico(dados_os)
        if self.popular_tabela_ordem_servico:
            self.popular_tabela_ordem_servico()
        self.fechar_modal()
