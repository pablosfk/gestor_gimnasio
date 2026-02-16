from dataclasses import dataclass

# Estas son DTO (Data transfer object)
# Son objetos que se usan para transferir datos entre capas
# Serán encargados de darle el formato deseado para la impresión en pantalla

@dataclass
class RutinaViewDTO:
    ID: int
    Nombre: str
    QR: str = "🔎"
    Acciones: str = "🛠️ 🗑️" # Placeholder que luego serán botones reales

@dataclass
class InstructorViewDTO:
    Nombre_y_Apellido: str
    Acciones: str = "🛠️ 🗑️" # Placeholder que luego serán botones reales

@dataclass
class ClienteViewDTO:
    Nombre_y_Apellido: str
    Rutina: str
    Ciclo: str
    Fechas: str
    QR: str = "🔎"
    Acciones: str = "🛠️ 🗑️" # Placeholder que luego serán botones reales
