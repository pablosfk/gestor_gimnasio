# Changelog

Todas las modificaciones notables al proyecto **Learn Lifting** se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a versionado semántico.

## [Unreleased] - (Roadmap a v1.0.0) 🆕
### Pendiente ⚠️
- 📌 Implementación de popups modales para Creación/Edición de entidades.
- 🔔 Sistema de notificaciones (SnackBars) para feedback de usuario (éxito/error).
- ✏️ Botonera de acciones (Editar/Eliminar) dentro de cada fila de las tablas.
- 🔎 Implementación de orden ascendente-descendente en `Tablas`.
- ↕️ Reordenamiento de columnas (orden ascendente/descendente desde la cabecera) — pendiente de integración (`src/GUI/tables.py`).
- 🧾 Generar las release notes completas en Markdown con la 1.0

## 📦 [0.11.0]
### Cambiado ✅ 
#### Cambios menores
- **Nombre del proyecto**: `Gimnasio Cristian` -> `Learn Lifting`
- **Cambio de etiqueta en menú**: `Clientes` -> `Usuarios`

### Añadido ✅
- **Persistencia de tema**: El tema actual se guarda en un archivo JSON en la carpeta de perfil del usuario y se carga al iniciar la aplicación.
- **Archivos añadidos**: `src/GUI/assets/themes/theme_manager.py`

## 📦 [0.10.0]
### Añadido ✅
- **DTOs de presentación**: `ClienteViewDTO` y `RutinaViewDTO` para reempaquetado visual de datos en la UI (`src/GUI/controllers.py`).
- 🎨 **Ajustes estéticos** derivados del reempaquetado (mejor formato de columnas y representación de ciclos/fechas).
- 🔢 **Campo `ciclo_rutina`** consolidado en la entidad `Cliente` y mostrado en las vistas (`src/domain/entities.py`).

### Añadido (reciente) 🆕
- 📁 **Ubicación de la base de datos en `APPDATA`**: el archivo de base de datos se crea en la carpeta de perfil del usuario (ruta construida usando la variable de entorno `APPDATA`) y se inicializa en el arranque mediante `db_manager.init_db()` (`src/main.py`).
- 🛠️ **Soporte de migraciones básicas**: `DatabaseConnection.init_db()` incluye un arreglo para aplicar `ALTER TABLE` desde la lista `campos_nuevos` (permite añadir columnas a instalaciones existentes) (`src/infrastructure/db_conn.py`).

## ✳️ [0.9.0]
### Añadido ✅
- 📥 **BottomSheet & DatePicker**: Implementación de un `BottomSheet` (diálogo tipo sheet) para creación de registros con `DatePicker` integrado, stack de `TextField` + `IconButton` para selección de fechas, y lógica `AddRegistro` que valida y castea campos antes de enviar al servicio (`src/GUI/views.py`, `src/GUI/controllers.py`).


## ✨ [0.8.0]
### Añadido ✅
- 🧾 **Formularios dinámicos**: Generación dinámica de `add_fields` a partir de la reflexión sobre dataclasses, validación por tipo (fechas, ints), y recolección/casteo previo al envío al servicio (`src/GUI/controllers.py`, `src/GUI/views.py`).
- 📊 **Tabla dinámica con `DataTable2`**: Renderizado de tablas con columnas generadas por reflexión sobre las dataclasses y filas construidas desde `asdict()`; utiliza la librería externa `flet_datatable2` para `DataTable2` (`src/GUI/tables.py`).
- ⚡ **Reactividad y Hooks**: Integración de `@ft.observable` en `GymState` y uso extensivo de `ft.use_state`/`ft.use_effect` para garantizar repaint y sincronización del estado de UI (`src/GUI/controllers.py`, `src/GUI/views.py`).
### Corregido 🐛
- 🐞 **Bug de Reactividad**: Ajustes para asegurar repintado de la UI al cambiar datos (uso apropiado de hooks en `Body`).


## 🔧 [0.7.0]
### Cambiado 🔁
- 🧩 **Refactor de Arquitectura GUI**: Migración de helpers imperativos a componentes declarativos con `@ft.component` (`AppView`, `Tablas`, `MenuTheme`) y separación de responsabilidades en controllers/views (`src/GUI/views.py`, `src/GUI/tables.py`, `src/GUI/controllers.py`).
- 🧹 **Limpieza de servicios**: Reducción de métodos duplicados y mejor manejo de excepciones en `GymService` (`src/application/services.py`).

## 🗄️ [0.6.0]
### Hito: "Infrastructure & Persistence" 🏗️
- 🗃️ **Repositorios y persistencia**: `SQLite3Repository` implementa `add/get_by_id/get_all/update/delete` con mapeo de errores de SQLite a excepciones del dominio (`src/infrastructure/sqlite3_repo.py`).
- 🧱 **Conexión y migraciones**: `DatabaseConnection` administra `init_db()` y `get_connection()` (context manager), activa `PRAGMA foreign_keys = ON`, usa `row_factory=sqlite3.Row` y soporta migraciones básicas vía `campos_nuevos` (`src/infrastructure/db_conn.py`).
- ⚠️ **Manejo de errores y transacciones**: Rollback en fallos, commit al final de operaciones y traducción de errores técnicos a `PersistenciaError`/`RegistroNoEncontrado`/`ReferenciaEnUso` (`src/infrastructure/sqlite3_repo.py`, `src/domain/exceptions.py`).
- 🧪 **Suite de tests**: `pytest` con cobertura para Dominio y Servicios (`src/tests/test_domain.py`, `src/tests/test_services.py`).

## 🔌 [0.5.0]
### Añadido ✅
- 🔗 **Inyección de servicios**: `GymServiceContext` y wrapper en `main.py` para proveer `GymService` y `Theme` por contexto a la UI (`src/GUI/contexts/service_context.py`, `src/main.py`).

## 🎨 [0.4.0]
### Añadido ✅
- 🧭 **Interfaz inicial y menús**: Botonera de navegación y estilos base (`src/GUI/views.py`, `src/GUI/styles.py`).
- 🎛️ **Theming**: Switch de modo claro/oscuro y selector de paleta de colores con `PopupMenuButton` y `PopupColorItem` (`src/GUI/theme.py`, `src/GUI/assets/themes/colors.py`).

## ⚙️ [0.3.0]
### Añadido ✅
- 🛠️ **Servicios y Repositorios**: Implementación de `GymService` con métodos para añadir, buscar, actualizar y eliminar; y contractos de repositorio (`src/application/services.py`).

## 🗃️ [0.2.0]
### Añadido ✅
- 🗄️ **Infrastructure & Persistence (base)**: Repositorio SQLite (`src/infrastructure/sqlite3_repo.py`) y conexión a la base de datos (`src/infrastructure/db_conn.py`).

## 🏁 [0.1.0]
### Hito: "Domain Definition" 🏷️
- 📚 **Definición de Entidades Clave**: `Cliente`, `Rutina`, `Instructor` y diccionario dinámico `ENTIDADES` para reflexión (`src/domain/entities.py`).
- 🗂️ **Estructura de carpetas basada en DDD** (Domain, Application, Infrastructure, GUI).

