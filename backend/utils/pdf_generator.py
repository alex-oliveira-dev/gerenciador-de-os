import os
from fpdf import FPDF


def gerar_pdf_ordem_servico(ordem, pasta="interface/assets/os/"):
    if not os.path.exists(pasta):
        os.makedirs(pasta)

    # Gera PDF simples em arquivo temporário
    from tempfile import mkstemp

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Ordem de Serviço", ln=True, align="C")
    pdf.ln(4)
    # escreve campos principais
    for k, v in ordem.items():
        try:
            pdf.multi_cell(0, 6, txt=f"{k}: {v}")
        except Exception:
            pdf.cell(0, 6, txt=f"{k}: {v}", ln=True)

    nome_arquivo = f"os_{ordem.get('id','')}.pdf"
    caminho = os.path.join(pasta, nome_arquivo)

    # salva em temporário para possível mesclagem com template
    tmp_fd, tmp_path = mkstemp(suffix=".pdf")
    try:
        os.close(tmp_fd)
    except Exception:
        pass
    pdf.output(tmp_path)

    # tenta mesclar com template se existir
    try:
        base_folder = os.path.abspath(pasta)
        stemplate = os.path.join(base_folder, "stemplate_os.pdf")
        # se existir template, mescla: coloca o conteúdo gerado sobre o template
        if os.path.exists(stemplate):
            try:
                from PyPDF2 import PdfReader, PdfWriter

                reader_t = PdfReader(stemplate)
                reader_tmp = PdfReader(tmp_path)
                writer = PdfWriter()

                for i, tpage in enumerate(reader_t.pages):
                    if i < len(reader_tmp.pages):
                        try:
                            tmp_page = reader_tmp.pages[i]
                            try:
                                tmp_page.merge_page(tpage)
                            except Exception:
                                pass
                            writer.add_page(tmp_page)
                        except Exception:
                            writer.add_page(tpage)
                    else:
                        writer.add_page(tpage)

                # anexar páginas extras do tmp (se existirem)
                for j in range(len(reader_t.pages), len(reader_tmp.pages)):
                    writer.add_page(reader_tmp.pages[j])

                with open(caminho, "wb") as f:
                    writer.write(f)
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
                return caminho
            except Exception as e:
                print("[PDF O.S.] falha ao mesclar com stemplate_os.pdf:", e)

    except Exception:
        pass

    # fallback: copia o PDF gerado para destino
    try:
        from shutil import copyfile

        copyfile(tmp_path, caminho)
    except Exception as e:
        print("[PDF O.S.] erro ao salvar PDF:", e)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

    return caminho


import os
from fpdf import FPDF
from backend.services.company_service import CompanyService
import zipfile
import tempfile
import re
import unicodedata


def _safe_text(s):
    if s is None:
        return ""
    s = str(s)
    # common replacements
    s = s.replace("\u2013", "-")
    s = s.replace("\u2014", "-")
    s = s.replace("\u2018", "'")
    s = s.replace("\u2019", "'")
    s = s.replace("\u201c", '"')
    s = s.replace("\u201d", '"')
    s = s.replace("\u2026", "...")
    s = s.replace("\u00a0", " ")
    # normalize compatibility characters but keep accents (latin-1)
    try:
        s.encode("latin-1")
        return s
    except Exception:
        # fallback: remove any non-latin1 by replacement
        return s.encode("latin-1", "replace").decode("latin-1")


class MeuPDF(FPDF):
    def header(self):
        # Cabeçalho com título à esquerda e logo à direita
        try:
            left_margin = 10
            right_margin = 10
            logo_w = 36
            spacing = 8

            # posição do logo (à direita)
            logo_x = self.w - right_margin - logo_w
            logo_y = 10

            # tenta inserir logo a partir de self.company ou assets
            inserted = False
            try:
                if hasattr(self, "company") and isinstance(self.company, dict):
                    logo_cfg = self.company.get("logo_path")
                else:
                    logo_cfg = None
                candidates = []
                if logo_cfg:
                    candidates.append(logo_cfg)
                try:
                    assets_logo_dir = os.path.abspath(
                        os.path.join(
                            os.path.dirname(__file__),
                            "..",
                            "..",
                            "interface",
                            "assets",
                            "logo",
                        )
                    )
                    if os.path.isdir(assets_logo_dir):
                        for fname in os.listdir(assets_logo_dir):
                            if fname.lower().startswith("company_logo"):
                                candidates.append(os.path.join(assets_logo_dir, fname))
                except Exception:
                    pass

                # dedupe
                seen = set()
                candidates = [
                    p for p in candidates if p and not (p in seen or seen.add(p))
                ]

                # não inserir imagem no header (evita duplicação) — apenas registre candidatos
                inserted = False
                # dedupe já feito acima; armazena candidatos para uso posterior
                try:
                    self._logo_candidates = candidates
                except Exception:
                    pass
            except Exception:
                pass

            # registra estado para uso posterior evitando duplicação
            try:
                self._header_logo_inserted = bool(inserted)
                self._header_logo_size = logo_w
            except Exception:
                pass

            # desenha título à esquerda, respeitando espaço da logo
            title_x = left_margin
            title_w = self.w - left_margin - right_margin - (logo_w + spacing)
            self.set_xy(title_x, logo_y + 4)
            self.set_font("Arial", "B", 12)
            self.set_text_color(40, 40, 40)
            try:
                self.cell(title_w, 8, "Orçamento Comercial", ln=False, align="L")
            except Exception:
                self.cell(0, 8, "Orçamento Comercial", ln=False, align="L")

            # linha separadora abaixo do cabeçalho
            self.ln(12)
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.5)
            yline = self.get_y() - 6
            self.line(10, yline, self.w - 10, yline)
            # apenas registre candidatos de logo; a inserção real será feita
            # em `gerar_pdf()` para permitir alinhamento com a tabela de empresa
            try:
                logo_cfg = None
                if hasattr(self, "company") and isinstance(self.company, dict):
                    logo_cfg = self.company.get("logo_path")
                candidates = []
                if logo_cfg:
                    candidates.append(logo_cfg)
                try:
                    assets_logo_dir = os.path.abspath(
                        os.path.join(
                            os.path.dirname(__file__),
                            "..",
                            "..",
                            "interface",
                            "assets",
                            "logo",
                        )
                    )
                    if os.path.isdir(assets_logo_dir):
                        for fname in os.listdir(assets_logo_dir):
                            if fname.lower().startswith("company_logo"):
                                candidates.append(os.path.join(assets_logo_dir, fname))
                except Exception:
                    pass
                # dedupe
                seen = set()
                candidates = [
                    p for p in candidates if p and not (p in seen or seen.add(p))
                ]
                try:
                    self._logo_candidates = candidates
                except Exception:
                    pass
            except Exception:
                pass
        except Exception:
            # fallback simples
            self.set_font("Arial", "B", 12)
            self.set_text_color(40, 40, 40)
            self.cell(0, 8, "Orçamento Comercial", ln=True, align="C")
            self.ln(2)
            self.set_draw_color(200, 200, 200)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), self.w - 10, self.get_y())
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Página {self.page_no()}/{{nb}}", align="C")


def gerar_pdf(orcamento: dict, itens: list, caminho_saida: str, logo_path: str = None):
    pdf = MeuPDF()
    pdf.alias_nb_pages()
    # carregar configuração da empresa e deixar disponível no objeto PDF
    try:
        cfg = CompanyService().obter_config()
    except Exception:
        cfg = None
    if cfg:
        pdf.company = cfg
        # se não foi passado logo_path explicitamente, tente usar o do config
        if not logo_path and cfg.get("logo_path"):
            logo_path = cfg.get("logo_path")

    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Se existir um exemplo .docx (teste.docx), extraia texto bruto e desenhe no topo
    try:
        template_docx = os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "interface",
            "assets",
            "orçamentos",
            "teste.docx",
        )
        template_docx = os.path.abspath(template_docx)
        if os.path.exists(template_docx):
            try:
                with zipfile.ZipFile(template_docx) as z:
                    with z.open("word/document.xml") as f:
                        xml = f.read().decode("utf-8")
                # Extrai textos entre <w:t>...</w:t>
                texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml, flags=re.DOTALL)
                # Junta em parágrafos aproximados: separa por </w:p>
                paras = re.split(r"</w:p>", xml)
                para_texts = []
                for p in paras:
                    ts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, flags=re.DOTALL)
                    if ts:
                        # limpa tags simples
                        txt = " ".join(ts)
                        txt = re.sub(r"\s+", " ", txt).strip()
                        if txt:
                            para_texts.append(txt)
                # desenha os primeiros parágrafos do template no topo do PDF
                if para_texts:
                    pdf.set_font("Arial", "B", 12)
                    for i, p_text in enumerate(para_texts[:6]):
                        p_text = _safe_text(p_text)
                        if i == 0:
                            pdf.cell(0, 8, p_text, ln=True, align="C")
                        else:
                            pdf.set_font("Arial", "", 10)
                            pdf.multi_cell(0, 6, p_text)
                    pdf.ln(6)
            except Exception as e:
                print("[PDF] não foi possível usar teste.docx como template:", e)
    except Exception:
        pass

    # --- Tabela de configurações da empresa (tabela à esquerda, logo à direita) ---
    try:
        if cfg and isinstance(cfg, dict):
            left_margin = 10
            right_margin = 10
            usable_w = pdf.w - left_margin - right_margin

            # tenta aproveitar tamanho definido no header para manter coerência
            header_logo_size = getattr(pdf, "_header_logo_size", None)
            logo_w = header_logo_size if header_logo_size else 50
            spacing = 8
            # tabela à esquerda, logo à direita
            table_x = left_margin
            table_y = pdf.get_y()
            table_w = usable_w - logo_w - spacing
            label_w = int(table_w * 0.30)
            value_w = table_w - label_w
            row_h = 8

            # desenha logo à direita (debug do caminho caso não apareça)
            logo_cfg = cfg.get("logo_path") if cfg else None
            candidates = []
            # procura por arquivos company_logo.* em interface/assets/logo (PRIORIDADE)
            try:
                assets_logo_dir = os.path.abspath(
                    os.path.join(
                        os.path.dirname(__file__),
                        "..",
                        "..",
                        "interface",
                        "assets",
                        "logo",
                    )
                )
                if os.path.isdir(assets_logo_dir):
                    for fname in os.listdir(assets_logo_dir):
                        if fname.lower().startswith("company_logo"):
                            candidates.append(os.path.join(assets_logo_dir, fname))
            except Exception:
                pass
            # depois tenta os caminhos vindos do parâmetro e do config (fallback)
            if logo_path:
                candidates.append(logo_path)
            if logo_cfg:
                candidates.append(logo_cfg)

            # inserir logo ao lado da tabela, escalando para a altura da tabela de campos
            logo_x = left_margin + table_w + spacing
            logo_y = table_y
            logo_inserted_fp = False
            # prefere candidatos coletados no header (se houver)
            candidates_final = getattr(pdf, "_logo_candidates", None) or candidates
            # altura desejada: total de linhas da tabela (com um pequeno padding)
            table_h = row_h * len(
                [
                    f
                    for f in [
                        ("Nome", (cfg.get("nome") or "")),
                        ("Endereço", (cfg.get("endereco") or "")),
                        ("CEP", (cfg.get("cep") or "")),
                        ("Estado", (cfg.get("estado") or "")),
                        ("Telefone", (cfg.get("telefone") or "")),
                        ("CPF/CNPJ", (cfg.get("cpf_cnpj") or "")),
                    ]
                ]
            )
            logo_h = table_h * 0.95
            try:
                for cand in candidates_final:
                    try:
                        cand_abs = (
                            cand if os.path.isabs(cand) else os.path.abspath(cand)
                        )
                    except Exception:
                        cand_abs = cand
                    if not cand_abs or not os.path.exists(cand_abs):
                        continue
                    try:
                        pdf.image(cand_abs, x=logo_x, y=logo_y, h=logo_h)
                        logo_inserted_fp = True
                        break
                    except Exception as img_e:
                        try:
                            from PIL import Image

                            im = Image.open(cand_abs)
                            if im.mode in ("RGBA", "LA"):
                                bg = Image.new("RGB", im.size, (255, 255, 255))
                                bg.paste(im, mask=im.split()[-1])
                                im = bg
                            tmp_logo_fd, tmp_logo_path = tempfile.mkstemp(suffix=".png")
                            os.close(tmp_logo_fd)
                            im.save(tmp_logo_path, format="PNG")
                            try:
                                pdf.image(tmp_logo_path, x=logo_x, y=logo_y, h=logo_h)
                                logo_inserted_fp = True
                                try:
                                    os.remove(tmp_logo_path)
                                except Exception:
                                    pass
                                break
                            except Exception:
                                try:
                                    os.remove(tmp_logo_path)
                                except Exception:
                                    pass
                        except Exception:
                            pass
            except Exception:
                pass

            # campos da tabela (à esquerda)
            fields = [
                ("Nome", (cfg.get("nome") or "")),
                ("Endereço", (cfg.get("endereco") or "")),
                ("CEP", (cfg.get("cep") or "")),
                ("Estado", (cfg.get("estado") or "")),
                ("Telefone", (cfg.get("telefone") or "")),
                ("CPF/CNPJ", (cfg.get("cpf_cnpj") or "")),
            ]

            # garante que a tabela começa na posição calculada
            try:
                pdf.set_xy(table_x, table_y)
            except Exception:
                pass

            fill = True
            for label, value in fields:
                pdf.set_font("Arial", "B", 10)
                (
                    pdf.set_fill_color(245, 245, 245)
                    if fill
                    else pdf.set_fill_color(255, 255, 255)
                )
                pdf.cell(label_w, row_h, label, border=1, align="L", fill=True)
                pdf.set_font("Arial", "", 10)
                txt = str(value).replace("\n", " ")
                pdf.cell(value_w, row_h, (txt[:120]), border=1, align="L", fill=True)
                pdf.ln()
                fill = not fill

            # ajustar cursor para abaixo do maior entre logo e tabela
            end_table_y = pdf.get_y()
            logo_bottom = table_y + (logo_h if logo_inserted_fp else (logo_w * 0.6))
            next_y = max(end_table_y, logo_bottom) + 6
            pdf.set_y(next_y)
    except Exception:
        pass

    # Área do cliente e número do orçamento (tabela com bordas)
    pdf.set_text_color(0, 0, 0)
    left_margin = 10
    right_margin = 10
    usable_w = pdf.w - left_margin - right_margin
    # largura: 65% para cliente, 35% para número/data
    client_w = int(usable_w * 0.65)
    meta_w = usable_w - client_w
    row_h = 8

    x = left_margin
    y = pdf.get_y()

    # Cabeçalho das duas colunas
    pdf.set_xy(x, y)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(client_w, row_h, "Cliente", border=1, align="L", fill=True)
    pdf.cell(meta_w, row_h, "Orçamento", border=1, align="L", fill=True)
    pdf.ln()

    # Conteúdo do bloco do cliente (linhas com label / valor)
    nome_val = _safe_text(
        orcamento.get("cliente_nome") or orcamento.get("cliente") or ""
    )
    telefone = _safe_text(orcamento.get("cliente_telefone") or "")
    email = _safe_text(orcamento.get("cliente_email") or "")
    endereco = _safe_text(orcamento.get("cliente_endereco") or "")

    client_label_w = int(client_w * 0.25)
    client_value_w = client_w - client_label_w

    pdf.set_font("Arial", "B", 9)
    pdf.cell(client_label_w, row_h, "Nome", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(client_value_w, row_h, nome_val, border=1, align="L")

    # meta coluna (Nº na mesma linha)
    meta_label_w = int(meta_w * 0.5)
    meta_value_w = meta_w - meta_label_w
    numero = _safe_text(str(orcamento.get("numero") or orcamento.get("id") or ""))
    pdf.set_font("Arial", "B", 9)
    pdf.cell(meta_label_w, row_h, "Nº", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(meta_value_w, row_h, numero, border=1, align="L")
    pdf.ln()

    pdf.set_font("Arial", "B", 9)
    pdf.cell(client_label_w, row_h, "Telefone", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(client_value_w, row_h, telefone, border=1, align="L")

    # meta coluna (Data na mesma linha)
    data = _safe_text(str(orcamento.get("data") or ""))
    pdf.set_font("Arial", "B", 9)
    pdf.cell(meta_label_w, row_h, "Data", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(meta_value_w, row_h, data, border=1, align="L")
    pdf.ln()

    pdf.set_font("Arial", "B", 9)
    pdf.cell(client_label_w, row_h, "Email", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 9)
    pdf.cell(client_value_w, row_h, email, border=1, align="L")
    # coluna meta vazia nesta linha
    pdf.cell(meta_w, row_h, "", border=1, align="L")
    pdf.ln()

    pdf.set_font("Arial", "B", 9)
    pdf.cell(client_label_w, row_h, "Endereço", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 9)
    # quebra o endereço em múltiplas linhas se necessário
    pdf.multi_cell(client_value_w, row_h, endereco, border=1)
    # garantir que a coluna meta abaixo do endereço esteja com borda
    curr_y = pdf.get_y()
    pdf.set_xy(x + client_w, curr_y - row_h)
    pdf.cell(meta_w, row_h, "", border=1)
    pdf.ln(12)

    # Cabeçalho da tabela de peças (Produto | Qtd | Preço)
    pdf.set_font("Arial", "B", 11)
    pdf.set_fill_color(230, 230, 230)
    left_margin = 10
    right_margin = 10
    usable_w = pdf.w - left_margin - right_margin

    col_prod = int(usable_w * 0.68)
    col_qtd = int(usable_w * 0.12)
    col_preco = usable_w - (col_prod + col_qtd)

    pdf.cell(col_prod, 8, "Produto", border=1, align="L", fill=True)
    pdf.cell(col_qtd, 8, "Qtd", border=1, align="C", fill=True)
    pdf.cell(col_preco, 8, "Preço", border=1, align="R", fill=True)
    pdf.ln()

    # Garanta ao menos 10 linhas: preenche abaixo com linhas vazias
    rows_required = max(10, len(itens))
    pdf.set_font("Arial", "", 11)
    for idx in range(rows_required):
        if idx % 2 == 0:
            pdf.set_fill_color(255, 255, 255)
        else:
            pdf.set_fill_color(245, 245, 245)

        if idx < len(itens):
            it = itens[idx]
            nome = _safe_text(str(it.get("produto", "")))[:120]
            qtd = _safe_text(str(it.get("quantidade", "")))
            preco = _safe_text(f"R$ {float(it.get('preco', 0)):.2f}")
        else:
            nome = ""
            qtd = ""
            preco = ""

        pdf.cell(col_prod, 8, nome, border=1, fill=True)
        pdf.cell(col_qtd, 8, qtd, border=1, align="C", fill=True)
        pdf.cell(col_preco, 8, preco, border=1, align="R", fill=True)
        pdf.ln()

    pdf.ln(6)
    # Tabela de totais com bordas no canto direito
    left_margin = 10
    right_margin = 10
    usable_w = pdf.w - left_margin - right_margin
    box_w = int(usable_w * 0.35)
    box_x = left_margin + usable_w - box_w
    box_y = pdf.get_y()
    row_h = 8

    # Mensagem adicional (à esquerda dos totais) — exibe somente se houver
    mensagem = (orcamento.get("mensagem_adicional") or "").strip()
    if mensagem:
        msg_w = usable_w - box_w - 6
        if msg_w > 80:
            pdf.set_xy(left_margin, box_y)
            pdf.set_font("Arial", "", 10)
            # desenha caixa de mensagem com borda
            pdf.multi_cell(msg_w, 6, _safe_text(mensagem), border=1)
            # observa: não alterar box_y para manter totals no topo

    # primeira linha: Total sem desconto
    pdf.set_xy(box_x, box_y)
    pdf.set_font("Arial", "", 10)
    label_w = int(box_w * 0.65)
    value_w = box_w - label_w
    pdf.cell(label_w, row_h, "Total sem desconto", border=1, align="L", fill=True)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(
        value_w,
        row_h,
        f"R$ {float(orcamento.get('total_sem_desconto',0)):.2f}",
        border=1,
        align="R",
    )
    pdf.ln()

    # segunda linha: Desconto
    pdf.set_x(box_x)
    pdf.set_font("Arial", "", 10)
    pdf.cell(label_w, row_h, "Desconto", border=1, align="L", fill=True)
    pdf.set_font("Arial", "", 10)
    pdf.cell(
        value_w,
        row_h,
        f"R$ {float(orcamento.get('desconto',0)):.2f}",
        border=1,
        align="R",
    )
    pdf.ln()

    # terceira linha: Total com desconto
    pdf.set_x(box_x)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(label_w, row_h, "Total com desconto", border=1, align="L", fill=True)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(
        value_w,
        row_h,
        f"R$ {float(orcamento.get('total_com_desconto',0)):.2f}",
        border=1,
        align="R",
    )
    pdf.ln()

    # escreve em arquivo temporário primeiro
    import tempfile

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".pdf")
    try:
        os.close(tmp_fd)
    except Exception:
        pass
    pdf.output(tmp_path)

    # diagnóstico: inspeciona imagens no PDF temporário (antes de mesclar)
    try:
        import fitz

        try:
            doc_tmp = fitz.open(tmp_path)
            for pnum, pg in enumerate(doc_tmp):
                imgs = pg.get_images(full=True)
                if imgs:
                    for img in imgs:
                        xref = img[0]
                        bbox = None
                        try:
                            bbox = pg.get_image_bbox(xref)
                        except Exception:
                            bbox = None
                        dims = None
                        try:
                            pix = fitz.Pixmap(doc_tmp, xref)
                            dims = (pix.width, pix.height)
                        except Exception:
                            dims = None
                        print(
                            "[PDF] tmp image - page",
                            pnum + 1,
                            "xref",
                            xref,
                            "bbox",
                            bbox,
                            "dims",
                            dims,
                        )
            doc_tmp.close()
        except Exception as e:
            print("[PDF] falha ao inspecionar tmp PDF:", e)
    except Exception:
        pass

    # Prefer stemplate.pdf (template com placeholders). Se não existir, tenta teste.pdf (mesclagem simples).
    try:
        base_folder = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "interface",
                "assets",
                "orçamentos",
            )
        )
        stemplate = os.path.join(base_folder, "stemplate.pdf")
        teste = os.path.join(base_folder, "teste.pdf")

        if os.path.exists(stemplate):
            try:
                import fitz

                doc = fitz.open(stemplate)

                # mapa de tokens -> valores
                tokens = {}
                if cfg and isinstance(cfg, dict):
                    tokens.update(
                        {
                            "{COMPANY_NOME}": _safe_text(cfg.get("nome") or ""),
                            "{COMPANY_ENDERECO}": _safe_text(cfg.get("endereco") or ""),
                            "{COMPANY_CEP}": _safe_text(cfg.get("cep") or ""),
                            "{COMPANY_ESTADO}": _safe_text(cfg.get("estado") or ""),
                            "{COMPANY_BAIRRO}": _safe_text(cfg.get("bairro") or ""),
                            "{COMPANY_TELEFONE}": _safe_text(cfg.get("telefone") or ""),
                            "{COMPANY_CPF_CNPJ}": _safe_text(cfg.get("cpf_cnpj") or ""),
                        }
                    )
                tokens.update(
                    {
                        "{CLIENTE_NOME}": _safe_text(
                            orcamento.get("cliente_nome")
                            or orcamento.get("cliente")
                            or ""
                        ),
                        "{CLIENTE_TELEFONE}": _safe_text(
                            orcamento.get("cliente_telefone") or ""
                        ),
                        "{CLIENTE_EMAIL}": _safe_text(
                            orcamento.get("cliente_email") or ""
                        ),
                        "{CLIENTE_ENDERECO}": _safe_text(
                            orcamento.get("cliente_endereco") or ""
                        ),
                        "{ORC_NUMERO}": _safe_text(
                            str(orcamento.get("numero") or orcamento.get("id") or "")
                        ),
                        "{ORC_DATA}": _safe_text(str(orcamento.get("data") or "")),
                        "{ORC_DESCONTO}": _safe_text(
                            f"R$ {float(orcamento.get('desconto',0)):.2f}"
                        ),
                        "{ORC_TOTAL_SEM_DESCONTO}": _safe_text(
                            f"R$ {float(orcamento.get('total_sem_desconto',0)):.2f}"
                        ),
                        "{ORC_TOTAL_COM_DESCONTO}": _safe_text(
                            f"R$ {float(orcamento.get('total_com_desconto',0)):.2f}"
                        ),
                    }
                )

                for idx in range(1, max(12, len(itens)) + 1):
                    it = itens[idx - 1] if idx - 1 < len(itens) else {}
                    tokens[f"{{ITEM_{idx}_COD}}"] = _safe_text(it.get("codigo") or "")
                    tokens[f"{{ITEM_{idx}_PRODUTO}}"] = _safe_text(
                        it.get("produto") or ""
                    )
                    tokens[f"{{ITEM_{idx}_QTD}}"] = _safe_text(
                        str(it.get("quantidade") or "")
                    )
                    tokens[f"{{ITEM_{idx}_PRECO}}"] = _safe_text(
                        f"R$ {float(it.get('preco',0)):.2f}"
                    )

                # alias de tokens comuns para compatibilidade com templates diferentes
                for idx in range(1, max(12, len(itens)) + 1):
                    it = itens[idx - 1] if idx - 1 < len(itens) else {}
                    code = _safe_text(it.get("codigo") or "")
                    prod = _safe_text(it.get("produto") or "")
                    qtd = _safe_text(str(it.get("quantidade") or ""))
                    preco = _safe_text(f"R$ {float(it.get('preco',0)):.2f}")
                    tokens[f"{{ITEM_COD_{idx}}}"] = code
                    tokens[f"{{ITEMCOD_{idx}}}"] = code
                    tokens[f"{{ITEM_{idx}COD}}"] = code
                    tokens[f"{{ITEM_{idx}_PROD}}"] = prod
                    tokens[f"{{ITEM_PROD_{idx}}}"] = prod
                    tokens[f"{{ITEM_QTD_{idx}}}"] = qtd
                    tokens[f"{{ITEM_PRECO_{idx}}}"] = preco

                # tokens genéricos para a primeira linha (compatibilidade com templates simples)
                if len(itens) > 0:
                    first = itens[0]
                    tokens.setdefault("{CODIGO}", _safe_text(first.get("codigo") or ""))
                    tokens.setdefault(
                        "{PRODUTO}", _safe_text(first.get("produto") or "")
                    )
                    tokens.setdefault(
                        "{QTD}", _safe_text(str(first.get("quantidade") or ""))
                    )
                    tokens.setdefault(
                        "{PRECO}", _safe_text(f"R$ {float(first.get('preco',0)):.2f}")
                    )

                replaced_count = 0
                logo_inserted = False
                for page in doc:
                    for token, value in tokens.items():
                        try:
                            areas = page.search_for(token)
                        except Exception:
                            areas = []
                        for r in areas:
                            # decide alinhamento
                            if (
                                "_PRECO" in token
                                or "TOTAL" in token
                                or "DESCONTO" in token
                            ):
                                align = 2
                            elif "_QTD" in token:
                                align = 1
                            else:
                                align = 0

                            fontsize = 12
                            fontname = "helv"
                            try:
                                text_width = fitz.get_text_length(
                                    value, fontsize=fontsize, fontname=fontname
                                )
                            except Exception:
                                text_width = fontsize * 0.6 * max(1, len(value))
                            max_w = r.width - 2
                            while fontsize > 6 and text_width > max_w:
                                fontsize -= 1
                                try:
                                    text_width = fitz.get_text_length(
                                        value, fontsize=fontsize, fontname=fontname
                                    )
                                except Exception:
                                    text_width = fontsize * 0.6 * max(1, len(value))

                            page.insert_textbox(
                                r,
                                value,
                                fontsize=fontsize,
                                fontname=fontname,
                                align=align,
                            )
                            replaced_count += 1

                    try:
                        logo_areas = page.search_for("{LOGO}")
                    except Exception:
                        logo_areas = []
                    if logo_areas:
                        # construir candidatos priorizando interface/assets/logo
                        logo_cfg = cfg.get("logo_path") if cfg else None
                        candidates = []
                        try:
                            assets_logo_dir = os.path.abspath(
                                os.path.join(
                                    os.path.dirname(__file__),
                                    "..",
                                    "..",
                                    "interface",
                                    "assets",
                                    "logo",
                                )
                            )
                            if os.path.isdir(assets_logo_dir):
                                for fname in os.listdir(assets_logo_dir):
                                    if fname.lower().startswith("company_logo"):
                                        candidates.append(
                                            os.path.join(assets_logo_dir, fname)
                                        )
                        except Exception:
                            pass
                        if logo_path:
                            candidates.append(logo_path)
                        if logo_cfg:
                            candidates.append(logo_cfg)

                        # dedupe
                        seen = set()
                        candidates = [
                            p
                            for p in candidates
                            if p and not (p in seen or seen.add(p))
                        ]

                        inserted = False
                        for cand in candidates:
                            try:
                                cand_abs = (
                                    cand
                                    if os.path.isabs(cand)
                                    else os.path.abspath(cand)
                                )
                            except Exception:
                                cand_abs = cand
                            print(
                                "[PDF] fitz candidato logo:",
                                cand_abs,
                                "exists:",
                                os.path.exists(cand_abs),
                            )
                            if not cand_abs or not os.path.exists(cand_abs):
                                continue
                            for r in logo_areas:
                                try:
                                    page.insert_image(r, filename=cand_abs)
                                    logo_inserted = True
                                    inserted = True
                                except Exception as e:
                                    print(
                                        "[PDF] falha ao inserir logo via fitz para",
                                        cand_abs,
                                        ":",
                                        e,
                                    )
                                    # tentar converter via PIL e re-tentar
                                    try:
                                        from PIL import Image

                                        im = Image.open(cand_abs)
                                        if im.mode in ("RGBA", "LA"):
                                            bg = Image.new(
                                                "RGB", im.size, (255, 255, 255)
                                            )
                                            bg.paste(im, mask=im.split()[-1])
                                            im = bg
                                        tmp_logo_fd, tmp_logo_path = tempfile.mkstemp(
                                            suffix=".png"
                                        )
                                        os.close(tmp_logo_fd)
                                        im.save(tmp_logo_path, format="PNG")
                                        try:
                                            page.insert_image(r, filename=tmp_logo_path)
                                            logo_inserted = True
                                            inserted = True
                                            print(
                                                "[PDF] logo inserida via PIL fallback (fitz) a partir de:",
                                                cand_abs,
                                            )
                                        except Exception as e2:
                                            print(
                                                "[PDF] fitz fallback com PIL falhou para",
                                                cand_abs,
                                                ":",
                                                e2,
                                            )
                                        try:
                                            os.remove(tmp_logo_path)
                                        except Exception:
                                            pass
                                    except Exception as pil_e:
                                        print(
                                            "[PDF] não foi possível usar PIL para converter logo (fitz):",
                                            pil_e,
                                        )
                                if inserted:
                                    break
                            if inserted:
                                break
                        if not inserted:
                            print(
                                "[PDF] nenhum candidato de logo funcionou para inserção via fitz"
                            )

                # se nada foi substituído, faz fallback para mesclar o PDF gerado sobre o template
                if replaced_count == 0:
                    doc.close()
                    print(
                        "[PDF] nenhum placeholder encontrado em stemplate.pdf — fazendo fallback de mesclagem."
                    )
                    try:
                        from PyPDF2 import PdfReader, PdfWriter

                        reader_t = PdfReader(stemplate)
                        reader_tmp = PdfReader(tmp_path)
                        writer = PdfWriter()

                        # garantir que o PDF gerado (reader_tmp) fique por cima do template
                        for i, tpage in enumerate(reader_t.pages):
                            if i < len(reader_tmp.pages):
                                try:
                                    tmp_page = reader_tmp.pages[i]
                                    try:
                                        tmp_page.merge_page(tpage)
                                    except Exception:
                                        pass
                                    writer.add_page(tmp_page)
                                except Exception:
                                    writer.add_page(tpage)
                            else:
                                writer.add_page(tpage)

                        # anexar páginas extras do tmp (se existirem)
                        for j in range(len(reader_t.pages), len(reader_tmp.pages)):
                            writer.add_page(reader_tmp.pages[j])

                        with open(caminho_saida, "wb") as f:
                            writer.write(f)
                        try:
                            os.remove(tmp_path)
                        except Exception:
                            pass
                        return
                    except Exception as e:
                        print("[PDF] fallback de mesclagem falhou:", e)

                # caso contrário salva o documento modificado
                doc.save(caminho_saida)
                doc.close()
            except Exception as e:
                print("[PDF] falha ao aplicar stemplate com fitz:", e)
                try:
                    from shutil import copyfile

                    copyfile(tmp_path, caminho_saida)
                except Exception as e2:
                    print("[PDF] erro ao copiar tmp para destino:", e2)
        elif os.path.exists(teste):
            try:
                from PyPDF2 import PdfReader, PdfWriter

                reader_t = PdfReader(teste)
                reader_tmp = PdfReader(tmp_path)
                writer = PdfWriter()

                for i, tpage in enumerate(reader_t.pages):
                    if i < len(reader_tmp.pages):
                        try:
                            tpage.merge_page(reader_tmp.pages[i])
                        except Exception:
                            pass
                        writer.add_page(tpage)
                    else:
                        writer.add_page(tpage)

                for j in range(len(reader_t.pages), len(reader_tmp.pages)):
                    writer.add_page(reader_tmp.pages[j])

                with open(caminho_saida, "wb") as f:
                    writer.write(f)
            except Exception as e:
                print("[PDF] falha ao mesclar teste.pdf, usando gerado apenas:", e)
                try:
                    from shutil import copyfile

                    copyfile(tmp_path, caminho_saida)
                except Exception as e2:
                    print("[PDF] erro ao copiar PDF temporário:", e2)
        else:
            from shutil import copyfile

            copyfile(tmp_path, caminho_saida)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
    # diagnóstico final: inspeciona imagens embutidas no PDF gerado
    try:
        import fitz

        if os.path.exists(caminho_saida):
            try:
                doc_final = fitz.open(caminho_saida)
                total_images = 0
                imgs_info = []
                for pnum, pg in enumerate(doc_final):
                    imgs = pg.get_images(full=True)
                    if imgs:
                        imgs_info.append((pnum + 1, len(imgs)))
                        total_images += len(imgs)
                print(
                    "[PDF] diagnóstico final - imagens por página:",
                    imgs_info,
                    "total:",
                    total_images,
                )
                doc_final.close()
            except Exception as e:
                print("[PDF] falha ao inspecionar imagens no PDF final:", e)
    except Exception:
        pass
