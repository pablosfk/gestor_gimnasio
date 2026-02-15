from abc import ABC, abstractmethod

# Interface para los Repositorios
class Repository(ABC):

    @abstractmethod
    def get_by_id(self, entity_id: int, entity: object) -> object:
        pass

    @abstractmethod
    def get_all(self, entity: object) -> list[object]:
        pass

    @abstractmethod
    def update(self, entity: object):
        pass

    @abstractmethod
    def delete(self, entity: object):
        pass
    
    @abstractmethod
    def add(self, entity: object):
        pass