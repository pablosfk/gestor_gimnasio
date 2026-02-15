import sqlite3
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path

    #Inicialización de la base de datos en la carpeta data
    def init_db(self):
        ''' Inicialización de la base de datos en la carpeta data '''
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Creamos la tabla instructores.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS instructor (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL
                )
            ''')

            # Creamos la tabla rutinas.
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS rutina (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    pdf_link TEXT NOT NULL
                )
            ''')
            
            # --- 1. DEFINICIÓN INICIAL (Para instalaciones nuevas) ---
            # Creamos la tabla clientes. 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS cliente (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    apellido TEXT NOT NULL,
                    fecha_inicio_rutina TEXT NOT NULL,
                    fecha_fin_rutina TEXT NOT NULL,
                    instructor_id INTEGER NOT NULL,
                    rutina_id INTEGER NOT NULL,
                    ciclo_rutina INTEGER NOT NULL,

                    -- Anclajes de las foreign keys:
                    FOREIGN KEY (instructor_id) REFERENCES instructor (id),
                    FOREIGN KEY (rutina_id) REFERENCES rutina (id)
                )
            ''')

            # --- 2. MIGRACIÓN (Para instalaciones existentes) ---
            # Lista de Migraciones (De momento vacía)
            # Formato: [(tabla1, columna1, tipo1), (tabla2, columna2, tipo2), ...]
            # Ejemplo: [("instructores", "telefono", "TEXT NOT NULL"), ...]
            campos_nuevos = [] 

            for tabla, columna, tipo in campos_nuevos:
                try:
                    cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {tipo}")
                except sqlite3.OperationalError:
                    pass # La columna ya existe, no hay nada que hacer
            
            conn.commit()

        except sqlite3.Error as e:
            print(f"Error SQLite3 al inicializar la base de datos: {e}")
        except Exception as e:
            print(f"Error inesperado al inicializar la base de datos: {e}")
        
        finally:
            conn.close()


    @contextmanager
    def get_connection(self):
        conn = None
        try:
            # Aseguramos que haga la conversión de tipos de datos con "detect_types=sqlite3.PARSE_DECLTYPES"
            conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            conn.row_factory = sqlite3.Row  # Permite acceder a columnas por nombre
            
            # Activamos FK para esta sesión de trabajo
            conn.execute("PRAGMA foreign_keys = ON")

            yield conn # Aquí "presta" la conexión al repositorio
            conn.commit() # Si no hay error, guardamos los cambios
        except sqlite3.Error as e:
            conn.rollback() # Si hay error, deshacemos los cambios
            print(f"Error SQLite3 al obtener la conexión: {e}")
        except Exception as e:
            conn.rollback() # Si hay error, deshacemos los cambios
            print(f"Error inesperado al obtener la conexión: {e}")
        finally:
            if conn:
                conn.close() # Se asegura de cerrar siempre