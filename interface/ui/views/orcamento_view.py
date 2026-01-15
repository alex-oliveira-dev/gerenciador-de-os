import flet as ft
from interface.ui.tabelas.tabela_orcamento import TabelaOrcamento
from interface.ui.modais.modal_novo_orcamento import ModalNovoOrcamento
from backend.services.orcamento_service import OrcamentoService
from backend.services.estoque_service import EstoqueService
from backend.services.cliente_service import ClienteService


class OrcamentoView:

    def __init__(self, page, mostrar_snack_mensagem):
        self.page = page
        self.mostrar_snack_mensagem = mostrar_snack_mensagem
        self.orcamento_service = OrcamentoService()
        self.produto_service = EstoqueService()
        self.cliente_service = ClienteService()
        # indicador de carregamento removido para agilizar interface
        from interface.ui.modais.modal_editar_orcamento import ModalEditarOrcamento

        self.tabela_orcamento = TabelaOrcamento(
            page,
            self.editar_orcamento,
            self.excluir_orcamento,
            self.abrir_modal_editar_orcamento,
        )
        self.btn_novo_orcamento = ft.Button(
            "Novo Orçamento", on_click=self.abrir_modal_novo_orcamento
        )
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.ElevatedButton(
                        "Novo Orçamento",
                        icon=ft.Icons.ADD,
                        bgcolor=ft.Colors.BLUE_400,
                        color=ft.Colors.WHITE,
                        on_click=self.abrir_modal_novo_orcamento,
                    ),
                    self.tabela_orcamento.layout,
                ],
                expand=True,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=24,
        )
        self.atualizar_orcamentos()

    def abrir_lista_orcamentos_por_cliente(self, e):
        orcamentos = self.orcamento_service.listar_orcamentos()
        clientes = {}
        for o in orcamentos:
            nome = o.get("cliente", "Desconhecido")
            if nome not in clientes:
                clientes[nome] = []
            clientes[nome].append(o)
        if not clientes:
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Orçamentos por Cliente"),
                content=ft.Text("Nenhum cliente com orçamento cadastrado."),
                actions=[
                    ft.OutlinedButton(
                        "Fechar",
                        on_click=lambda e: self.page.dialog.__setattr__("open", False),
                    )
                ],
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()
            return

        dropdown = ft.Dropdown(
            label="Selecione o cliente",
            options=[ft.dropdown.Option(nome) for nome in clientes.keys()],
            width=300,
        )
        btn_filtrar = ft.Button("Mostrar Orçamentos", disabled=True)
        btn_todos = ft.OutlinedButton(
            "Mostrar Todos", on_click=lambda e: self._mostrar_todos_orcamentos(dialog)
        )

        def on_dropdown_change(ev):
            btn_filtrar.disabled = not bool(dropdown.value)
            self.page.update()

        dropdown.on_change = on_dropdown_change

        def filtrar_orcamentos(ev):
            nome = dropdown.value
            if nome and nome in clientes:
                orcs = list(clientes[nome])
                if orcs:
                    self.tabela_orcamento.atualizar(orcs)
                else:
                    self.tabela_orcamento.atualizar([])
                    self.mostrar_snack_mensagem(
                        f"Nenhum orçamento encontrado para {nome}."
                    )
                dialog.open = False
                self.page.update()

        btn_filtrar.on_click = filtrar_orcamentos

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Orçamentos por Cliente"),
            content=ft.Column(
                [dropdown, btn_filtrar, btn_todos], width=400, height=180
            ),
            actions=[
                ft.OutlinedButton(
                    "Fechar",
                    on_click=lambda e: self.page.dialog.__setattr__("open", False),
                )
            ],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _mostrar_todos_orcamentos(self, dialog):
        self.atualizar_orcamentos()
        dialog.open = False
        self.page.update()

    def abrir_modal_editar_orcamento(self, orcamento):
        from interface.ui.modais.modal_editar_orcamento import ModalEditarOrcamento

        modal = ModalEditarOrcamento(self.page, orcamento, self.salvar_edicao_orcamento)
        modal.abrir()

    def salvar_edicao_orcamento(self, orcamento, pdf_path):
        # Atualiza o orçamento no serviço
        self.orcamento_service.editar_orcamento(orcamento)
        self.mostrar_snack_mensagem(f"Orçamento atualizado e PDF gerado em: {pdf_path}")
        self.atualizar_orcamentos()
        self.page.update()

    def atualizar_orcamentos(self):
        orcamentos = self.orcamento_service.listar_orcamentos()
        self.tabela_orcamento.atualizar(orcamentos)

    def abrir_modal_novo_orcamento(self, e):
        produtos = self.produto_service.listar_produtos()
        clientes = self.cliente_service.listar_clientes()
        modal = ModalNovoOrcamento(self.page, self.salvar_orcamento, produtos, clientes)
        modal.abrir()

    def salvar_orcamento(self, orcamento):
        novo_id = self.orcamento_service.adicionar_orcamento(orcamento)
        self.mostrar_snack_mensagem("Orçamento salvo com sucesso!")
        self.atualizar_orcamentos()
        self.page.update()
        return novo_id

    def editar_orcamento(self, orcamento):
        # Implementar edição se necessário
        self.mostrar_snack_mensagem(
            "Função de edição de orçamento ainda não implementada."
        )

    def excluir_orcamento(self, orcamento):
        self.orcamento_service.deletar_orcamento(orcamento["id"])
        self.mostrar_snack_mensagem("Orçamento excluído!")
        self.atualizar_orcamentos()
        self.page.update()

    def abrir(self):
        self.page.dialog = None  # Garante que não há outro dialog aberto
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
