import flet as ft
from .styles import MenuButton
from .theme import MenuTheme
from .tables import Tablas
from .controllers import gym_controller
from .contexts.service_context import GymServiceContext
from domain.entities import Rutina, Instructor, Cliente

# Temporal:=====================================
#from main import gimnasio_servicios
# ==============================================

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
                        on_click=lambda e: gym_controller.GetTabla(servicio=servicio,entidad=Rutina)
                        ),
                    ft.Button(
                        content = "Instructores",
                        style=MenuButton(),
                        on_click=lambda e: gym_controller.GetTabla(servicio=servicio,entidad=Instructor)
                        ),
                    ft.Button(
                        content = "Clientes",
                        style=MenuButton(),
                        on_click=lambda e: gym_controller.GetTabla(servicio=servicio,entidad=Cliente)
                        ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            )

    @ft.component
    def Body():
        return ft.Container(
            bgcolor=ft.Colors.SURFACE,
            padding=25,
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    Tablas()
                ],
                #alignment=ft.MainAxisAlignment.CENTER,
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
            #horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ), 
    )