import flet as ft
import datetime
import json


class ModalNovoOrcamento:
    def __init__(self, page, salvar_orcamento_callback, produtos, clientes, desconto=0):
        self.page = page
        self.salvar_orcamento_callback = salvar_orcamento_callback
        self.produtos = produtos
        self.clientes = clientes
        self.desconto = desconto
        self.itens = []
        self.total_sem_desconto = 0
        self.total_com_desconto = 0
        self.dialog = None
        self._montar_modal()

    def _montar_modal(self):
        self.cliente_dropdown = ft.Dropdown(
            label="Cliente",
            options=[ft.dropdown.Option(c["nome"]) for c in self.clientes],
            width=300,
        )
        self.data_field = ft.TextField(
            label="Data", value=datetime.date.today().strftime("%d/%m/%Y"), width=150
        )
        self.lista_itens = ft.Column([])
        self.btn_add_item = ft.Button("Adicionar Item", on_click=self._abrir_modal_item)
        self.total_sem_desc_field = ft.TextField(
            label="Total sem desconto", value="0.00", width=200, read_only=True
        )
        self.desconto_field = ft.TextField(
            label="Desconto (%)",
            value="0",
            width=120,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        self.desconto_field.on_change = lambda e: self._atualizar_totais()
        self.total_com_desc_field = ft.TextField(
            label="Total com desconto", value="0.00", width=200, read_only=True
        )
        self.mensagem_field = ft.TextField(
            label="Informação adicional (aparecerá no PDF)",
            multiline=True,
            height=80,
            width=480,
        )
        self.btn_salvar = ft.Button("Salvar Orçamento", on_click=self._salvar_orcamento)
        self.btn_cancelar = ft.OutlinedButton("Cancelar", on_click=self._cancelar_modal)
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Novo Orçamento", color=ft.Colors.BLUE_700),
            content=ft.Container(
                content=ft.Column(
                    [
                        self.cliente_dropdown,
                        self.data_field,
                        ft.Text(
                            "Itens do Orçamento:",
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                        self.lista_itens,
                        self.btn_add_item,
                        self.total_sem_desc_field,
                        self.desconto_field,
                        self.total_com_desc_field,
                        ft.Text(""),
                        self.mensagem_field,
                    ],
                    spacing=10,
                    scroll="auto",
                ),
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=24,
            ),
            actions=[self.btn_cancelar, self.btn_salvar],
        )

    def _abrir_modal_item(self, e):
        self.produto_dropdown = ft.Dropdown(
            label="Produto",
            options=[ft.dropdown.Option(p["nome"]) for p in self.produtos],
            width=250,
        )
        self.qtd_field = ft.TextField(
            label="Quantidade", width=100, keyboard_type=ft.KeyboardType.NUMBER
        )
        self.preco_field = ft.TextField(
            label="Preço Unitário", width=120, read_only=True
        )
        self.btn_add = ft.Button("Adicionar", on_click=self._adicionar_item)
        self.btn_cancelar_item = ft.OutlinedButton(
            "Cancelar", on_click=self._cancelar_modal_item
        )
        self.btn_concluir = ft.OutlinedButton(
            "Concluir", on_click=self._concluir_modal_item
        )
        self.lista_itens_temp = ft.Column([])
        self.item_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Adicionar Itens ao Orçamento"),
            content=ft.Column(
                [
                    self.produto_dropdown,
                    self.qtd_field,
                    self.preco_field,
                    self.btn_add,
                    ft.Text("Itens adicionados:"),
                    self.lista_itens_temp,
                ],
                width=400,
            ),
            actions=[self.btn_cancelar_item, self.btn_concluir],
        )

        def atualizar_preco(ev=None):
            nome = self.produto_dropdown.value
            produto = next((p for p in self.produtos if p["nome"] == nome), None)
            if produto:
                # Busca preco_venda se existir, senão usa preco
                preco = produto.get("preco_venda")
                if preco is None:
                    preco = produto.get("preco", "0.00")
                self.preco_field.value = str(preco)
            else:
                self.preco_field.value = "0.00"
            self.page.update()

        def atualizar_total_item(ev=None):
            atualizar_preco()

        self.produto_dropdown.on_change = atualizar_preco
        self.qtd_field.on_change = atualizar_total_item
        atualizar_preco()
        if self.item_dialog not in self.page.overlay:
            self.page.overlay.append(self.item_dialog)
        self.page.dialog = self.item_dialog
        self.item_dialog.open = True
        self._atualizar_lista_itens_temp()
        self.page.update()

    def _adicionar_item(self, e):
        nome = self.produto_dropdown.value
        qtd = int(self.qtd_field.value or 0)
        produto = next((p for p in self.produtos if p["nome"] == nome), None)
        preco = 0.0
        if produto:
            preco = float(produto.get("preco_venda") or produto.get("preco") or 0.0)
        if nome and qtd > 0 and preco > 0:
            item = {"produto": nome, "quantidade": qtd, "preco": preco}
            self.itens.append(item)
            self._atualizar_lista_itens()
            self._atualizar_totais()
            self._atualizar_lista_itens_temp()
            # Limpa campos para novo item
            self.produto_dropdown.value = None
            self.qtd_field.value = ""
            self.preco_field.value = ""
            self.page.update()

    def _atualizar_lista_itens_temp(self):
        self.lista_itens_temp.controls.clear()
        for idx, item in enumerate(self.itens):

            def _make_remove(i):
                return lambda e: self._remover_item(i)

            row = ft.Row(
                [
                    ft.Text(
                        f"{item['produto']} - Qtd: {item['quantidade']} x R$ {item['preco']:.2f}",
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        tooltip="Remover item",
                        on_click=_make_remove(idx),
                    ),
                ],
                alignment="spaceBetween",
            )
            self.lista_itens_temp.controls.append(row)
        self.page.update()

    def _concluir_modal_item(self, e):
        self.item_dialog.open = False
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def _atualizar_lista_itens(self):
        self.lista_itens.controls.clear()
        for idx, item in enumerate(self.itens):

            def _make_remove(i):
                return lambda e: self._remover_item(i)

            row = ft.Row(
                [
                    ft.Text(
                        f"{item['produto']} - Qtd: {item['quantidade']} x R$ {item['preco']:.2f}"
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        tooltip="Remover item",
                        on_click=_make_remove(idx),
                    ),
                ],
                alignment="spaceBetween",
            )
            self.lista_itens.controls.append(row)
        self.page.update()

    def _remover_item(self, index, e=None):
        try:
            # remove o item pelo índice e atualiza tudo
            self.itens.pop(index)
        except Exception:
            return
        self._atualizar_totais()
        # atualizar ambas as listas (temp e principal)
        if hasattr(self, "lista_itens_temp"):
            self._atualizar_lista_itens_temp()
        self._atualizar_lista_itens()

    def _atualizar_totais(self):
        self.total_sem_desconto = sum(
            item["quantidade"] * item["preco"] for item in self.itens
        )
        try:
            desconto_percent = float(self.desconto_field.value or 0)
        except Exception:
            desconto_percent = 0
        self.desconto = (
            (self.total_sem_desconto * desconto_percent) / 100
            if desconto_percent > 0
            else 0
        )
        self.total_com_desconto = self.total_sem_desconto - self.desconto
        self.total_sem_desc_field.value = f"{self.total_sem_desconto:.2f}"
        self.total_com_desc_field.value = f"{self.total_com_desconto:.2f}"
        self.page.update()

    def _salvar_orcamento(self, e):
        import os
        from backend.utils.pdf_generator import gerar_pdf

        # salvar sem overlay/ProgressRing para agilizar interação

        # monta dicionário do orçamento incluindo dados do cliente
        cliente_nome = self.cliente_dropdown.value
        cliente_obj = next(
            (c for c in self.clientes if c.get("nome") == cliente_nome), None
        )
        orcamento = {
            "cliente": cliente_nome,
            "cliente_nome": cliente_nome,
            "cliente_telefone": (cliente_obj.get("telefone") if cliente_obj else None),
            "cliente_email": (cliente_obj.get("email") if cliente_obj else None),
            "cliente_endereco": (cliente_obj.get("endereco") if cliente_obj else None),
            "data": self.data_field.value,
            "itens": self.itens,
            "mensagem_adicional": (self.mensagem_field.value or ""),
            "total_sem_desconto": self.total_sem_desconto,
            "total_com_desconto": self.total_com_desconto,
            "desconto": self.desconto,
        }
        # Salva o orçamento no banco e obtém o id final
        novo_id = self.salvar_orcamento_callback(orcamento)
        # Gera PDF e salva na pasta assets usando o id real
        pdf_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "assets", "orçamentos")
        )
        os.makedirs(pdf_dir, exist_ok=True)
        # define número/ID único do orçamento
        numero_unico = novo_id or orcamento.get("id") or None
        if not numero_unico:
            import time

            numero_unico = f"tmp-{int(time.time())}"
        orcamento["id"] = numero_unico
        orcamento["numero"] = numero_unico
        pdf_id = numero_unico
        pdf_filename = f"orcamento_{pdf_id}.pdf"
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        try:
            gerar_pdf(orcamento, self.itens, pdf_path)
        except Exception as err:
            print("Erro ao gerar PDF:", err)
        self.dialog.open = False
        if self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
        # Seleciona a aba de orçamentos (índice 3 ou 4, dependendo da ordem)
        if hasattr(self.page, "tabs") and self.page.tabs:
            for idx, tab in enumerate(self.page.tabs.tabs):
                if getattr(tab, "text", "").upper() == "ORÇAMENTOS":
                    self.page.tabs.selected_index = idx
                    break
        elif hasattr(self.page, "controls"):
            # Busca Tabs no layout
            for c in self.page.controls:
                if isinstance(c, ft.Tabs):
                    for idx, tab in enumerate(c.tabs):
                        if getattr(tab, "text", "").upper() == "ORÇAMENTOS":
                            c.selected_index = idx
                            break
        self.page.update()
        self._cancelar_modal_item(e)

    def _cancelar_modal(self, e):
        self.dialog.open = False
        self.page.update()

    def _cancelar_modal_item(self, e):
        self.item_dialog.open = False
        self.page.update()

    def abrir(self):
        print("abriu modal novo orçamento")
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.page.dialog = None  # Garante que não há outro dialog aberto
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
