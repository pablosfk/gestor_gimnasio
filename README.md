# Administrador de Gimnasios 🏋️

Sistema de Gestión Integral para Gimnasios desarrollado con **Python** y **Flet**, siguiendo estrictos principios de **Clean Architecture**, **SOLID** y **Domain-Driven Design (DDD)**.

## 📋 Descripción del Proyecto

Esta aplicación de escritorio multiplataforma (Windows/Linux/macOS) permite la administración eficiente de alumnos, instructores y rutinas de entrenamiento. Diseñada no solo para ser funcional, sino también mantenible y escalable, sirve como un ejemplo robusto de cómo implementar patrones de arquitectura de software complejos en interfaces de usuario modernas y reactivas.

## 🚀 Características Principales (v1.0)

*   **Gestión CRUD Completa:** Altas, Bajas, Modificaciones y Consultas de:
    *   👥 **Clientes:** Administración de perfiles y estados de membresía.
    *   💪 **Instructores:** Gestión del staff.
    *   📝 **Rutinas:** Asignación y control de planes de entrenamiento (con soporte para links PDF).
*   **Interfaz Reactiva Moderna:**
    *   Desarrollada con **Flet** (Framework declarativo basado en Flutter).
    *   **Modo Oscuro/Claro** con persistencia de configuración.
    *   **Temas Personalizables:** Selección de color semilla (Seed Color) dinámico para toda la UI.
*   **Arquitectura Sólida:**
    *   Desacoplamiento total entre lógica de negocio y UI.
    *   Inyección de Dependencias a través de Contextos (`Context API`).
    *   Manejo de estados reactivos mediante Hooks (`use_state`).
*   **Persistencia Fiable:** Base de datos **SQLite** embebida con integridad referencial y patrón Repository.

## 🛠️ Tecnologías y Arquitectura

El proyecto se estructura siguiendo **Clean Architecture**, dividiendo el código en capas concéntricas de responsabilidad:

1.  **Domain (Núcleo):** Entidades (`Cliente`, `Instructor`) y Reglas de Negocio. Puro Python, sin dependencias externas.
2.  **Application (Servicios):** Casos de Uso (`GymService`). Orquestan la lógica sin saber de UI ni de SQL.
3.  **Infrastructure (Adaptadores):** Implementación técnica. Repositorios SQLite (`sqlite3_repo.py`) y conexiones (`db_conn.py`).
4.  **GUI (Presentación):** Interfaz de usuario con Flet. Componentes reactivos, contextos y controladores.

### Stack Tecnológico
*   **Lenguaje:** Python 3.10+
*   **Framework UI:** Flet (v0.80+)
*   **Base de Datos:** SQLite3
*   **Testing:** Pytest & Unittest.mock

## 📂 Estructura del Proyecto

```text
d:\Proyectos\gimnasio-cristian\
│
├── DOCS/                   # Documentación, Changelog y TODOs
├── src/
│   ├── application/        # Servicios y Casos de Uso
│   ├── domain/             # Entidades y Excepciones (Core)
│   ├── infrastructure/     # Repositorios e Implementación DB
│   ├── GUI/                # Vistas, Controladores, Temas (Flet)
│   │   ├── contexts/       # Inyección de Dependencias (Context API)
│   │   ├── assets/         # Recursos estáticos
│   │   └── ...
│   ├── tests/              # Tests Unitarios y de Integración
│   ├── config.py           # Variables de configuración
│   └── main.py             # Punto de entrada (Composition Root)
│
├── requirements.txt        # Dependencias
└── README.md
```

## 🔧 Instalación y Ejecución

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/gimnasio-cristian.git
    cd gimnasio-cristian
    ```

2.  **Crear entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```bash
    # Desde la raíz del proyecto
    python src/main.py
    ```
    *La base de datos se inicializará automáticamente en la primera ejecución.*

## 🧪 Testing

El proyecto cuenta con una suite de tests exhaustiva para garantizar la estabilidad del núcleo y la lógica de negocio.

Para ejecutar los tests:
```bash
# Asegúrate de estar en la raíz del proyecto
pytest src/tests/ -v
```