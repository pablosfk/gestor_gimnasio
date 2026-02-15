import flet as ft
import flet_datatable2 as ftd
from dataclasses import fields, asdict

@ft.component
def Tablas(datos: list, columnas: dict):
    # Tablas ahora es un componente puro: recibe datos y los pinta.
    # No sabe nada del estado global.
    # datos: list[Entidad]
    # columnas: dict

    # Definimos los estados: la lista de ítems, el índice de la columna y el orden
    sort_index, set_sort_index = ft.use_state(0)
    ascending, set_ascending = ft.use_state(True)
    #data_rows, _ = ft.use_state(list())
    
    if not columnas:
        # Si no hay columnas, mostramos un contenedor vacío (o con un mensaje sutil)
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.SURFACE,
        )

    def sort_column(e: ft.DataColumnSortEvent):
        # Aquí puedes implementar lógica de ordenamiento local si quieres,
        # pero para simplificar y ver si funciona, actualizamos el estado del hook:
        set_sort_index(e.column_index)
        set_ascending(e.ascending)
        # Nota: Si quieres que el orden persista, el sort debería hacerse sobre 'datos'

    # GENERAR FILAS DINÁMICAS (Accediendo a los atributos del objeto)
    data_rows = []
    if datos:
        for dato in datos:
            d_dict = asdict(dato)
            # Generamos la lista de celdas con list comprehension
            celdas = [ft.DataCell(ft.Text(str(d))) for t,d in d_dict.items() if t != "id"]
            # Añadimos la lista de celdas como una nueva fila a la lista de filas
            data_rows.append(ftd.DataRow2(cells=celdas))

    # 3.1 Añadimos la fila de "Agregar nuevo"
    def add_new_row():
        data_rows.append(ftd.DataRow2(cells=[ft.DataCell()]))

    # 4. GENERAR COLUMNAS DINÁMICAS
    columnas_formateadas = [
        ftd.DataColumn2(
            label=ft.Text(nombre.replace("_id", "").replace("_", " ").title()), 
            size=ftd.DataColumnSize.L, 
            on_sort=sort_column
        ) for nombre in columnas
    ]

    return ftd.DataTable2(
        empty = ft.Text("No hay registros actualmente"),
        columns=columnas_formateadas,
        rows=data_rows,
        show_checkbox_column=True,
        expand=True,
        sort_column_index=sort_index,
        sort_ascending=ascending,
        heading_row_color=ft.Colors.SECONDARY_CONTAINER,
        min_width=600,
    )