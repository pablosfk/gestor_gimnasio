from domain.interfaces import Repository, InstructorRepository, RutinaRepository, ClienteRepository
from domain.entities import Instructor, Rutina, Cliente
from infrastructure.db_conn import DatabaseConnection
from dataclasses import asdict
from domain.exceptions import RegistroNoEncontrado, ReferenciaEnUso, PersistenciaError, RegistroDuplicado
import sqlite3

class SQLite3InstructorRepository(InstructorRepository):
    def __init__(self, db_conn: DatabaseConnection):
        self.db = db_conn

    def add(self, instructor: Instructor):
        # Convertimos la entidad a diccionario
        datos = asdict(instructor)
        query = """
            INSERT INTO instructores (nombre, apellido)
            VALUES (:nombre, :apellido)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)

            except sqlite3.IntegrityError:
                raise RegistroDuplicado(f"Ya existe un instructor con estos datos.")

            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar agregar el instructor: {str(e)}")

    def get_by_id(self, entity_id: int) -> Instructor:
        datos = {"id": entity_id}
        query = """
            SELECT * FROM instructores WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                row = cursor.fetchone()
                if row:
                    # Accedemos por NOMBRE de columna (Gracias a sqlite3.Row)
                    # Esto es inmune a cambios de orden en la tabla
                    return Instructor(
                        id=row["id"],
                        nombre=row["nombre"],
                        apellido=row["apellido"])

                raise RegistroNoEncontrado(f"No existe un instructor con ID {entity_id}")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar obtener el instructor con ID {entity_id}: {str(e)}")

    def get_all(self) -> list[Instructor]:
        query = """
            SELECT * FROM instructores
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows:
                    # Accedemos por NOMBRE de columna (Gracias a sqlite3.Row)
                    # Esto es inmune a cambios de orden en la tabla
                    return [Instructor(
                        id=row["id"],
                        nombre=row["nombre"],
                        apellido=row["apellido"]) for row in rows]

                raise RegistroNoEncontrado(f"No existe ningún instructor registrado")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar obtener todos los instructores: {str(e)}")

    def update(self, instructor: Instructor):
        datos = asdict(instructor)
        query = """
            UPDATE instructores 
            SET nombre = :nombre, 
                apellido = :apellido
            WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0:
                    raise RegistroNoEncontrado(f"No se puede actualizar: ID {instructor.id} no existe.")
            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar actualizar el instructor: {str(e)}")
    
    def delete(self, instructor: Instructor):
        datos = asdict(instructor)
        query = """
            DELETE FROM instructores WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0: # Si no borró ninguna fila...
                    raise RegistroNoEncontrado(f"No existe el registro con ID {entity_id}")

            except sqlite3.IntegrityError:
                raise ReferenciaEnUso("No se puede eliminar porque está asignado a uno o más clientes.")

            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar eliminar el instructor: {str(e)}")


class SQLite3RutinaRepository(RutinaRepository):
    def __init__(self, db_conn: DatabaseConnection):
        self.db = db_conn

    def add(self, rutina: Rutina):
        # Convertimos la entidad a diccionario
        datos = asdict(rutina)
        query = """
            INSERT INTO rutinas (nombre, pdf_link)
            VALUES (:nombre, :pdf_link)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)

            except sqlite3.IntegrityError:
                raise RegistroDuplicado(f"Ya existe una rutina con estos datos.")
            
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar agregar la rutina: {str(e)}")

    def get_by_id(self, entity_id: int) -> Rutina:
        datos = {"id": entity_id}
        query = """
            SELECT * FROM rutinas WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                row = cursor.fetchone()
                if row:
                    # Accedemos por NOMBRE de columna (Gracias a sqlite3.Row)
                    # Esto es inmune a cambios de orden en la tabla
                    return Rutina(
                        id=row["id"],
                        nombre=row["nombre"],
                        pdf_link=row["pdf_link"])
                
                raise RegistroNoEncontrado(f"No existe una rutina con ID {entity_id}")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar obtener la rutina con ID {entity_id}: {str(e)}")

    def get_all(self) -> list[Rutina]:
        query = """
            SELECT * FROM rutinas
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows:
                    # Accedemos por NOMBRE de columna (Gracias a sqlite3.Row)
                    # Esto es inmune a cambios de orden en la tabla
                    return [Rutina(
                        id=row["id"],
                        nombre=row["nombre"],
                        pdf_link=row["pdf_link"]) for row in rows]
                
                raise RegistroNoEncontrado(f"No existe ninguna rutina registrada")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar obtener todas las rutinas: {str(e)}")

    def update(self, rutina: Rutina):
        datos = asdict(rutina)
        query = """
            UPDATE rutinas 
            SET nombre = :nombre, 
                pdf_link = :pdf_link
            WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0:
                    raise RegistroNoEncontrado(f"No se puede actualizar: ID {rutina.id} no existe.")

            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar actualizar la rutina: {str(e)}")

    def delete(self, rutina: Rutina):
        datos = asdict(rutina)
        query = """
            DELETE FROM rutinas WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0: # Si no borró ninguna fila...
                    raise RegistroNoEncontrado(f"No existe una rutina con ID {entity_id}")

            except sqlite3.IntegrityError:
                raise ReferenciaEnUso("No se puede eliminar porque está asignada a uno o más clientes.")
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar eliminar la rutina: {str(e)}")


class SQLite3ClienteRepository(ClienteRepository):
    def __init__(self, db_conn: DatabaseConnection):
        self.db = db_conn

    def add(self, cliente: Cliente):
        # Convertimos la entidad a diccionario
        datos = asdict(cliente)
        query = """
            INSERT INTO clientes (nombre, apellido, fecha_fin_rutina, instructor_id, rutina_id)
            VALUES (:nombre, :apellido, :fecha_fin_rutina, :instructor_id, :rutina_id)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)

            except sqlite3.IntegrityError:
                raise RegistroDuplicado(f"Ya existe un cliente con estos datos.")

            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar eliminar el cliente: {str(e)}")

    def get_by_id(self, entity_id: int) -> Cliente:
        datos = {"id": entity_id}
        query = """
            SELECT * FROM clientes WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                row = cursor.fetchone()
                if row:
                    # Accedemos por NOMBRE de columna (Gracias a sqlite3.Row)
                    # Esto es inmune a cambios de orden en la tabla
                    return Cliente(
                        id=row["id"],
                        nombre=row["nombre"],
                        apellido=row["apellido"],
                        fecha_fin_rutina=row["fecha_fin_rutina"],
                        instructor_id=row["instructor_id"],
                        rutina_id=row["rutina_id"]
                    )
            
                raise RegistroNoEncontrado(f"No existe un cliente con ID {entity_id}")

            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e

            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar obtener el cliente: {str(e)}")

    def get_all(self) -> list[Cliente]:
        query = """
            SELECT * FROM clientes
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows:
                    # Accedemos por NOMBRE de columna (Gracias a sqlite3.Row)
                    # Esto es inmune a cambios de orden en la tabla
                    return [Cliente(
                        id=row["id"],
                        nombre=row["nombre"],
                        apellido=row["apellido"],
                        fecha_fin_rutina=row["fecha_fin_rutina"],
                        instructor_id=row["instructor_id"],
                        rutina_id=row["rutina_id"]
                    ) for row in rows]

                raise RegistroNoEncontrado(f"No existe ningún cliente registrado")
                
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar obtener todos los clientes: {str(e)}")

    def update(self, cliente: Cliente):
        datos = asdict(cliente)
        query = """
            UPDATE clientes 
            SET nombre = :nombre, 
                apellido = :apellido, 
                fecha_fin_rutina = :fecha_fin_rutina,
                instructor_id = :instructor_id, 
                rutina_id = :rutina_id
            WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0:
                    raise RegistroNoEncontrado(f"No se puede actualizar: ID {cliente.id} no existe.")
            except sqlite3.Error as e:
                raise PersistenciaError(f"Error técnico al intentar actualizar el cliente: {str(e)}")

    def delete(self, cliente: Cliente):
        datos = asdict(cliente)
        query = """
            DELETE FROM clientes WHERE id = :id
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, datos)
                if cursor.rowcount == 0: # Si no borró ninguna fila...
                    raise RegistroNoEncontrado(f"No existe un cliente con ID {entity_id}")
            
            except RegistroNoEncontrado as e:
                # Re-lanzamos nuestra propia excepción para que suba limpia
                raise e
                
            except sqlite3.Error as e:
                # Error técnico de SQLite (Disco lleno, base bloqueada)
                raise PersistenciaError(f"Error técnico al intentar eliminar el cliente: {str(e)}")
