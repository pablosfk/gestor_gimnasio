import flet as ft
from GUI.contexts.service_context import GymServiceContext as servicio
from domain.entities import ENTIDADES, Instructor, Rutina, Cliente
from domain.exceptions import NegocioError, PersistenciaError, ServiceNoDisponibleError
from dataclasses import dataclass, field, fields, asdict
from typing import Type, get_type_hints
from datetime import datetime
from GUI.assets.themes.colors import Colors
from GUI.DTOs import ClienteViewDTO, RutinaViewDTO, InstructorViewDTO

@ft.observable
@dataclass
class GymState:
    # Esta es la "Source of Truth" que la vista (views.py) observará
    datos_actuales: list = field(default_factory=list)
    columnas_actuales: dict = field(default_factory=dict)
    add_fields: list = field(default_factory=list)
    tabla_actual: str = ""

class GymController:
    """
    Controlador principal que utiliza el servicio inyectado por contexto.
    No mantiene estado visual (eso lo hace la View), pero orquesta las llamadas.
    """
    def __init__(self, state: GymState):
        self.state = state

    def _formatear_clientes(self, clientes_crudos):
        lista_formateada = []
        dict_instr = {i.id: f"{i.nombre} {i.apellido}" for i in self.lista_instructores}
        dict_rutinas = {r.id: f"{r.nombre} (id:{r.id})" for r in self.lista_rutinas}

        for c in clientes_crudos:
            lista_formateada.append({
                "Nombre y Apellido": f"{c.nombre} {c.apellido}",
                "Rutina": dict_rutinas.get(c.rutina_id, "N/A"),
                "Ciclo": str(c.ciclo_rutina),
                "Fechas": f"{datetime.strptime(c.fecha_inicio_rutina, '%Y-%m-%d').strftime('%d/%m/%y')} - {datetime.strptime(c.fecha_fin_rutina, '%Y-%m-%d').strftime('%d/%m/%y')}",
                "QR": "🔎", # Ícono de lupa como placeholder para el futuro
                "Edición": "🛠️" 
            })
        return lista_formateada

    def limpiar_error(self, e):
        # 1. La lógica para detectar si es fecha por el diccionario de tipos
        # Usamos getattr(e.control, "data", None) por si el evento viene de un control sin data
        es_fecha = self.state.columnas_actuales.get(getattr(e.control, "data", None)) == datetime
        
        # 2. Definimos el target (Si es fecha, es el primer hijo del Stack; si no, el control mismo)
        if es_fecha:
            target = e.control.parent.controls[0]
        else:
            target = e.control
        
        # 3. Verificamos si tiene algún tipo de error (error o error_text)
        # Esto es lo que añadimos para que los Dropdowns no rompan la función
        tiene_error = getattr(target, "error", None) or getattr(target, "error_text", None)

        if tiene_error:
            # Limpiamos ambos atributos de forma segura
            if hasattr(target, "error"):
                target.error = None
            if hasattr(target, "error_text"):
                target.error_text = None
                
            # Restauramos el borde original
            target.border_color = Colors.INPUT_BORDE
            target.update()

    def GetTabla(self, servicio, entidad: Type[ENTIDADES]): # entidad: clase, no instancia. Por eso ponemos Type[ENTIDADES].
        # ESTO ES PARA EL FORMULARIO (DB Real). Estas van a perdurar sin modificarse.
        columnas_para_formulario = servicio.obtener_columnas_por_entidad(entidad)

        # Obtenemos columnas (incluso si la tabla está vacía)
        self.state.columnas_actuales = servicio.obtener_columnas_por_entidad(entidad) # Columnas reales de la entidad (DB), luego serán modificadas. 
        self.state.tabla_actual = entidad.__name__.lower().capitalize() # Por ejemplo: "Cliente", "Instructor", "Rutina"
        self.inputs_fecha = {}

        # Generamos los campos para agregar un nuevo registro
        if self.state.columnas_actuales:
            fields_box = []

            # Convertimos para efecto visual los datos de la DB de Rutina y Cliente conforme a los DTOs
            # Con esto logramos que si hay nuevos cambios, solo vaste con modificar los DTOs y nada más. 
            try:
                self.lista_instructores = servicio.buscar_todos(Instructor) or []
                self.lista_rutinas = servicio.buscar_todos(Rutina) or []
                # >>> ----------------------------------------------------------------------------- <<<
                datos_db = servicio.buscar_todos(entidad) or []

                if entidad == Cliente:
                    # RE-EMPAQUETADO PARA CLIENTES
                    dict_rutinas = {r.id: f"{r.nombre} (id:{r.id})" for r in self.lista_rutinas}
                    
                    nuevos_datos = []
                    for c in datos_db:
                        f_inicio = datetime.strptime(c.fecha_inicio_rutina, '%Y-%m-%d').strftime('%d/%m/%y')
                        f_fin = datetime.strptime(c.fecha_fin_rutina, '%Y-%m-%d').strftime('%d/%m/%y')
                    
                        nuevos_datos.append(ClienteViewDTO(
                            Nombre_y_Apellido=f"{c.nombre} {c.apellido}",
                            Rutina=dict_rutinas.get(c.rutina_id, "N/A"),
                            Ciclo=c.ciclo_rutina,
                            Fechas=f"{f_inicio} - {f_fin}"
                        ))
                
                    self.state.datos_actuales = nuevos_datos
                    # Importante: Las columnas ahora son las del DTO
                    self.state.columnas_actuales = {f.name: f.type for f in fields(ClienteViewDTO)}

                elif entidad == Rutina:
                    # RE-EMPAQUETADO PARA RUTINAS (para mostrar el ID)
                    self.state.datos_actuales = [RutinaViewDTO(ID=r.id, Nombre=r.nombre) for r in datos_db]
                    self.state.columnas_actuales = {f.name: f.type for f in fields(RutinaViewDTO)}

                elif entidad == Instructor:
                    # RE-EMPAQUETADO PARA INSTRUCTORES
                    self.state.datos_actuales = [InstructorViewDTO(Nombre_y_Apellido=f"{i.nombre} {i.apellido}") for i in datos_db]
                    self.state.columnas_actuales = {f.name: f.type for f in fields(InstructorViewDTO)}
            
                else:
                    self.state.datos_actuales = datos_db
                    self.state.columnas_actuales = columnas_para_formulario

                # >>> ----------------------------------------------------------------------------- <<<
            except Exception as e:
                print(f"Error al cargar catálogos: {e}")
                self.lista_instructores = []
                self.lista_rutinas = []
                self.state.datos_actuales = []

            for campo ,tipo in columnas_para_formulario.items():
                if campo == "instructor_id":
                    # Verificación de existencia para evitar el TypeError
                    hay_instructores = len(self.lista_instructores) > 0
                    
                    fields_box.append(ft.Dropdown(
                        label="Instructor" if hay_instructores else "Sin instructores registrados",
                        expand=True,
                        data=campo,
                        # Si no hay datos, deshabilitamos y mostramos error visual
                        disabled=not hay_instructores,
                        error_text=None if hay_instructores else "Cargue un instructor primero",
                        # Usamos on_select como indica tu versión de Flet
                        on_select=lambda e: self.limpiar_error(e),
                        options=[
                            ft.dropdown.Option(
                                key=str(ins.id), 
                                text=f"{ins.nombre} {ins.apellido}"
                            ) for ins in self.lista_instructores
                        ] if hay_instructores else []
                    ))

                elif campo == "ciclo_rutina":
                    fields_box.append(ft.Dropdown(
                        label="Ciclo de Rutina",
                        expand=True,
                        data=campo,
                        on_select=lambda e: self.limpiar_error(e),
                        options=[
                            ft.dropdown.Option("1"),
                            ft.dropdown.Option("2"),
                            ft.dropdown.Option("3"),
                        ]
                    ))

                elif campo == "rutina_id":
                    hay_rutinas = len(self.lista_rutinas) > 0
                    fields_box.append(ft.Dropdown(
                        label="Rutina" if hay_rutinas else "Sin rutinas registradas",
                        expand=True,
                        data=campo,
                        disabled=not hay_rutinas,
                        on_select=lambda e: self.limpiar_error(e),
                        options=[
                            ft.dropdown.Option(
                                key=str(rut.id), 
                                # Formato sugerido: Nombre (id:X)
                                text=f"{rut.nombre} (id:{rut.id})"
                            ) for rut in self.lista_rutinas
                        ] if hay_rutinas else []
                    ))
                
                elif tipo == datetime:
                    # Textfield que recibe la fecha (solo lectura)
                    self.inputs_fecha[campo] = ft.TextField(
                        label=campo.replace("_", " ").title(),
                        read_only=True,
                        expand=True,
                        value="",
                        data=campo,
                        )

                    # Picker y su lógica de cambio
                    # Usamos una función anidada para capturar 'campo_calendario' correctamente
                    def crear_handle_fecha(txt_field):
                        return lambda e: (
                            setattr(txt_field, "value", e.control.value.strftime("%d-%m-%Y")),
                            setattr(txt_field, "error_text", None), # Limpia error al elegir fecha
                            txt_field.update()
                        )

                    picker = ft.DatePicker(
                        data=campo,
                        on_change=lambda e, clave=campo: (
                            setattr(self.inputs_fecha[clave], "value", e.control.value.strftime("%d-%m-%Y")),
                            setattr(self.inputs_fecha[clave], "error_text", None),
                            self.inputs_fecha[clave].update(),
                            self.limpiar_error(
                                ft.ControlEvent(
                                    name="on_change",
                                    control=self.inputs_fecha[clave],
                                )
                            )
                        )
                    )

                    # Ícono donde pulsar para seleccionar la fecha
                    icono_calendario = ft.IconButton(
                        icon=ft.Icons.CALENDAR_MONTH,
                        height=40,
                        width=40,
                        right= 0,
                        on_click=lambda _, p=picker: (
                            ft.context.page.overlay.append(p) if p not in ft.context.page.overlay else None,
                            setattr(p, "open", True),
                            ft.context.page.update()
                        ),
                    )

                    field = ft.Stack([
                        self.inputs_fecha[campo],
                        icono_calendario],
                        expand=True,
                        data=campo,
                    )

                    # INYECTAMOS REFERENCIAS para que la lógica de error.text lo encuentre
                    field.input = self.inputs_fecha[campo] # Referencia genérica
                    #field.campo_calendario = campo_calendario # Referencia específica
                    #field.value = campo_calendario.value # Para que IsAllFieldsFilled lo lea directo

                    fields_box.append(field)

                elif ("Optional[int]" in str(tipo)) or (tipo == int) or (tipo == float):
                    fields_box.append(ft.TextField(
                        label=campo.replace("_", " ").title(),
                        keyboard_type="number",
                        expand=True,
                        data=campo,
                        on_change=lambda e: self.limpiar_error(e)
                        ))
                
                else:
                    fields_box.append(ft.TextField(
                        label=campo.replace("_", " ").title(),
                        expand=True,
                        data=campo,
                        on_change=lambda e: self.limpiar_error(e)
                        ))

            self.state.add_fields = fields_box
    
    def SendRegistro(self, servicio, entidad: Type[ENTIDADES]):
        """
        Recolecta los datos de add_fields, los valida y los envía al servicio.
        """
        # 1. Validar si todos los campos están llenos
        def IsAllFieldsFilled():
            for control in self.state.add_fields:
                # Si es un Stack (fecha), usamos nuestra referencia inyectada .input
                target = control.input if hasattr(control, "input") else control
                if not target.value or target.value == "":
                    return False
            return True

        if IsAllFieldsFilled():
            # 2. Recolectar datos
            payload = {}
            tipos = self.state.columnas_actuales
            
            for control in self.state.add_fields:
                target = control.input if hasattr(control, "input") else control
                nombre_campo = target.data
                valor_raw = target.value
                
                # Casteo dinámico según el tipo de la columna
                tipo_destino = tipos.get(nombre_campo)
                
                if tipo_destino == datetime:
                    # Convertimos el string "DD-MM-YYYY" al formato que SQLite ama "YYYY-MM-DD"
                    payload[nombre_campo] = datetime.strptime(valor_raw, "%d-%m-%Y").strftime("%Y-%m-%d")
                elif "int" in str(tipo_destino) or tipo_destino == int:
                    payload[nombre_campo] = int(valor_raw)
                else:
                    payload[nombre_campo] = valor_raw

            try:
                # 3. Intentar guardar
                nuevo_obj = entidad(**payload)
                servicio.agregar(nuevo_obj)
                
                # 4. Refrescar la tabla y limpiar campos
                self.GetTabla(servicio, entidad)
                print(f"Registro agregado con éxito en {entidad.__name__}")
                
            except Exception as e:
                print(f"Error al guardar: {e}")
        
        else:
            # 5. Lógica de error visual (la que ya teníamos)
            for control in self.state.add_fields:
                target = control.input if hasattr(control, "input") else control
                if not target.value:
                    if hasattr(target, "error_text"):
                        target.error_text = "Campo requerido"
                    if hasattr(target, "error"):
                        target.error = "Campo requerido"
                    target.border_color = Colors.INPUT_ERROR_BORDE
                target.update()


# Instancia global del ESTADO (Observable)
gym_state = GymState()
# Instancia del controlador que manipula ese estado
gym_controller = GymController(gym_state)
