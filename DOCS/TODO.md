# Para la 1.0
0. [ ] Automatización ORM para la creación de tablas en SQLite, repositorio y servicios.
    0.1 [✅]'interfaces.py': unificar todo en Repository aprovechando la listas 'Entidades' de interfaces.py. 
    0.2 [✅]'sqlite3_repo.py': Luego, en infrastructure, hacer lo mismo para crear las tablas de forma dinámica, unificando SQLite3Repository(Repository), obteniendo del objeto "entidad: Entidades" y "entidad:Type[ENTIDADES]" en cada función los parámetros necesarios para el CRUD de cada tabla.
    0.3 [✅] 'services.py': Ajustar el servicio para que funcione con los repositorios unificados.
    0.4 [✅] 'controllers.py': Ajustar el controlador para que funcione con los servicios unificados.
    0.5 [✅] 'main.py': Ajustar el main para que esté correcta la inyección de dependencias.
    0.6 [✅] Eliminar gimnasio.db a fin de que se cree de forma correcta.
1. [ ] Añadir toda la estructura de manejo CRUD de los datos en GUI.
2. [ ] Poner bien los colores de todos los componentes en los diferentes archivos. 
3. [✅] Crear un repositorio Github para el proyecto y subirlo.
4. [ ] Revisar todas las excepciones y que se capturen debidamente, y presenten una correcta notificación al usuario.
5. [ ] Hacer la GUI de ventanas emergentes para edición CRUD de datos.
6. [ ] Llevar los tests al siguiente nivel:
    - [ ] **Coverage Report:** `pip install pytest-cov` y ejecutar `pytest --cov=src --cov-report=html`
    - [ ] **Tests de Infraestructura:** Crear `test_infrastructure.py` con tests de integración real con SQLite
    - [ ] **Parametrized Tests:** Usar `@pytest.mark.parametrize` para probar múltiples casos con una sola función
    - [ ] **GitHub Actions:** CI/CD que ejecute los tests automáticamente en cada commit
    - [ ] **Otros tests:**  Revisar si no es necesario alguna batería mas de testeo antes de presentar la 1.0.
    - [ ] **Rehacer tests de servicios:** Rehacer los tests de servicios para que funcionen correctamente. 
7. **Refinamiento UX/UI (Crítico para usabilidad):**
    - [ ] Implementar **Acciones por Fila**: Agregar columnas con botones de "Editar" y "Eliminar" en `Tablas`.
    - [ ] Implementar **Buscador/Filtro**: Input de texto para filtrar los resultados de la tabla en tiempo real.
    - [✅] Implementar **Validaciones Visuales**: Feedback en rojo/verde en los inputs de los formularios (Required, Tipos de datos).

# Luego de la 1.0
1. [ ] Revisar el README.md para que sea más completo y claro. con todo lo que se ha hecho.
2. [ ] Añadir la automatización completa de la creación de las tablas en SQLite en src/infrastructure/sqlite3_repo.py usando incluso entidad in ENTIDADES.values().

3. [ ]🛠️ Plan de Automatización y Migraciones
    1. Fase de Inspección y Comparación
        [ ] Mapear tipos de Python a SQL: Crear un diccionario de equivalencias que traduzca 'str', 'int', 'datetime' y 'Optional' a sus respectivos tipos en SQLite ('TEXT', 'INTEGER', 'TIMESTAMP').
        [ ] Extraer metadata de las Dataclasses: Utilizar 'get_type_hints' y 'fields()' para obtener la estructura deseada de cada entidad en tiempo de ejecución.
        [ ] Consultar el esquema real de la DB: Ejecutar 'PRAGMA table_info(nombre_tabla)' para obtener las columnas, tipos y nulidad que existen actualmente en el archivo .db.
        [ ] Detectar discrepancias (Diff): Comparar ambos esquemas para identificar qué columnas faltan en la base de datos y cuáles sobran respecto al código.

    2. Fase de Ejecución y Sincronización
        [ ] Implementar adición automática de columnas: Ejecutar 'ALTER TABLE ... ADD COLUMN' para cada atributo nuevo detectado en las dataclasses.
        [ ] Definir valores por defecto para nuevos campos: Establecer una lógica de "Default Values" (ej: '' para 'str', 0 para 'int') para evitar errores de restricción 'NOT NULL' en tablas que ya tienen registros.
        [ ] Gestionar claves foráneas dinámicas: Detectar sufijos '_id' en los nombres de atributos para generar automáticamente las cláusulas 'FOREIGN KEY (...) REFERENCES ...'.

    3. Fase de Limpieza y Depreciación (Manejo de Sobrantes)
        [ ] Taggear columnas obsoletas como "Deprecated": En lugar de eliminar, renombrar columnas que ya no existen en el código (ej: 'nombre' -> 'DEPRECATED_nombre') para permitir auditorías o rollbacks manuales.
        [ ] Ignorar columnas depreciadas en el ORM: Ajustar el repositorio dinámico para que ignore cualquier columna que tenga el prefijo 'DEPRECATED_' al realizar los 'SELECT *' o reconstruir objetos.
        [ ] Implementar borrado físico mediante tabla temporal: Para una limpieza definitiva, crear una tabla nueva con el esquema correcto, migrar los datos necesarios desde la tabla vieja, eliminar la vieja y renombrar la nueva.

    4. Robustez y Seguridad
        [ ] Validar orden de creación: Implementar un algoritmo de ordenamiento por dependencias para que las tablas "padre" se creen siempre antes que las "hijas" (clientes).
        [ ] Generar logs de migración: Imprimir en consola o guardar en un archivo cada cambio estructural realizado ('ALTER', 'RENAME', etc.) para trazabilidad.
        [ ] Realizar Backup preventivo: Crear una copia del archivo .db automáticamente antes de iniciar cualquier proceso de alteración de esquema.

    ## Código Python del posible camino de desarrollo de la automatización
    ### Mapeo de tipos para la automatización de la creación de tablas:
    ```python
    import datetime
    from typing import get_type_hints, Optional, Union, get_origin, get_args

    MAPEO_TIPOS = {
        str: "TEXT NOT NULL",
        int: "INTEGER NOT NULL",
        datetime.datetime: "TIMESTAMP NOT NULL",
        float: "REAL NOT NULL",
        bool: "INTEGER NOT NULL" # SQLite usa 0 o 1
    }
    ```

    ### Función que revisa las dataclass y genere las CREATE TABLE
    ```python
    def generar_sql_creacion(clase_entidad):
        nombre_tabla = clase_entidad.__name__.lower()
        tipos = get_type_hints(clase_entidad)
        
        lineas_columnas = []
        restricciones = []

        for nombre_campo, tipo in tipos.items():
            # Manejo del ID
            if nombre_campo == "id":
                lineas_columnas.append("id INTEGER PRIMARY KEY AUTOINCREMENT")
                continue

            # Manejo de Optional (Union[int, None])
            origin = get_origin(tipo)
            if origin is Union:
                tipo = get_args(tipo)[0] # Tomamos el tipo base (int, str, etc)
                sql_tipo = MAPEO_TIPOS.get(tipo, "TEXT").replace("NOT NULL", "")
            else:
                sql_tipo = MAPEO_TIPOS.get(tipo, "TEXT NOT NULL")

            lineas_columnas.append(f"{nombre_campo} {sql_tipo}")

            # Detección de Foreign Keys por nombre
            if nombre_campo.endswith("_id"):
                tabla_referenciada = nombre_campo.replace("_id", "")
                restricciones.append(
                    f"FOREIGN KEY ({nombre_campo}) REFERENCES {tabla_referenciada} (id)"
                )

        todo_junto = lineas_columnas + restricciones
        query = f"CREATE TABLE IF NOT EXISTS {nombre_tabla} (\n    " + ",\n    ".join(todo_junto) + "\n)"
        return query
    ```

    ### Se debe ordenar la creación según las que tengan Foreign Key al final, para evitar errores de referencia.
    ```python
    def init_db(self):
    from domain.entities import ENTIDADES
    
    with self.get_connection() as conn:
        cursor = conn.cursor()
        
        # Ordenamos: primero las que no tienen FKs para evitar conflictos
        clases = list(ENTIDADES.values())
        # Una forma simple de ordenar: las que tienen menos campos "_id" van primero
        clases.sort(key=lambda c: len([f for f in fields(c) if "_id" in f.name]))

        for clase in clases:
            query = generar_sql_creacion(clase)
            cursor.execute(query)
    ```