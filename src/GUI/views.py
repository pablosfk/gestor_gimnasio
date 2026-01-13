import flet as ft
from .styles import MenuButton
from .theme import MenuTheme
from .tables import Tablas
from .controllers import gym_controller, gym_state # Importamos el estado y controlador
from .contexts.service_context import GymServiceContext
from domain.entities import Rutina, Instructor, Cliente

@ft.component
def AppView():
    # AQUÍ SÍ es legal usar el context porque estamos en el renderizado
    servicio = ft.use_context(GymServiceContext)

    @ft.component
    def Navigation():
        return ft.Container(
            padding=20,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            alignment=ft.Alignment.CENTER,
            content = ft.Column(
                    width=150,
                    controls=[
                        MenuCrud(),
                        MenuTheme(),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
        ) 

    @ft.component
    def MenuCrud():
        return ft.Column(
                expand=True,
                controls=[
                    ft.Button(
                        content = "Rutinas",
                        style=MenuButton(),
                        on_click=lambda e: gym_controller.GetTabla(servicio=servicio, entidad=Rutina)
                        ),
                    ft.Button(
                        content = "Instructores",
                        style=MenuButton(),
                        on_click=lambda e: gym_controller.GetTabla(servicio=servicio, entidad=Instructor)
                        ),
                    ft.Button(
                        content = "Clientes",
                        style=MenuButton(),
                        on_click=lambda e: gym_controller.GetTabla(servicio=servicio, entidad=Cliente)
                        ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            )

    @ft.component
    def Body():
        # AQUÍ OCURRE LA MAGIA: Al leer el estado, nos suscribimos a él.
        # Flet 0.80+ detecta que este componente depende de 'gym_state.datos_actuales'
        state, _ = ft.use_state(gym_state) 
        
        return ft.Container(
            bgcolor=ft.Colors.SURFACE,
            padding=25,
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    # Pasamos los datos explícitamente al componente Tablas
                    Tablas(datos=state.datos_actuales, columnas=state.columnas_actuales) 
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    return ft.Container(
        expand=True, # Ocupa todo el espacio que le da la página
        bgcolor = ft.ColorScheme.surface,
        content=ft.Row(
            spacing=0,
            controls= [
                Navigation(),
                ft.VerticalDivider(width=2, color=ft.Colors.ON_SURFACE,),
                Body(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ), 
    )