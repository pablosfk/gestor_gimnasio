import flet as ft
import flet_datatable2 as fdt
from datetime import datetime
from dataclasses import dataclass, field
from domain.entities import Cliente, Instructor, Rutina
from domain.exceptions import RequisitoClienteInstructorError, RequisitoClienteRutinaError
from config import Config
from GUI.theme import AppWithTheme
from GUI.views import AppView
from GUI.contexts.service_context import GymServiceContext

# Inicialización e instanciación de la base de datos
from infrastructure.db_conn import DatabaseConnection as DB
db_manager = DB(Config.DB_PATH)
db_manager.init_db()

# Instanciación del repositorio
from infrastructure.sqlite3_repo import SQLite3InstructorRepository, SQLite3RutinaRepository, SQLite3ClienteRepository
instructor_repo = SQLite3InstructorRepository(db_manager)
rutina_repo = SQLite3RutinaRepository(db_manager)
cliente_repo = SQLite3ClienteRepository(db_manager)

# Instanciación del servicio
from application.services import GymService
gimnasio_servicios = GymService(cliente_repo=cliente_repo, instructor_repo=instructor_repo, rutina_repo=rutina_repo)

def main(page: ft.Page):
    window = ft.Window()
    # --- Configuración de la página ---
    page.padding = 0
    page.window.min_width = 800
    page.window.min_height = 600
    page.theme_mode = ft.ThemeMode.DARK # SYSTEM, LIGHT, DARK
    page.bgcolor = ft.Colors.PRIMARY_CONTAINER
    
    # --- Renderizado ---
    # definimos un wrapper para inyectar el servicio
    # Para que funcione bien y los contextos no devuelvan un "None", 
    # se debe anidar las llamadas para que cada capa se cree dentro de la otra.
    # Así se asegura que el hijo pueda ver al padre.
    # Esto se debe a que Flet espera en callback (o child o similar)
    # una función que genere el componente, no una instancia ya cocinada.
    @ft.component
    def AppRoot():
        # Capa Exterior: Servicio
        return GymServiceContext(
            value=gimnasio_servicios, 
            # Usamos callback con lambda para que la construcción ocurra DENTRO del contexto
            callback=lambda: AppWithTheme( # El hijo del contexto de servicio es el Tema
                view_builder=AppView # El hijo del Tema es la App. Pasamos la referencia a la clase/función, NO la instancia ()
            )
        )

    page.render(AppRoot)


if __name__ == "__main__":
    ft.run(main)
