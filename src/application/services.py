from domain.entities import ENTIDADES, Cliente, Instructor, Rutina
from domain.exceptions import RequisitoClienteInstructorError, RequisitoClienteRutinaError, NegocioError, EntidadNoValidaError
from dataclasses import fields
from typing import Type

class GymService:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def añadir(self, entidad: ENTIDADES): # entidad: instancia de clase
        repo = self.repositorio

        if isinstance(entidad, Cliente):
            instructor_id = entidad.instructor_id
            rutina_id = entidad.rutina_id
                    
            # Validar requisitos. Si existen, continúa sin problemas. Si no existen en la DB, Infra lanza una excepción.
            self.repositorio.get_by_id(entity_id = entidad.instructor_id, class_entity = Instructor)
            self.repositorio.get_by_id(entity_id = entidad.rutina_id, class_entity = Rutina)

            # Validamos coherencia de fechas
            if entidad.fecha_fin_rutina and entidad.fecha_inicio_rutina and entidad.fecha_fin_rutina < entidad.fecha_inicio_rutina:
                raise NegocioError("La fecha de fin no puede ser anterior a la de inicio.")
                
            # Si todo está bien, añade el cliente
        return repo.add(entidad)

    def buscar_por_id(self, clase_entidad: Type[ENTIDADES], entity_id: int) -> ENTIDADES: # entidad: clase
        repo = self.repositorio
        
        return repo.get_by_id(entity_id= entity_id, class_entity=clase_entidad)

    def buscar_todos(self, clase_entidad: Type[ENTIDADES]) -> list[ENTIDADES]: # entidad: clase
        repo = self.repositorio
        
        return repo.get_all(class_entity=clase_entidad)

    def actualizar(self, entidad: ENTIDADES): # entidad: instancia de clase
        repo = self.repositorio
        return repo.update(entidad)

    def eliminar(self, entidad: ENTIDADES): # entidad: instancia de clase
        repo = self.repositorio
        return repo.delete(entidad)

    def obtener_columnas_por_entidad(self, entidad: ENTIDADES):
            if not entidad in ENTIDADES.values():
                raise EntidadNoValidaError(f"Entidad {entidad.__name__} no reconocida")
            
            # Generamos los nombres de columna dinámicamente con su tipo haciendo {columna: tipo}
            # Donde 'columna' es el nombre del campo de la entidad dataclass y 'tipo' es el tipo de datos. Y eliminamos el campo id.
            # Por ejemplo: { "nombre": str, "edad": int, "fecha_inicio": datetime, "fecha_fin": datetime, "instructor_id": int, "rutina_id": int }
            columnas_dict = {f.name: f.type for f in fields(entidad) if f.name != "id"}
            return columnas_dict

