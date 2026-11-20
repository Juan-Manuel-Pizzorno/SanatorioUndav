# [SU-39] Pruebas unitarias de inicio de sesión y restricción de acceso por rol
from backUsuarios import USUARIOS_SISTEMA, iniciar_sesion, tiene_acceso_modulo


def test_login_exitoso():
    sesion = iniciar_sesion("laura.gomez@undav.edu.ar", "1234")
    assert sesion is not None
    assert sesion["rol"] == "Admisión"
    assert "password" not in sesion


def test_login_normaliza_mayusculas_y_espacios():
    sesion = iniciar_sesion("  SOFIA.MARTINEZ@UNDAV.EDU.AR  ", "1234")
    assert sesion is not None
    assert sesion["nombre"] == "Dra. Sofía Martínez"


def test_negar_login_password_incorrecta():
    sesion = iniciar_sesion("sofia.martinez@undav.edu.ar", "incorrecta")
    assert sesion is None


def test_negar_login_usuario_inexistente():
    sesion = iniciar_sesion("intruso@undav.edu.ar", "1234")
    assert sesion is None


def test_negar_login_campos_vacios():
    assert iniciar_sesion("", "1234") is None
    assert iniciar_sesion("   ", "") is None


def test_restriccion_modulos_por_rol():
    triage = iniciar_sesion("carlos.mendez@undav.edu.ar", "1234")
    assert tiene_acceso_modulo(triage, "Clasificación Triage")
    assert not tiene_acceso_modulo(triage, "Atención de Guardia")
    assert not tiene_acceso_modulo(triage, "Alta de Profesionales")