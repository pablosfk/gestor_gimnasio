# colors.py
from enum import Enum
import flet as ft


class Colors(Enum):
    # ======================================================
    # 1. SIDEBAR
    # ======================================================

    # Fondo general del sidebar
    SIDEBAR_FONDO = ft.Colors.SECONDARY_CONTAINER
    SIDEBAR_TEXTO = ft.Colors.ON_SECONDARY_CONTAINER
    SIDEBAR_DIVISOR = ft.Colors.OUTLINE_VARIANT

    # Botón sidebar - estado normal (plano)
    SIDEBAR_BOTON_FONDO = ft.Colors.SECONDARY_CONTAINER
    SIDEBAR_BOTON_TEXTO = ft.Colors.ON_SECONDARY_CONTAINER

    # Botón sidebar - hover
    SIDEBAR_BOTON_HOVER_FONDO = ft.Colors.SURFACE_TINT
    SIDEBAR_BOTON_HOVER_BORDE = ft.Colors.OUTLINE

    # Botón sidebar - activo / seleccionado
    SIDEBAR_BOTON_ACTIVO_FONDO = ft.Colors.SECONDARY_FIXED
    SIDEBAR_BOTON_ACTIVO_TEXTO = ft.Colors.ON_SECONDARY_FIXED
    SIDEBAR_BOTON_ACTIVO_INDICADOR = ft.Colors.PRIMARY

    # ======================================================
    # 2. BODY / CONTENIDO PRINCIPAL
    # ======================================================

    BODY_FONDO = ft.Colors.SURFACE
    BODY_TEXTO = ft.Colors.ON_SURFACE
    BODY_TEXTO_SECUNDARIO = ft.Colors.ON_SURFACE_VARIANT

    # ======================================================
    # 3. TABLAS (DataTable2)
    # ======================================================

    # Contenedor general de la tabla
    TABLA_FONDO = ft.Colors.SURFACE_CONTAINER
    TABLA_BORDE = ft.Colors.OUTLINE
    TABLA_SOMBRA = ft.Colors.SHADOW

    # Header de la tabla (fila fija superior)
    TABLA_HEADER_FONDO = ft.Colors.SURFACE_CONTAINER_HIGHEST
    TABLA_HEADER_TEXTO = ft.Colors.ON_SURFACE
    TABLA_HEADER_BORDE = ft.Colors.OUTLINE

    # Filas normales
    TABLA_FILA_PAR_FONDO = ft.Colors.SURFACE_CONTAINER_LOW
    TABLA_FILA_IMPAR_FONDO = ft.Colors.SURFACE_CONTAINER_LOWEST
    TABLA_FILA_TEXTO = ft.Colors.ON_SURFACE

    # Hover sobre fila
    TABLA_FILA_HOVER_FONDO = ft.Colors.SURFACE_CONTAINER_HIGH

    # Fila seleccionada (persistente)
    TABLA_FILA_SELECCIONADA_FONDO = ft.Colors.PRIMARY_CONTAINER
    TABLA_FILA_SELECCIONADA_TEXTO = ft.Colors.ON_PRIMARY_CONTAINER

    # ======================================================
    # 4. POPUPS / MODALES CRUD
    # ======================================================

    # Fondo oscuro detrás del popup
    POPUP_OVERLAY = ft.Colors.SCRIM

    # Card del popup
    POPUP_FONDO = ft.Colors.SURFACE_CONTAINER_HIGH
    POPUP_TEXTO = ft.Colors.ON_SURFACE
    POPUP_SOMBRA = ft.Colors.SHADOW

    # ======================================================
    # 5. INPUTS Y FORMULARIOS
    # ======================================================

    INPUT_FONDO = ft.Colors.SURFACE_CONTAINER_LOW
    INPUT_TEXTO = ft.Colors.ON_SURFACE
    INPUT_BORDE = ft.Colors.OUTLINE

    # Input con error
    INPUT_ERROR_BORDE = ft.Colors.ERROR
    INPUT_ERROR_TEXTO = ft.Colors.ON_ERROR

    # ======================================================
    # 6. BOTONES GENERALES
    # ======================================================

    # Botón primario (Guardar, Confirmar)
    BOTON_PRIMARIO_FONDO = ft.Colors.PRIMARY
    BOTON_PRIMARIO_TEXTO = ft.Colors.ON_PRIMARY

    # Botón secundario (Cancelar, Volver)
    BOTON_SECUNDARIO_FONDO = ft.Colors.SECONDARY
    BOTON_SECUNDARIO_TEXTO = ft.Colors.ON_SECONDARY

    # ======================================================
    # 7. ESTADOS ESPECIALES / INVERSOS
    # ======================================================

    TOOLTIP_FONDO = ft.Colors.INVERSE_SURFACE
    TOOLTIP_TEXTO = ft.Colors.ON_INVERSE_SURFACE

    BOTON_SOBRE_FONDO_OSCURO = ft.Colors.INVERSE_PRIMARY
