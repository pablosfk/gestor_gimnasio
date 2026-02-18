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

    # Obtener lista de nombres de columnas (sin "id")
    nombres_columnas = [nombre for nombre in columnas.keys() if nombre != "id"]

    def sort_column(e: ft.DataColumnSortEvent):
        set_sort_index(e.column_index)
        set_ascending(e.ascending)

    # GENERAR FILAS DINÁMICAS (Accediendo a los atributos del objeto)
    data_rows = []
    
    # Ordenar datos si es necesario
    datos_para_mostrar = datos
    if sort_index >= 0 and sort_index < len(nombres_columnas):
        nombre_columna = nombres_columnas[sort_index]
        
        def get_sort_key(obj):
            valor = getattr(obj, nombre_columna, "")
            if valor is None:
                return ""
            
            valor_str = str(valor)
            
            # Si contiene " - ", tomar solo la primera parte (para fechas de inicio-fin)
            if " - " in valor_str:
                valor_str = valor_str.split(" - ")[0]
            
            # Si contiene "/", probablemente sea una fecha (DD/MM/YY)
            # Convertir a YYYYMMDD para ordenamiento correcto
            if "/" in valor_str:
                try:
                    partes = valor_str.split("/")
                    if len(partes) == 3:
                        dia, mes, año = partes
                        # Convertir año de 2 dígitos a 4 dígitos
                        año_completo = "20" + año if len(año) == 2 else año
                        # Retornar YYYYMMDD para ordenamiento correcto
                        return f"{año_completo}{mes.zfill(2)}{dia.zfill(2)}"
                except:
                    pass  # Si falla, tratarlo como string normal
            
            # Para strings, hacer lowercase para ordenamiento case-insensitive
            return valor_str.lower()
        
        datos_para_mostrar = sorted(
            datos,
            key=get_sort_key,
            reverse=not ascending
        )
    
    if datos_para_mostrar:
        for dato in datos_para_mostrar:
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
                    content = ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.QR_CODE_2,
                            icon_color=ft.Colors.PRIMARY,
                            tooltip="Ver Rutina",
                            on_click=lambda e, d=dato: on_qr(d.id) if on_qr else None
                        )
                    ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
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
                            on_click=lambda e, d=dato: on_delete(
                                d.id, 
                                getattr(d, 'Nombre_y_Apellido', None) or getattr(d, 'Nombre', None) or f"ID {d.id}"
                            ) if on_delete else None
                        ),
                    ], spacing=0, alignment=ft.MainAxisAlignment.CENTER)
                else:
                    content = ft.Row([
                        ft.Text(value=str(v), text_align="center")
                    ], spacing = 0, alignment=ft.MainAxisAlignment.CENTER)
                
                celdas.append(ft.DataCell(content))

            # Añadimos la lista de celdas como una nueva fila a la lista de filas
            data_rows.append(ftd.DataRow2(cells=celdas))

    # 4. GENERAR COLUMNAS DINÁMICAS
    columnas_formateadas = []
    columnas_ordenables = ["Nombre", "Ciclo", "ID", "Nombre_y_Apellido", "Rutina", "Fechas", "Instructor"]
    for nombre in columnas:
        if nombre == "id":
            continue
            
        if nombre == "QR":
            col = ftd.DataColumn2(
                label=ft.Text(value="QR", text_align=ft.TextAlign.CENTER),
                fixed_width=60,
                numeric=False,
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        elif nombre == "ID":
            col = ftd.DataColumn2(
                label=ft.Text(value="ID", text_align=ft.TextAlign.CENTER),
                fixed_width=40,
                numeric=False,
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        elif nombre == "Acciones":
            # Columna especial de acciones: Ancho fijo y al final
            col = ftd.DataColumn2(
                label=ft.Text(value="Acciones", text_align=ft.TextAlign.CENTER),
                fixed_width=120,
                numeric=False, 
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        else:
            col = ftd.DataColumn2(
                label=ft.Text(value=nombre.replace("_id", "").replace("_", " ").title(), text_align=ft.TextAlign.CENTER), 
                size=ftd.DataColumnSize.L,
                on_sort=sort_column if nombre in columnas_ordenables else None,
                numeric = False,
                heading_row_alignment=ft.MainAxisAlignment.CENTER,
            )
        columnas_formateadas.append(col)

    # Validar que sort_index sea válido para esta tabla
    effective_sort_index = sort_index if (sort_index >= 0 and sort_index < len(columnas_formateadas)) else 0

    return ftd.DataTable2(
        empty = ft.Text("No hay registros actualmente"),
        columns=columnas_formateadas,
        rows=data_rows,
        show_checkbox_column=True,
        expand=True,
        column_spacing = 0,
        sort_column_index=effective_sort_index,
        sort_ascending=ascending,
        heading_row_color=ft.Colors.SECONDARY_CONTAINER,
        min_width=600,
        vertical_lines=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
    )