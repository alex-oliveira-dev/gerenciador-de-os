import flet as ft


def alertSnackBarMensage(page, mensagem, bgcolor=ft.Colors.AMBER, text_color=ft.Colors.WHITE, close_icon_color=None):
    if close_icon_color is None:
        close_icon_color = text_color
    # Normaliza o conteúdo: aceita string, Control ou lista de strings/Controls
    content = None

    if isinstance(mensagem, str):
        content = ft.Text(mensagem, color=text_color)
    elif isinstance(mensagem, ft.Control):
        content = mensagem
    elif isinstance(mensagem, (list, tuple)):
        # Se for lista de Controls, agrupa em Column; se for lista de strings, junta
        if len(mensagem) == 0:
            content = ft.Text("", color=text_color)
        else:
            if all(isinstance(m, ft.Control) for m in mensagem):
                content = ft.Column(mensagem)
            else:
                # converte todos para texto
                text = " ".join(str(m) for m in mensagem)
                content = ft.Text(text, color=text_color)
    else:
        # fallback para string
        content = ft.Text(str(mensagem), color=text_color)

    snack = ft.SnackBar(
        content=content,
        close_icon_color=close_icon_color,
        bgcolor=bgcolor,
    )

    # tente usar API de diálogo (recomendada) — fallback para atribuir page.snack_bar
    try:
        # page.show_dialog exige que dialog.content seja um string ou Control visível
        page.show_dialog(snack)
    except Exception:
        try:
            page.snack_bar = snack
            page.snack_bar.open = True
            page.update()
        except Exception:
            # última tentativa silenciosa
            pass