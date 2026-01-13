1. Hacer los archivos para las tablas en GUI/tables.py
2. Poner bien los colores en los diferentes archivos. 
3. Crear un repositorio Github para el proyecto y subirlo. 
4. Llevar los tests al siguiente nivel:
    - **Coverage Report:** `pip install pytest-cov` y ejecutar `pytest --cov=src --cov-report=html`
    - **Tests de Infraestructura:** Crear `test_infrastructure.py` con tests de integración real con SQLite
    - **Parametrized Tests:** Usar `@pytest.mark.parametrize` para probar múltiples casos con una sola función
    - **GitHub Actions:** CI/CD que ejecute los tests automáticamente en cada commit

5. Añadir la automatización completa de la creación de las tablas en SQLite en src/infrastructure/sqlite3_repo.py usando incluso entidad in ENTIDADES.values().
