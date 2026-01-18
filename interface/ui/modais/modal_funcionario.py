import flet as ft


class ModalFuncionario:
    def __init__(self, page, adicionar_funcionario, editar_funcionario):
        self.page = page
        self.adicionar_funcionario = adicionar_funcionario
        self.editar_funcionario = editar_funcionario
        self.funcionario_id = None

        self.nome = ft.TextField(label="Nome", on_change=self._upper_text)
        self.cargo = ft.TextField(label="Cargo", on_change=self._upper_text)
        self.cpf = ft.TextField(label="CPF", on_change=self._upper_text)
        self.telefone = ft.TextField(label="Telefone", on_change=self._upper_text)
        self.email = ft.TextField(label="Email", on_change=self._upper_text)

        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("", color=ft.Colors.BLUE_700),
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([self.nome, self.cargo]),
                        ft.Row([self.cpf, self.telefone]),
                        ft.Row([self.email]),
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

    def abrir_modal(self, funcionario=None):
        self.limpar_campos()
        if funcionario:
            self.funcionario_id = funcionario["id"]
            self.dialog.title.value = "Editar Funcionário"
            self.nome.value = funcionario["nome"]
            self.cargo.value = funcionario["cargo"]
            self.cpf.value = funcionario["cpf"]
            self.telefone.value = funcionario["telefone"]
            self.email.value = funcionario["email"]
        else:
            self.dialog.title.value = "Adicionar Funcionário"
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.dialog.open = True

    def fechar(self, e=None):
        self.dialog.open = False
        self.limpar_campos()

    def salvar(self, e):
        funcionario = {
            "id": self.funcionario_id,
            "nome": self.nome.value,
            "cargo": self.cargo.value,
            "cpf": self.cpf.value,
            "telefone": self.telefone.value,
            "email": self.email.value,
        }
        try:
            if self.funcionario_id:
                self.editar_funcionario(funcionario)
            else:
                self.adicionar_funcionario(funcionario)
        finally:
            self.fechar()

    def limpar_campos(self):
        self.funcionario_id = None
        self.nome.value = ""
        self.cargo.value = ""
        self.cpf.value = ""
        self.telefone.value = ""
        self.email.value = ""
        pass
