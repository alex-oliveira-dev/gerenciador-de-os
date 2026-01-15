import flet as ft
import os
import shutil
from backend.services.company_service import CompanyService


class ConfiguracoesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.service = CompanyService()
        self.assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "assets")
        )
        os.makedirs(self.assets_dir, exist_ok=True)
        # pasta dedicada para logos
        self.logo_dir = os.path.join(self.assets_dir, "logo")
        os.makedirs(self.logo_dir, exist_ok=True)
        self.logo_path = os.path.join(self.logo_dir, "company_logo.png")

        # campos
        self.nome_field = ft.TextField(
            label="Nome da Empresa", width=400, bgcolor=ft.Colors.WHITE
        )
        self.endereco_field = ft.TextField(
            label="Endereço", width=400, bgcolor=ft.Colors.WHITE
        )
        self.cep_field = ft.TextField(label="CEP", width=200, bgcolor=ft.Colors.WHITE)
        self.estado_field = ft.TextField(
            label="Estado", width=200, bgcolor=ft.Colors.WHITE
        )
        self.bairro_field = ft.TextField(
            label="Bairro", width=300, bgcolor=ft.Colors.WHITE
        )
        self.telefone_field = ft.TextField(
            label="Telefone", width=200, bgcolor=ft.Colors.WHITE
        )
        self.cpf_cnpj_field = ft.TextField(
            label="CPF/CNPJ", width=300, bgcolor=ft.Colors.WHITE
        )

        # garantir que os textos digitados fiquem em UPPERCASE
        def _to_upper(field):
            try:
                if field.value:
                    field.value = str(field.value).upper()
                    self.page.update()
            except Exception:
                pass

        # associa handlers
        self.nome_field.on_change = lambda e: _to_upper(self.nome_field)
        self.endereco_field.on_change = lambda e: _to_upper(self.endereco_field)
        self.cep_field.on_change = lambda e: _to_upper(self.cep_field)
        self.estado_field.on_change = lambda e: _to_upper(self.estado_field)
        self.bairro_field.on_change = lambda e: _to_upper(self.bairro_field)
        self.telefone_field.on_change = lambda e: _to_upper(self.telefone_field)
        self.cpf_cnpj_field.on_change = lambda e: _to_upper(self.cpf_cnpj_field)

        self.logo_preview = ft.Column(controls=[ft.Text("Nenhum logo carregado")])

        btn_upload_logo = ft.Button("CARREGAR LOGO", on_click=self._pick_logo)
        btn_clear_logo = ft.Button("REMOVER LOGO", on_click=self._remover_logo)
        btn_salvar = ft.Button(
            "SALVAR CONFIGURAÇÕES",
            on_click=self._salvar,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
        )

        self.layout = ft.Column(
            [
                ft.Row(
                    [
                        self.logo_preview,
                        ft.Column(
                            [
                                btn_upload_logo,
                                btn_clear_logo,
                                ft.Text("FORMATOS: PNG/JPG"),
                            ]
                        ),
                    ]
                ),
                self.nome_field,
                self.endereco_field,
                ft.Row([self.cep_field, self.estado_field, self.bairro_field]),
                self.telefone_field,
                self.cpf_cnpj_field,
                ft.Row([btn_salvar]),
            ],
            scroll="auto",
            expand=True,
        )

        self._load()

    def _pick_logo(self, e=None):
        try:
            import tkinter as tk
            from tkinter import filedialog

            root = tk.Tk()
            root.withdraw()
            path = filedialog.askopenfilename(
                title="Selecione o arquivo de logo",
                filetypes=[("Images", "*.png *.jpg *.jpeg *.gif *.bmp")],
            )
            root.destroy()
        except Exception:
            path = None

        if path:
            try:
                # preserve extension
                _, ext = os.path.splitext(path)
                dst = os.path.join(self.logo_dir, f"company_logo{ext}")
                shutil.copy(path, dst)
                self.logo_path = dst
                self._load_logo_preview()
            except Exception as err:
                print("Erro ao copiar logo:", err)

    def _load_logo_preview(self):
        self.logo_preview.controls.clear()
        if os.path.exists(self.logo_path):
            try:
                # carregar imagem em base64 para evitar problemas de URI
                import base64

                with open(self.logo_path, "rb") as f:
                    data = f.read()
                ext = os.path.splitext(self.logo_path)[1].lower().replace(".", "")
                mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
                b64 = base64.b64encode(data).decode("ascii")
                data_uri = f"data:{mime};base64,{b64}"
                self.logo_preview.controls.append(
                    ft.Image(src=data_uri, width=150, height=150)
                )
            except Exception:
                self.logo_preview.controls.append(
                    ft.Text("Logo presente (não renderizável)")
                )
        else:
            self.logo_preview.controls.append(ft.Text("Nenhum logo carregado"))
        self.page.update()

    def _load(self):
        cfg = self.service.obter_config()
        if cfg:
            self.nome_field.value = (cfg.get("nome") or "").upper()
            self.endereco_field.value = (cfg.get("endereco") or "").upper()
            self.cep_field.value = (cfg.get("cep") or "").upper()
            self.estado_field.value = (cfg.get("estado") or "").upper()
            self.bairro_field.value = (cfg.get("bairro") or "").upper()
            self.telefone_field.value = (cfg.get("telefone") or "").upper()
            self.cpf_cnpj_field.value = (cfg.get("cpf_cnpj") or "").upper()
            # se houver logo_path no DB (pode ser relativo), resolve para o caminho absoluto da workspace
            lp = cfg.get("logo_path")
            if lp:
                if not os.path.isabs(lp):
                    base = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), "..", "..")
                    )
                    candidate = os.path.abspath(os.path.join(base, lp))
                else:
                    candidate = lp
                if os.path.exists(candidate):
                    self.logo_path = candidate
        self._load_logo_preview()

    def _salvar(self, e=None):
        data = {
            "nome": (self.nome_field.value or "").upper(),
            "endereco": (self.endereco_field.value or "").upper(),
            "cep": (self.cep_field.value or "").upper(),
            "estado": (self.estado_field.value or "").upper(),
            "bairro": (self.bairro_field.value or "").upper(),
            "telefone": (self.telefone_field.value or "").upper(),
            "cpf_cnpj": (self.cpf_cnpj_field.value or "").upper(),
            # salvar caminho relativo para portabilidade entre máquinas
            "logo_path": None,
        }
        try:
            if self.logo_path and os.path.exists(self.logo_path):
                # relativo à raiz do projeto (dois níveis acima deste arquivo)
                base = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "..")
                )
                rel = os.path.relpath(self.logo_path, start=base)
                data["logo_path"] = rel
        except Exception:
            data["logo_path"] = (
                self.logo_path if os.path.exists(self.logo_path) else None
            )

        try:
            print("[CONFIG] Salvando config:", data)
            self.service.salvar_config(data)
            print("[CONFIG] Salvo com sucesso no service")
            self.page.snack_bar = ft.SnackBar(ft.Text("Configurações salvas"))
            self.page.snack_bar.open = True
        except Exception as err:
            print("Erro ao salvar config:", err)
        self.page.update()

    def _remover_logo(self, e=None):
        try:
            if os.path.exists(self.logo_path):
                os.remove(self.logo_path)
            self.service.deletar_logo()
            self._load_logo_preview()
            self.page.snack_bar = ft.SnackBar(ft.Text("Logo removido"))
            self.page.snack_bar.open = True
        except Exception as err:
            print("Erro ao remover logo:", err)
        self.page.update()
