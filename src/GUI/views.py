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
                        content = "Usuarios",
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

        def SendRegistroCallback(e):
            """Delega a SendRegistro del controlador, detectando si es ADD o UPDATE."""
            entidad = ENTIDADES[state.tabla_actual]
            es_actualizacion = state.entidad_a_editar is not None
            
            # Delegamos al controlador con el flag correcto
            guardado_exitosamente = gym_controller.SendRegistro(servicio, entidad, es_actualizacion=es_actualizacion)
            
            # Cerrar el sheet SOLO si se guardó exitosamente
            if guardado_exitosamente:
                # Limpiar modo edición al guardar
                gym_controller.state.entidad_a_editar = None
                ft.context.page.pop_dialog()

        def cancelar_formulario(e):
            """Cancela y descarta el formulario (limpia edición si la hay)."""
            gym_controller.state.entidad_a_editar = None
            ft.context.page.pop_dialog()

        def on_sheet_dismiss(e):
            """Al cerrar el Sheet (por click afuera), solo limpiar sin cerrar nada más."""
            gym_controller.state.entidad_a_editar = None

        def crear_sheet():
            """Crea un nuevo BottomSheet con los campos actuales (siempre fresco)."""
            # Botón dinámico: cambia según si es ADD o UPDATE
            boton_texto = "Guardar cambios" if state.entidad_a_editar else "Agregar"
            
            return ft.BottomSheet(
                on_dismiss=lambda e: on_sheet_dismiss(e),
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
                            ft.Row(
                                controls=[
                                    ft.Button(boton_texto, on_click=SendRegistroCallback, expand=True),
                                    ft.Button("Cancelar", on_click=cancelar_formulario, expand=True),
                                ],
                                spacing=10,
                            ),
                        ],
                    ),
                ),
            )

        def abrir_sheet_edicion():
            """Abre un nuevo Sheet cuando se inicia modo edición."""
            if state.entidad_a_editar:
                sheet = crear_sheet()
                ft.context.page.show_dialog(sheet)

        def abrir_sheet_add():
            """Limpia el modo edición y abre un nuevo Sheet para agregar."""
            entidad = ENTIDADES[state.tabla_actual]
            # Regenerar campos sin precarga (limpia todos los valores a "")
            gym_controller.GetTabla(servicio, entidad)
            # Limpiar modo edición para que el formulario sea de ADD
            gym_controller.state.entidad_a_editar = None
            # Abrir un Sheet nuevo (fresco)
            sheet = crear_sheet()
            ft.context.page.show_dialog(sheet)

        def use_effect_edicion():
            """Hook reactivo: abre Sheet cuando entidad_a_editar cambia a no-None."""
            if state.entidad_a_editar:
                abrir_sheet_edicion()
        
        ft.use_effect(use_effect_edicion, [state.entidad_a_editar])

        # Callbacks para la tabla
        def call_qr(id_registro):
            entidad_tipo = ENTIDADES[state.tabla_actual]
            gym_controller.mostrar_qr(servicio, entidad_tipo, id_registro)

        def call_delete(id_registro, nombre_registro):
            entidad_tipo = ENTIDADES[state.tabla_actual]
            gym_controller.eliminar_registro(servicio, entidad_tipo, id_registro, nombre_registro)

        def call_edit(id_registro):
            entidad_tipo = ENTIDADES[state.tabla_actual]
            # preparar_edicion precarga los datos; use_effect detectará el cambio y abrirá el Sheet
            gym_controller.preparar_edicion(servicio, entidad_tipo, id_registro)

        return ft.Container(
            bgcolor=ft.Colors.SURFACE,
            padding=25,
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                controls=[
                    Tablas(
                        datos=state.datos_actuales, 
                        columnas=state.columnas_actuales,
                        on_qr=call_qr,
                        on_delete=call_delete,
                        on_edit=call_edit
                    ),
                    ft.Container(
                        content=ft.IconButton(
                            icon=ft.Icons.ADD_CIRCLE_OUTLINE, 
                            icon_color=ft.Colors.GREEN, 
                            icon_size=40,
                            on_click=lambda e: abrir_sheet_add(),
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