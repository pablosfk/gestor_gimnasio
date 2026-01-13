class GymException(Exception):
    """Base para todas las excepciones del sistema"""
    pass

# --- Grupo de Persistencia ---
class PersistenciaError(GymException): pass

class RegistroNoEncontrado(PersistenciaError): pass
class RegistroDuplicado(PersistenciaError): pass
class ReferenciaEnUso(PersistenciaError): 
    """Específica para el caso de las Foreign Keys"""
    pass

# --- Grupo de Negocio ---
class NegocioError(GymException): pass

class CupoExcedidoError(NegocioError): pass
class EstadoFinancieroError(NegocioError): pass
class DatosIncompletosError(NegocioError): pass

class RequisitoClienteInstructorError(NegocioError):
    """Excepción lanzada cuando un cliente no tiene instructor."""
    pass

class RequisitoClienteRutinaError(NegocioError):
    """Excepción lanzada cuando un cliente no tiene rutina."""
    pass

# --- Grupo de Servicios ---
class ServicioError(GymException): pass

class ServicioNoDisponibleError(ServicioError): pass
class EntidadNoValidaError(ServicioError): pass

# --- Grupo de Estados (controller) ---
class EstadoError(GymException): pass

class EstadoIncompletoError(EstadoError): pass
class ServiceNoDisponibleError(EstadoError): pass