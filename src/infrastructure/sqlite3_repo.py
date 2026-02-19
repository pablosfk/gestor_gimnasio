from domain.interfaces import Repository
from domain.entities import ENTIDADES
from infrastructure.db_conn import DatabaseConnection
from dataclasses import asdict
from domain.exceptions import RegistroNoEncontrado, ReferenciaEnUso, PersistenciaError, RegistroDuplicado
import sqlite3
from typing import get_type_hints, Type

class SQLite3Repository(Repository):
    def __init__(self, db_conn: DatabaseConnection):
        self.db = db_conn

    def add(self, entity: ENTIDADES): # Este "entity" debería ser un objeto instancia de alguna clase ENTIDADES, tiene datos!
        tabla = type(entity).__name__.lower()
        tipos = get_type_hints(type(entity)) # Obtenemos los tipos en un diccionario {"id": int, "nombre": str, "apellido": str}
        datos = asdict(entity) # Obtenemos los datos del objeto en un diccionario {"id": 1, "nombre": "Juan", "apellido": "Perez"}

        if "id" in datos:
            del datos["id"]

        if "id" in tipos:
            del tipos["id"]
        
        columnas = ", ".join(datos.keys())
        valores = ", ".join([f":{k}" for k in datos.keys()])

        query = f"INSERT INTO {tabla} ({columnas}) VALUES ({valores})"

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)

            except sqlite3.IntegrityError:
                raise RegistroDuplicado(f"Ya existe un registro con estos datos.")

            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar agregar el registro: {str(e)}")

    def get_by_id(self, entity_id: int, class_entity: Type[ENTIDADES]) -> ENTIDADES: # Este "entity" solo es la clase, no tiene datos. Por eso ponemos Type[ENTIDADES]
        tabla = class_entity.__name__.lower()

        query = f"SELECT * FROM {tabla} WHERE id = :id"

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, {"id": entity_id})
                row = cursor.fetchone() # Obtenemos la fila en un diccionario
                if row:
                    # Devolvemos el objeto con los datos de la fila aprovechando el constructor de la dataclass.
                    return class_entity(**row)
                else:
                    return None

                raise RegistroNoEncontrado(f"No existe un registro con ID {entity_id}")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar obtener el registro con ID {entity_id}: {str(e)}")

    def get_all(self, class_entity: Type[ENTIDADES]) -> list[ENTIDADES]: # Este "entity" solo es la clase, no tiene datos. Por eso ponemos Type[ENTIDADES]
        tabla = class_entity.__name__.lower()
        query = f"SELECT * FROM {tabla}"

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                
                if rows:
                    # Devolvemos una lista de los objetos con los datos de cada fila aprovechando el constructor de la dataclass.
                    return [class_entity(**row) for row in rows]
                else:
                    return []

                raise RegistroNoEncontrado(f"No existe ningún registro de {tabla}")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar obtener todos los registros de {tabla}: {str(e)}")

    def update(self, entity: ENTIDADES) -> ENTIDADES: # Este "entity" debería ser un objeto instancia de alguna clase ENTIDADES, tiene datos!
        tabla = type(entity).__name__.lower()
        datos = asdict(entity) # Obtenemos los datos del objeto en un diccionario {"id": 1, "nombre": "Juan", "apellido": "Perez"}
        entity_id = None

        if "id" in datos:
            entity_id = datos["id"]
        else:
            raise PersistenciaError("No se puede actualizar: ID no existe.")

        query_values = []
        for key in datos.keys():
            if key == "id":
                continue
            query_values.append(f"{key} = :{key}")
            
        query_values_str = ", ".join(query_values)
        
        query = f"UPDATE {tabla} SET {query_values_str} WHERE id = :id"

        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0:
                    raise RegistroNoEncontrado(f"No se puede actualizar: ID {entity_id} no existe.")
            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar actualizar el registro: {str(e)}")
    
    def delete(self, entity: ENTIDADES): # Este "entity" debería ser un objeto instancia de alguna clase ENTIDADES, tiene datos!
        entity_id = getattr(entity, "id", None)
        tabla = type(entity).__name__.lower()

        if entity_id is None:
            raise PersistenciaError("No se puede eliminar: ID no existe.")

        query = f"DELETE FROM {tabla} WHERE id = :id"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, {"id": entity_id})
                if cursor.rowcount == 0: # Si no borró ninguna fila...
                    raise RegistroNoEncontrado(f"No existe el registro con ID {entity_id}")

            except sqlite3.IntegrityError:
                raise ReferenciaEnUso("No se puede eliminar porque está asignado a uno o más clientes.")

            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar eliminar el registro: {str(e)}")

