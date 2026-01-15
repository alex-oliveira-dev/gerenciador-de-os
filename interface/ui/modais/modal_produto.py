import flet as ft


class ModalProduto:
    def __init__(
        self, page: ft.Page, adicionar_produto, carregar_produtos, salvar_edicao
    ):
        self.page = page
        self.on_salvar = adicionar_produto
        self.carregar_produtos = carregar_produtos
        self.on_salvar_alteracoes = salvar_edicao
        self.produto_id = None

        self.nome = ft.TextField(label="Nome")
        self.codigo = ft.TextField(label="Código")
        self.quantidade = ft.TextField(label="Quantidade")
        self.marca = ft.TextField(label="Marca")
        self.fornecedores = ft.TextField(label="Fornecedores")

        self.preco_custo = ft.TextField(
            label="Preço de Custo", keyboard_type=ft.KeyboardType.NUMBER
        )
        self.preco_venda = ft.TextField(
            label="Preço de Venda", keyboard_type=ft.KeyboardType.NUMBER
        )
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Adicionar NovoProduto",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    ft.Divider(height=2, color=ft.Colors.BLUE_100),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    self.nome,
                                    self.codigo,
                                    self.quantidade,
                                ],
                                spacing=16,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    self.marca,
                                    self.fornecedores,
                                    ft.Row(
                                        [self.preco_custo, self.preco_venda], spacing=16
                                    ),
                                ],
                                spacing=16,
                                expand=True,
                            ),
                        ],
                        spacing=32,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Salvar",
                                icon=ft.Icons.SAVE,
                                bgcolor=ft.Colors.BLUE_400,
                                color=ft.Colors.WHITE,
                                on_click=self.salvar,
                            ),
                            ft.OutlinedButton(
                                "Cancelar",
                                icon=ft.Icons.CLOSE,
                                on_click=self.fechar,
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

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(""),
            content=self.layout,
        )

    def abrir_modal_produto(self, item=None):
        self.limpar_campos()

        if item:
            self.produto_id = item["id"]
            self.dialog.title.value = "Editar Produto"

            self.nome.value = item["nome"]
            self.codigo.value = item["codigo"]
            self.quantidade.value = str(item["quantidade"])
            self.marca.value = item["marca"]
            self.fornecedores.value = item["fornecedores"]

            self.preco_custo.value = str(item.get("preco_custo", "0.00"))
            self.preco_venda.value = str(item.get("preco_venda", "0.00"))
        else:
            self.dialog.title.value = "Adicionar Produto"
            self.preco_custo.value = ""
            self.preco_venda.value = ""

        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True

    def fechar(self, e=None):
        self.dialog.open = False
        if self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
        self.limpar_campos()
        self.carregar_produtos()
        print("Fechou modal produto")
        self.page.update()

    def salvar(self, e):
        # salvar sem overlay de loading
        produto = {
            "id": self.produto_id,
            "nome": self.nome.value,
            "codigo": self.codigo.value,
            "quantidade": int(self.quantidade.value),
            "marca": self.marca.value,
            "fornecedores": self.fornecedores.value,
            "preco_custo": float(self.preco_custo.value or 0),
            "preco_venda": float(self.preco_venda.value or 0),
        }
        try:
            if self.produto_id:
                self.on_salvar_alteracoes(produto)
            else:
                self.on_salvar(produto)
        finally:
            self.fechar()

    def limpar_campos(self):

        # LIMPA OS CAMPOS
        self.produto_id = None
        self.nome.value = ""
        self.codigo.value = ""
        self.quantidade.value = ""
        self.marca.value = ""
        self.fornecedores.value = ""

        self.preco_custo.value = ""
        self.preco_venda.value = ""

    def salvar_alteracoes(self, e):
        produto = {
            "id": self.produto_id,  # ✅ ID CORRETO
            "nome": self.nome.value,
            "codigo": self.codigo.value,
            "quantidade": int(self.quantidade.value),
            "marca": self.marca.value,
            "fornecedores": self.fornecedores.value,
            "preco_custo": float(self.preco_custo.value or 0),
            "preco_venda": float(self.preco_venda.value or 0),
        }
        self.limpar_campos()
        self.fechar()
        self.on_salvar_alteracoes(produto)
        pass
