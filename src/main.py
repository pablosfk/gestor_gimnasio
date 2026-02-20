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
import os
import tomllib
import json
from pathlib import Path

#=============================================================================
# METADATOS DEL PROYECTO
#=============================================================================
def get_project_metadata():
    # Buscamos el archivo pyproject.toml en la raíz del proyecto
    toml_path = Path(__file__).parent.parent / "pyproject.toml"

    # También construimos la ruta al config.json en APPDATA para sincronizar
    app_data = os.getenv("APPDATA") or str(Path.home())
    base_path = os.path.join(app_data, "LearnLifting")
    if not os.path.exists(base_path):
        try:
            os.makedirs(base_path, exist_ok=True)
        except Exception:
            pass
    config_json_path = os.path.join(base_path, "config.json")

    # Si existe pyproject.toml, lo leemos y persistimos name/version en config.json
    try:
        with open(toml_path, "rb") as f:
            data = tomllib.load(f)
            name = data.get("project", {}).get("name")
            version = data.get("project", {}).get("version")
            if name and version:
                # Merge con config.json existente si corresponde
                cfg = {}
                if os.path.exists(config_json_path):
                    try:
                        with open(config_json_path, "r", encoding="utf-8") as jf:
                            cfg = json.load(jf)
                    except Exception:
                        cfg = {}
                cfg.update({"name": name, "version": version})
                try:
                    with open(config_json_path, "w", encoding="utf-8") as jf:
                        json.dump(cfg, jf, ensure_ascii=False, indent=2)
                except Exception:
                    pass
                return name, version
    except (FileNotFoundError, KeyError):
        # No hay pyproject.toml o está malformado: fallback a config.json
        pass
    except Exception:
        pass

    # Fallback: leer config.json si existe
    try:
        if os.path.exists(config_json_path):
            with open(config_json_path, "r", encoding="utf-8") as jf:
                cfg = json.load(jf)
                name = cfg.get("name")
                version = cfg.get("version")
                if name and version:
                    return name, version
    except Exception:
        pass

    # Valores por defecto si todo falla
    return "App", "0.0.0"

# Cargamos los datos
APP_NAME, VERSION = get_project_metadata()

# Obtenemos la ruta para la base de datos, 
# será la carpeta de perfil de usuario para asegurar permisos
def get_db_path():
    app_data = os.getenv("APPDATA") # En Windows: C:\Users\Nombre\AppData\Roaming y se puede ingresar por %APPDATA%
    base_path = os.path.join(app_data, "LearnLifting")
    
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    return os.path.join(base_path, "learnlifting.db")

# Instanciación e inicialización de la base de datos
from infrastructure.db_conn import DatabaseConnection as DB
db_path = get_db_path()
db_manager = DB(db_path)
db_manager.init_db()

# Instanciación del repositorio
from infrastructure.sqlite3_repo import SQLite3Repository
repo = SQLite3Repository(db_manager)

# Instanciación del servicio
from application.services import GymService
gimnasio_servicios = GymService(repositorio=repo)

# Definición de la función principal
def main(page: ft.Page):
    window = ft.Window()
    # Configuramos el título usando los datos del TOML
    page.title = f"{APP_NAME} v{VERSION}"
    # --- Configuración de la página ---
    page.padding = 0
    page.window.min_width = 800
    page.window.min_height = 600
    page.window.width = 1500
    page.window.height = 800
    #page.theme_mode = ft.ThemeMode.DARK # SYSTEM, LIGHT, DARK
    #page.bgcolor = ft.Colors.PRIMARY_CONTAINER
    # Configuramos el idioma a español (Argentina o genérico)
    page.locale_configuration = ft.LocaleConfiguration(
        current_locale=ft.Locale("es", "AR"), # "es" para español, "AR" para Argentina
        supported_locales=[ft.Locale("es", "AR"), ft.Locale("en", "US")],
    )
    
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
