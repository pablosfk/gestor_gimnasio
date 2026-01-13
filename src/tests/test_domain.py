"""
Tests para la capa de Dominio (Entidades y Excepciones)

Estos tests verifican:
1. Creación correcta de entidades
2. Validación de reglas de negocio
3. Comportamiento de excepciones personalizadas
"""

import pytest
from datetime import datetime
from domain.entities import Cliente, Instructor, Rutina
from domain.exceptions import (
    GymException, 
    NegocioError, 
    PersistenciaError,
    RequisitoClienteInstructorError,
    RequisitoClienteRutinaError,
    RegistroNoEncontrado,
    RegistroDuplicado,
    ReferenciaEnUso,
    CupoExcedidoError,
    EstadoFinancieroError,
    DatosIncompletosError
)


# ========================================
# TESTS DE ENTIDAD: RUTINA
# ========================================

class TestRutinaEntity:
    """Tests para la entidad Rutina"""
    
    def test_crear_rutina_valida(self):
        """Test: Crear una rutina con todos los campos válidos"""
        rutina = Rutina(
            id=1,
            nombre="Pierna y Glúteo",
            pdf_link="https://ejemplo.com/rutinas/pierna.pdf"
        )
        
        assert rutina.id == 1
        assert rutina.nombre == "Pierna y Glúteo"
        assert rutina.pdf_link == "https://ejemplo.com/rutinas/pierna.pdf"
    
    def test_rutina_sin_id(self):
        """Test: No se puede crear una rutina sin ID (campo obligatorio)"""
        with pytest.raises(TypeError):
            Rutina(nombre="Cardio", pdf_link="link.pdf")
    
    def test_rutina_sin_nombre(self):
        """Test: No se puede crear una rutina sin nombre (campo obligatorio)"""
        with pytest.raises(TypeError):
            Rutina(id=1, pdf_link="link.pdf")
    
    def test_rutina_sin_pdf_link(self):
        """Test: No se puede crear una rutina sin pdf_link (campo obligatorio)"""
        with pytest.raises(TypeError):
            Rutina(id=1, nombre="Cardio")
    
    def test_rutina_con_id_cero(self):
        """Test: Se puede crear una rutina con ID = 0 (válido antes del INSERT)"""
        rutina = Rutina(id=0, nombre="Temporal", pdf_link="")
        assert rutina.id == 0
    
    def test_rutina_con_nombre_vacio(self):
        """Test: Se puede crear en memoria, pero debería fallar en validación de negocio"""
        rutina = Rutina(id=1, nombre="", pdf_link="")
        assert rutina.nombre == ""  # La entidad permite strings vacíos


# ========================================
# TESTS DE ENTIDAD: INSTRUCTOR
# ========================================

class TestInstructorEntity:
    """Tests para la entidad Instructor"""
    
    def test_crear_instructor_valido(self):
        """Test: Crear un instructor con todos los campos válidos"""
        instructor = Instructor(
            id=1,
            nombre="Juan",
            apellido="Pérez"
        )
        
        assert instructor.id == 1
        assert instructor.nombre == "Juan"
        assert instructor.apellido == "Pérez"
    
    def test_instructor_sin_id(self):
        """Test: No se puede crear un instructor sin ID"""
        with pytest.raises(TypeError):
            Instructor(nombre="Juan", apellido="Pérez")
    
    def test_instructor_sin_nombre(self):
        """Test: No se puede crear un instructor sin nombre"""
        with pytest.raises(TypeError):
            Instructor(id=1, apellido="Pérez")
    
    def test_instructor_sin_apellido(self):
        """Test: No se puede crear un instructor sin apellido"""
        with pytest.raises(TypeError):
            Instructor(id=1, nombre="Juan")
    
    def test_instructor_con_nombres_vacios(self):
        """Test: Se puede crear en memoria con strings vacíos"""
        instructor = Instructor(id=1, nombre="", apellido="")
        assert instructor.nombre == ""
        assert instructor.apellido == ""


# ========================================
# TESTS DE ENTIDAD: CLIENTE
# ========================================

class TestClienteEntity:
    """Tests para la entidad Cliente"""
    
    def test_crear_cliente_completo(self):
        """Test: Crear un cliente con todos los campos válidos"""
        fecha = datetime(2026, 1, 10, 12, 0, 0)
        cliente = Cliente(
            id=1,
            nombre="María",
            apellido="González",
            fecha_fin_rutina=fecha,
            instructor_id=5,
            rutina_id=3
        )
        
        assert cliente.id == 1
        assert cliente.nombre == "María"
        assert cliente.apellido == "González"
        assert cliente.fecha_fin_rutina == fecha
        assert cliente.instructor_id == 5
        assert cliente.rutina_id == 3
    
    def test_crear_cliente_con_fecha_default(self):
        """Test: Si no se pasa fecha, se asigna la fecha actual (datetime.now)"""
        cliente = Cliente(
            id=1,
            nombre="Pedro",
            apellido="Martínez",
            instructor_id=2,
            rutina_id=1
        )
        
        # La fecha debe ser aproximadamente datetime.now()
        assert isinstance(cliente.fecha_fin_rutina, datetime)
        assert (datetime.now() - cliente.fecha_fin_rutina).seconds < 2
    
    def test_crear_cliente_sin_instructor(self):
        """Test: Se puede crear en memoria sin instructor (None es el default)"""
        cliente = Cliente(
            id=1,
            nombre="Ana",
            apellido="López",
            rutina_id=1
        )
        
        assert cliente.instructor_id is None
    
    def test_crear_cliente_sin_rutina(self):
        """Test: Se puede crear en memoria sin rutina (None es el default)"""
        cliente = Cliente(
            id=1,
            nombre="Carlos",
            apellido="Ruiz",
            instructor_id=2
        )
        
        assert cliente.rutina_id is None
    
    def test_cliente_is_complete_retorna_true(self):
        """Test: is_complete() retorna True si todos los campos obligatorios están llenos"""
        cliente = Cliente(
            id=1,
            nombre="Laura",
            apellido="Fernández",
            instructor_id=3,
            rutina_id=2
        )
        
        assert cliente.is_complete() is True
    
    def test_cliente_is_complete_retorna_false_sin_nombre(self):
        """Test: is_complete() retorna False si falta el nombre"""
        cliente = Cliente(
            id=1,
            nombre="",
            apellido="Gómez",
            instructor_id=1,
            rutina_id=1
        )
        
        assert cliente.is_complete() is False
    
    def test_cliente_is_complete_retorna_false_sin_apellido(self):
        """Test: is_complete() retorna False si falta el apellido"""
        cliente = Cliente(
            id=1,
            nombre="Jorge",
            apellido="",
            instructor_id=1,
            rutina_id=1
        )
        
        assert cliente.is_complete() is False
    
    def test_cliente_is_complete_retorna_false_sin_instructor(self):
        """Test: is_complete() retorna False si falta instructor_id"""
        cliente = Cliente(
            id=1,
            nombre="Sofía",
            apellido="Ramírez",
            instructor_id=None,
            rutina_id=1
        )
        
        assert cliente.is_complete() is False
    
    def test_cliente_is_complete_retorna_false_sin_rutina(self):
        """Test: is_complete() retorna False si falta rutina_id"""
        cliente = Cliente(
            id=1,
            nombre="Diego",
            apellido="Torres",
            instructor_id=1,
            rutina_id=None
        )
        
        assert cliente.is_complete() is False
    
    def test_cliente_sin_id(self):
        """Test: No se puede crear un cliente sin ID"""
        with pytest.raises(TypeError):
            Cliente(nombre="Test", apellido="User")


# ========================================
# TESTS DE EXCEPCIONES
# ========================================

class TestExceptions:
    """Tests para las excepciones personalizadas del dominio"""
    
    def test_gym_exception_es_base(self):
        """Test: GymException es la clase base de todas las excepciones"""
        assert issubclass(NegocioError, GymException)
        assert issubclass(PersistenciaError, GymException)
    
    def test_negocio_error_hereda_de_gym_exception(self):
        """Test: NegocioError hereda de GymException"""
        error = NegocioError("Error de prueba")
        assert isinstance(error, GymException)
        assert str(error) == "Error de prueba"
    
    def test_persistencia_error_hereda_de_gym_exception(self):
        """Test: PersistenciaError hereda de GymException"""
        error = PersistenciaError("Error de base de datos")
        assert isinstance(error, GymException)
        assert str(error) == "Error de base de datos"
    
    def test_requisito_cliente_instructor_error(self):
        """Test: RequisitoClienteInstructorError se puede lanzar"""
        with pytest.raises(RequisitoClienteInstructorError):
            raise RequisitoClienteInstructorError("El cliente necesita un instructor")
    
    def test_requisito_cliente_rutina_error(self):
        """Test: RequisitoClienteRutinaError se puede lanzar"""
        with pytest.raises(RequisitoClienteRutinaError):
            raise RequisitoClienteRutinaError("El cliente necesita una rutina")
    
    def test_registro_no_encontrado(self):
        """Test: RegistroNoEncontrado es una excepción de persistencia"""
        error = RegistroNoEncontrado("Cliente con ID 999 no existe")
        assert isinstance(error, PersistenciaError)
        assert str(error) == "Cliente con ID 999 no existe"
    
    def test_registro_duplicado(self):
        """Test: RegistroDuplicado es una excepción de persistencia"""
        error = RegistroDuplicado("Ya existe un instructor con ese DNI")
        assert isinstance(error, PersistenciaError)
        assert str(error) == "Ya existe un instructor con ese DNI"
    
    def test_referencia_en_uso(self):
        """Test: ReferenciaEnUso es una excepción de persistencia (Foreign Key)"""
        error = ReferenciaEnUso("No se puede eliminar: está asignado a clientes")
        assert isinstance(error, PersistenciaError)
        assert str(error) == "No se puede eliminar: está asignado a clientes"
    
    def test_cupo_excedido_error(self):
        """Test: CupoExcedidoError es una excepción de negocio"""
        error = CupoExcedidoError("El instructor ya tiene 20 clientes")
        assert isinstance(error, NegocioError)
        assert str(error) == "El instructor ya tiene 20 clientes"
    
    def test_estado_financiero_error(self):
        """Test: EstadoFinancieroError es una excepción de negocio"""
        error = EstadoFinancieroError("El cliente tiene pagos pendientes")
        assert isinstance(error, NegocioError)
        assert str(error) == "El cliente tiene pagos pendientes"
    
    def test_datos_incompletos_error(self):
        """Test: DatosIncompletosError es una excepción de negocio"""
        error = DatosIncompletosError("Faltan campos obligatorios")
        assert isinstance(error, NegocioError)
        assert str(error) == "Faltan campos obligatorios"


# ========================================
# TESTS DE EDGE CASES
# ========================================

class TestEdgeCases:
    """Tests de casos límite y situaciones especiales"""
    
    def test_cliente_con_fecha_futura(self):
        """Test: Se puede crear un cliente con fecha futura (válido para programación)"""
        fecha_futura = datetime(2027, 12, 31, 23, 59, 59)
        cliente = Cliente(
            id=1,
            nombre="Test",
            apellido="Future",
            fecha_fin_rutina=fecha_futura,
            instructor_id=1,
            rutina_id=1
        )
        
        assert cliente.fecha_fin_rutina.year == 2027
    
    def test_cliente_con_fecha_pasada(self):
        """Test: Se puede crear un cliente con fecha pasada (rutina vencida)"""
        fecha_pasada = datetime(2020, 1, 1, 0, 0, 0)
        cliente = Cliente(
            id=1,
            nombre="Test",
            apellido="Past",
            fecha_fin_rutina=fecha_pasada,
            instructor_id=1,
            rutina_id=1
        )
        
        assert cliente.fecha_fin_rutina.year == 2020
    
    def test_rutina_con_link_muy_largo(self):
        """Test: Se puede crear una rutina con un link extremadamente largo"""
        link_largo = "https://ejemplo.com/" + "a" * 10000
        rutina = Rutina(id=1, nombre="Test", pdf_link=link_largo)
        
        assert len(rutina.pdf_link) > 10000
    
    def test_instructor_con_nombre_unicode(self):
        """Test: Se pueden usar caracteres Unicode en nombres"""
        instructor = Instructor(
            id=1,
            nombre="Søren",
            apellido="Müller-Öztürk"
        )
        
        assert "ø" in instructor.nombre
        assert "ü" in instructor.apellido
    
    def test_cliente_con_emojis_en_nombre(self):
        """Test: Los nombres pueden contener emojis (aunque no sea recomendable)"""
        cliente = Cliente(
            id=1,
            nombre="💪 Fitness",
            apellido="Fan 🏋️",
            instructor_id=1,
            rutina_id=1
        )
        
        assert "💪" in cliente.nombre
        assert "🏋️" in cliente.apellido
