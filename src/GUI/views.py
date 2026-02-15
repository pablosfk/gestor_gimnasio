import flet as ft
from .styles import MenuButton
from .theme import MenuTheme
from .tables import Tablas
from .assets.themes.colors import Colors
from .controllers import gym_controller, gym_state # Importamos el estado y controlador
from .contexts.service_context import GymServiceContext
from domain.entities import Rutina, Instructor, Cliente, ENTIDADES
from typing import get_type_hints
from datetime import datetime

@ft.component
def AppView():
    # AQUÍ SÍ es legal usar el context porque estamos en el renderizado
    servicio = ft.use_context(GymServiceContext)

    @ft.component
    def Navigation():
        return ft.Container(
            padding=10,
            bgcolor=ft.Colors.SECONDARY_CONTAINER,
            alignment=ft.Alignment.CENTER,
            content = ft.Column(
                    width=130,
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
        state, _ = ft.use_state(gym_state)

        def IsAllFieldsFilled(tipos):
            for control in state.add_fields:
                es_fecha = tipos.get(control.data) == datetime
                if es_fecha and not control.controls[0].value:
                    return False
                elif not es_fecha and not control.value:
                    return False
            return True

        def AddRegistro(e): # Agregamos 'e' por el evento del botón
            entidad = ENTIDADES[state.tabla_actual]
            tipos = get_type_hints(entidad)
            
            # 1. Validación Previa
            if not IsAllFieldsFilled(tipos):
                for control in state.add_fields:
                    es_fecha = tipos.get(control.data) == datetime
                    # Usamos la referencia .input que inyectamos en controllers.py
                    target = control.input if hasattr(control, "input") else control
                    
                    if not target.value:
                        # Soporte para ambos tipos de error (TextField/Dropdown)
                        if hasattr(target, "error"): target.error = "Requerido"
                        if hasattr(target, "error_text"): target.error_text = "Requerido"
                        target.border_color = Colors.INPUT_ERROR_BORDE
                    target.update()
                return # Cortamos la ejecución si falta algo

            # 2. Recolección y Casteo
            payload = {"id": 0} # ID placeholder para el constructor
            for control in state.add_fields:
                target = control.input if hasattr(control, "input") else control
                nombre_campo = target.data
                valor_raw = target.value
                tipo_esperado = tipos[nombre_campo]

                if not valor_raw:
                    payload[nombre_campo] = None
                elif tipo_esperado == datetime:
                    # Guardamos en formato ISO (YYYY-MM-DD) para la DB
                    payload[nombre_campo] = datetime.strptime(valor_raw, "%d-%m-%Y").strftime("%Y-%m-%d")
                elif "int" in str(tipo_esperado) or tipo_esperado == int:
                    payload[nombre_campo] = int(valor_raw)
                else:
                    payload[nombre_campo] = valor_raw

            # 3. Envío al Servicio y Limpieza
            try:
                nueva_entidad = entidad(**payload)
                servicio.buscar_todos(entidad) # Verificación rápida opcional
                servicio.añadir(nueva_entidad) 
                
                # Éxito: Cerramos y Refrescamos
                ft.context.page.pop_dialog()
                gym_controller.GetTabla(servicio=servicio, entidad=entidad)
                print(f"Guardado exitoso en {state.tabla_actual}")
                
            except Exception as ex:
                print(f"Error al guardar en DB: {ex}")

        Sheet = ft.BottomSheet(
            on_dismiss=lambda e: ft.context.page.pop_dialog(),
            scrollable=True,
            content=ft.Container(
                padding=30,
                width=350,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                    scroll=ft.ScrollMode.ADAPTIVE,
                    controls=[
                        ft.Column(controls=state.add_fields),
                        ft.Button("Agregar", on_click=AddRegistro),
                    ],
                ),
            ),
        )

        return ft.Container(
            bgcolor=ft.Colors.SURFACE,
            padding=25,
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    Tablas(datos=state.datos_actuales, columnas=state.columnas_actuales),
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
                            icon_color=ft.Colors.GREEN, 
                            icon_size=40,
                            on_click=lambda e: ft.context.page.show_dialog(Sheet),
                            ),
                        alignment=ft.Alignment.BOTTOM_RIGHT,
                    ) if state.columnas_actuales else ft.Container(),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    
    return ft.Container(
        expand=True, # Ocupa todo el espacio que le da la página
        bgcolor = ft.Colors.SURFACE,
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

'''
        def AddRegistro():
            payload = {}
            entidad = ENTIDADES[state.tabla_actual]
            tipos = get_type_hints(entidad)

            for control in state.add_fields:
                nombre_campo = control.data # Aquí recuperamos el 'nombre' o 'fecha_inicio'
                valor_raw = control.value if hasattr(control, "value") else control.controls[0].value # Por si es DatePicker
                
                # En este punto, valor_raw es un string, por lo que debemos castearlo
                # según el tipo esperado. Vamos armando un diccionario que luego se convertirá en un objeto real.
                # Dado que este sistema está orientado en ORM, el servicio espera un objeto real. Por lo tanto,
                # debemos castear los valores según el tipo esperado.
                tipo_esperado = tipos[nombre_campo]
                
                if valor_raw is None or valor_raw == "":
                    payload[nombre_campo] = None
                elif tipo_esperado == int:
                    payload[nombre_campo] = int(valor_raw)
                elif tipo_esperado == datetime:
                    payload[nombre_campo] = valor_raw 
                else:
                    payload[nombre_campo] = valor_raw
            
                # Ponemos un ID por defecto para poder crear la instancia sin error, luego se descartará en infraestructura.
                payload["id"] = 0

            # Creamos el objeto real y lo mandamos al servicio
            entidad_lista = entidad(**payload)
            servicio.añadir(entidad_lista)
            
            if IsAllFieldsFilled(tipos):
                # Actualizamos el estado de la tabla y cerramos el sheet
                ft.context.page.pop_dialog()
                gym_controller.GetTabla(servicio=servicio, entidad=entidad)
            else:
                for control in state.add_fields:
                    # 1. Identificamos el control que recibe el error (el primero del Stack si es fecha)
                    es_fecha = tipos.get(control.data) == datetime
                    target = control.controls[0] if es_fecha else control
                    
                    # 2. Validamos si está vacío
                    if not target.value:
                        # Seteamos el mensaje de error según lo que el control soporte
                        # Intentamos con .error y con .error_text
                        if hasattr(target, "error"):
                            target.error = "Campo requerido"
                        if hasattr(target, "error_text"):
                            target.error_text = "Campo requerido"
                            
                        target.border_color = Colors.INPUT_ERROR_BORDE
                        target.update()
                    else:
                        # 3. Si tiene valor, limpiamos errores y ponemos color de éxito
                        if hasattr(target, "error"):
                            target.error = None
                        if hasattr(target, "error_text"):
                            target.error_text = None
                        
                        target.border_color = Colors.INPUT_SUCCESS_BORDE
                        target.update()
'''