import flet as ft

# Creamos el contexto. El valor por defecto puede ser None o un Mock para tests.
# En tiempo de ejecución real, main.py proveerá la instancia correcta.
GymServiceContext = ft.create_context(None)
