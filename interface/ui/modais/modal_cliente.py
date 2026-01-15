import flet as ft


class ModalCliente:
    def __init__(self, page, adicionar_cliente, editar_cliente):
        self.page = page
        self.adicionar_cliente = adicionar_cliente
        self.editar_cliente = editar_cliente
        self.cliente_id = None

        self.nome = ft.TextField(label="Nome", on_change=self._upper_text)
        self.cpf = ft.TextField(label="CPF", on_change=self._upper_text)
        self.telefone = ft.TextField(label="Telefone", on_change=self._upper_text)
        self.email = ft.TextField(label="Email", on_change=self._upper_text)
        self.endereco = ft.TextField(label="Endereço", on_change=self._upper_text)

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("", color=ft.Colors.BLUE_700),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.nome, self.cpf]),
                        ft.Row([self.telefone, self.email]),
                        ft.Row([self.endereco]),
                    ],
                    tight=True,
                    width=800,
                    spacing=10,
                ),
                bgcolor=ft.Colors.WHITE,
                border_radius=12,
                padding=24,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar),
                ft.ElevatedButton(
                    "Salvar",
                    on_click=self.salvar,
                    bgcolor=ft.Colors.BLUE_400,
                    color=ft.Colors.WHITE,
                ),
            ],
        )
        # overlay removido para agilizar interação

    def _upper_text(self, e):
        if e.control.value is not None:
            e.control.value = e.control.value.upper()
            self.page.update()

    def abrir_modal(self, cliente=None):
        self.limpar_campos()
        if cliente:
            self.cliente_id = cliente["id"]
            self.dialog.title.value = "Editar Cliente"
            self.nome.value = cliente["nome"]
            self.cpf.value = cliente["cpf"]
            self.telefone.value = cliente["telefone"]
            self.email.value = cliente["email"]
            self.endereco.value = cliente["endereco"]
        else:
            self.dialog.title.value = "Adicionar Cliente"
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True

    def fechar(self, e=None):
        self.dialog.open = False
        if self.dialog in self.page.overlay:
            self.page.overlay.remove(self.dialog)
        self.limpar_campos()

    def salvar(self, e):
        cliente = {
            "id": self.cliente_id,
            "nome": self.nome.value,
            "cpf": self.cpf.value,
            "telefone": self.telefone.value,
            "email": self.email.value,
            "endereco": self.endereco.value,
        }
        try:
            if self.cliente_id:
                self.editar_cliente(cliente)
            else:
                self.adicionar_cliente(cliente)
        finally:
            self.fechar()

    def limpar_campos(self):
        self.cliente_id = None
        self.nome.value = ""
        self.cpf.value = ""
        self.telefone.value = ""
        self.email.value = ""
        self.endereco.value = ""
        pass
