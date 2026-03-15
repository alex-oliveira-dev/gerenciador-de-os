import flet as ft
from interface.components.alertaSnack import alertSnackBarMensage


class ModalCliente:
    def __init__(self, page, adicionar_cliente, editar_cliente):
        self.page = page
        self.adicionar_cliente = adicionar_cliente
        self.editar_cliente = editar_cliente
        self.cliente_id = None

        self.nome = ft.TextField(label="Nome")
        self.cpf = ft.TextField(label="CPF")
        self.telefone = ft.TextField(label="Telefone")
        self.email = ft.TextField(label="Email")
        self.endereco = ft.TextField(label="Endereço")

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
        self.page.update()

    def fechar(self, e=None):
        self.dialog.open = False
        self.limpar_campos()
        self.page.update()

    def salvar(self, e):
        cliente = {
            "id": self.cliente_id,
            "nome": self.nome.value,
            "cpf": self.cpf.value,
            "telefone": self.telefone.value,
            "email": self.email.value,
            "endereco": self.endereco.value,
        }
        if not (cliente["nome"] or "").strip():
            alertSnackBarMensage(
                self.page,
                "Informe ao menos o nome do cliente.",
                bgcolor=ft.Colors.RED_400,
            )
            return

        try:
            if self.cliente_id:
                self.editar_cliente(cliente)
            else:
                self.adicionar_cliente(cliente)
            self.fechar()
        except Exception as erro:
            alertSnackBarMensage(
                self.page,
                f"Erro ao salvar cliente: {erro}",
                bgcolor=ft.Colors.RED_400,
            )

    def limpar_campos(self):
        self.cliente_id = None
        self.nome.value = ""
        self.cpf.value = ""
        self.telefone.value = ""
        self.email.value = ""
        self.endereco.value = ""
