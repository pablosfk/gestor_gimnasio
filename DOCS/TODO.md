# Para la 1.0
1. Añadir toda la estructura de manejo CRUD de los datos.
2. Poner bien los colores de todos los componentes en los diferentes archivos. 
3. Crear un repositorio Github para el proyecto y subirlo.
4. Revisar todas las excepciones y que se capturen debidamente, y presenten una correcta notificación al usuario.
5. Hacer la GUI de ventanas emergentes para edición CRUD de datos.
6. Llevar los tests al siguiente nivel:
    - **Coverage Report:** `pip install pytest-cov` y ejecutar `pytest --cov=src --cov-report=html`
    - **Tests de Infraestructura:** Crear `test_infrastructure.py` con tests de integración real con SQLite
    - **Parametrized Tests:** Usar `@pytest.mark.parametrize` para probar múltiples casos con una sola función
    - **GitHub Actions:** CI/CD que ejecute los tests automáticamente en cada commit
    - **Otros tests:**  Revisar si no es necesario alguna batería mas de testeo antes de presentar la 1.0.
7. **Refinamiento UX/UI (Crítico para usabilidad):**
    - [ ] Implementar **Acciones por Fila**: Agregar columnas con botones de "Editar" y "Eliminar" en `Tablas`.
    - [ ] Implementar **Buscador/Filtro**: Input de texto para filtrar los resultados de la tabla en tiempo real.
    - [ ] Implementar **Validaciones Visuales**: Feedback en rojo/verde en los inputs de los formularios (Required, Tipos de datos).

# Luego de la 1.0
1. Revisar el README.md para que sea más completo y claro. con todo lo que se ha hecho.
2. Añadir la automatización completa de la creación de las tablas en SQLite en src/infrastructure/sqlite3_repo.py usando incluso entidad in ENTIDADES.values().
