import flet as ft


def alertSnackBarMensage(page, mensagem, bgcolor=ft.Colors.AMBER, text_color=ft.Colors.WHITE, close_icon_color=None):
    if close_icon_color is None:
        close_icon_color = text_color
    page.snack_bar = ft.SnackBar(
        content=ft.Text(mensagem, color=text_color),
        close_icon_color=close_icon_color,
        bgcolor=bgcolor,
    )
    page.snack_bar.open = True
    page.update()