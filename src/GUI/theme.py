from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

#=============================================================================
# THEME CONTEXT
#=============================================================================

@dataclass(frozen=True)
class ThemeContextValue:
    mode: ft.ThemeMode
    seed_color: ft.Colors
    toggle_mode: Callable[[], None]
    color_name: str = ""
    set_color_name: Callable[[str], None] = lambda name: None
    set_seed_color: Callable[[ft.Colors], None] = lambda color: None


ThemeContext = ft.create_context(
    ThemeContextValue(
        mode=ft.ThemeMode.LIGHT,
        seed_color=ft.Colors.TEAL,
        toggle_mode=lambda: None,
        set_seed_color=lambda color: None,
        color_name="Verde\nazulado",
        set_color_name=lambda name: None,
    )
)

#=============================================================================
# THEME MENU
#=============================================================================

@ft.component
def MenuTheme():
    return ft.Column(
        controls=[
            ThemeModeToggle(),
            ThemeSeedColor(),
        ],
    )

@ft.component
def ThemeModeToggle():
    theme = ft.use_context(ThemeContext)
    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.DARK_MODE
                if theme.mode == ft.ThemeMode.DARK
                else ft.Icons.LIGHT_MODE,
                tooltip="Cambio de modo claro/oscuro",
                on_click=lambda: theme.toggle_mode(),
            ),
            ft.Text(
                value="Modo\nclaro" if theme.mode == ft.ThemeMode.LIGHT else "Modo\noscuro"
            ),
        ]
    )

@ft.component
def ThemeSeedColor():
    theme = ft.use_context(ThemeContext)
    return ft.Row(
        controls=[
            ft.PopupMenuButton(
                icon=ft.Icons.COLOR_LENS_OUTLINED,
                tooltip="Cambio de color de tema",
                items=[
                    PopupColorItem(color=ft.Colors.DEEP_PURPLE, name=f"Púrpura\nprofundo"),
                    PopupColorItem(color=ft.Colors.INDIGO, name="Indigo"),
                    PopupColorItem(color=ft.Colors.BLUE, name="Azul"),
                    PopupColorItem(color=ft.Colors.TEAL, name="Verde\nazulado"),
                    PopupColorItem(color=ft.Colors.GREEN, name="Verde"),
                    PopupColorItem(color=ft.Colors.YELLOW, name="Amarillo"),
                    PopupColorItem(color=ft.Colors.ORANGE, name="Naranja"),
                    PopupColorItem(color=ft.Colors.DEEP_ORANGE, name="Naranja\nprofundo"),
                    PopupColorItem(color=ft.Colors.PINK, name="Rosa"),
                ],
            ),
            ft.Text(theme.color_name),
        ]
    )

@ft.component
def PopupColorItem(color: ft.Colors, name: str) -> ft.PopupMenuItem:
    theme = ft.use_context(ThemeContext)
    return ft.PopupMenuItem(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.COLOR_LENS_OUTLINED, color=color),
                ft.Text(name),
            ],
        ),
        on_click=lambda _: (theme.set_seed_color(color), theme.set_color_name(name)),
    )

#=============================================================================
# THEME APP (AppView envuelto en ThemeContext)
#=============================================================================

# Envolvemos `AppView` con un proveedor de tema para que los componentes que usan
# `ft.use_context(ThemeContext)` reciban `toggle_mode`, `set_seed_color` y `set_color_name` funcionales.
@ft.component
def AppWithTheme(view_builder: Callable[[], ft.Control]): # Recibe la CLASE o FUNCIÓN, no la instancia
    theme_mode, set_theme_mode = ft.use_state(ft.ThemeMode.DARK)
    theme_color, set_theme_color = ft.use_state(ft.Colors.TEAL)
    theme_color_name, set_theme_color_name = ft.use_state("Verde\nazulado")

    toggle_mode = ft.use_callback(
        lambda: set_theme_mode(
            ft.ThemeMode.DARK if theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        ),
        dependencies=[theme_mode],
    )

    set_seed_color = ft.use_callback(lambda color: set_theme_color(color), dependencies=[theme_color])
    set_color_name = ft.use_callback(lambda name: set_theme_color_name(name), dependencies=[theme_color_name])

    theme_value = ft.use_memo(
        lambda: ThemeContextValue(
            mode=theme_mode,
            seed_color=theme_color,
            toggle_mode=toggle_mode,
            set_seed_color=set_seed_color,
            color_name=theme_color_name,
            set_color_name=set_color_name,
        ),
        dependencies=[theme_mode, theme_color, toggle_mode, set_seed_color, theme_color_name, set_color_name],
    )

    def update_theme():
        if not ft.context.page:
            return
        ft.context.page.theme_mode = theme_mode
        ft.context.page.theme = ft.context.page.dark_theme = ft.Theme(color_scheme_seed=theme_color)
        ft.context.page.update()

    ft.use_effect(update_theme, [theme_mode, theme_color])

    return ThemeContext(
        value=theme_value, 
        callback=lambda: view_builder() # <--- AQUÍ se instancia la vista dentro de la burbuja segura
    )