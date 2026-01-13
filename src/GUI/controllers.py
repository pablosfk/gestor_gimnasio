import flet as ft
from GUI.contexts.service_context import GymServiceContext
from domain.entities import Cliente, Instructor, Rutina
from domain.exceptions import NegocioError, PersistenciaError, ServiceNoDisponibleError
from dataclasses import dataclass, field


@ft.observable
@dataclass
class GymState:
    # Esta es la "Source of Truth" que la vista (views.py) observará
    datos_actuales: list = field(default_factory=list)
    columnas_actuales: list = field(default_factory=list)
    #tabla_actual: str = ""

class GymController:
    """
    Controlador principal que utiliza el servicio inyectado por contexto.
    No mantiene estado visual (eso lo hace la View), pero orquesta las llamadas.
    """
    def __init__(self, state: GymState):
        self.state = state

    def GetTabla(self, servicio, entidad):
        # Obtenemos columnas (incluso si la tabla está vacía)
        self.state.columnas_actuales = servicio.obtener_columnas_por_entidad(entidad)
        #self.state.tabla_actual = entidad.__name__.lower()

        # Al asignar algo a 'state.datos_actuales', ya que la clase a la que pertenece es @ft.observable, 
        # Flet disparará el re-renderizado de cualquier componente que haya usado 'state.datos_actuales'
        try:
            # Intentamos obtener los datos
            self.state.datos_actuales = servicio.buscar_todos(entidad)
        except RegistroNoEncontrado:
            # Si no hay datos, inicializamos con una lista vacía
            self.state.datos_actuales = []


# Instancia global del ESTADO (Observable)
gym_state = GymState()
# Instancia del controlador que manipula ese estado
gym_controller = GymController(gym_state)