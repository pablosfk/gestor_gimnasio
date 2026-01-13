import flet as ft

def MenuButton():
    return ft.ButtonStyle(
        shape=ft.RoundedRectangleBorder(radius=4),
        bgcolor=ft.ColorScheme.on_primary_container,
        color=ft.ColorScheme.primary,
    )