import flet as ft
import flet_datatable2 as ftd
from dataclasses import fields, asdict

@ft.component
def Tablas(datos: list, columnas: dict, on_qr=None, on_edit=None, on_delete=None):
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
            celdas = []
            
            # El ID interno para lógica (el que está en minúscula 'id') lo saltamos.
            # El ID visible (el que está en mayúscula 'ID' en Rutinas) lo mostramos.
            for k, v in d_dict.items():
                if k == "id": 
                    continue
                
                content = None
                
                if k == "QR":
                     content = ft.IconButton(
                        icon=ft.Icons.QR_CODE_2,
                        tooltip="Ver Rutina",
                        icon_color=ft.Colors.PRIMARY,
                        on_click=lambda e, d=dato: on_qr(d.id) if on_qr else None
                    )
                elif k == "Acciones":
                    content = ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT, 
                            icon_color=ft.Colors.BLUE,
                            tooltip="Editar",
                            on_click=lambda e, d=dato: on_edit(d.id) if on_edit else None
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE, 
                            icon_color=ft.Colors.RED,
                            tooltip="Eliminar",
                            on_click=lambda e, d=dato: on_delete(d.id) if on_delete else None
                        ),
                    ], spacing=0, alignment=ft.MainAxisAlignment.END)
                else:
                    content = ft.Text(str(v))
                
                celdas.append(ft.DataCell(content))

            # Añadimos la lista de celdas como una nueva fila a la lista de filas
            data_rows.append(ftd.DataRow2(cells=celdas))

    # 4. GENERAR COLUMNAS DINÁMICAS
    columnas_formateadas = []
    for nombre in columnas:
        if nombre == "id":
            continue
            
        if nombre == "Acciones":
            # Columna especial de acciones: Ancho fijo y al final
            col = ftd.DataColumn2(
                label=ft.Text("Acciones"),
                fixed_width=120,
                numeric=False, 
            )
        else:
            col = ftd.DataColumn2(
                label=ft.Text(nombre.replace("_id", "").replace("_", " ").title()), 
                size=ftd.DataColumnSize.L, 
                on_sort=sort_column
            )
        columnas_formateadas.append(col)

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