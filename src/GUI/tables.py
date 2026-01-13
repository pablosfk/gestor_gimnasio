import flet as ft
import flet_datatable2 as ftd
from dataclasses import fields
from .controllers import gym_state, gym_controller

def Tablas():
    # Observamos los datos
    datos = gym_state.datos_actuales
    columnas = gym_state.columnas_actuales

    print(datos)
    print(columnas)

    # Definimos los estados: la lista de ítems, el índice de la columna y el orden
    sort_index, set_sort_index = ft.use_state(0)
    ascending, set_ascending = ft.use_state(True)

    if not columnas:
        # Si no hay columnas, mostramos un contenedor vacío (o con un mensaje sutil)
        return ft.Container()

    def sort_column(e: ft.DataColumnSortEvent):
        # Aquí puedes implementar lógica de ordenamiento local si quieres,
        # pero para simplificar y ver si funciona, actualizamos el estado del hook:
        set_sort_index(e.column_index)
        set_ascending(e.ascending)
        # Nota: Si quieres que el orden persista, el sort debería hacerse sobre 'datos'

    # 3. GENERAR FILAS DINÁMICAS (Accediendo a los atributos del objeto)
    data_rows = []
    if datos:
        is_empty = None
        for d in datos:
            # Usamos reflexión para obtener los valores de cualquier entidad (Cliente, Instructor, etc.)
            celdas = [
                ft.DataCell(ft.Text(str(getattr(d, f.name)))) 
                for f in fields(d)
            ]
            data_rows.append(ftd.DataRow2(cells=celdas))
    
    columnas_formateadas = [
        ftd.DataColumn2(
            label=ft.Text(nombre), 
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