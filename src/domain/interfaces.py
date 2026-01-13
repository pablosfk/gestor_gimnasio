from abc import ABC, abstractmethod
from domain.entities import Rutina, Instructor, Cliente

# Interface para los Repositorios
class Repository(ABC):

    @abstractmethod
    def get_by_id(self, entity_id: int) -> object:
        pass

    @abstractmethod
    def get_all(self) -> list[object]:
        pass

    @abstractmethod
    def update(self, entity: object):
        pass

    @abstractmethod
    def delete(self, entity: object):
        pass

# Interface para los Repositorios de Rutina
class RutinaRepository(Repository):
    
    @abstractmethod
    def add(self, rutina: Rutina):
        pass

# Interface para los Repositorios de Instructor
class InstructorRepository(Repository):
    
    @abstractmethod
    def add(self, instructor: Instructor):
        pass

# Interface para los Repositorios de Cliente
class ClienteRepository(Repository):

    @abstractmethod
    def add(self, cliente: Cliente):
        pass
    
    #@abstractmethod
    #def get_by_instructor(self, instructor_id: int) -> list[Cliente]:
    #    pass