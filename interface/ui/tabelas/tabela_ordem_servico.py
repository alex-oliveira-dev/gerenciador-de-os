import flet as ft
from backend.services.ordem_servico_service import (
    OrdemServicoService,
    ordem_servico_service,
)
from interface.ui.modais.modal_nova_ordem_servico import ModalAdicionarOrdemServico


class TabelaOrdemServico:
    def __init__(
        self,
        page: ft.Page,
        dialog_adicionar_ordem_servico,
        excluir_ordem_servico,
        editar_ordem_servico,
        carregar_ordens_servico,
        mostrar_snack_mensagem,
    ):
        self.page = page
        self.carregar_ordens_servico_callback = carregar_ordens_servico
        self.modal_nova_ordem_servico = ModalAdicionarOrdemServico(
            self.page,
            editar_ordem_servico,
            dialog_adicionar_ordem_servico,
            mostrar_snack_mensagem,
            self.popular_tabela_ordem_servico,
        )
        self.on_excluir = excluir_ordem_servico
        # armazenar callback opcional para mostrar mensagens; pode ser None
        self.mostrar_snack_mensagem = mostrar_snack_mensagem

        # Inicializa componentes da tabela
        self.mensagem_tabela_ordem_vazia = ft.Text(
            "NENHUMA O.S. CADASTRADA!",
            text_align=ft.TextAlign.CENTER,
            color=ft.Colors.RED_400,
            size=20,
            weight=ft.FontWeight.BOLD,
        )
        self.lista_itens_ordem_servico = ft.ListView(
            expand=True,
            spacing=0,
            padding=0,
        )
        self.tabela_ordem_servico = ft.Container(
            border=ft.border.all(2, ft.Colors.BLACK54),
            border_radius=8,
            content=ft.Column(
                spacing=0,
                controls=[
                    self._cabecalho_ordem_servico(),
                    ft.Container(
                        expand=True,
                        content=self.lista_itens_ordem_servico,
                    ),
                ],
            ),
        )
        self.botao_adicionar = ft.Button(
            "ADICIONAR O.S.",
            icon=ft.Icons.ADD,
            on_click=lambda e: self.modal_nova_ordem_servico.abrir_modal_adicionar_ordem_servico(),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.BLUE_100,
                color=ft.Colors.BLACK,
            ),
        )
        self.botao_pdf = ft.Button(
            "GERAR PDF O.S.",
            icon=ft.Icons.PICTURE_AS_PDF,
            on_click=self.gerar_pdf_ordem_servico,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                bgcolor=ft.Colors.GREEN_100,
                color=ft.Colors.BLACK,
            ),
        )
        self.layout = ft.Column(
            [
                ft.Row(
                    [self.botao_adicionar, self.botao_pdf],
                    alignment=ft.MainAxisAlignment.START,
                ),
                self.tabela_ordem_servico,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            spacing=20,
            on_scroll="auto",
        )

    def _mostrar_snack_mensagem(self, mensagem: str):
        # usa o callback se fornecido e chamável, caso contrário usa page.snack_bar
        try:
            if callable(self.mostrar_snack_mensagem):
                self.mostrar_snack_mensagem(mensagem)
                return
        except Exception:
            pass
        # fallback para exibir snack bar pela página
        try:
            from flet import SnackBar, Text

            self.page.snack_bar = SnackBar(Text(mensagem), open=True)
            self.page.update()
        except Exception:
            # último recurso: print
            print(mensagem)
        # fim do fallback

    # continuação da inicialização do objeto (antes estava indentado incorretamente)

    def gerar_pdf_ordem_servico(self, e=None):
        from backend.utils.pdf_generator import gerar_pdf_ordem_servico

        ordens = (
            self.carregar_ordens_servico_callback()
            if callable(self.carregar_ordens_servico)
            else []
        )
        if not ordens:
            self._mostrar_snack_mensagem("Nenhuma O.S. para gerar PDF.")
            return
        for ordem in ordens:
            gerar_pdf_ordem_servico(ordem, pasta="interface/assets/os/")
        self._mostrar_snack_mensagem("PDFs das O.S. gerados em interface/assets/os/")

    def on_editar(self, i):
        self.modal_nova_ordem_servico.abrir_modal_editar_ordem_servico(i)

    def on_excluir(self, i):
        self.on_excluir(i)

    def _cabecalho_ordem_servico(self):
        return ft.Container(
            bgcolor=ft.Colors.GREY_300,
            padding=10,
            border=ft.border.only(bottom=ft.BorderSide(2, ft.Colors.BLACK54)),
            content=ft.Row(
                [
                    ft.Text(
                        "Nº O.S.",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "DATA ABERT.",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "CLIENTE",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Text(
                        "VEÍCULO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    # ft.Text(
                    #     "DEFEITO",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    ft.Text(
                        "STATUS",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    # ft.Text(
                    #     "TECNICO",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    # ft.Text(
                    #     "SERVIÇO",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    # ft.Text(
                    #     "SERV. EXECULTADOS",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    ft.Text(
                        "VALOR SERVIÇO",
                        expand=0,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    # ft.Text(
                    #     "Peças",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    # ft.Text(
                    #     "Valor Peças",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    # ft.Text(
                    #     "Valor Total",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    # ft.Text(
                    #     "DATA FECHAM.",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    ft.Text(
                        "PGTO",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                    # ft.Text(
                    #     "SITUAÇÃO",
                    #     expand=1,
                    #     weight=ft.FontWeight.BOLD,
                    #     text_align=ft.TextAlign.CENTER,
                    #     color=ft.Colors.BLACK,
                    # ),
                    ft.Text(
                        "AÇÕES",
                        expand=1,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER,
                        color=ft.Colors.BLACK,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        )

    def popular_tabela_ordem_servico(self):
        self.lista_itens_ordem_servico.controls.clear()
        if self.carregar_ordens_servico_callback:
            ordens = self.carregar_ordens_servico_callback()
            print(ordens)
        else:
            ordens = []
        if not ordens:
            self.lista_itens_ordem_servico.controls.append(
                self.mensagem_tabela_ordem_vazia
            )
        else:
            for ordem in ordens:

                def atualizar_status(e, ordem=ordem):
                    novo_status = e.control.value
                    ordem["status"] = novo_status
                    ordem_servico_service.editar_ordem_servico(ordem)
                    self.popular_tabela_ordem_servico()

                def atualizar_pagamento(e, ordem=ordem):
                    nova_situacao = e.control.value
                    ordem["situacao_pagamento"] = nova_situacao
                    ordem_servico_service.editar_ordem_servico(ordem)
                    self.popular_tabela_ordem_servico()

                self.lista_itens_ordem_servico.controls.append(
                    ft.Container(
                        padding=10,
                        border=ft.border.only(
                            bottom=ft.BorderSide(1, ft.Colors.BLACK54)
                        ),
                        content=ft.Row(
                            [
                                ft.Text(
                                    str(ordem.get("id", "")),
                                    expand=0,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    str(ordem.get("data_abertura", "")),
                                    expand=1,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    str(ordem.get("cliente", "")),
                                    expand=1,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                ft.Text(
                                    str(ordem.get("veiculo", "")),
                                    expand=1,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                # ft.Text(
                                #     str(ordem.get("defeito_relatado", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                ft.Dropdown(
                                    expand=1,
                                    value=ordem.get("status", "Aberta"),
                                    options=[
                                        ft.dropdown.Option(s)
                                        for s in [
                                            "Aberta",
                                            "Em andamento",
                                            "Aguardando peça",
                                            "Finalizada",
                                            "Cancelada",
                                        ]
                                    ],
                                    on_select=atualizar_status,
                                    dense=True,
                                ),
                                # ft.Text(
                                #     str(ordem.get("responsavel", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                # ft.Text(
                                #     str(ordem.get("servico", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                # ft.Text(
                                #     str(ordem.get("servico_executado", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                ft.Text(
                                    f"R$ {ordem.get('valor_total', 0.0):.2f}",
                                    expand=1,
                                    text_align=ft.TextAlign.CENTER,
                                ),
                                # ft.Text(
                                #     str(ordem.get("pecas_utilizadas", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                # ft.Text(
                                #     f"R$ {ordem.get('valor_pecas', 0.0):.2f}",
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                # ft.Text(
                                #     f"R$ {ordem.get('valor_total', 0.0):.2f}",
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                # ft.Text(
                                #     str(ordem.get("data_fechamento", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                # ft.Text(
                                #     str(ordem.get("forma_pagamento", "")),
                                #     expand=1,
                                #     text_align=ft.TextAlign.CENTER,
                                # ),
                                ft.Dropdown(
                                    expand=0,
                                    value=ordem.get("situacao_pagamento", "Pendente"),
                                    options=[
                                        ft.dropdown.Option(s)
                                        for s in ["Pendente", "Pago"]
                                    ],
                                    on_select=atualizar_pagamento,
                                    dense=True,
                                ),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color=ft.Colors.BLUE,
                                            tooltip="Editar",
                                            on_click=lambda e, i=ordem: self.on_editar(
                                                i
                                            ),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.PICTURE_AS_PDF,
                                            icon_color=ft.Colors.GREEN,
                                            tooltip="Gerar PDF",
                                            on_click=lambda e, i=ordem: self.gerar_pdf_ordem_servico_individual(
                                                i
                                            ),
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=ft.Colors.RED,
                                            tooltip="Excluir",
                                            on_click=lambda e, i=ordem: self.on_excluir(
                                                i
                                            ),
                                        ),
                                    ],
                                    spacing=4,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    expand=1,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    )
                )
        self.page.update()

    def gerar_pdf_ordem_servico_individual(self, ordem):
        from backend.utils.pdf_generator import gerar_pdf_ordem_servico

        gerar_pdf_ordem_servico(ordem, pasta="interface/assets/os/")
        self._mostrar_snack_mensagem(f"PDF da O.S. {ordem.get('id', '')} gerado!")

    def carregar_ordens_servico(self):
        return ordem_servico_service.listar_ordens_servico()
