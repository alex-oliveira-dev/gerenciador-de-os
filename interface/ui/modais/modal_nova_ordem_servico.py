import flet as ft
import datetime
from backend.services.funcionario_service import FuncionarioService
from backend.services.estoque_service import EstoqueService
from backend.repository.cliente_repository import ClienteRepository
from backend.services.estoque_service import EstoqueService
from backend.repository.funcionario_repository import FuncionarioRepository


class ModalAdicionarOrdemServico:
    def __init__(
        self,
        page: ft.Page,
        adicionar_ordem_servico,
        editar_ordem_servico,
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
        itens_estoque = EstoqueService().listar_produtos()
        funcionarios = FuncionarioRepository().listar_funcionarios()
        formas_pagamento = ["Dinheiro", "Cartão", "Pix", "Boleto"]

        self.estoque = ft.Dropdown(
            label="Item do Estoque",
            width=200,
            options=[ft.dropdown.Option(e["nome"]) for e in itens_estoque],
        )
        self.quantidade = ft.TextField(label="Quantidade", width=100)
        self.preco = ft.TextField(label="Valor", width=100)
        self.responsavel = ft.TextField(label="Responsável", width=200)
        self.descricao = ft.TextField(label="Descrição", width=200)
        self.itens_os = []
        self.lista_itens = ft.Column([])

        self.data_abertura = ft.TextField(
            label="Data de abertura", width=150, disabled=True
        )
        self.cliente = ft.Dropdown(
            label="Cliente",
            width=200,
            options=[ft.dropdown.Option(c["nome"]) for c in clientes],
        )
        self.veiculo = ft.TextField(label="Veículo", width=200)
        self.defeito_relatado = ft.TextField(label="Defeito relatado", width=200)
        # Apenas campos essenciais para nova OS
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
                        [
                            self.data_abertura,
                            self.cliente,
                            self.veiculo,
                            self.defeito_relatado,
                        ],
                        spacing=16,
                    ),
                    ft.Divider(height=2, color=ft.Colors.BLUE_100),
                    ft.Text("Itens da O.S.", size=16, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        [
                            self.estoque,
                            self.quantidade,
                            self.preco,
                            self.responsavel,
                            self.descricao,
                            ft.ElevatedButton(
                                "Adicionar Item",
                                icon=ft.Icons.ADD,
                                on_click=self.adicionar_item,
                            ),
                        ],
                        spacing=8,
                    ),
                    self.lista_itens,
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
            "estoque": self.estoque.value,
            "quantidade": self.quantidade.value,
            "preco": self.preco.value,
            "responsavel": self.responsavel.value,
            "descricao": self.descricao.value,
        }
        if not item["estoque"] or not item["quantidade"] or not item["preco"]:
            self.mostrar_snack("Preencha o item de estoque, quantidade e valor.")
            return
        self.itens_os.append(item)
        self.atualizar_lista_itens()
        self.estoque.value = ""
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
                            f"{item['estoque']} - Qtd: {item['quantidade']} - Valor: {item['preco']}",
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
            self.page.update()

    def abrir_modal_adicionar_ordem_servico(self):
        # Sempre limpar _id_edicao ao abrir para garantir que é adição
        self._id_edicao = None
        # Buscar dados atualizados do banco
        from backend.repository.cliente_repository import ClienteRepository
        from backend.services.estoque_service import EstoqueService

        clientes = ClienteRepository().listar_clientes()
        itens_estoque = EstoqueService().listar_produtos()
        self.cliente.options = [ft.dropdown.Option(c["nome"]) for c in clientes]
        self.estoque.options = [ft.dropdown.Option(e["nome"]) for e in itens_estoque]
        self.estoque.update()
        # Preencher data automaticamente ao abrir
        self.data_abertura.value = datetime.datetime.now().strftime("%d/%m/%Y")
        self.page.update()
        if not hasattr(self, "dialog"):
            self.dialog = ft.AlertDialog(
                content=self.layout,
                modal=True,
            )
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def abrir_modal_editar_ordem_servico(self, ordem):
        print("chamou editar os")
        # Preencher campos com dados da OS
        self.data_abertura.value = ordem.get("data_abertura", "")
        self.cliente.value = ordem.get("cliente", "")
        self.veiculo.value = ordem.get("veiculo", "")
        self.defeito_relatado.value = ordem.get("defeito_relatado", "")
        self.data_abertura.disabled = True
        self._id_edicao = ordem.get("id")  # Salva o id para edição
        self.page.update()
        if not hasattr(self, "dialog"):
            self.dialog = ft.AlertDialog(
                content=self.layout,
                modal=True,
            )
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def salvar_ordem_servico(self, e):
        dados_os = {
            "data_abertura": self.data_abertura.value,
            "cliente": self.cliente.value,
            "veiculo": self.veiculo.value,
            "defeito_relatado": self.defeito_relatado.value,
        }
        self.adicionar_ordem_servico(dados_os)
        if self.popular_tabela_ordem_servico:
            self.popular_tabela_ordem_servico()
        self.fechar_modal()

        self.page.update()
