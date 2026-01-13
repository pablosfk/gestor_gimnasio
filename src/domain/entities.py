from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import inspect
import sys

@dataclass
class Rutina:
    id: int
    nombre: str
    pdf_link: str

@dataclass
class Instructor:
    id: int
    nombre: str
    apellido: str

@dataclass
class Cliente:
    id: int
    nombre: str
    apellido: str
    fecha_fin_rutina: datetime = field(default_factory=datetime.now)
    instructor_id: Optional[int] = None
    rutina_id: Optional[int] = None

    def is_complete(self) -> bool:
        """La regla de negocio pura"""
        return all([
            len(self.nombre) > 0,
            len(self.apellido) > 0,
            self.instructor_id is not None,
            self.rutina_id is not None
        ])

# --- Automatización: Devuelvo todas las entidades registradas ---
def obtener_entidades_registradas():
    """Retorna un diccionario {nombre_clase: clase} de todas las dataclasses en este archivo"""
    clases = {}
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and hasattr(obj, "__dataclass_fields__"):
            clases[name.lower()] = obj
    return clases

# Diccionario dinámico que se propaga solo
ENTIDADES = obtener_entidades_registradas() # Luego se puede usar: entidad in ENTIDADES.values() # Da True o False