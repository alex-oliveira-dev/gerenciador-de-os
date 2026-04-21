import flet as ft
import os
import shutil
import re
from math import floor
from backend.services.company_service import CompanyService
from interface.components.alertaSnack import alertSnackBarMensage


class ConfiguracoesView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.service = CompanyService()
        self.assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "assets")
        )
        os.makedirs(self.assets_dir, exist_ok=True)
        # pasta dedicada para logos (usar sempre company_logo.jpg)
        self.logo_dir = os.path.join(self.assets_dir, "logo")
        os.makedirs(self.logo_dir, exist_ok=True)
        self.logo_path = os.path.join(self.logo_dir, "company_logo.jpg")
        # computed target preview size (px) based on PDF layout
        self._logo_target_w = 100
        self._logo_target_h = 100

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
                    field.update()
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

        btn_upload_logo = ft.ElevatedButton("CARREGAR LOGO", on_click=self._pick_logo)
        btn_clear_logo = ft.ElevatedButton("REMOVER LOGO", on_click=self._remover_logo)
        btn_salvar = ft.ElevatedButton(
            "SALVAR CONFIGURAÇÕES",
            on_click=self._salvar,
            bgcolor=ft.Colors.GREEN_400,
            color=ft.Colors.WHITE,
        )

        # layout consistente com as outras views do sistema
        self.layout = ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column([self.logo_preview], width=140),
                            ft.Column([
                                btn_upload_logo,
                                btn_clear_logo,
                                ft.Text("FORMATOS: PNG/JPG"),
                            ]),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        spacing=20,
                    ),
                    self.nome_field,
                    self.endereco_field,
                    ft.Row([self.cep_field, self.estado_field, self.bairro_field]),
                    self.telefone_field,
                    self.cpf_cnpj_field,
                    ft.Row([btn_salvar], alignment=ft.MainAxisAlignment.END),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                expand=True,
                spacing=20,
            ),
            bgcolor=ft.Colors.WHITE,
            border_radius=12,
            padding=24,
        )

        self._load()

    def _get_pdf_logo_dimensions(self):
        # Parse backend/utils/pdf_generator.py to extract PDF logo measures (mm)
        try:
            pdf_path = os.path.join(
                os.path.dirname(__file__), "..", "..", "backend", "utils", "pdf_generator.py"
            )
            pdf_path = os.path.abspath(pdf_path)
            if not os.path.exists(pdf_path):
                # try relative to project root
                pdf_path = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), "..", "..", "backend", "utils", "pdf_generator.py")
                )
            text = open(pdf_path, "r", encoding="utf-8").read()
            # header logo width (logo_w = 36)
            m = re.search(r"logo_w\s*=\s*([0-9]+(\.[0-9]+)?)", text)
            logo_w = float(m.group(1)) if m else None
            # find row_h and fields list to compute logo_h = row_h * len(fields) * 0.95
            m_row = re.search(r"row_h\s*=\s*([0-9]+(\.[0-9]+)?)", text)
            row_h = float(m_row.group(1)) if m_row else None
            fields_block = None
            m_fields = re.search(r"fields\s*=\s*\[([\s\S]*?)\]", text)
            if m_fields:
                fields_block = m_fields.group(1)
                # count tuples like ("Nome", ...)
                fields_count = len(re.findall(r"\([\s]*['\"]", fields_block))
            else:
                fields_count = None

            if logo_w is None and row_h is None:
                return None

            if logo_w is None:
                # fallback width guess
                logo_w = 36.0
            if row_h is None or fields_count is None:
                # fallback height guess
                logo_h = logo_w * 1.2
            else:
                table_h = row_h * fields_count
                logo_h = table_h * 0.95

            # convert FPDF units (mm) to px approx at 96dpi: 1 mm ~= 3.78 px
            mm_to_px = 3.78
            w_px = max(48, floor(logo_w * mm_to_px))
            h_px = max(48, floor(logo_h * mm_to_px))
            return (w_px, h_px)
        except Exception:
            return None

    def _pick_logo(self, e=None):
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(
            title="Selecione o arquivo de logo",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp")],
        )
        root.destroy()
        if not path:
            return
        try:
            _, ext = os.path.splitext(path)
            ext = ext.lower() if ext else ".png"
            # target filename: company_logo.jpg (overwrite existing file first)
            dst_jpg = os.path.join(self.logo_dir, "company_logo.jpg")
            TARGET_W, TARGET_H = 100, 100
            try:
                # remove existing file first if present
                if os.path.exists(dst_jpg):
                    try:
                        os.remove(dst_jpg)
                    except Exception:
                        pass

                from PIL import Image

                im = Image.open(path)
                # convert to RGB and preserve aspect ratio: fit into TARGET box then center on white
                if im.mode in ("RGBA", "LA"):
                    im = im.convert("RGBA")
                else:
                    im = im.convert("RGB")

                im.thumbnail((TARGET_W, TARGET_H), Image.LANCZOS)
                bg = Image.new("RGB", (TARGET_W, TARGET_H), (255, 255, 255))
                offset = ((TARGET_W - im.width) // 2, (TARGET_H - im.height) // 2)
                try:
                    if im.mode == "RGBA":
                        bg.paste(im.convert("RGBA"), offset, im.split()[-1])
                    else:
                        bg.paste(im, offset)
                except Exception:
                    bg.paste(im, offset)
                # save as JPG
                bg.save(dst_jpg, format="JPEG", quality=95)
                self.logo_path = dst_jpg
            except Exception:
                # fallback: remove existing and copy original file to the target name
                try:
                    if os.path.exists(dst_jpg):
                        try:
                            os.remove(dst_jpg)
                        except Exception:
                            pass
                    shutil.copy(path, dst_jpg)
                    self.logo_path = dst_jpg
                except Exception:
                    alertSnackBarMensage(
                        self.page,
                        "Erro ao salvar logo. Verifique permissões.",
                        bgcolor=ft.Colors.RED_400,
                    )
            self._load_logo_preview()
        except Exception as err:
            print("Erro ao copiar logo:", err)
            alertSnackBarMensage(
                self.page,
                "Erro ao carregar logo selecionada.",
                bgcolor=ft.Colors.RED_400,
            )

    def _load_logo_preview(self):
        self.logo_preview.controls.clear()
        if os.path.exists(self.logo_path):
            try:
                import base64
                with open(self.logo_path, "rb") as f:
                    data = f.read()
                ext = os.path.splitext(self.logo_path)[1].lower().replace(".", "")
                mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
                b64 = base64.b64encode(data).decode("ascii")
                data_uri = f"data:{mime};base64,{b64}"
                # preview at the fixed target size used for PDFs
                PREVIEW_W, PREVIEW_H = 100, 100
                self.logo_preview.controls.append(
                    ft.Image(src=data_uri, width=PREVIEW_W, height=PREVIEW_H)
                )
            except Exception:
                self.logo_preview.controls.append(ft.Text("Logo presente (não renderizável)"))
        else:
            self.logo_preview.controls.append(ft.Text("Nenhum logo carregado"))

        try:
            self.page.update()
        except Exception:
            pass

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
            alertSnackBarMensage(self.page, "Configurações salvas")
        except Exception as err:
            print("Erro ao salvar config:", err)

    def _remover_logo(self, e=None):
        try:
            if os.path.exists(self.logo_path):
                os.remove(self.logo_path)
            self.service.deletar_logo()
            self._load_logo_preview()
            alertSnackBarMensage(self.page, "Logo removido")
        except Exception as err:
            print("Erro ao remover logo:", err)
