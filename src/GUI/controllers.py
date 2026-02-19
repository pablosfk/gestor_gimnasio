import flet as ft
from GUI.contexts.service_context import GymServiceContext as servicio
from domain.entities import ENTIDADES, Instructor, Rutina, Cliente
from domain.exceptions import NegocioError, PersistenciaError, ServiceNoDisponibleError
from dataclasses import dataclass, field, fields, asdict
from typing import Type, get_type_hints
from datetime import datetime
from GUI.assets.themes.colors import Colors
from GUI.DTOs import ClienteViewDTO, RutinaViewDTO, InstructorViewDTO
import qrcode
import io
import base64

@ft.observable
@dataclass
class GymState:
    # Esta es la "Source of Truth" que la vista (views.py) observará
    datos_actuales: list = field(default_factory=list)
    columnas_actuales: dict = field(default_factory=dict)
    columnas_reales: dict = field(default_factory=dict)  # Columnas reales de la entidad (para UPDATE)
    add_fields: list = field(default_factory=list)
    tabla_actual: str = ""
    entidad_a_editar: object = None  # Almacena la entidad siendo editada para operaciones UPDATE

class GymController:
    """
    Controlador principal que utiliza el servicio inyectado por contexto.
    No mantiene estado visual (eso lo hace la View), pero orquesta las llamadas.
    """
    def __init__(self, state: GymState):
        self.state = state
        self.lista_instructores = []
        self.lista_rutinas = []
        self.inputs_fecha = {}

    def _formatear_clientes(self, clientes_crudos):
        lista_formateada = []
        dict_instr = {i.id: f"{i.nombre} {i.apellido}" for i in self.lista_instructores}
        dict_rutinas = {r.id: f"{r.nombre} (id:{r.id})" for r in self.lista_rutinas}

        for c in clientes_crudos:
            lista_formateada.append({
                "id": c.id,
                "Nombre y Apellido": f"{c.nombre} {c.apellido}",
                "Rutina": dict_rutinas.get(c.rutina_id, "N/A"),
                "Ciclo": str(c.ciclo_rutina),
                "Fechas": f"{datetime.strptime(c.fecha_inicio_rutina, '%Y-%m-%d').strftime('%d/%m/%y')} - {datetime.strptime(c.fecha_fin_rutina, '%Y-%m-%d').strftime('%d/%m/%y')}",
                "QR": "🔎", # Ícono de lupa como placeholder para el futuro
                "Edición": "🛠️" 
            })
        return lista_formateada

    def mostrar_qr(self, servicio, entidad_tipo, id_registro):
        """Genera y muestra un QR basado en el pdf_link de la rutina."""
        url = None
        
        # 1. Obtener la URL dependiendo de la entidad
        try:
            if entidad_tipo == Rutina:
                rutina = servicio.buscar_por_id(Rutina, id_registro)
                url = rutina.pdf_link
            elif entidad_tipo == Cliente:
                cliente = servicio.buscar_por_id(Cliente, id_registro)
                if cliente.rutina_id:
                    rutina = servicio.buscar_por_id(Rutina, cliente.rutina_id)
                    url = rutina.pdf_link
        except Exception as e:
            print(f"Error recuperando link para QR: {e}")

        if not url:
            # Mostrar un snackbar o error si no hay link
            snack = ft.SnackBar(ft.Text("No hay enlace PDF asociado para generar QR"))
            ft.context.page.overlay.append(snack)
            snack.open = True
            ft.context.page.update()
            return

        # 2. Generar QR en memoria
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # 3. Convertir a Base64 para Flet
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        img_control = ft.Image(src=f"data:image/png;base64,{img_str}", width=300, height=300)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Escanea tu Rutina"),
            content=img_control,
            actions=[ft.TextButton("Cerrar", on_click=lambda e: setattr(dlg, "open", False) or ft.context.page.update())],
        )
        ft.context.page.show_dialog(dlg)

    def eliminar_registro(self, servicio, entidad_tipo, id_registro, nombre_registro):
        def ejecutar_eliminacion(e):
            """Callback que se ejecuta al confirmar la eliminación."""
            # Cerramos el diálogo primero
            dlg_confirmacion.open = False
            ft.context.page.update()

            eliminado = False
            mensaje = "No se pudo eliminar el registro"
            try:
                entidad = servicio.buscar_por_id(entidad_tipo, id_registro)
                servicio.eliminar(entidad)
                eliminado = True
                mensaje = "Registro eliminado correctamente"
            except Exception as ex:
                mensaje = str(ex) if str(ex) else "No se pudo eliminar el registro"
                print(f"Error al eliminar: {ex}")
            
            # Refrescar tabla SOLO si la eliminación fue exitosa
            if eliminado:
                try:
                    self.GetTabla(servicio, entidad_tipo)
                except Exception as ex:
                    print(f"Error al refrescar tabla: {ex}")
            
            # Mostrar feedback
            snack = ft.SnackBar(
                ft.Text(mensaje, color=ft.Colors.WHITE),
                bgcolor=ft.Colors.GREEN_700 if eliminado else ft.Colors.RED_700
            )
            ft.context.page.overlay.append(snack)
            snack.open = True
            ft.context.page.update()

        def cancelar(e):
            dlg_confirmacion.open = False
            ft.context.page.update()

        dlg_confirmacion = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Está seguro de eliminar el registro \"{nombre_registro}\"?"),
            actions=[
                ft.TextButton("Cancelar", on_click=cancelar),
                ft.TextButton("Eliminar", on_click=ejecutar_eliminacion,
                    style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
        )
        ft.context.page.show_dialog(dlg_confirmacion)

    def preparar_edicion(self, servicio, entidad_tipo, id_registro):
        """
        1. Busca la entidad.
        2. Carga la tabla con la entidad en modo edición (precargando valores).
        """
        try:
            entidad = servicio.buscar_por_id(entidad_tipo, id_registro)
            # Cargar la tabla en modo edición: GetTabla cargará los campos precargados
            self.GetTabla(servicio, entidad_tipo, entidad_a_editar=entidad)
        except Exception as e:
            print(f"Error al preparar edición: {e}")

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

    def form_gen(self, columnas: dict, valores_precargados: dict = None):
        """Genera campos de formulario. Si valores_precargados es dict, carga esos valores."""
        fields_box = []
        for campo ,tipo in columnas.items():
            if campo == "instructor_id":
                # Verificación de existencia para evitar el TypeError
                hay_instructores = len(self.lista_instructores) > 0
                valor_precargado = valores_precargados.get(campo) if valores_precargados else None
                
                dropdown = ft.Dropdown(
                    label="Instructor" if hay_instructores else "Sin instructores registrados",
                    expand=True,
                    data=campo,
                    # Si no hay datos, deshabilitamos y mostramos error visual
                    disabled=not hay_instructores,
                    error_text=None if hay_instructores else "Cargue un instructor primero",
                    on_select=lambda e: self.limpiar_error(e),
                    options=[
                        ft.dropdown.Option(
                            key=str(ins.id), 
                            text=f"{ins.nombre} {ins.apellido}"
                        ) for ins in self.lista_instructores
                    ] if hay_instructores else []
                )
                if valor_precargado:
                    dropdown.value = str(valor_precargado)
                fields_box.append(dropdown)

            elif campo == "ciclo_rutina":
                valor_precargado = valores_precargados.get(campo) if valores_precargados else None
                dropdown = ft.Dropdown(
                    label="Ciclo de Rutina",
                    expand=True,
                    data=campo,
                    on_select=lambda e: self.limpiar_error(e),
                    options=[
                        ft.dropdown.Option("1"),
                        ft.dropdown.Option("2"),
                        ft.dropdown.Option("3"),
                    ]
                )
                if valor_precargado:
                    dropdown.value = str(valor_precargado)
                fields_box.append(dropdown)

            elif campo == "rutina_id":
                hay_rutinas = len(self.lista_rutinas) > 0
                valor_precargado = valores_precargados.get(campo) if valores_precargados else None
                dropdown = ft.Dropdown(
                    label="Rutina" if hay_rutinas else "Sin rutinas registradas",
                    expand=True,
                    data=campo,
                    error_text=None if hay_rutinas else "Cargue una rutina primero",
                    disabled=not hay_rutinas,
                    on_select=lambda e: self.limpiar_error(e),
                    options=[
                        ft.dropdown.Option(
                            key=str(rut.id), 
                            # Formato sugerido: Nombre (id:X)
                            text=f"{rut.nombre} (id:{rut.id})"
                        ) for rut in self.lista_rutinas
                    ] if hay_rutinas else []
                )
                if valor_precargado:
                    dropdown.value = str(valor_precargado)
                fields_box.append(dropdown)
            
            elif tipo == datetime:
                # Textfield que recibe la fecha (solo lectura)
                valor_precargado = valores_precargados.get(campo) if valores_precargados else None
                valor_inicial = ""
                if valor_precargado:
                    # Si viene de BD en formato YYYY-MM-DD, lo convertimos a DD-MM-YYYY
                    if isinstance(valor_precargado, str) and "T" not in valor_precargado:
                        try:
                            valor_inicial = datetime.strptime(valor_precargado, "%Y-%m-%d").strftime("%d-%m-%Y")
                        except:
                            valor_inicial = valor_precargado
                    else:
                        valor_inicial = valor_precargado if isinstance(valor_precargado, str) else ""
                
                self.inputs_fecha[campo] = ft.TextField(
                    label=campo.replace("_", " ").title(),
                    read_only=True,
                    expand=True,
                    value=valor_inicial,
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
                valor_precargado = valores_precargados.get(campo) if valores_precargados else None
                field = ft.TextField(
                    label=campo.replace("_", " ").title(),
                    keyboard_type="number",
                    expand=True,
                    data=campo,
                    value=str(valor_precargado) if valor_precargado else "",
                    on_change=lambda e: self.limpiar_error(e)
                    )
                fields_box.append(field)
            
            else:
                valor_precargado = valores_precargados.get(campo) if valores_precargados else None
                field = ft.TextField(
                    label=campo.replace("_", " ").title(),
                    expand=True,
                    data=campo,
                    value=str(valor_precargado) if valor_precargado else "",
                    on_change=lambda e: self.limpiar_error(e)
                    )
                fields_box.append(field)

        return fields_box

    def GetTabla(self, servicio, entidad: Type[ENTIDADES], entidad_a_editar=None): # entidad: clase, no instancia. Por eso ponemos Type[ENTIDADES].
        # ESTO ES PARA EL FORMULARIO (DB Real). Estas van a perdurar sin modificarse.
        columnas_para_formulario = servicio.obtener_columnas_por_entidad(entidad)

        # Obtenemos columnas (incluso si la tabla está vacía)
        self.state.columnas_reales = columnas_para_formulario  # Guardar las columnas reales para UPDATE
        self.state.columnas_actuales = servicio.obtener_columnas_por_entidad(entidad) # Columnas reales de la entidad (DB), luego serán modificadas. 
        self.state.tabla_actual = entidad.__name__.lower().capitalize() # Por ejemplo: "Cliente", "Instructor", "Rutina"
        self.inputs_fecha = {}

        # Generamos los campos para agregar un nuevo registro
        if self.state.columnas_actuales:
            fields_box = []
        
            # Convertimos para efecto visual los datos de la DB de Rutina y Cliente conforme a los DTOs
            # Con esto logramos que si hay nuevos cambios, solo vaste con modificar los DTOs y nada más. 
            try:
                try: datos_db = servicio.buscar_todos(entidad)
                except: datos_db = []

                if entidad == Cliente:
                    try: 
                        self.lista_instructores = servicio.buscar_todos(Instructor)
                    except Exception as e: 
                        error_msg = f"Error cargando instructores: {e}"
                        print(error_msg)
                        self.lista_instructores = []
                        # Mostrar error en snackbar
                        snack = ft.SnackBar(ft.Text(error_msg, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700)
                        ft.context.page.overlay.append(snack)
                        snack.open = True
                        ft.context.page.update()
                        
                    try: 
                        self.lista_rutinas = servicio.buscar_todos(Rutina)
                    except Exception as e: 
                        error_msg = f"Error cargando rutinas: {e}"
                        print(error_msg)
                        self.lista_rutinas = []
                        # Mostrar error en snackbar
                        snack = ft.SnackBar(ft.Text(error_msg, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED_700)
                        ft.context.page.overlay.append(snack)
                        snack.open = True
                        ft.context.page.update()

                    # RE-EMPAQUETADO PARA CLIENTES
                    dict_rutinas = {r.id: f"{r.nombre} (id:{r.id})" for r in self.lista_rutinas}
                    dict_instructores = {i.id: f"{i.nombre} {i.apellido}" for i in self.lista_instructores}
                    
                    nuevos_datos = []
                    for c in datos_db:
                        # Intentar convertir fechas con múltiples formatos posibles
                        try:
                            f_inicio = datetime.strptime(c.fecha_inicio_rutina, '%Y-%m-%d').strftime('%d/%m/%y')
                        except:
                            try:
                                f_inicio = datetime.strptime(c.fecha_inicio_rutina, '%d-%m-%Y').strftime('%d/%m/%y')
                            except:
                                f_inicio = c.fecha_inicio_rutina  # Fallback a valor original
                        
                        try:
                            f_fin = datetime.strptime(c.fecha_fin_rutina, '%Y-%m-%d').strftime('%d/%m/%y')
                        except:
                            try:
                                f_fin = datetime.strptime(c.fecha_fin_rutina, '%d-%m-%Y').strftime('%d/%m/%y')
                            except:
                                f_fin = c.fecha_fin_rutina  # Fallback a valor original
                    
                        nuevos_datos.append(ClienteViewDTO(
                            id=c.id,
                            Nombre_y_Apellido=f"{c.nombre} {c.apellido}",
                            Rutina=dict_rutinas.get(c.rutina_id, "N/A"),
                            Instructor=dict_instructores.get(c.instructor_id, "N/A"),
                            Ciclo=c.ciclo_rutina,
                            Fechas=f"{f_inicio} - {f_fin}"
                        ))
                
                    self.state.datos_actuales = nuevos_datos
                    # Importante: Las columnas ahora son las del DTO
                    self.state.columnas_actuales = {f.name: f.type for f in fields(ClienteViewDTO)}

                elif entidad == Rutina:
                    # RE-EMPAQUETADO PARA RUTINAS (para mostrar el ID)
                    self.state.datos_actuales = [RutinaViewDTO(id=r.id, ID=r.id, Nombre=r.nombre) for r in datos_db]
                    self.state.columnas_actuales = {f.name: f.type for f in fields(RutinaViewDTO)}

                elif entidad == Instructor:
                    # RE-EMPAQUETADO PARA INSTRUCTORES
                    self.state.datos_actuales = [InstructorViewDTO(id=i.id, Nombre_y_Apellido=f"{i.nombre} {i.apellido}") for i in datos_db]
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

            # Preparar valores precargados si estamos en modo edición
            valores_precargados = None
            if entidad_a_editar:
                self.state.entidad_a_editar = entidad_a_editar
                valores_precargados = asdict(entidad_a_editar)
            else:
                self.state.entidad_a_editar = None
            
            # Generamos los campos para el formulario de agregar/editar nuevo registro según las columnas reales de la entidad (DB)
            fields_box = self.form_gen(columnas_para_formulario, valores_precargados)
            # Enviamos los campos al estado
            self.state.add_fields = fields_box
    
    def SendRegistro(self, servicio, entidad: Type[ENTIDADES], es_actualizacion=False):
        """
        Recolecta los datos de add_fields, los valida y los envía al servicio.
        Si es_actualizacion=True, actualiza; si False, agrega nuevo registro.
        Devuelve True si se guardó exitosamente, False en caso contrario.
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
            # Para UPDATE usamos columnas_reales (estructura real), para ADD usamos columnas_actuales
            tipos = self.state.columnas_reales if self.state.entidad_a_editar else self.state.columnas_actuales
            
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
                if es_actualizacion:
                    # Modo UPDATE: reinyectar ID y actualizar
                    if self.state.entidad_a_editar:
                        payload["id"] = self.state.entidad_a_editar.id
                    obj_actualizado = entidad(**payload)
                    servicio.actualizar(obj_actualizado)
                    
                    # 4. Refrescar la tabla y limpiar campos
                    self.GetTabla(servicio, entidad)
                    print(f"Registro actualizado con éxito en {entidad.__name__}")
                    return True  # Éxito
                else:
                    # Modo ADD: crear nuevo objeto y agregar (id temporal = 0, será ignorado por repo)
                    payload["id"] = 0
                    nuevo_obj = entidad(**payload)
                    servicio.añadir(nuevo_obj)
                    
                    # 4. Refrescar la tabla y limpiar campos
                    self.GetTabla(servicio, entidad)
                    print(f"Registro agregado con éxito en {entidad.__name__}")
                    return True  # Éxito
                
            except Exception as e:
                print(f"Error al guardar: {e}")
                return False  # Error interno
        
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
            return False  # Validación falló


# Instancia global del ESTADO (Observable)
gym_state = GymState()
# Instancia del controlador que manipula ese estado
gym_controller = GymController(gym_state)
