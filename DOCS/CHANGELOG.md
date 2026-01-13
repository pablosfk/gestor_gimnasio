# Changelog

Todas las modificaciones notables al proyecto **Gimnasio Cristian** se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/), y este proyecto adhiere a versionado semántico.

## [Unreleased] - (Roadmap a v1.0.0)
### Pendiente
- Implementación de popups modales para Creación/Edición de entidades.
- Sistema de notificaciones (SnackBars) para feedback de usuario (éxito/error).
- Botonera de acciones (Editar/Eliminar) dentro de cada fila de las tablas.
- Implementación de filtros y buscadores en `Tablas`.

## [0.7.0] - 2026-01-13
### Hito: "Reactive Core & Architecture Stability"
Versión enfocada en la robustez de la arquitectura Clean + DDD y la estabilización de la capa visual con Flet 0.80+ (Declarative UI).

### Añadido
- **Testing**: Suite completa de tests unitarios con `pytest` para:
  - Capa de Dominio (`src/tests/test_domain.py`): Cobertura de entidades y reglas de negocio.
  - Capa de Aplicación (`src/tests/test_services.py`): Cobertura de servicios con Mocks de repositorios.
- **GUI / State Management**: 
  - Implementación del patrón **Observable State** usando `@ft.observable` en `GymState`.
  - Integración correcta con **Hooks** (`ft.use_state`) para la reactividad en componentes (`Tablas`).
  - Renderizado dinámico de columnas de tablas utilizando **Reflexión** sobre las Python Dataclasses (ya no se hardcoean columnas).
- **Inyección de Dependencias**:
  - Creación de `GymServiceContext` para inyectar la lógica de negocio en el árbol visual sin acoplamiento fuerte.
  - Wrapper en `main.py` para asegurar la disponibilidad de contextos (`Theme` y `Service`) en toda la aplicación.
- **Theme**: Switch funcional de Modo Claro/Oscuro y selector de paleta de colores.

### Cambiado
- **Refactor de Arquitectura GUI**: Migración de funciones helper imperativas a componentes declarativos decorados con `@ft.component` (`Body`, `Tablas`).
- **Dominio**: Corrección de inconsistencia en nombres de campos (`fecha_alta_rutina` -> `fecha_fin_rutina`) para alinear Entidad con Base de Datos.
- **Servicios**: Limpieza de métodos duplicados en `GymService` y mejora en el manejo de excepciones de negocio.
- **Main**: Reestructuración del `main.py` para evitar la instanciación prematura de componentes antes de la creación del contexto (Lazy Loading con lambdas).

### Corregido
- **Bug de Reactividad**: Solucionado el problema donde la GUI no se repintaba al cambiar los datos del backend. Se solucionó vinculando el `gym_state` global mediante un hook `ft.use_state` local en el componente `Body`.
- **Bug de Inyección**: Solucionado error `GymService no encontrado` asegurando el anidamiento correcto de los Providers en el root de la app.

## [0.6.0] - Previo
### Hito: "Infrastructure & Persistence"
- Implementación de Repositorios SQLite (`infrastructure/sqlite3_repo.py`).
- Conexión a Base de Datos y migraciones iniciales (`db_conn.py`).
- Definición de Excepciones de Dominio personalizadas (`domain/exceptions.py`).

## [0.5.0] - Previo
### Hito: "Domain Definition"
- Definición de Entidades Clave: `Cliente`, `Rutina`, `Instructor`.
- Estructura de carpetas basada en DDD (Domain, Application, Infrastructure, GUI).
