import flet as ft
import json
from fpdf import FPDF
import tempfile
import os
from backend.utils.pdf_generator import _safe_text


class ModalEditarOrcamento:
    def __init__(self, page, orcamento, salvar_callback):
        self.page = page
        self.orcamento = orcamento.copy()
        self.salvar_callback = salvar_callback
        self.dialog = None
        self._montar_modal()

    def _montar_modal(self):
        self.cliente_field = ft.TextField(
            label="Cliente", value=self.orcamento["cliente"], width=300
        )
        self.data_field = ft.TextField(
            label="Data", value=self.orcamento["data"], width=150
        )
        itens = (
            json.loads(self.orcamento["itens"])
            if isinstance(self.orcamento["itens"], str)
            else self.orcamento["itens"]
        )
        # Buscar lista de produtos para garantir atualização de preço
        from backend.services.estoque_service import EstoqueService

        self.produtos = EstoqueService().listar_produtos()
        self.itens_fields = []
        for item in itens:
            if (
                isinstance(item, dict)
                and "produto" in item
                and "quantidade" in item
                and "preco" in item
            ):
                produto_dropdown = ft.Dropdown(
                    label="Produto",
                    options=[ft.dropdown.Option(p["nome"]) for p in self.produtos],
                    value=item["produto"],
                    width=150,
                )
                qtd_field = ft.TextField(
                    label="Quantidade",
                    value=str(item["quantidade"]),
                    width=80,
                    keyboard_type=ft.KeyboardType.NUMBER,
                )
                preco_field = ft.TextField(
                    label="Preço", value=str(item["preco"]), width=100, read_only=True
                )

                def atualizar_preco(
                    ev=None, prod_dropdown=produto_dropdown, preco_f=preco_field
                ):
                    nome = prod_dropdown.value
                    produto = next(
                        (p for p in self.produtos if p["nome"] == nome), None
                    )
                    if produto:
                        preco_f.value = str(produto.get("preco", "0.00"))
                    else:
                        preco_f.value = "0.00"
                    self.page.update()

                produto_dropdown.on_change = atualizar_preco
                qtd_field.on_change = atualizar_preco
                atualizar_preco()
                self.itens_fields.append(
                    ft.Row([produto_dropdown, qtd_field, preco_field])
                )
        self.total_sem_desc_field = ft.TextField(
            label="Total sem desconto",
            value=str(self.orcamento["total_sem_desconto"]),
            width=200,
        )
        self.total_com_desc_field = ft.TextField(
            label="Total com desconto",
            value=str(self.orcamento["total_com_desconto"]),
            width=200,
        )
        self.btn_salvar = ft.Button("Salvar e Gerar PDF", on_click=self._salvar)
        self.btn_cancelar = ft.OutlinedButton("Cancelar", on_click=self._cancelar)
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Orçamento #{self.orcamento['id']}"),
            content=ft.Column(
                [
                    self.cliente_field,
                    self.data_field,
                    ft.Text("Itens do Orçamento:", weight=ft.FontWeight.BOLD),
                    *self.itens_fields,
                    self.total_sem_desc_field,
                    self.total_com_desc_field,
                ],
                scroll="always",
                width=500,
                height=500,
            ),
            actions=[self.btn_cancelar, self.btn_salvar],
        )

    def abrir(self):
        if self.dialog not in self.page.overlay:
            self.page.overlay.append(self.dialog)
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def _cancelar(self, e):
        self.dialog.open = False
        self.page.update()

    def _salvar(self, e):
        # salvar sem overlay/ProgressRing

        # Atualiza dados do orçamento
        self.orcamento["cliente"] = self.cliente_field.value
        self.orcamento["data"] = self.data_field.value
        itens = []
        total_sem_desc = 0.0
        for row in self.itens_fields:
            produto_nome = row.controls[0].value
            quantidade = int(row.controls[1].value)
            produto = next(
                (p for p in self.produtos if p["nome"] == produto_nome), None
            )
            preco = float(produto["preco"]) if produto and "preco" in produto else 0.0
            itens.append(
                {"produto": produto_nome, "quantidade": quantidade, "preco": preco}
            )
            total_sem_desc += quantidade * preco
        self.orcamento["itens"] = json.dumps(itens)
        self.orcamento["total_sem_desconto"] = total_sem_desc
        self.orcamento["total_com_desconto"] = (
            total_sem_desc  # ajuste se houver desconto
        )
        # Gera PDF
        pdf_path = self._gerar_pdf(self.orcamento, itens)
        # Chama callback para salvar alterações
        self.salvar_callback(self.orcamento, pdf_path)
        self.dialog.open = False
        self.page.update()

    def _gerar_pdf(self, orcamento, itens):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.cell(
            200, 10, txt=f"Orçamento #{orcamento.get('id','')}", ln=True, align="C"
        )

        # Área cliente simples
        left_margin = 10
        usable_w = pdf.w - left_margin - 10
        client_w = int(usable_w * 0.65)
        meta_w = usable_w - client_w
        row_h = 6

        x = left_margin
        y = pdf.get_y()

        pdf.set_xy(x, y)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(client_w, row_h, "Cliente", border=1, align="L", fill=True)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(meta_w, row_h, "Nº / Data", border=1, align="L", fill=True)
        pdf.ln()

        pdf.set_xy(x, pdf.get_y())
        nome_val = _safe_text(orcamento.get("cliente") or "")
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(client_w, row_h, _safe_text(f"Nome: {nome_val}"), border=1)

        meta_x = left_margin + client_w
        pdf.set_xy(meta_x, y + row_h)
        pdf.multi_cell(
            meta_w,
            row_h,
            _safe_text(
                f"Nº: {orcamento.get('id','')}\nData: {orcamento.get('data','')}"
            ),
            border=1,
        )

        curr_y = pdf.get_y()
        pdf.set_xy(x, curr_y)
        pdf.multi_cell(client_w, row_h, f"Tel: \nEmail: \nEndereço: ", border=1)

        pdf.ln(6)

        pdf.cell(200, 10, txt="Itens:", ln=True)
        for item in itens:
            codigo = _safe_text(item.get("codigo", ""))
            produto = _safe_text(item.get("produto", ""))
            quantidade = _safe_text(str(item.get("quantidade", "")))
            preco = _safe_text(f"R$ {item.get('preco', 0):.2f}")
            pdf.cell(
                200,
                10,
                txt=f"{codigo} {produto} - Qtd: {quantidade} - Preço: {preco}",
                ln=True,
            )
        pdf.ln(10)
        pdf.cell(
            200,
            10,
            txt=f"Total sem desconto: R$ {orcamento.get('total_sem_desconto',0):.2f}",
            ln=True,
        )
        pdf.cell(
            200,
            10,
            txt=f"Total com desconto: R$ {orcamento.get('total_com_desconto',0):.2f}",
            ln=True,
        )
        # salvar dentro de interface/assets/orçamentos para consistência
        assets_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "assets", "orçamentos")
        )
        os.makedirs(assets_dir, exist_ok=True)
        pdf_path = os.path.join(assets_dir, f"orcamento_{orcamento.get('id','')}.pdf")
        pdf.output(pdf_path)
        return pdf_path
