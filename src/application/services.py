from domain.entities import ENTIDADES
from domain.interfaces import ClienteRepository, InstructorRepository, RutinaRepository
from domain.exceptions import RequisitoClienteInstructorError, RequisitoClienteRutinaError, NegocioError, EntidadNoValidaError
from dataclasses import fields

class GymService:
    def __init__(self, cliente_repo: ClienteRepository, instructor_repo: InstructorRepository, rutina_repo: RutinaRepository):
        self.cliente_repo = cliente_repo
        self.instructor_repo = instructor_repo
        self.rutina_repo = rutina_repo

        # este mapeo en el __init__ es debido a problemas con el match con clases puras (Rutina, Cliente, Instructor)
        self.mapeo = {
            ENTIDADES["rutina"]: self.rutina_repo,
            ENTIDADES["instructor"]: self.instructor_repo,
            ENTIDADES["cliente"]: self.cliente_repo
        }

    def añadir(self, entidad: ENTIDADES):
        repo = self.mapeo.get(entidad)
        if not repo:
            raise NegocioError("Entidad no válida")

        if isinstance(entidad, Cliente):
            instructor_id = entidad.instructor_id
            rutina_id = entidad.rutina_id
                    
            # Validar requisitos. Si existen, continúa sin problemas. Si no existen en la DB, Infra lanza una excepción.
            self.instructor_repo.get_by_id(instructor_id)
            self.rutina_repo.get_by_id(rutina_id)
                
            # Si todo está bien, añade el cliente
        return repo.add(entidad)

    def buscar_por_id(self, entidad: ENTIDADES):
        repo = self.mapeo.get(entidad)
        if not repo:
            raise NegocioError("Entidad no válida")
        
        return repo.get_by_id(entidad.id)

    def buscar_todos(self, entidad: ENTIDADES):
        repo = self.mapeo.get(entidad)
        if not repo:
            raise NegocioError("Entidad no válida")
        
        return repo.get_all()

    def actualizar(self, entidad: ENTIDADES):
        repo = self.mapeo.get(entidad)
        if not repo:
            raise NegocioError("Entidad no válida")
        
        return repo.update(entidad)

    def eliminar(self, entidad: ENTIDADES):
        repo = self.mapeo.get(entidad)
        if not repo:
            raise NegocioError("Entidad no válida")
        
        return repo.delete(entidad)

    def obtener_columnas_por_entidad(self, entidad: ENTIDADES):
            if not entidad in ENTIDADES.values():
                raise EntidadNoValidaError(f"Entidad {entidad.__name__} no reconocida")
            
            # Generamos los nombres de columna dinámicamente
            return [f.name.replace("_", " ").title() for f in fields(entidad)]