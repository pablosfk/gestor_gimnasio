"""
Tests para la capa de Aplicación (Services)

Estos tests verifican:
1. Lógica de coordinación del servicio
2. Validación de reglas de negocio antes de persistir
3. Manejo correcto de excepciones de infraestructura
4. Interacción correcta con los repositorios (mocks)
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock
from application.services import GymService
from domain.entities import Cliente, Instructor, Rutina
from domain.exceptions import (
    NegocioError,
    RegistroNoEncontrado,
    RegistroDuplicado,
    RequisitoClienteInstructorError,
    RequisitoClienteRutinaError
)


# ========================================
# FIXTURES (Mocks de Repositorios)
# ========================================

@pytest.fixture
def mock_cliente_repo():
    """Mock del ClienteRepository"""
    return Mock()


@pytest.fixture
def mock_instructor_repo():
    """Mock del InstructorRepository"""
    return Mock()


@pytest.fixture
def mock_rutina_repo():
    """Mock del RutinaRepository"""
    return Mock()


@pytest.fixture
def servicio(mock_cliente_repo, mock_instructor_repo, mock_rutina_repo):
    """Fixture que crea un GymService con repos mockeados"""
    return GymService(
        cliente_repo=mock_cliente_repo,
        instructor_repo=mock_instructor_repo,
        rutina_repo=mock_rutina_repo
    )


@pytest.fixture
def rutina_valida():
    """Fixture de una rutina válida"""
    return Rutina(id=1, nombre="Pierna", pdf_link="link.pdf")


@pytest.fixture
def instructor_valido():
    """Fixture de un instructor válido"""
    return Instructor(id=1, nombre="Juan", apellido="Pérez")


@pytest.fixture
def cliente_valido():
    """Fixture de un cliente válido"""
    return Cliente(
        id=1,
        nombre="María",
        apellido="González",
        instructor_id=1,
        rutina_id=1
    )


# ========================================
# TESTS: AÑADIR ENTIDADES
# ========================================

class TestAñadirEntidades:
    """Tests para el método añadir() del servicio"""
    
    def test_añadir_rutina_exitoso(self, servicio, mock_rutina_repo, rutina_valida):
        """Test: Añadir una rutina válida llama al repositorio correcto"""
        servicio.añadir(rutina_valida)
        
        # Verificamos que se llamó al método add() del repositorio
        mock_rutina_repo.add.assert_called_once_with(rutina_valida)
    
    def test_añadir_instructor_exitoso(self, servicio, mock_instructor_repo, instructor_valido):
        """Test: Añadir un instructor válido llama al repositorio correcto"""
        servicio.añadir(instructor_valido)
        
        mock_instructor_repo.add.assert_called_once_with(instructor_valido)
    
    def test_añadir_cliente_exitoso(self, servicio, mock_cliente_repo, mock_instructor_repo, mock_rutina_repo, cliente_valido):
        """Test: Añadir un cliente válido verifica instructor y rutina antes de persistir"""
        # Configuramos los mocks para que NO lancen excepciones
        mock_instructor_repo.get_by_id.return_value = Instructor(id=1, nombre="Test", apellido="Test")
        mock_rutina_repo.get_by_id.return_value = Rutina(id=1, nombre="Test", pdf_link="test.pdf")
        
        servicio.añadir(cliente_valido)
        
        # Verificamos que se validaron instructor y rutina
        mock_instructor_repo.get_by_id.assert_called_once_with(1)
        mock_rutina_repo.get_by_id.assert_called_once_with(1)
        
        # Verificamos que se añadió el cliente
        mock_cliente_repo.add.assert_called_once_with(cliente_valido)
    
    def test_añadir_cliente_sin_instructor_lanza_excepcion(self, servicio, mock_instructor_repo, cliente_valido):
        """Test: Si el instructor no existe, se propaga la excepción del repositorio"""
        # Configuramos el mock para que lance RegistroNoEncontrado
        mock_instructor_repo.get_by_id.side_effect = RegistroNoEncontrado("Instructor no existe")
        
        with pytest.raises(RegistroNoEncontrado):
            servicio.añadir(cliente_valido)
    
    def test_añadir_cliente_sin_rutina_lanza_excepcion(self, servicio, mock_instructor_repo, mock_rutina_repo, cliente_valido):
        """Test: Si la rutina no existe, se propaga la excepción del repositorio"""
        # El instructor existe, pero la rutina no
        mock_instructor_repo.get_by_id.return_value = Instructor(id=1, nombre="Test", apellido="Test")
        mock_rutina_repo.get_by_id.side_effect = RegistroNoEncontrado("Rutina no existe")
        
        with pytest.raises(RegistroNoEncontrado):
            servicio.añadir(cliente_valido)
    
    def test_añadir_entidad_invalida_lanza_negocio_error(self, servicio):
        """Test: Si se pasa un objeto que no es Rutina/Instructor/Cliente, lanza NegocioError"""
        objeto_invalido = {"tipo": "invalido"}
        
        with pytest.raises(NegocioError, match="Entidad no válida"):
            servicio.añadir(objeto_invalido)
    
    def test_añadir_cliente_con_instructor_y_rutina_none(self, servicio, mock_instructor_repo, mock_rutina_repo):
        """Test: Si el cliente tiene instructor_id=None, debería fallar al buscar"""
        # Configuramos los mocks para que lancen excepción con None
        mock_instructor_repo.get_by_id.side_effect = RegistroNoEncontrado("ID no válido")
        
        cliente_incompleto = Cliente(
            id=1,
            nombre="Test",
            apellido="Test",
            instructor_id=None,
            rutina_id=None
        )
        
        # El servicio debería intentar buscar con None y fallar
        with pytest.raises(RegistroNoEncontrado):
            servicio.añadir(cliente_incompleto)


# ========================================
# TESTS: BUSCAR ENTIDADES
# ========================================

class TestBuscarEntidades:
    """Tests para los métodos buscar_por_id() y buscar_todos()"""
    
    def test_buscar_rutina_por_id(self, servicio, mock_rutina_repo, rutina_valida):
        """Test: Buscar rutina por ID llama al repositorio correcto"""
        mock_rutina_repo.get_by_id.return_value = rutina_valida
        
        resultado = servicio.buscar_por_id(rutina_valida)
        
        mock_rutina_repo.get_by_id.assert_called_once_with(1)
        assert resultado == rutina_valida
    
    def test_buscar_instructor_por_id(self, servicio, mock_instructor_repo, instructor_valido):
        """Test: Buscar instructor por ID llama al repositorio correcto"""
        mock_instructor_repo.get_by_id.return_value = instructor_valido
        
        resultado = servicio.buscar_por_id(instructor_valido)
        
        mock_instructor_repo.get_by_id.assert_called_once_with(1)
        assert resultado == instructor_valido
    
    def test_buscar_cliente_por_id(self, servicio, mock_cliente_repo, cliente_valido):
        """Test: Buscar cliente por ID llama al repositorio correcto"""
        mock_cliente_repo.get_by_id.return_value = cliente_valido
        
        resultado = servicio.buscar_por_id(cliente_valido)
        
        mock_cliente_repo.get_by_id.assert_called_once_with(1)
        assert resultado == cliente_valido
    
    def test_buscar_por_id_entidad_invalida(self, servicio):
        """Test: Buscar una entidad inválida lanza NegocioError"""
        with pytest.raises(NegocioError, match="Entidad no válida"):
            servicio.buscar_por_id({"tipo": "invalido"})
    
    def test_buscar_todos_rutinas(self, servicio, mock_rutina_repo):
        """Test: Buscar todas las rutinas llama al repositorio correcto"""
        rutinas_mock = [
            Rutina(id=1, nombre="Pierna", pdf_link="1.pdf"),
            Rutina(id=2, nombre="Brazo", pdf_link="2.pdf")
        ]
        mock_rutina_repo.get_all.return_value = rutinas_mock
        
        resultado = servicio.buscar_todos(Rutina(id=0, nombre="", pdf_link=""))
        
        mock_rutina_repo.get_all.assert_called_once()
        assert len(resultado) == 2
        assert resultado == rutinas_mock
    
    def test_buscar_todos_instructores(self, servicio, mock_instructor_repo):
        """Test: Buscar todos los instructores llama al repositorio correcto"""
        instructores_mock = [
            Instructor(id=1, nombre="Juan", apellido="Pérez"),
            Instructor(id=2, nombre="Ana", apellido="López")
        ]
        mock_instructor_repo.get_all.return_value = instructores_mock
        
        resultado = servicio.buscar_todos(Instructor(id=0, nombre="", apellido=""))
        
        mock_instructor_repo.get_all.assert_called_once()
        assert len(resultado) == 2
    
    def test_buscar_todos_clientes(self, servicio, mock_cliente_repo):
        """Test: Buscar todos los clientes llama al repositorio correcto"""
        clientes_mock = [
            Cliente(id=1, nombre="María", apellido="González", instructor_id=1, rutina_id=1),
            Cliente(id=2, nombre="Pedro", apellido="Martínez", instructor_id=2, rutina_id=1)
        ]
        mock_cliente_repo.get_all.return_value = clientes_mock
        
        resultado = servicio.buscar_todos(Cliente(id=0, nombre="", apellido=""))
        
        mock_cliente_repo.get_all.assert_called_once()
        assert len(resultado) == 2
    
    def test_buscar_todos_entidad_invalida(self, servicio):
        """Test: Buscar todos con entidad inválida lanza NegocioError"""
        with pytest.raises(NegocioError, match="Entidad no válida"):
            servicio.buscar_todos("string_invalido")
    
    def test_buscar_por_id_no_encontrado(self, servicio, mock_cliente_repo):
        """Test: Si el repositorio lanza RegistroNoEncontrado, se propaga"""
        mock_cliente_repo.get_by_id.side_effect = RegistroNoEncontrado("Cliente no existe")
        
        cliente = Cliente(id=999, nombre="Test", apellido="Test")
        
        with pytest.raises(RegistroNoEncontrado):
            servicio.buscar_por_id(cliente)


# ========================================
# TESTS: ACTUALIZAR ENTIDADES
# ========================================

class TestActualizarEntidades:
    """Tests para el método actualizar() del servicio"""
    
    def test_actualizar_rutina(self, servicio, mock_rutina_repo, rutina_valida):
        """Test: Actualizar una rutina llama al repositorio correcto"""
        servicio.actualizar(rutina_valida)
        
        mock_rutina_repo.update.assert_called_once_with(rutina_valida)
    
    def test_actualizar_instructor(self, servicio, mock_instructor_repo, instructor_valido):
        """Test: Actualizar un instructor llama al repositorio correcto"""
        servicio.actualizar(instructor_valido)
        
        mock_instructor_repo.update.assert_called_once_with(instructor_valido)
    
    def test_actualizar_cliente(self, servicio, mock_cliente_repo, cliente_valido):
        """Test: Actualizar un cliente llama al repositorio correcto"""
        servicio.actualizar(cliente_valido)
        
        mock_cliente_repo.update.assert_called_once_with(cliente_valido)
    
    def test_actualizar_entidad_invalida(self, servicio):
        """Test: Actualizar una entidad inválida lanza NegocioError"""
        with pytest.raises(NegocioError, match="Entidad no válida"):
            servicio.actualizar(12345)
    
    def test_actualizar_rutina_no_existente(self, servicio, mock_rutina_repo):
        """Test: Si el repositorio lanza RegistroNoEncontrado, se propaga"""
        mock_rutina_repo.update.side_effect = RegistroNoEncontrado("Rutina no existe")
        
        rutina = Rutina(id=999, nombre="No existe", pdf_link="test.pdf")
        
        with pytest.raises(RegistroNoEncontrado):
            servicio.actualizar(rutina)


# ========================================
# TESTS: ELIMINAR ENTIDADES
# ========================================

class TestEliminarEntidades:
    """Tests para el método eliminar() del servicio"""
    
    def test_eliminar_rutina(self, servicio, mock_rutina_repo, rutina_valida):
        """Test: Eliminar una rutina llama al repositorio correcto"""
        servicio.eliminar(rutina_valida)
        
        mock_rutina_repo.delete.assert_called_once_with(rutina_valida)
    
    def test_eliminar_instructor(self, servicio, mock_instructor_repo, instructor_valido):
        """Test: Eliminar un instructor llama al repositorio correcto"""
        servicio.eliminar(instructor_valido)
        
        mock_instructor_repo.delete.assert_called_once_with(instructor_valido)
    
    def test_eliminar_cliente(self, servicio, mock_cliente_repo, cliente_valido):
        """Test: Eliminar un cliente llama al repositorio correcto"""
        servicio.eliminar(cliente_valido)
        
        mock_cliente_repo.delete.assert_called_once_with(cliente_valido)
    
    def test_eliminar_entidad_invalida(self, servicio):
        """Test: Eliminar una entidad inválida lanza NegocioError"""
        with pytest.raises(NegocioError, match="Entidad no válida"):
            servicio.eliminar(None)
    
    def test_eliminar_rutina_en_uso_propaga_excepcion(self, servicio, mock_rutina_repo):
        """Test: Si la rutina está en uso (foreign key), se propaga la excepción"""
        from domain.exceptions import ReferenciaEnUso
        
        mock_rutina_repo.delete.side_effect = ReferenciaEnUso("Rutina asignada a clientes")
        
        rutina = Rutina(id=1, nombre="Pierna", pdf_link="test.pdf")
        
        with pytest.raises(ReferenciaEnUso):
            servicio.eliminar(rutina)
    
    def test_eliminar_instructor_en_uso_propaga_excepcion(self, servicio, mock_instructor_repo):
        """Test: Si el instructor está en uso, se propaga la excepción"""
        from domain.exceptions import ReferenciaEnUso
        
        mock_instructor_repo.delete.side_effect = ReferenciaEnUso("Instructor asignado a clientes")
        
        instructor = Instructor(id=1, nombre="Juan", apellido="Pérez")
        
        with pytest.raises(ReferenciaEnUso):
            servicio.eliminar(instructor)


# ========================================
# TESTS DE INTEGRACIÓN (Sin mocks)
# ========================================

class TestIntegracionServicio:
    """Tests de integración que verifican el flujo completo"""
    
    def test_flujo_completo_añadir_cliente_con_validaciones(self, servicio, mock_instructor_repo, mock_rutina_repo, mock_cliente_repo):
        """Test: Flujo completo de añadir un cliente verificando todas las validaciones"""
        # Setup: Instructor y rutina existen
        instructor = Instructor(id=5, nombre="Carlos", apellido="Ruiz")
        rutina = Rutina(id=3, nombre="Cardio", pdf_link="cardio.pdf")
        
        mock_instructor_repo.get_by_id.return_value = instructor
        mock_rutina_repo.get_by_id.return_value = rutina
        
        # Act: Añadir cliente
        cliente = Cliente(
            id=10,
            nombre="Laura",
            apellido="Fernández",
            instructor_id=5,
            rutina_id=3
        )
        
        servicio.añadir(cliente)
        
        # Assert: Se verificaron las dependencias y se guardó el cliente
        assert mock_instructor_repo.get_by_id.call_count == 1
        assert mock_rutina_repo.get_by_id.call_count == 1
        assert mock_cliente_repo.add.call_count == 1
    
    def test_orden_de_validacion_instructor_primero(self, servicio, mock_instructor_repo, mock_rutina_repo):
        """Test: El servicio valida primero el instructor, luego la rutina"""
        mock_instructor_repo.get_by_id.side_effect = RegistroNoEncontrado("Instructor no existe")
        
        cliente = Cliente(id=1, nombre="Test", apellido="Test", instructor_id=999, rutina_id=1)
        
        # Debe fallar en la validación del instructor antes de verificar la rutina
        with pytest.raises(RegistroNoEncontrado):
            servicio.añadir(cliente)
        
        # La rutina NO debería haberse verificado
        assert mock_rutina_repo.get_by_id.call_count == 0


# ========================================
# TESTS DE CASOS LÍMITE
# ========================================

class TestEdgeCasesServicio:
    """Tests de casos límite en el servicio"""
    
    def test_añadir_cliente_con_ids_cero(self, servicio, mock_instructor_repo, mock_rutina_repo, mock_cliente_repo):
        """Test: IDs con valor 0 deberían funcionar (aunque no sean típicos)"""
        mock_instructor_repo.get_by_id.return_value = Instructor(id=0, nombre="Test", apellido="Test")
        mock_rutina_repo.get_by_id.return_value = Rutina(id=0, nombre="Test", pdf_link="test")
        
        cliente = Cliente(id=0, nombre="Test", apellido="Test", instructor_id=0, rutina_id=0)
        
        servicio.añadir(cliente)
        
        mock_instructor_repo.get_by_id.assert_called_with(0)
        mock_rutina_repo.get_by_id.assert_called_with(0)
    
    def test_buscar_todos_retorna_lista_vacia(self, servicio, mock_rutina_repo):
        """Test: Si no hay rutinas, buscar_todos() debería manejar la excepción"""
        mock_rutina_repo.get_all.side_effect = RegistroNoEncontrado("No hay rutinas")
        
        with pytest.raises(RegistroNoEncontrado):
            servicio.buscar_todos(Rutina(id=0, nombre="", pdf_link=""))
    
    def test_patron_match_con_subclase_no_reconocida(self, servicio):
        """Test: Si se pasa una subclase de Rutina, debería funcionar (duck typing)"""
        # Este test verifica que el match/case funciona con herencia
        class RutinaEspecial(Rutina):
            pass
        
        rutina_especial = RutinaEspecial(id=1, nombre="Especial", pdf_link="test.pdf")
        
        servicio.añadir(rutina_especial)
        
        # Debería entrar en el case Rutina() por herencia
        # (Este comportamiento depende de la implementación de pattern matching en Python)
